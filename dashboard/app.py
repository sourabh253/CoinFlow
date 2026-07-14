import streamlit as st
import pandas as pd
import plotly.express as px
from sqlalchemy import create_engine

from config.config import *
from ml.predict import predict_next_price
from utils.investment import simulate_investment

# ---------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------
st.set_page_config(
    page_title="CoinFlow Analytics",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------------------------------------------------
# DATABASE CONNECTION
# ---------------------------------------------------
engine = create_engine(
    f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_sql("SELECT * FROM crypto_prices", engine)

# ---------------------------------------------------
# LOAD LATEST DATA
# ---------------------------------------------------
latest_df = df.sort_values("snapshot_time").groupby("coin_id").tail(1).copy()
latest_df.rename(columns={"price_change_percentage_24h": "change_24h"}, inplace=True)

# ---------------------------------------------------
# CSS ARCHITECTURE (GLOBAL DESKTOP THEME)
# ---------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* Global Reset and Layout Structure */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif;
    background-color: #CED1BC !important;
    color: #1E1E1E !important;
}

/* Hide Default Elements */
header, footer, [data-testid="stHeader"], [data-testid="stSidebar"] {
    visibility: hidden;
    display: none !important;
}

/* Remove default main block container padding and enforce full-width grid layout */
.block-container {
    padding: 0rem !important;
    max-width: 100% !important;
}

/* MAIN CONTENT SPACE */
.main-content {
    max-width: 100%;
    margin: 0 auto;
    padding: 40px 48px;
    background-color: #CED1BC;
}

/* Horizontal Top Header Panel */
.header-container {
    margin-bottom: 32px;
}
.brand-title-top {
    font-size: 40px;
    font-weight: 700;
    color: #1E1E1E !important;
    margin: 0 0 4px 0;
    letter-spacing: -1px;
}
.developer-text {
    font-size: 14px;
    font-weight: 600;
    color: #1E1E1E !important;
    margin: 0;
}
.developer-subtext {
    font-size: 12px;
    color: #4B5563 !important;
    margin: 2px 0 0 0;
}

/* Section Title Typography Styles */
.section-title-custom {
    font-size: 22px;
    font-weight: 700;
    color: #1E1E1E !important;
    margin: 32px 0 16px 0;
}
.card-title-custom {
    font-size: 18px;
    font-weight: 700;
    color: #1E1E1E !important;
    margin-bottom: 15px;
}

/* Custom Core UI Cards Container */
.dashboard-card-wrapper {
    background-color: #9FA86D !important;
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 25px;
    display: flex;
    flex-direction: column;
}

/* Premium KPI System Elements */
.kpi-flex-card {
    background-color: #9FA86D !important;
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 130px;
    margin-bottom: 25px;
}
.kpi-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.kpi-title-box {
    display: flex;
    align-items: center;
    gap: 8px;
}
.kpi-title {
    font-size: 18px;
    font-weight: 700;
    color: #1E1E1E !important;
}
.kpi-subtitle {
    font-size: 14px;
    color: #4B5563 !important;
}
.kpi-value {
    font-size: 26px;
    font-weight: 700;
    color: #1E1E1E !important;
    margin: 12px 0 4px 0;
}
.kpi-trend {
    font-size: 14px;
    font-weight: 600;
    display: inline-flex;
    align-items: center;
    gap: 4px;
    color: #1E1E1E !important;
}

/* Selector Card Styles */
.selector-card-center {
    background-color: #9FA86D !important;
    border-radius: 25px;
    padding: 25px;
    box-shadow: 0 10px 25px rgba(0,0,0,0.08);
    margin-bottom: 25px;
}

/* Streamlit Element Styling Injectors */
.stButton>button {
    width: 100% !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 16px !important;
    background-color: #9FA86D !important;
    color: #1E1E1E !important;
    height: 48px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.2s ease !important;
}
.stButton>button:hover {
    background-color: #CED1BC !important;
    color: #1E1E1E !important;
    border-color: #1E1E1E !important;
}
.stDownloadButton>button {
    width: 100% !important;
    border: 1px solid #1E1E1E !important;
    border-radius: 16px !important;
    background-color: #9FA86D !important;
    color: #1E1E1E !important;
    height: 48px !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.03) !important;
    transition: all 0.2s ease !important;
}
.stDownloadButton>button:hover {
    background-color: #CED1BC !important;
    color: #1E1E1E !important;
    border-color: #1E1E1E !important;
}

