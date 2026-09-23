import streamlit as st
import yfinance as yf

st.set_page_config(page_title="DARELL V9", layout="centered")
st.title("DARELL V9 ULTIMATE FIXED")

coins = {
"BTC/USDT": "BTC-USD",
"ETH/USDT": "ETH-USD",
"BNB/USDT": "BNB-USD",
"GOLD/USDT": "GC=F"
}

def get_price(sym):
    try:
        c = yf.Ticker(sym).history(period="5d")["Close"].iloc[-1]
        return float(c)
    except:
        return 2740.0

def get_type(tf):
    if tf in ["5M","15M","30M"]:
        return "SCALPING"
    if tf in ["1H","4H"]:
        return "INTRADAY"
    return "SWING"

tab1, tab2, tab3, tab4 = st.tabs(["ANALYZER","TF","NEWS","ALERTS"])

with tab1:
    p = st.selectbox("Pair", list(coins.keys()), index=1)
    tf = st.select_slider("TF", ["5M","15M","30M","1H","4H","1D","1W"], value="1H")
    t = get_type(tf)
    st.info(t)
    if st.button("Analyze", use_container_width=True, type="primary"):
        price = get_price(coins[p])
        st.metric("ENTRY", f"${price}")
        st.metric("TP1", f"${price*1.02:.2f}")
        st.metric("SL", f"${price*0.98:.2f}")
        st.success(f"{p} {t} {tf}")

with tab2:
    p = st.selectbox("Pair2", list(coins.keys()), key="p2")
    tf = st.select_slider("TF2", ["5M","15M","30M","1H","4H","1D","1W"], value="15M", key="tf2")
    t = get_type(tf)
    price = get_price(coins[p])
    st.write(f"Folder: {t}")
    st.write(f"Price ${price}")
    st.write(f"TP ${price*1.01:.2f} SL ${price*0.99:.2f}")

with tab3:
    p = st.selectbox("News Pair", list(coins.keys()), key="p3")
    st.write(f"Folder News {p}")
    st.link_button("News", f"https://finance.yahoo.com/quote/{coins[p]}/news")

with tab4:
    p = st.selectbox("Alert Pair", list(coins.keys()), key="p4")
    tf = st.selectbox("TF Alert", ["5M","15M","30M","1H","4H","1D","1W"], key="ta")
    t = get_type(tf)
    target = st.number_input("Target", value=2740.0)
    if "a" not in st.session_state:
        st.session_state["a"] = []
    if st.button("Set Alert"):
        st.session_state["a"].append(f"{t} {p} {tf} {target}")
        st.success("Alert Set")
    for i in st.session_state["a"]:
        st.write(i)
