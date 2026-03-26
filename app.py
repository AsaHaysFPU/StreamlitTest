# Asa Hays U0000022185

import streamlit as st
import requests
import pandas as pd
import datetime

st.set_page_config(page_title="Crypto Tracker Dashboard", layout="wide")
st.title("📈 Crypto Market Interactive Dashboard")

@st.cache_data(ttl=300)
def fetch_coin_data(coin_id, days):
    url = f"https://api.coingecko.com/api/v3/coins/{coin_id}/market_chart"
    params = {"vs_currency": "usd", "days": days, "interval": "daily"}
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None

st.sidebar.header("Dashboard Settings")
selected_coin = st.sidebar.selectbox(
    "Select Cryptocurrency",
    ["bitcoin", "ethereum", "dogecoin", "solana", "cardano"]
)

days_range = st.sidebar.slider("Select Date Range (Days)", 7, 365, 30)

raw_data = fetch_coin_data(selected_coin, days_range)

if raw_data:
    df = pd.DataFrame(raw_data['prices'], columns=['timestamp', 'price'])
    
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df = df.set_index('timestamp')

    current_price = df['price'].iloc[-1]
    price_delta = current_price - df['price'].iloc[0]
    
    col1, col2 = st.columns(2)
    col1.metric(label=f"Current {selected_coin.capitalize()} Price", value=f"${current_price:,.2f}", delta=f"${price_delta:,.2f}")
    col2.metric(label="Data Points Collected", value=len(df))

    st.subheader(f"{selected_coin.capitalize()} Price Trend (Last {days_range} Days)")
    st.line_chart(df['price'])

    st.subheader("Raw Market Data (Processed)")
    st.dataframe(df.tail(10), use_container_width=True)
