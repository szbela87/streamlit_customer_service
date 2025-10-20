# 🧠 Vendor Feedback & ChatCSV App

This is a Streamlit-based web application that enables users to analyze and interact with vendor-related feedback data using natural language and advanced AI models.

## 🚀 Features

- **ChatCSV**: Ask natural language questions about a CSV file with conversational memory (remembers last 3 questions)
- **Vendor Feedback Analysis**: Automatically extract vendor names and classify sentiment using OpenAI GPT
- **Predefined Reports**: Generate summary reports and visualizations
- **Conversation Grouping**: Merge message streams by time window
- **Interactive Examples**: Clickable example questions for quick exploration

## 🧰 Tech Stack

- [Streamlit](https://streamlit.io/)
- [OpenAI API](https://platform.openai.com/)
- [PandasAI](https://github.com/gventuri/pandas-ai)
- [Python-dotenv](https://github.com/theskumar/python-dotenv)
- [Matplotlib](https://matplotlib.org/)
- [Pandas](https://pandas.pydata.org/)

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/szbela87/streamlit_customer_service.git
cd your-repo-name
```

### 2. (Optional) Create and activate a virtual environment

**Option A: Using venv**

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**Option B: Using conda**

```bash
conda create -n streamlit-apps python=3.10 -y
conda activate streamlit-apps
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Create a `.streamlit/secrets.toml` file in the root directory:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-api-key-here"
```

This file is used for both local development and Streamlit Cloud deployment.

## ▶️ Run Locally

```bash
streamlit run Home.py
```

## ☁️ Deploy on Streamlit Cloud

1. Push the repository to your GitHub account.
2. Go to [Streamlit Cloud](https://streamlit.io/cloud) and create a new app.
3. Select your repo and `Home.py` as the main file.
4. Under **Settings > Secrets**, add your API key:

   ```toml
   OPENAI_API_KEY = "your-api-key-here"
   ```

## 📁 Sample CSV Files

Downloadable sample CSV files are available within the app via Google Drive links.

## 🔧 Future Enhancements

The application could be further developed with these features:

1. **Customer Service Agent Evaluation**: Automatically provide performance evaluations for the customer service agent for each incoming feedback based on the conversation.
2. **Assigned Agent Tracking**: Log and display which customer service agent was assigned to each case, facilitating accountability and case history tracking.
