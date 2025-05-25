import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import streamlit as st

st.set_page_config(layout="wide")
st.title("🏠 Welcome to the Vendor Analysis App!")

st.markdown("""
This application is a PandasAI + OpenAI API + Streamlit demo and offers three main features:

- **ChatCSV**: Chat with the CSV file
- **Preset Reports**: Predefined reports and statistics
- **Vendor Feedback Analysis**: Process vendor feedback from a separate CSV file
""")

st.markdown("""
---

📂 **Source code available on [GitHub](https://github.com/szbela87/streamlit_customer_service)**.

## 🔧 Future Enhancements

- **Customer Service Agent Evaluation**: Automatically provide performance evaluations for the customer service agent for each incoming feedback based on the conversation.
- **Assigned Agent Tracking**: Log and display which customer service agent was assigned to each case, facilitating accountability and case history tracking.
""")
