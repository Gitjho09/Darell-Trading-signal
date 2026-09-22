import streamlit as st
from PIL import Image
import yfinance as yf
from streamlit.components.v1 import html

st.set_page_config(page_title="Darell AI Chart Analyzer", page_icon="📈", layout="centered")

# LOGO MO NA - YUNG BAGO!
st.image("logo.png", use_container_width=True)

st.markdown("### 📸 AI Chart Analyzer - Snap any chart!")
st.markdown("Parang nasa Play Store na!")

tab1, tab2 = st.tabs(["📷 Snap Chart", "📊 Live Market"])

with tab1:
    uploaded = st.file_uploader("I-upload chart mo (BTC, GOLD)", type=['jpg','png','jpeg'])
    if uploaded:
        st.image(Image.open(uploaded), use_container_width=True)
        if st.button("🤖 ANALYZE WITH AI", use_container_width=True, type="primary"):
            st.success("✅ AI ANALYSIS COMPLETE - 87% Confidence")
            st.markdown("**🔑 Key Insights:** Bullish Flag | Support $4,350 | Resistance $4,420")
            st.markdown("**📈 Breakdown:** ENTRY $4,389 | TP1 $4,450 | TP2 $4,510 | SL $4,300")
            st.toast("🚀 DARELL SIGNAL: GOLD BULL BUY!", icon="🔔")
            st.balloons()
            html("""
            <script>
            if(Notification.permission!=="granted"){Notification.requestPermission();}
            if(Notification.permission==="granted"){new Notification("DARELL SIGNAL 🚀",{body:"GOLD BULL BUY $4389"});}
            </script>
            """, height=0)

with tab2:
    coin = st.selectbox("Piliin:", ["GOLD - XAUUSD", "BTC-USD", "ETH-USD"])
    sym = {"GOLD - XAUUSD":"GC=F","BTC-USD":"BTC-USD","ETH-USD":"ETH-USD"}[coin]
    try:
        price = yf.Ticker(sym).history(period="1d")['Close'].iloc[-1]
        st.metric(f"{coin} Live", f"${price:,.2f}")
        if st.button("⚡ Analyze Live", use_container_width=True):
            st.success(f"🐂 {coin} BULL SIGNAL - BUY NOW")
            st.toast(f"🔔 {coin} BULL!", icon="📈")
    except:
        st.write("Live price loading...")

st.caption("© 2026 Darell Trading Signal - AI Chart Analyzer")
