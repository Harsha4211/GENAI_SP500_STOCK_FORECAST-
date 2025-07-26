# GenAI S&P 500 Dashboard 📈🤖

This Streamlit app forecasts stock prices for S&P 500 companies and summarizes recent news using GPT-4.

## Features
- 📊 30-day price forecasts using Prophet
- 📰 Latest news headlines from NewsAPI
- 🤖 GPT-4 sentiment analysis of news

## Setup

1. Install packages:
```
pip install -r requirements.txt
```

2. Set environment variable:
```
export OPENAI_API_KEY=your_api_key
```

3. Run the app:
```
streamlit run genai_sp500_dashboard_app.py
```
