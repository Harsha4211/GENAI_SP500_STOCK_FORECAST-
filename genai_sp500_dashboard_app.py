import streamlit as st
import pandas as pd
import yfinance as yf
from prophet import Prophet
from plotly import graph_objs as go
import requests
import openai
import os

# Set page config
st.set_page_config(page_title="S&P 500 Forecast + GenAI Sentiment", layout="wide")

# Load S&P 500 tickers
@st.cache_data
def get_sp500():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    df = pd.read_html(url)[0]
    return df

sp500 = get_sp500()
ticker = st.selectbox("Choose S&P 500 Stock", sp500['Symbol'])
company_name = sp500[sp500['Symbol'] == ticker]['Security'].values[0]
st.title(f"{ticker} - {company_name}")

# Fetch historical data
df = yf.download(ticker, period="1y")
df.reset_index(inplace=True)
st.subheader("📉 1-Year Historical Prices")
st.line_chart(df[['Date', 'Close']].set_index('Date'))

# Forecasting with Prophet
st.subheader("🔮 30-Day Forecast")
df_prophet = df[['Date', 'Close']].rename(columns={"Date": "ds", "Close": "y"})
m = Prophet()
m.fit(df_prophet)
future = m.make_future_dataframe(periods=30)
forecast = m.predict(future)
fig1 = go.Figure()
fig1.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast'))
fig1.add_trace(go.Scatter(x=df['Date'], y=df['Close'], name='Actual'))
st.plotly_chart(fig1)

# Fetch News
st.subheader("📰 Latest News Headlines")
news_api_key = "REPLACE_WITH_YOUR_NEWS_API_KEY"

def fetch_news(ticker_symbol):
    url = f"https://newsapi.org/v2/everything?q={ticker_symbol}&sortBy=publishedAt&apiKey={news_api_key}&language=en"
    response = requests.get(url)
    articles = response.json().get("articles", [])[:5]
    return [[a["title"], a["url"]] for a in articles]

news = fetch_news(ticker)
for title, url in news:
    st.markdown(f"[{title}]({url})")

# OpenAI Sentiment Summary
st.subheader("🤖 GPT-4 Sentiment Summary")
openai.api_key = os.getenv("OPENAI_API_KEY")

if news:
    prompt = "Analyze the following news headlines for stock sentiment (positive, neutral, or negative) and summarize:

"
    prompt += "
".join([n[0] for n in news])
    try:
        response = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=150
        )
        st.write(response.choices[0].message.content)
    except Exception as e:
        st.error(f"OpenAI error: {e}")
else:
    st.info("No news found for sentiment analysis.")
