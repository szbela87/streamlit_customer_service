import matplotlib.pyplot as plt
import streamlit as st
import pandas as pd

st.title("📊 Preset Reports and Statistics")

data = st.session_state.get("data", None)

if data is not None:
    col1, col2 = st.columns(2)

    # Negatív visszajelzések vendorként
    neg = data[data['Semantic'] == 'negative']
    neg_counts = neg['Vendor'].value_counts().nlargest(10)
    with col1:
        if not neg_counts.empty:
            fig1, ax1 = plt.subplots()
            neg_counts.plot(kind='bar', ax=ax1)
            ax1.set_title('Top 10 negative feedback count by vendor')
            ax1.set_ylabel('Number')
            st.pyplot(fig1)
            plt.close(fig1)
        else:
            st.info("No negative feedback found in the data.")

    # Pozitív visszajelzések vendorként
    pos = data[data['Semantic'] == 'positive']
    pos_counts = pos['Vendor'].value_counts().nlargest(10)
    with col2:
        if not pos_counts.empty:
            fig2, ax2 = plt.subplots()
            pos_counts.plot(kind='bar', ax=ax2)
            ax2.set_title('Top 10 positive feedback count by vendor')
            ax2.set_ylabel('Number')
            st.pyplot(fig2)
            plt.close(fig2)
        else:
            st.info("No positive feedback found in the data.")
else:
    st.info("Please upload a CSV file in the 'Chat' window to see the reports.")
