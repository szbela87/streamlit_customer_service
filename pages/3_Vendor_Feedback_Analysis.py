import os
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import unicodedata
from openai import OpenAI
from dotenv import load_dotenv
from pydantic import BaseModel
from timeit import default_timer

# ─── Setup ───────────────────────────────────────────────────
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or st.secrets.get("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

# ─── Pydantic model a GPT válasz parse-olásához ────────────────
class Vendor(BaseModel):
    name: str
    semantic: str

# ─── Segéd: ékezetek eltávolítása és kisbetűsítés ─────────────
def remove_accents_and_lowercase(text):
    normalized = unicodedata.normalize('NFKD', text)
    without_accents = "".join([c for c in normalized if not unicodedata.combining(c)])
    return without_accents.lower()

# ─── Vendor és sentiment kinyerése GPT-vel ────────────────────
def vendor_name(text):
    completion = client.beta.chat.completions.parse(
        model="gpt-4o-2024-08-06",
        messages=[
            {"role": "system", "content": (
                "The input message can be either in Hungarian or in English.\n\n"
                "- Extract the vendor name from the message and place it in the 'name' field. "
                "If no vendor name is found, use 'UNKNOWN'.\n"
                "- Perform a semantic classification of the message and place it in the 'semantic' field. "
                "The value must be exactly one of the following English words: 'positive', 'neutral', or 'negative'.\n\n"
                "Respond strictly in JSON format matching the following schema:\n"
                "{'name': '<vendor name>', 'semantic': '<semantic value>'}\n\n"
                "Do not add any explanations or extra text, only output the JSON."
            )},
            {"role": "user", "content": text},
        ],
        response_format=Vendor,
    )
    vendor = completion.choices[0].message.parsed
    return vendor.name, vendor.semantic

# ─── Adatok beolvasása és előfeldolgozás, cache-elve ───────────
@st.cache_data
def load_and_clean_csv(file_path):
    df = pd.read_csv(file_path)
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    return df

# ─── Üzenetfolyamok csoportosítása időablakon belül, cache-elve ─
@st.cache_data
def merge_conversations(df, max_diff_hours=8):
    df = df.copy()
    df['conv_id'] = df.apply(
        lambda r: r['sender_id'] if r['sender_type']=='user' else r['reply_to'], axis=1
    )
    df = df.sort_values(by=['conv_id','timestamp'])
    merged_groups = []
    for conv_id, group in df.groupby('conv_id'):
        temp_group = []
        for _, row in group.iterrows():
            if not temp_group:
                temp_group.append(row)
            else:
                prev = temp_group[-1]
                if (row['timestamp'] - prev['timestamp']).total_seconds() <= max_diff_hours * 3600:
                    temp_group.append(row)
                else:
                    merged_groups.append(temp_group)
                    temp_group = [row]
        if temp_group:
            merged_groups.append(temp_group)
    rows = []
    for grp in merged_groups:
        first = grp[0]
        combined = ' | '.join([r['message'] for r in grp])
        rows.append({
            'timestamp': first['timestamp'],
            'conv_id': first['conv_id'],
            'Messages': combined,
            'reply_to': first['reply_to']
        })
    return pd.DataFrame(rows)

# ─── Vendor analízis pivot táblázat ───────────────────────────
@st.cache_data
def analyze_vendor_sentiment(df, limit=0):
    counts = df.pivot_table(index='Vendor', columns='Semantic', aggfunc='size', fill_value=0)
    counts['Total'] = counts.sum(axis=1)
    filtered = counts[counts['Total'] >= limit]
    return filtered.drop(columns=['Total'])

# ─── Streamlit UI multipage/tab-elés és állapotmegőrzés ──────
st.set_page_config(layout="wide")
st.title("📊 Vendor Feedback Analysis")

tabs = st.tabs(["Uploading & Grouping", "Vendor Analysis"])

with tabs[0]:
    # init df_raw in session_state
    if "df_raw" not in st.session_state:
        st.session_state.df_raw = None

    # 1) CSV feltöltése
    uploaded_file = st.file_uploader(
        "Please, choose a CSV file:", type=["csv"]
    )
    # 2) Minta betöltése gombbal
    sample_download_url = "https://drive.google.com/uc?export=download&id=1OHO7isIaZQViUpinG_OOvekqNLizA0aL"
    if st.button("Load sample CSV"):
        st.session_state.df_raw = load_and_clean_csv(sample_download_url)
    elif uploaded_file:
        st.session_state.df_raw = load_and_clean_csv(uploaded_file)

    df_raw = st.session_state.df_raw

    # Ha tényleg van adat, csak akkor csoportosítunk
    if df_raw is not None:
        # A number_input most már kap egy key-t, állapotot tarthat
        max_diff = st.number_input(
            "Max time (in hours) for grouping:", 1, 48, 8, key="max_diff"
        )

        # Ezt is session_state-ből érdemes építeni, hogy ne fusson újra fölöslegesen
        if "df_groups" not in st.session_state or st.session_state.max_diff != max_diff:
            df_groups = merge_conversations(df_raw, max_diff_hours=max_diff)
            df_groups.drop(columns=['reply_to'], inplace=True)
            st.session_state.df_groups = df_groups

        st.success("Grouping is finished.")
        st.dataframe(st.session_state.df_groups)
    else:
        st.info("Upload a CSV file or click 'Load sample CSV' to get started.")

with tabs[1]:
    if 'df_groups' not in st.session_state:
        st.info("Please upload and group a file first on the 'Upload & Grouping' tab.")
    else:
        dfg = st.session_state['df_groups']
        run = st.button("Run the analyis")
        if run or 'df_analysis' in st.session_state:
            if run:
                t0 = default_timer()
                vendors, sems = [], []
                progress = st.progress(0)
                status = st.empty()
                for i, msg in enumerate(dfg['Messages']):
                    vn, sem = vendor_name(msg)
                    vendors.append(remove_accents_and_lowercase(vn))
                    sems.append(sem)
                    progress.progress(int((i+1)/len(dfg)*100))
                    status.text(f"{i+1}/{len(dfg)} processed")
                dfg['Vendor'] = vendors
                dfg['Semantic'] = sems
                dfg = dfg[dfg['Vendor'] != 'unknown']
                st.session_state['df_analysis'] = dfg
                t1 = default_timer()
                st.write(f"Running time: {t1-t0:.2f} s")
            else:
                dfg = st.session_state['df_analysis']

            st.subheader("Processed DataFrame")
            st.dataframe(dfg)
            csv_bytes = dfg.to_csv(index=False).encode('utf-8')
            st.download_button("CSV downloading", csv_bytes, "analysis.csv")

            limit = st.slider(
                "Minimum number of ratings per vendor:", 0, 50, 0
            )
            summary = analyze_vendor_sentiment(dfg, limit)
            st.subheader("Vendor Sentiment Summary")
            st.dataframe(summary)
            if not summary.empty:
                fig, ax = plt.subplots(figsize=(10,4))
                summary.plot(kind='bar', stacked=True, ax=ax)
                ax.set_xlabel('Vendor')
                ax.set_ylabel('Count')
                plt.xticks(rotation=45)
                st.pyplot(fig)
