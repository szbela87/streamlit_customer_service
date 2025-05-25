import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import streamlit as st

st.set_page_config(layout="wide")
st.title("🏠 Welcome to the Vendor Analysis App! +++")

st.markdown("""
This application is a PandasAI + OpenAI API + Streamlit demo and offers three main features:

- **ChatCSV**: Chat with the CSV file
- **Preset Reports**: Predefined reports and statistics
- **Vendor Feedback Analysis**: Process vendor feedback from a separate CSV file
""")
