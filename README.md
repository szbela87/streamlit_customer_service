# 🧠 Vendor Feedback & ChatCSV App

This is a Streamlit-based web application that enables users to analyze and interact with vendor-related feedback data using natural language and advanced AI models.

## 🚀 Features

* **ChatCSV**: Ask natural language questions about a CSV file
* **Vendor Feedback Analysis**: Automatically extract vendor names and classify sentiment using OpenAI GPT
* **Predefined Reports**: Generate summary reports and visualizations
* **Conversation Grouping**: Merge message streams by time window

## 🧰 Tech Stack

* [Streamlit](https://streamlit.io/)
* [OpenAI API](https://platform.openai.com/)
* [PandasAI](https://github.com/gventuri/pandas-ai)
* [Python-dotenv](https://github.com/theskumar/python-dotenv)
* [Matplotlib](https://matplotlib.org/)
* [Pandas](https://pandas.pydata.org/)

## 📦 Installation

### 1. Clone the repository

```bash
git clone https://github.com/szbela87/streamlit_customer_service.git
cd your-repo-name
```

### 2. (Optional) Create and activate a virtual environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your OpenAI API key

Create a `.env` file in the root directory with:

```
OPENAI_API_KEY=your-api-key-here
```

Alternatively, use `secrets.toml` when deploying to Streamlit Cloud:

```toml
# .streamlit/secrets.toml
OPENAI_API_KEY = "your-api-key-here"
```

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

## 🔧 Bővítési lehetőségek

Az alkalmazás további fejlesztési lehetőségei:

1. **Ügyfélszolgálatos kolléga értékelése**: Minden beérkező visszajelzés esetén az ügyfélszolgálatos kolléga is kapjon automatikus teljesítményértékelést a beszélgetés alapján.
2. **Hozzárendelt kolléga nyomon követése**: Az adott ügyhöz legyen naplózva és megjelenítve, hogy mely ügyfélszolgálatos kolléga volt rendelve, így könnyebb legyen a felelősség és az esettörténet követése.
