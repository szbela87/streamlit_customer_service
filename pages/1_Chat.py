import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import os
import glob
import matplotlib
import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv
from pandasai_litellm import LiteLLM
from pandasai import SmartDataframe
from datetime import datetime

# Setup
os.environ["MPLBACKEND"] = "Agg"
matplotlib.use("Agg")
matplotlib.rcParams['figure.figsize'] = (3, 2)
plt.ioff()
plt.show = lambda *args, **kwargs: None
from pandasai.core.response.chart import ChartResponse
ChartResponse.show = lambda self, *args, **kwargs: None

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)
export_dir = "exports/charts"
os.makedirs(export_dir, exist_ok=True)

# Page
st.title("💬 Vendor ChatCSV")

st.sidebar.subheader("📄 CSV uploading")
input_csv = st.sidebar.file_uploader("Choose a CSV file:", type=["csv"], key="chat_csv")
# Download sample link
st.sidebar.markdown(
    "[📂 Download sample CSV file]"
    "(https://drive.google.com/uc?export=download&id=1F1gvAry6Czj6RWY5-UZTZzKskyLwK-wg)",
    unsafe_allow_html=True
)
# Load sample CSV button
df = None
if st.sidebar.button("Load sample CSV"):
    sample_url = "https://drive.google.com/uc?export=download&id=1F1gvAry6Czj6RWY5-UZTZzKskyLwK-wg"
    df = pd.read_csv(sample_url)
elif input_csv:
    df = pd.read_csv(input_csv)
# Keep only required columns if df is loaded
if df is not None:
    df = df[["timestamp", "conv_id", "Messages", "Vendor", "Semantic"]]
    st.session_state.data = df

# Main logic
data = st.session_state.get("data", None)

st.header("Chat with the Vendor CSV")
if data is not None:
    st.subheader("🔢 Uploaded data")
    st.dataframe(data, use_container_width=True)

    st.sidebar.title("Settings")
    model = st.sidebar.selectbox(
        "Model:", ["gpt-4o", "gpt-4", "gpt-3.5-turbo"], index=0
    )
    system_prompt = st.sidebar.text_area(
        "System Prompt:",
        value=(
            "You are an expert data analyst who provides highly detailed answers based on CSV data "
            "in English, and if necessary, generates matplotlib charts."
        )
    )
    beautify_answer = st.sidebar.checkbox("Beautify the answer output")
    if beautify_answer:
        system_prompt_2 = st.sidebar.text_area(
            "Beautify System Prompt:",
            value=(
                "Please reformat the output text to be clearer, properly structured, and if possible, "
                "convert tabular-looking content into a markdown table. Also, answer in English."
            )
        )

    if "history" not in st.session_state:
        st.session_state.history = []

    st.subheader("Ask a question about the CSV:")
    user_prompt = st.text_area(
        "Question:", placeholder="E.g.: Which vendor received the most negative feedback?"
    )

    if st.button("Send", key="chat_send"):
        with st.spinner("AI is working..."):
            llm = LiteLLM(model=model)
            sdf = SmartDataframe(data, config={"llm": llm, "save_charts": True})
            prev = set(glob.glob(f"{export_dir}/temp_chart*.png"))
            full_prompt = f"{system_prompt} Question: {user_prompt}"
            answer_text = sdf.chat(full_prompt)

            if beautify_answer:
                beautify_prompt = f"{system_prompt_2}\n\nInput:\n{answer_text}"
                beautified = client.chat.completions.create(
                    model=model,
                    messages=[
                        {"role": "system", "content": "You are a text beautifier and formatter."},
                        {"role": "user",   "content": beautify_prompt}
                    ],
                    temperature=0.2,
                )
                answer_text = beautified.choices[0].message.content

            curr = set(glob.glob(f"{export_dir}/temp_chart*.png"))
            new_imgs = sorted(curr - prev)

            st.success("✅ Answer:")
            st.markdown(answer_text)

            # Save new images and collect paths
            saved = []
            for img in new_imgs:
                ts = datetime.now().strftime("%Y%m%d_%H%M%S")
                base = os.path.basename(img)
                new_name = f"chart_{ts}_{base[len('temp_chart_'):]}"
                new_path = os.path.join(export_dir, new_name)
                os.rename(img, new_path)
                saved.append(new_path)
                st.image(new_path, use_container_width=True)
                st.caption(f"Figure saved as: `{new_path}`")
            plt.close('all')

            # Append history once per interaction
            st.session_state.history.append({
                'question': user_prompt,
                'answer': answer_text,
                'images': saved
            })

    st.markdown("---")
    if st.session_state.history:
        st.header("📜 History")
        for turn in st.session_state.history:
            st.markdown(f"**👤 Question:** {turn['question']}")
            with st.expander("🧐 View answer"):
                st.markdown(turn['answer'])
            for img in turn['images']:
                st.image(img, use_container_width=True)
                st.caption(os.path.basename(img))
else:
    st.info("Upload a CSV file on the left to get started.")
