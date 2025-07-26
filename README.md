
# GenAI S&P 500 Dashboard 📈🤖

This Streamlit app forecasts stock prices for S&P 500 companies and summarizes recent news for each stock using GPT-4.It also gives you Top 50 companies by Average trading volume over last 3 months.

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
