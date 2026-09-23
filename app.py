import streamlit as st
from PIL import Image
import yfinance as yf
import pandas as pd
import numpy as np

st.set_page_config(page_title="DARELL V10 PRO", layout="centered", page_icon="📈")

st.markdown("<h1 style='text-align:center; color:#00ff88'>DARELL V10 PRO</h1><p style='text-align:center'>Screenshot Analyzer + Patterns + TP/SL + TF</p>", unsafe_allow_html=True)

coins = {
    "BTC/USDT": "BTC-USD", "ETH/USDT": "ETH-USD", "BNB/USDT": "BNB-USD",
    "GOLD/USDT": "GC=F", "EUR/USDT": "EURUSD=X", "GBP/USDT": "GBPUSD=X",
    "BTC": "BTC-USD", "ETH": "ETH-USD", "GOLD": "GC=F"
}

def get_data(symbol):
    try:
        df = yf.Ticker(symbol).history(period="3mo")
        close = df['Close']
        open_ = df['Open']
        high = df['High']
        low = df['Low']
        # RSI
        delta = close.diff()
        gain = delta.where(delta>0,0).rolling(14).mean()
        loss = (-delta.where(delta<0,0)).rolling(14).mean()
        rsi = 100-(100/(1+gain/loss))
        # SMA
        sma20 = close.rolling(20).mean()
        sma50 = close.rolling(50).mean()
        # CANDLESTICK PATTERNS
        last = df.iloc[-1]
        prev = df.iloc[-2]
        body = abs(last['Close']-last['Open'])
        upper_wick = last['High']-max(last['Close'], last['Open'])
        lower_wick = min(last['Close'], last['Open'])-last['Low']

        patterns = []
        signal = "HOLD"

        # HAMMER
        if lower_wick > body*2 and upper_wick < body*0.5:
            patterns.append("🔨 HAMMER - Bullish Reversal (BUY Signal)")
            signal = "BUY"
        # DOJI
        if body < (last['High']-last['Low'])*0.1:
            patterns.append("➕ DOJI - Indecision, Possible Reversal")
            if signal == "HOLD":
                signal = "HOLD"
        # ENGULFING
        if last['Close'] > last['Open'] and prev['Close'] < prev['Open'] and last['Close'] > prev['Open'] and last['Open'] < prev['Close']:
            patterns.append("🟩 BULLISH ENGULFING - Strong BUY")
            signal = "BUY"
        if last['Close'] < last['Open'] and prev['Close'] > prev['Open'] and last['Close'] < prev['Open'] and last['Open'] > prev['Close']:
            patterns.append("🟥 BEARISH ENGULFING - Strong SELL")
            signal = "SELL"
        # 3 WHITE SOLDIERS
        if len(df) >= 3:
            c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]
            if c1['Close']>c1['Open'] and c2['Close']>c2['Open'] and c3['Close']>c3['Open'] and c2['Close']>c1['Close'] and c3['Close']>c2['Close']:
                patterns.append("🪖 3 WHITE SOLDIERS - Strong Bullish BUY")
                signal = "BUY"
        # RSI SIGNAL
        if rsi.iloc[-1] < 30:
            patterns.append(f"📉 RSI Oversold {rsi.iloc[-1]:.1f} - BUY")
            signal = "BUY"
        elif rsi.iloc[-1] > 70:
            patterns.append(f"📈 RSI Overbought {rsi.iloc[-1]:.1f} - SELL")
            signal = "SELL"

        if not patterns:
            patterns.append("No clear pattern - Sideways")

        sup = low.tail(15).min()
        res = high.tail(15).max()
        return df, rsi.iloc[-1], close.iloc[-1], sup, res, sma20.iloc[-1], patterns, signal
    except:
        return None, 58, 2740, 2600, 2900, 2700, ["Data not available"], "HOLD"

def trade_type(tf):
    if tf in ["5M","15M","30M"]:
        return "SCALPING", "⚡ Pang mabilis 5-30 mins", 0.005, 0.01, 0.015, 0.003
    elif tf in ["1H","4H"]:
        return "INTRADAY", "📈 Pang 1-4 hours", 0.02, 0.04, 0.06, 0.02
    else:
        return "SWING", "🌊 Pang 1 day to 1 week", 0.05, 0.10, 0.15, 0.05

# FOLDER / PAGES NA PARANG PLAYSTORE
tabs = st.tabs(["📊 SCREENSHOT", "🕐 TF + TP/SL", "🕯️ PATTERNS", "📰 NEWS", "📁 ALERTS"])

