import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Darell Trading Signal", page_icon="🐂", layout="centered")

st.markdown("<h1 style='text-align:center; color:#00E676;'>🐂 DARELL TRADING SIGNAL 🐻</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;'>₿ BTC • ⟠ ETH • 🥇 GOLD | Bull & Bear Full Body</p>", unsafe_allow_html=True)

coins = {
    "BTC-USD": "BTC - Bitcoin",
    "ETH-USD": "ETH - Ethereum",
    "GC=F": "GOLD - XAUUSD",
    "BNB-USD": "BNB",
    "SOL-USD": "SOL"
}

choice = st.selectbox("Piliin ang Coin:", list(coins.values()))
symbol = [k for k,v in coins.items() if v==choice][0]

if st.button("🚀 CHECK SIGNAL NGAYON", use_container_width=True):
    with st.spinner("Analyzing..."):
        df = yf.download(symbol, period="5d", interval="15m", progress=False, auto_adjust=True)
        try:
            df.columns = df.columns.get_level_values(0)
        except: pass

        if len(df) > 5:
            price = float(df['Close'].iloc[-1])
            last = df.iloc[-1]
            body = abs(float(last['Close'])-float(last['Open']))
            low_wick = min(float(last['Close']),float(last['Open']))-float(last['Low'])
            up_wick = float(last['High'])-max(float(last['Close']),float(last['Open']))

            st.divider()
            st.metric(f"Live {choice}", f"${price:.2f}")

            if low_wick > body*1.5:
                st.success(f"🐂 BULL SIGNAL - BUY / CALL - {choice}")
                st.write(f"**ENTRY:** ${price:.2f} | **TP1:** ${price*1.015:.2f} | **TP2:** ${price*1.03:.2f} | **SL:** ${price*0.98:.2f}")
                st.balloons()
            elif up_wick > body*1.5:
                st.error(f"🐻 BEAR SIGNAL - SELL / PUT - {choice}")
                st.write(f"**ENTRY:** ${price:.2f} | **TP1:** ${price*0.985:.2f} | **TP2:** ${price*0.97:.2f} | **SL:** ${price*1.02:.2f}")
            else:
                st.warning(f"⏳ WAIT - No Bull/Bear Full Body yet")

st.caption("© 2026 Darell Trading Signal")