/* ---------------------------------------------------
    STRICT COMPREHENSIVE ADVANCED SELECTBOX FIXES
--------------------------------------------------- */
div[data-baseweb="select"] {
    border-radius: 14px !important;
    border: 1px solid #1E1E1E !important;
    background-color: #1F2027 !important;
}
div[data-baseweb="select"] div,
div[data-baseweb="select"] span,
div[data-baseweb="select"] svg,
div[data-baseweb="select"] input {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] *,
[role="listbox"],
[role="listbox"] * {
    background-color: #1F2027 !important;
    color: #FFFFFF !important;
}
ul[data-baseweb="menu"],
ul[data-baseweb="menu"] * {
    background-color: #1F2027 !important;
    color: #FFFFFF !important;
}
li[role="option"],
div[role="option"],
[data-baseweb="menu"] [role="option"] {
    background-color: #1F2027 !important;
    color: #FFFFFF !important;
    transition: background-color 0.15s ease-in-out !important;
}
li[role="option"]:hover,
div[role="option"]:hover,
[data-baseweb="menu"] [role="option"]:hover,
li[role="option"][aria-selected="false"]:hover,
div[role="option"][aria-selected="false"]:hover {
    background-color: #343746 !important;
    color: #FFFFFF !important;
}
li[role="option"][aria-selected="true"],
div[role="option"][aria-selected="true"],
[data-baseweb="menu"] [role="option"][aria-selected="true"] {
    background-color: #4A5060 !important;
    color: #FFFFFF !important;
}
div[data-baseweb="select"] svg path {
    fill: #FFFFFF !important;
}
[role="listbox"]::-webkit-scrollbar,
ul[data-baseweb="menu"]::-webkit-scrollbar {
    width: 6px !important;
    height: 6px !important;
    display: block !important;
}
[role="listbox"]::-webkit-scrollbar-thumb,
ul[data-baseweb="menu"]::-webkit-scrollbar-thumb {
    background: #4A5060 !important;
    border-radius: 4px !important;
}

/* ---------------------------------------------------
    DATAFRAME, ALERT AND SYSTEM METRICS INJECTIONS
--------------------------------------------------- */
div[data-testid="stDataFrame"] {
    border-radius: 20px !important;
    overflow: hidden !important;
    border: 1px solid #1E1E1E !important;
    background-color: #9FA86D !important;
    padding: 10px;
}
div[data-testid="stDataFrame"] [role="gridcell"] div {
    color: #1E1E1E !important;
}
div[data-testid="stAlert"] {
    border-radius: 18px !important;
    border: 1px solid #1E1E1E !important;
    background-color: #CED1BC !important;
}
div[data-testid="stAlert"] div {
    color: #1E1E1E !important;
}
input {
    border-radius: 14px !important;
    background-color: #CED1BC !important;
    color: #1E1E1E !important;
    border: 1px solid #1E1E1E !important;
}
label, p, span, div, h1, h2, h3, h4, h5, h6, caption {
    color: #1E1E1E !important;
}
div[data-testid="stMetricValue"] > div {
    color: #1E1E1E !important;
}
div[data-testid="stMetricLabel"] > div {
    color: #4B5563 !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------
# COMMON CHART STYLE WITH VISIBLE TOOLBAR
# ---------------------------------------------------
def style_chart(fig):
    fig.update_layout(
        height=380,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Inter", color="#1E1E1E", size=12),
        title_font=dict(size=16, color="#1E1E1E", family="Inter"),
        margin=dict(l=15, r=15, t=50, b=15),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=dict(color="#1E1E1E"),
            title_font=dict(color="#1E1E1E")
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="#CED1BC",
            zeroline=False,
            tickfont=dict(color="#1E1E1E"),
            title_font=dict(color="#1E1E1E")
        ),
        legend=dict(
            orientation="h",
            y=1.05,
            x=0.38,
            bgcolor="rgba(0,0,0,0)",
            font=dict(color="#4B5563")
        ),
        hoverlabel=dict(
            bgcolor="#CED1BC",
            font_color="#1E1E1E",
            font_family="Inter",
            bordercolor="#1E1E1E"
        ),
        modebar=dict(
            bgcolor="rgba(255,255,255,0.95)",
            color="#1E1E1E",
            activecolor="#000000"
        )
    )
    return fig

