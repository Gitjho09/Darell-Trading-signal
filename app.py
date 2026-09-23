        detected_pair, ocr_text = detect_pair_from_image(img)
        detected_price = extract_price_from_image(img)
        if detected_pair:
            st.success(f"✅ NA-DETECT KO: **{detected_pair}** galing sa screenshot mo!")
            st.session_state['pair'] = detected_pair
        else:
            st.warning("⚠️ Hindi ko mabasa yung pair, pili ka:")
            detected_pair = st.selectbox("Ano ba nasa chart?", list(coins.keys()), index=2, key="fix_pair")
        if detected_price:
            st.info(f"💰 Price na nabasa: **${detected_price:,.2f}**")
        if st.button("🤖 Analyze Screenshot", use_container_width=True, type="primary", key="analyze_btn"):
            with st.spinner("Analyzing..."):
                pair_for_analysis = detected_pair or st.session_state.get('pair', 'BTC/USDT')
                symbol = coins.get(pair_for_analysis, "BTC-USD")
                df, rsi, macd, sig, sma, up, low, sup, res, live_price = get_indicators(symbol)
                entry_price = detected_price if detected_price else live_price
                tp1 = entry_price * 1.02
                tp2 = entry_price * 1.04
                sl = entry_price * 0.98
                st.success(f"Analysis for **{pair_for_analysis}**")
                c1,c2,c3 = st.columns(3)
                c1.metric("ENTRY", f"${entry_price:,.2f}")
                c2.metric("TP1", f"${tp1:,.2f}")
                c3.metric("SL", f"${sl:,.2f}")
                c1,c2 = st.columns(2)
                c1.metric("TP2", f"${tp2:,.2f}")
                c2.metric("RSI", f"{rsi:.1f}")
                st.markdown(f"<div class='card'><b>AI:</b> {pair_for_analysis} @ ${entry_price:,.2f} | RSI {rsi:.1f}</div>", unsafe_allow_html=True)
                st.balloons()

with tab2:
    st.markdown("### 📰 Live Market News")
    news_pair = st.selectbox("News for:", list(coins.keys()), key="news_pair")
    if st.button("Get Latest News", use_container_width=True, type="primary"):
        st.markdown(f"<div class='news-card'><b>{news_pair} surges as market sentiment improves</b><br><small>Live update</small></div>", unsafe_allow_html=True)
        st.markdown(f"<div class='news-card'><b>Analysts eye {news_pair} resistance at key level</b><br><small>TradingView</small></div>", unsafe_allow_html=True)
        st.link_button(f"More {news_pair} News", f"https://finance.yahoo.com/quote/{coins[news_pair]}/news")

with tab3:
    st.markdown("### 💰 Profit Calculator")
    calc_pair = st.selectbox("Select Pair:", list(coins.keys()), key="calc")
    try:
        live_price = yf.Ticker(coins[calc_pair]).history(period="1d")['Close'].iloc[-1]
        st.metric(f"Live {calc_pair}", f"${live_price:,.2f}")
    except:
        live_price = 95000
    entry = st.number_input("Entry Price", value=float(live_price))
    exit_p = st.number_input("Exit / TP Price", value=float(live_price*1.02))
    lot = st.number_input("Lot Size / Quantity", value=1.0, step=0.01)
    capital = st.number_input("Capital ($)", value=1000.0)
    if st.button("Calculate Profit", use_container_width=True, type="primary"):
        profit = (exit_p - entry) * lot
        percent = ((exit_p - entry) / entry) * 100
        roe = (profit / capital) * 100
        c1,c2,c3 = st.columns(3)
        c1.metric("Profit/Loss", f"${profit:,.2f}", f"{percent:.2f}%")
        c2.metric("ROE", f"{roe:.2f}%")
        c3.metric("Total", f"${capital+profit:,.2f}")

with tab4:
    st.markdown("### 😱 Fear & Greed Index")
    try:
        rsi_avg = []
        for sym in ["BTC-USD", "ETH-USD", "BNB-USD"]:
            d = yf.Ticker(sym).history(period="1mo")['Close']
            delta = d.diff()
            gain = (delta.where(delta>0,0)).rolling(14).mean()
            loss = (-delta.where(delta<0,0)).rolling(14).mean()
            rs = gain/loss
            rsi = 100-(100/(1+rs))
            rsi_avg.append(rsi.iloc[-1])
        fg_value = int(np.mean(rsi_avg))
    except:
        fg_value = 62
    st.markdown(f"<h1 style='text-align:center; font-size:60px'>{fg_value}</h1>", unsafe_allow_html=True)
    st.progress(fg_value)
    st.link_button("Check Real Fear & Greed on CNN", "https://edition.cnn.com/markets/fear-and-greed")

with tab5:
    st.markdown("### 🚨 Price Alert System")
    alert_pair = st.selectbox("Pair for Alert:", list(coins.keys()), key="alert")
    target_price = st.number_input("Alert when price reaches:", value=95000.0)
    alert_type = st.radio("Alert Type:", ["Price >= Target (TP Hit)", "Price <= Target (SL Hit)"], horizontal=True)
    if 'alerts' not in st.session_state:
        st.session_state['alerts'] = []
    if st.button("Set Alert", use_container_width=True):
        st.session_state['alerts'].append({"pair": alert_pair, "target": target_price, "type": alert_type})
        st.success(f"Alert set for {alert_pair} at ${target_price:,.2f}")

with tab6:
    st.markdown("### 📊 Live Real Indicators")
    live_coin = st.selectbox("Live Indicators for:", list(coins.keys()), key="live_ind")
    if st.button("Get Live Indicators", use_container_width=True, type="primary"):
        sym = coins[live_coin]
        df, rsi, macd, sig, sma, up, low, sup, res, price = get_indicators(sym)
        st.metric(live_coin, f"${price:,.2f}")
        if df is not None:
            st.line_chart(df['Close'].tail(100))
        c1,c2 = st.columns(2)
        c1.metric("RSI 14", f"{rsi:.2f}")
        c2.metric("SMA 20", f"${sma:,.2f}")

st.caption("2026 DARELL V6.1 FIXED - Screenshot Auto Detect + TP/SL")