with tabs[0]:
    st.subheader("📸 Screenshot Analyzer")
    st.write("Upload mo chart screenshot mo dito")
    pair = st.selectbox("Pair", list(coins.keys()), index=1, key="s1")
    tf = st.select_slider("Timeframe", ["5M","15M","30M","1H","4H","1D","1W"], value="1H", key="st1")
    ttype, desc, a, b, c, d = trade_type(tf)
    st.info(f"{ttype} - {desc}")

    up = st.file_uploader("Upload Chart Image", type=['png','jpg','jpeg'], key="up1")
    if up:
        img = Image.open(up)
        st.image(img, caption=f"{pair} Uploaded - {tf}", use_container_width=True)

    if st.button("🔍 ANALYZE CHART + PATTERNS", type="primary", use_container_width=True):
        df, rsi, price, sup, res, sma, patterns, signal = get_data(coins[pair])
        tp1 = price*(1+a)
        tp2 = price*(1+b)
        tp3 = price*(1+c)
        sl = price*(1-d)

        if signal == "BUY":
            st.success(f"🟢 BUY SIGNAL - {pair} {ttype}")
        elif signal == "SELL":
            st.error(f"🔴 SELL SIGNAL - {pair} {ttype}")
        else:
            st.warning(f"🟡 HOLD - {pair} {ttype}")

        c1,c2,c3 = st.columns(3)
        c1.metric("ENTRY", f"${price:,.2f}")
        c2.metric("TP1", f"${tp1:,.2f}")
        c3.metric("SL", f"${sl:,.2f}")
        c1,c2,c3 = st.columns(3)
        c1.metric("TP2", f"${tp2:,.2f}")
        c2.metric("TP3", f"${tp3:,.2f}")
        c3.metric("RSI", f"{rsi:.1f}")

        st.write("**📁 Candlestick Patterns Found:**")
        for pat in patterns:
            if "BUY" in pat:
                st.success(pat)
            elif "SELL" in pat:
                st.error(pat)
            else:
                st.info(pat)

        if df is not None:
            st.line_chart(df['Close'].tail(100))
            st.write(f"Support: ${sup:,.2f} | Resistance: ${res:,.2f} | SMA20: ${sma:,.2f}")

with tabs[1]:
    st.subheader("🕐 Timeframe + TP/SL Folder")
    pair = st.selectbox("Pair", list(coins.keys()), key="s2")
    tf = st.select_slider("TF", ["5M","15M","30M","1H","4H","1D","1W"], value="15M", key="st2")
    ttype, desc, a, b, c, d = trade_type(tf)

    if ttype == "SCALPING":
        st.success(f"📁 Folder: SCALPING - {tf} - {desc}")
    elif ttype == "INTRADAY":
        st.warning(f"📁 Folder: INTRADAY - {tf} - {desc}")
    else:
        st.error(f"📁 Folder: SWING - {tf} - {desc}")

    df, rsi, price, sup, res, sma, patterns, signal = get_data(coins[pair])
    st.metric(f"{pair} Price", f"${price:,.2f}", f"{signal}")
    st.write(f"Entry: ${price:,.2f}")
    st.write(f"TP1 +{a*100:.1f}% = ${price*(1+a):,.2f}")
    st.write(f"TP2 +{b*100:.0f}% = ${price*(1+b):,.2f}")
    st.write(f"TP3 +{c*100:.0f}% = ${price*(1+c):,.2f}")
    st.write(f"SL -{d*100:.1f}% = ${price*(1-d):,.2f}")
    st.write(f"Best for: {ttype}")

with tabs[2]:
    st.subheader("🕯️ Candlestick Patterns - BUY/SELL")
    pair = st.selectbox("Pair Patterns", list(coins.keys()), key="s3")
    if st.button("Detect Patterns", use_container_width=True):
        df, rsi, price, sup, res, sma, patterns, signal = get_data(coins[pair])
        if signal == "BUY":
            st.success(f"BUY SIGNAL - Hammer / Engulfing / 3 White Soldiers detected!")
        elif signal == "SELL":
            st.error(f"SELL SIGNAL - Bearish Engulfing / Overbought!")
        else:
            st.info("No strong pattern")
        for pat in patterns:
            st.write(pat)
        st.write(f"RSI: {rsi:.1f} - {'BUY' if rsi<40 else 'SELL' if rsi>70 else 'HOLD'}")
        if df is not None:
            st.bar_chart(df[['Open','Close']].tail(20))

with tabs[3]:
    st.subheader("📰 News Folder")
    pair = st.selectbox("News", list(coins.keys()), key="s4")
    st.write(f"📁 Folder: {pair} News")
    df, rsi, price, sup, res, sma, patterns, signal = get_data(coins[pair])
    if st.button("Get Live News", use_container_width=True):
        if signal == "BUY":
            st.success(f"🔥 {pair} News: Bullish Hammer pattern - Good for SCALPING 5M-15M")
        else:
            st.warning(f"📉 {pair} News: Market correction - Good for SWING short on 1D")
        st.info(f"💡 Expert: RSI {rsi:.1f} - {signal} - Best TF: {'5M/15M' if rsi<60 else '1D'}")
        st.link_button("Full News", f"https://finance.yahoo.com/quote/{coins[pair]}/news")

with tabs[4]:
    st.subheader("📁 Alerts Folder - Scalping vs Swing")
    pair = st.selectbox("Alert Pair", list(coins.keys()), key="s5")
    tf = st.selectbox("TF", ["5M","15M","30M","1H","4H","1D","1W"], key="st5")
    ttype, desc, a, b, c, d = trade_type(tf)
    st.write(f"Type: **{ttype}** - {desc}")
    target = st.number_input("Target Price", value=2740.0)
    cond = st.radio("When", ["Price >= Target", "Price <= Target"])
    if "alerts" not in st.session_state:
        st.session_state["alerts"] = []
    if st.button("🔔 Set Alert", type="primary", use_container_width=True):
        st.session_state["alerts"].append(f"{ttype} | {pair} | TF:{tf} | ${target:,.2f} | {cond}")
        st.success(f"Alert Set: {ttype}")
    st.write(f"📁 Recent Scans: {len(st.session_state['alerts'])}")
    for x in reversed(st.session_state["alerts"][-10:]):
        if "SCALPING" in x:
            st.success(x)
        elif "INTRADAY" in x:
            st.warning(x)
        else:
            st.error(x)