# ---------------------------------------------------
# MAIN DASHBOARD CONTAINER
# ---------------------------------------------------
st.markdown('<div class="main-content">', unsafe_allow_html=True)

# HEADER SECTION
st.markdown("""
<div class="header-container" style="padding-top:50px;">
    <div class="brand-title-top">CoinFlow Analytics</div>
    <div class="developer-text">Developed by Sourabh</div>
    <div class="developer-subtext">(Just a Project, Not for Any Commercial Purpose)</div>
</div>
""", unsafe_allow_html=True)

# SELECT COIN CARD AREA
st.markdown('<div class="selector-card-center">', unsafe_allow_html=True)
st.markdown('<div class="card-title-custom">Select Coin</div>', unsafe_allow_html=True)
coin_options = sorted(latest_df["coin_id"].unique())

# Intelligent initial calculation to default to "bitcoin" safely if present
default_index = coin_options.index("bitcoin") if "bitcoin" in coin_options else 0

selected_coin = st.selectbox(
    "Select Active Asset Context",
    options=coin_options,
    index=default_index,
    placeholder="Select the Coin",
    label_visibility="collapsed"
)
st.markdown('</div>', unsafe_allow_html=True)

# ---------------------------------------------------
# KPI DATA COMPUTATION
# ---------------------------------------------------
btc_row = latest_df.loc[latest_df["symbol"] == "btc"]
eth_row = latest_df.loc[latest_df["symbol"] == "eth"]

btc_price = btc_row["current_price"].iloc[0] if not btc_row.empty else 0.0
btc_change = btc_row["change_24h"].iloc[0] if not btc_row.empty else 0.0

eth_price = eth_row["current_price"].iloc[0] if not eth_row.empty else 0.0
eth_change = eth_row["change_24h"].iloc[0] if not eth_row.empty else 0.0

total_volume = latest_df["total_volume"].sum()

# ROW 1: KPI CARDS ROW
kpi_cols = st.columns(3)

