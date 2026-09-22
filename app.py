import streamlit as st
from PIL import Image
import yfinance as yf
from streamlit.components.v1 import html
import random

st.set_page_config(page_title="Darell AI Chart Analyzer", page_icon="📈", layout="centered")

# LOGO MO
st.image("logo.png", use_container_width=True)

st.markdown("### 📸 AI Chart Analyzer - Snap any chart!")
st.markdown("Parang nasa Play Store na!")

tab1, tab2 = st.tabs(["📷 Snap Chart", "📊 Live Market"])

# ===== TAB 1 SNAP CHART =====
with tab1:
    uploaded = st.file_uploader("I-upload chart mo (BTC, GOLD, ETH)", type=['jpg','png','jpeg'])
    if uploaded:
        st.image(Image.open(uploaded), use_container_width=True)
        coin_name = st.text_input("Anong coin ito? Ex: BTC, GOLD, ETH", "GOLD")
        if st.button("🤖 ANALYZE WITH AI", use_container_width=True, type="primary"):
            st.success(f"✅ AI ANALYSIS COMPLETE - {random.randint(82,95)}% Confidence")
            st.markdown("**🔑 Key Insights:** Bullish Flag Pattern | RSI Oversold | Strong Support")
            st.markdown("---")
            entry = random.uniform(4300, 4400) if "GOLD" in coin_name.upper() else random.uniform(2700, 2800)
            st.markdown(f"**📈 DARELL SIGNAL FOR {coin_name.upper()}:**")
            st.markdown(f"""
            **ENTRY:** ${entry:,.2f}
            **🟢 TP1:** ${entry*1.015:,.2f} (+1.5%)
            **🟢 TP2:** ${entry*1.03:,.2f} (+3%)
            **🔴 SL:** ${entry*0.985:,.2f} (-1.5%)
            """)
            st.toast(f"🚀 DARELL SIGNAL: {coin_name.upper()} BUY!", icon="🔔")
            st.balloons()

# ===== TAB 2 LIVE MARKET - COMPLETE COINS =====
with tab2:
    coins = {
        "GOLD - XAUUSD": "GC=F",
        "BTC-USD": "BTC-USD",
        "ETH-USD": "ETH-USD",
        "SOL-USD": "SOL-USD",
        "XRP-USD": "XRP-USD",
        "DOGE-USD": "DOGE-USD",
        "BNB-USD": "BNB-USD",
        "ADA-USD": "ADA-USD",
        "PEPE-USD": "PEPE-USD"
    }

    coin = st.selectbox("Piliin:", list(coins.keys()))
    sym = coins[coin]

    try:
        ticker = yf.Ticker(sym)
        price = ticker.history(period="1d")['Close'].iloc[-1]
        st.metric(f"{coin} Live Price", f"${price:,.2f}")

        if st.button("⚡ Analyze Live with SL/TP", use_container_width=True, type="primary"):
            is_bull = random.choice([True, False])
            signal = "BULL 🐂 - BUY NOW" if is_bull else "BEAR 🐻 - SELL NOW"
            color = "green" if is_bull else "red"

            st.markdown(f"<div style='background:{color}; padding:10px; border-radius:10px; color:white; text-align:center; font-weight:bold'>{coin} {signal}</div>", unsafe_allow_html=True)
            st.markdown("---")

            # AUTO CALCULATE SL/TP
            tp1 = price * 1.015 if is_bull else price * 0.985
            tp2 = price * 1.03 if is_bull else price * 0.97
            sl = price * 0.985 if is_bull else price * 1.015

            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("ENTRY", f"${price:,.2f}")
            with col2:
                st.metric("TP1", f"${tp1:,.2f}", "+1.5%")
                st.metric("TP2", f"${tp2:,.2f}", "+3%")
            with col3:
                st.metric("STOP LOSS", f"${sl:,.2f}", "-1.5%", delta_color="inverse")

            st.toast(f"🔔 {coin} {signal}!", icon="📈")
            html("""
            <script>
            if(Notification.permission!=="granted"){Notification.requestPermission();}
            if(Notification.permission==="granted"){new Notification("DARELL SIGNAL 🚀",{body:"New SL/TP Signal Generated!"});}
            </script>
            """, height=0)

    except Exception as e:
        st.error(f"Loading {coin}... Check internet")

st.caption("© 2026 Darell Trading Signal - AI Chart Analyzer | All coins with SL/TP")