with kpi_cols[0]:
    trend_sign = "Up" if btc_change >= 0 else "Down"
    st.markdown(f"""
    <div class="kpi-flex-card">
        <div class="kpi-header">
            <div class="kpi-title-box">
                <div>
                    <div class="kpi-title">Bitcoin</div>
                    <div class="kpi-subtitle">BTC / USD</div>
                </div>
            </div>
            <div class="kpi-trend trend-up">{trend_sign} {abs(btc_change):.2f}%</div>
        </div>
        <div class="kpi-value">${btc_price:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[1]:
    trend_sign = "Up" if eth_change >= 0 else "Down"
    st.markdown(f"""
    <div class="kpi-flex-card">
        <div class="kpi-header">
            <div class="kpi-title-box">
                <div>
                    <div class="kpi-title">Ethereum</div>
                    <div class="kpi-subtitle">ETH / USD</div>
                </div>
            </div>
            <div class="kpi-trend trend-down">{trend_sign} {abs(eth_change):.2f}%</div>
        </div>
        <div class="kpi-value">${eth_price:,.2f}</div>
    </div>
    """, unsafe_allow_html=True)

with kpi_cols[2]:
    st.markdown(f"""
    <div class="kpi-flex-card">
        <div class="kpi-header">
            <div class="kpi-title-box">
                <div>
                    <div class="kpi-title">24H Volume</div>
                    <div class="kpi-subtitle">Global Aggregated Market</div>
                </div>
            </div>
            <div class="kpi-trend trend-up">Live Data</div>
        </div>
        <div class="kpi-value">${total_volume:,.0f}</div>
    </div>
    """, unsafe_allow_html=True)

# ROW 2: HISTORICAL PRICE | AI FORECAST
history_query = f"SELECT coin_id, current_price, snapshot_time FROM crypto_prices WHERE coin_id='{selected_coin}' ORDER BY snapshot_time"
history_df = pd.read_sql(history_query, engine)

row2_cols = st.columns([2, 1])

with row2_cols[0]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    fig_history = px.line(
        history_df, x="snapshot_time", y="current_price", markers=True,
        color_discrete_sequence=["#1E1E1E"], title=f"Historical Price Continuum ({selected_coin.upper()})"
    )
    st.plotly_chart(style_chart(fig_history), use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

with row2_cols[1]:
    st.markdown('<div class="dashboard-card-wrapper" style="height: 100%;">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-custom">AI Forecast</div>', unsafe_allow_html=True)
    
    current_price, predicted_price, percentage, action, confidence = predict_next_price(selected_coin)
    
    fc1, fc2 = st.columns(2)
    with fc1:
        st.caption("Current Price")
        st.subheader(f"${current_price:,.2f}")
        st.caption("Confidence")
        st.subheader(f"{confidence}%")
    with fc2:
        st.caption("Predicted Price")
        st.subheader(f"${predicted_price:,.2f}")
        st.caption("Recommendation")
        st.info(action)
    st.markdown('</div>', unsafe_allow_html=True)

# ROW 3: TOP GAINERS | TOP LOSERS
st.markdown('<div class="section-title-custom">Market Overview</div>', unsafe_allow_html=True)
row3_cols = st.columns(2)

with row3_cols[0]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    gainers = latest_df.sort_values("change_24h", ascending=False).head(10)
    fig_gainers = px.bar(
        gainers, x="coin_name", y="change_24h",
        color_discrete_sequence=["#1E1E1E"], title="Top Gainers"
    )
    st.plotly_chart(style_chart(fig_gainers), use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

with row3_cols[1]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    losers = latest_df.sort_values("change_24h", ascending=True).head(10)
    fig_losers = px.bar(
        losers, x="coin_name", y="change_24h",
        color_discrete_sequence=["#4B5563"], title="Top Losers"
    )
    st.plotly_chart(style_chart(fig_losers), use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# ROW 4: TRADING VOLUME | MARKET CAP
row4_cols = st.columns(2)

with row4_cols[0]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    volume = latest_df.sort_values("total_volume", ascending=False).head(10)
    fig_volume = px.bar(
        volume, x="coin_name", y="total_volume",
        color_discrete_sequence=["#1E1E1E"], title="Trading Volume"
    )
    st.plotly_chart(style_chart(fig_volume), use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

with row4_cols[1]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    market_cap_df = latest_df.sort_values("market_cap", ascending=False).head(10)
    fig_market_cap = px.bar(
        market_cap_df, x="coin_name", y="market_cap",
        color_discrete_sequence=["#4B5563"], title="Market Cap Leaders"
    )
    st.plotly_chart(style_chart(fig_market_cap), use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# ROW 5: BTC vs ETH Comparison | Market Dominance
row5_cols = st.columns([1.5, 1])

with row5_cols[0]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    compare_df = latest_df[latest_df["symbol"].isin(["btc", "eth", "sol"])]
    fig_compare = px.bar(
        compare_df, x="symbol", y="current_price", color="symbol",
        color_discrete_map={"btc": "#1E1E1E", "eth": "#4B5563", "sol": "#7F8C8D"},
        title="BTC vs ETH Comparison Chart"
    )
    st.plotly_chart(style_chart(fig_compare), use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

with row5_cols[1]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    total_market_cap = latest_df["market_cap"].sum()
    btc_market_cap = latest_df.loc[latest_df["symbol"] == "btc", "market_cap"].sum()
    eth_market_cap = latest_df.loc[latest_df["symbol"] == "eth", "market_cap"].sum()
    others_market_cap = total_market_cap - btc_market_cap - eth_market_cap

    dominance_df = pd.DataFrame({
        "Category": ["Bitcoin", "Ethereum", "Others"],
        "Market Cap": [btc_market_cap, eth_market_cap, others_market_cap]
    })

    fig_dominance = px.pie(
        dominance_df, names="Category", values="Market Cap", hole=0.55,
        color_discrete_sequence=["#1E1E1E", "#4B5563", "#7F8C8D"],
        title="Market Dominance"
    )
    fig_dominance = style_chart(fig_dominance)
    fig_dominance.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_dominance, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

# ROW 6: Market Sentiment | Latest Snapshot Table
row6_cols = st.columns([1, 2])

with row6_cols[0]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    bullish = len(latest_df[latest_df["change_24h"] > 5])
    bearish = len(latest_df[latest_df["change_24h"] < -5])
    neutral = len(latest_df) - bullish - bearish

    sentiment_df = pd.DataFrame({
        "Sentiment": ["Bullish", "Neutral", "Bearish"],
        "Count": [bullish, neutral, bearish]
    })

    fig_sentiment = px.pie(
        sentiment_df, names="Sentiment", values="Count", hole=0.55,
        color_discrete_sequence=["#1E1E1E", "#7F8C8D", "#4B5563"],
        title="Market Sentiment"
    )
    fig_sentiment = style_chart(fig_sentiment)
    fig_sentiment.update_traces(textinfo="percent+label")
    st.plotly_chart(fig_sentiment, use_container_width=True, config={'displayModeBar': True})
    st.markdown('</div>', unsafe_allow_html=True)

with row6_cols[1]:
    st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
    st.markdown('<div class="card-title-custom">Latest Snapshot Table</div>', unsafe_allow_html=True)
    st.dataframe(latest_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

# ROW 7: INVESTMENT SIMULATOR
st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
st.markdown('<div class="card-title-custom">Investment Simulator</div>', unsafe_allow_html=True)

sim_input_col, sim_metrics_col = st.columns([1, 2])

with sim_input_col:
    investment = st.number_input(
        "Investment Amount (₹)",
        min_value=100, value=10000, step=500
    )

result = simulate_investment(investment, current_price, predicted_price)

with sim_metrics_col:
    m_col1, m_col2, m_col3 = st.columns(3)
    with m_col1:
        st.metric("Current Price", f"${current_price:,.2f}")
    with m_col2:
        st.metric("Predicted Price", f"${predicted_price:,.2f}")
    with m_col3:
        st.metric("Confidence", f"{confidence}%")

st.markdown("<hr style='border-color:#1E1E1E; margin:20px 0;'>", unsafe_allow_html=True)

res_col1, res_col2 = st.columns([1, 2])
with res_col1:
    st.markdown("<label style='font-size:14px; color:#1E1E1E; font-weight:600;'>Recommendation Matrix</label>", unsafe_allow_html=True)
    st.info(f"RECOMMENDED DIRECTION: {action}")

with res_col2:
    st.info(f"""
    Investment Strategy Metrics Output
    * Invested Principal: ₹{investment:,.0f}
    * Estimated Horizon Value: ₹{result['future_value']:,.2f}
    * Expected Yield Return: {percentage:.2f}% (Net Delta: ₹{result['profit']:,.2f})
    """)
st.markdown('</div>', unsafe_allow_html=True)

# ROW 8: DOWNLOAD BUTTON CARD
st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
csv = latest_df.to_csv(index=False)
st.download_button(
    "Download CSV Snapshot",
    csv, "crypto_snapshot.csv", "text/csv"
)
st.markdown('</div>', unsafe_allow_html=True)

# ROW 9: REFRESH BUTTON CARD
st.markdown('<div class="dashboard-card-wrapper">', unsafe_allow_html=True)
if st.button("Refresh Dashboard"):
    st.rerun()
st.markdown('</div>', unsafe_allow_html=True)

# SYSTEM FOOTER BLOCK
st.markdown("""
<div style="text-align: center; color: #4B5563; font-size: 13px; margin-top: 60px; padding-top: 20px; border-top: 1px solid #1E1E1E;">
    Made with care by <b>Sourabh</b> | CoinFlow © 2026 All Rights Reserved
</div>
""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)