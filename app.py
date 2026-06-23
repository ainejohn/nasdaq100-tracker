"""
NASDAQ-100 Tracker — Streamlit Web App
=======================================
A beginner-friendly data science app that tracks all 101 tickers
(100 companies) of the NASDAQ-100 index using yfinance for live data.

Install dependencies:
    pip install streamlit yfinance pandas plotly

Run:
    streamlit run nasdaq100_tracker.py
"""

import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import date, timedelta

# ─────────────────────────────────────────────────────────────────────────────
# 1.  NASDAQ-100 TICKERS  (101 symbols for 100 companies, Alphabet has GOOG+GOOGL)
# ─────────────────────────────────────────────────────────────────────────────
NASDAQ100 = {
    "AAPL":  ("Apple Inc.",                        "Technology"),
    "MSFT":  ("Microsoft Corporation",             "Technology"),
    "NVDA":  ("NVIDIA Corporation",                "Technology"),
    "AMZN":  ("Amazon.com Inc.",                   "Consumer Discretionary"),
    "META":  ("Meta Platforms Inc.",               "Communication Services"),
    "GOOGL": ("Alphabet Inc. (Class A)",           "Communication Services"),
    "GOOG":  ("Alphabet Inc. (Class C)",           "Communication Services"),
    "TSLA":  ("Tesla Inc.",                        "Consumer Discretionary"),
    "AVGO":  ("Broadcom Inc.",                     "Technology"),
    "COST":  ("Costco Wholesale Corporation",      "Consumer Staples"),
    "NFLX":  ("Netflix Inc.",                      "Communication Services"),
    "ASML":  ("ASML Holding N.V.",                 "Technology"),
    "AMD":   ("Advanced Micro Devices Inc.",       "Technology"),
    "AZN":   ("AstraZeneca PLC",                   "Healthcare"),
    "PEP":   ("PepsiCo Inc.",                      "Consumer Staples"),
    "LIN":   ("Linde PLC",                         "Materials"),
    "QCOM":  ("QUALCOMM Incorporated",             "Technology"),
    "INTU":  ("Intuit Inc.",                       "Technology"),
    "ARM":   ("Arm Holdings PLC",                  "Technology"),
    "AMAT":  ("Applied Materials Inc.",            "Technology"),
    "CSCO":  ("Cisco Systems Inc.",                "Technology"),
    "TXN":   ("Texas Instruments Incorporated",   "Technology"),
    "ISRG":  ("Intuitive Surgical Inc.",           "Healthcare"),
    "AMGN":  ("Amgen Inc.",                        "Healthcare"),
    "MU":    ("Micron Technology Inc.",            "Technology"),
    "CMCSA": ("Comcast Corporation",               "Communication Services"),
    "HON":   ("Honeywell International Inc.",      "Industrials"),
    "LRCX":  ("Lam Research Corporation",         "Technology"),
    "PANW":  ("Palo Alto Networks Inc.",           "Technology"),
    "VRTX":  ("Vertex Pharmaceuticals Inc.",       "Healthcare"),
    "ADI":   ("Analog Devices Inc.",               "Technology"),
    "KLAC":  ("KLA Corporation",                   "Technology"),
    "SBUX":  ("Starbucks Corporation",             "Consumer Discretionary"),
    "REGN":  ("Regeneron Pharmaceuticals Inc.",    "Healthcare"),
    "MELI":  ("MercadoLibre Inc.",                 "Consumer Discretionary"),
    "SNPS":  ("Synopsys Inc.",                     "Technology"),
    "CDNS":  ("Cadence Design Systems Inc.",       "Technology"),
    "CRWD":  ("CrowdStrike Holdings Inc.",         "Technology"),
    "MDLZ":  ("Mondelez International Inc.",       "Consumer Staples"),
    "CTAS":  ("Cintas Corporation",                "Industrials"),
    "MRVL":  ("Marvell Technology Inc.",           "Technology"),
    "PDD":   ("PDD Holdings Inc.",                 "Consumer Discretionary"),
    "CEG":   ("Constellation Energy Corporation", "Utilities"),
    "ORLY":  ("O'Reilly Automotive Inc.",          "Consumer Discretionary"),
    "ADSK":  ("Autodesk Inc.",                     "Technology"),
    "MAR":   ("Marriott International Inc.",       "Consumer Discretionary"),
    "FTNT":  ("Fortinet Inc.",                     "Technology"),
    "CSX":   ("CSX Corporation",                   "Industrials"),
    "ADP":   ("Automatic Data Processing Inc.",    "Technology"),
    "ROP":   ("Roper Technologies Inc.",           "Industrials"),
    "ABNB":  ("Airbnb Inc.",                       "Consumer Discretionary"),
    "PCAR":  ("PACCAR Inc.",                       "Industrials"),
    "KDP":   ("Keurig Dr Pepper Inc.",             "Consumer Staples"),
    "ROST":  ("Ross Stores Inc.",                  "Consumer Discretionary"),
    "MCHP":  ("Microchip Technology Inc.",         "Technology"),
    "WDAY":  ("Workday Inc.",                      "Technology"),
    "DXCM":  ("DexCom Inc.",                       "Healthcare"),
    "ODFL":  ("Old Dominion Freight Line Inc.",    "Industrials"),
    "EA":    ("Electronic Arts Inc.",              "Communication Services"),
    "EXC":   ("Exelon Corporation",                "Utilities"),
    "IDXX":  ("IDEXX Laboratories Inc.",           "Healthcare"),
    "BIIB":  ("Biogen Inc.",                       "Healthcare"),
    "PAYX":  ("Paychex Inc.",                      "Technology"),
    "TTWO":  ("Take-Two Interactive Software",     "Communication Services"),
    "MNST":  ("Monster Beverage Corporation",      "Consumer Staples"),
    "XEL":   ("Xcel Energy Inc.",                  "Utilities"),
    "LULU":  ("Lululemon Athletica Inc.",          "Consumer Discretionary"),
    "CTSH":  ("Cognizant Technology Solutions",    "Technology"),
    "GEHC":  ("GE HealthCare Technologies",        "Healthcare"),
    "FAST":  ("Fastenal Company",                  "Industrials"),
    "KHC":   ("The Kraft Heinz Company",           "Consumer Staples"),
    "VRSK":  ("Verisk Analytics Inc.",             "Industrials"),
    "ON":    ("ON Semiconductor Corporation",      "Technology"),
    "CCEP":  ("Coca-Cola Europacific Partners",    "Consumer Staples"),
    "ANSS":  ("ANSYS Inc.",                        "Technology"),
    "TEAM":  ("Atlassian Corporation",             "Technology"),
    "CDW":   ("CDW Corporation",                   "Technology"),
    "DDOG":  ("Datadog Inc.",                      "Technology"),
    "CPRT":  ("Copart Inc.",                       "Industrials"),
    "NXPI":  ("NXP Semiconductors N.V.",           "Technology"),
    "FANG":  ("Diamondback Energy Inc.",           "Energy"),
    "DLTR":  ("Dollar Tree Inc.",                  "Consumer Discretionary"),
    "ILMN":  ("Illumina Inc.",                     "Healthcare"),
    "GILD":  ("Gilead Sciences Inc.",              "Healthcare"),
    "GFS":   ("GlobalFoundries Inc.",              "Technology"),
    "BKR":   ("Baker Hughes Company",              "Energy"),
    "PYPL":  ("PayPal Holdings Inc.",              "Financials"),
    "MDB":   ("MongoDB Inc.",                      "Technology"),
    "MRNA":  ("Moderna Inc.",                      "Healthcare"),
    "TTD":   ("The Trade Desk Inc.",               "Technology"),
    "PTON":  ("Peloton Interactive Inc.",          "Consumer Discretionary"),
    "ZS":    ("Zscaler Inc.",                      "Technology"),
    "SGEN":  ("Seagen Inc.",                       "Healthcare"),
    "ENPH":  ("Enphase Energy Inc.",               "Technology"),
    "WBA":   ("Walgreens Boots Alliance Inc.",     "Consumer Staples"),
    "ALGN":  ("Align Technology Inc.",             "Healthcare"),
    "LCID":  ("Lucid Group Inc.",                  "Consumer Discretionary"),
    "WBD":   ("Warner Bros. Discovery Inc.",       "Communication Services"),
    "RIVN":  ("Rivian Automotive Inc.",            "Consumer Discretionary"),
    "ZM":    ("Zoom Video Communications Inc.",    "Technology"),
}

SECTORS = sorted(set(v[1] for v in NASDAQ100.values()))

SECTOR_COLORS = {
    "Technology":               "#4285F4",
    "Communication Services":   "#9B59B6",
    "Consumer Discretionary":   "#E67E22",
    "Consumer Staples":         "#27AE60",
    "Healthcare":               "#E74C3C",
    "Industrials":              "#1ABC9C",
    "Materials":                "#F1C40F",
    "Energy":                   "#D35400",
    "Utilities":                "#2ECC71",
    "Financials":               "#3498DB",
}

# ─────────────────────────────────────────────────────────────────────────────
# 2.  PAGE CONFIG
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="NASDAQ-100 Tracker",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# 3.  CUSTOM CSS  — dark finance dashboard feel
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
/* ── Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

/* ── App background ── */
.stApp { background-color: #0d1117; color: #e6edf3; }

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: #161b22;
    border-right: 1px solid #30363d;
}
section[data-testid="stSidebar"] .block-container { padding-top: 1.5rem; }

/* ── Metric cards ── */
[data-testid="metric-container"] {
    background: #161b22;
    border: 1px solid #30363d;
    border-radius: 10px;
    padding: 1rem;
}
[data-testid="metric-container"] label { color: #8b949e !important; font-size: 0.75rem !important; text-transform: uppercase; letter-spacing: .06em; }
[data-testid="metric-container"] [data-testid="stMetricValue"] { font-family: 'JetBrains Mono', monospace; font-size: 1.5rem !important; }

/* ── Dataframe ── */
.dataframe { font-family: 'JetBrains Mono', monospace !important; font-size: 0.82rem !important; }

/* ── Section headers ── */
.section-header {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: .12em;
    text-transform: uppercase;
    color: #8b949e;
    margin: 1.2rem 0 0.4rem 0;
    padding-bottom: 4px;
    border-bottom: 1px solid #30363d;
}

/* ── Ticker badge ── */
.ticker-badge {
    display: inline-block;
    background: #1f6feb22;
    color: #58a6ff;
    border: 1px solid #1f6feb55;
    border-radius: 6px;
    padding: 2px 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.8rem;
    font-weight: 600;
}

/* ── Hero title ── */
.hero-title {
    font-size: 1.6rem;
    font-weight: 700;
    color: #e6edf3;
    margin-bottom: 0;
    line-height: 1.2;
}
.hero-sub {
    font-size: 0.85rem;
    color: #8b949e;
    margin-top: 2px;
}

/* ── Hide streamlit branding ── */
#MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# 4.  SIDEBAR — Controls
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 📈 NASDAQ-100")
    st.markdown("Beginner Data Science Tracker")
    st.divider()

    # ── Sector filter ──
    st.markdown('<p class="section-header">Filter by Sector</p>', unsafe_allow_html=True)
    selected_sectors = st.multiselect(
        label="Sectors",
        options=SECTORS,
        default=SECTORS,
        label_visibility="collapsed",
    )

    # ── Ticker selector ──
    st.markdown('<p class="section-header">Choose Stock</p>', unsafe_allow_html=True)
    filtered_tickers = [
        t for t, (_, sec) in NASDAQ100.items() if sec in selected_sectors
    ]
    selected_ticker = st.selectbox(
        "Ticker",
        options=filtered_tickers,
        format_func=lambda t: f"{t} — {NASDAQ100[t][0][:28]}",
        label_visibility="collapsed",
    )

    # ── Date range ──
    st.markdown('<p class="section-header">Date Range</p>', unsafe_allow_html=True)
    period_option = st.radio(
        "Period",
        ["1M", "3M", "6M", "1Y", "2Y", "5Y"],
        index=3,
        horizontal=True,
        label_visibility="collapsed",
    )
    period_map = {"1M": 30, "3M": 90, "6M": 180, "1Y": 365, "2Y": 730, "5Y": 1825}
    end_dt   = date.today()
    start_dt = end_dt - timedelta(days=period_map[period_option])

    # ── Chart type ──
    st.markdown('<p class="section-header">Chart Style</p>', unsafe_allow_html=True)
    chart_type = st.radio(
        "Chart",
        ["Candlestick", "Line", "OHLC"],
        horizontal=True,
        label_visibility="collapsed",
    )

    # ── Overlays ──
    st.markdown('<p class="section-header">Overlays</p>', unsafe_allow_html=True)
    show_sma20  = st.checkbox("SMA 20",    value=True)
    show_sma50  = st.checkbox("SMA 50",    value=True)
    show_volume = st.checkbox("Volume",    value=True)
    show_bb     = st.checkbox("Bollinger Bands", value=False)

# ─────────────────────────────────────────────────────────────────────────────
# 5.  DATA FETCHING  (cached so we don't hit Yahoo Finance on every rerun)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=300, show_spinner=False)   # re-fetch every 5 minutes
def fetch_stock(ticker: str, start: date, end: date) -> pd.DataFrame:
    df = yf.download(ticker, start=str(start), end=str(end), auto_adjust=True, progress=False)
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    return df


@st.cache_data(ttl=300, show_spinner=False)
def fetch_quote(ticker: str) -> dict:
    info = yf.Ticker(ticker).fast_info
    return {
        "price":       getattr(info, "last_price",         None),
        "prev_close":  getattr(info, "previous_close",     None),
        "market_cap":  getattr(info, "market_cap",         None),
        "52w_high":    getattr(info, "fifty_two_week_high", None),
        "52w_low":     getattr(info, "fifty_two_week_low",  None),
        "volume":      getattr(info, "last_volume",        None),
    }


@st.cache_data(ttl=600, show_spinner=False)
def fetch_overview(tickers: list[str]) -> pd.DataFrame:
    rows = []
    for t in tickers:
        try:
            info = yf.Ticker(t).fast_info
            price      = getattr(info, "last_price",     None)
            prev_close = getattr(info, "previous_close", None)
            chg        = ((price - prev_close) / prev_close * 100) if price and prev_close else None
            rows.append({
                "Ticker":  t,
                "Company": NASDAQ100[t][0],
                "Sector":  NASDAQ100[t][1],
                "Price":   round(price, 2) if price else None,
                "Change%": round(chg, 2)   if chg   else None,
            })
        except Exception:
            rows.append({
                "Ticker":  t,
                "Company": NASDAQ100[t][0],
                "Sector":  NASDAQ100[t][1],
                "Price":   None,
                "Change%": None,
            })
    return pd.DataFrame(rows)

# ─────────────────────────────────────────────────────────────────────────────
# 6.  MAIN CONTENT — Tabs
# ─────────────────────────────────────────────────────────────────────────────
company_name = NASDAQ100[selected_ticker][0]
sector       = NASDAQ100[selected_ticker][1]
sector_color = SECTOR_COLORS.get(sector, "#8b949e")

# ── Hero header ──
col_title, col_badge = st.columns([5, 1])
with col_title:
    st.markdown(
        f'<p class="hero-title">{company_name}</p>'
        f'<p class="hero-sub">'
        f'<span class="ticker-badge">{selected_ticker}</span>&nbsp;&nbsp;'
        f'<span style="color:{sector_color}">● {sector}</span>'
        f'</p>',
        unsafe_allow_html=True,
    )
with col_badge:
    st.caption(f"Period: **{period_option}** · Style: **{chart_type}**")

st.write("")

tab_chart, tab_overview, tab_data, tab_guide = st.tabs([
    "📊 Chart", "🌐 Index Overview", "📋 Raw Data", "📚 Beginner Guide"
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CHART
# ══════════════════════════════════════════════════════════════════════════════
with tab_chart:
    with st.spinner(f"Fetching {selected_ticker} data…"):
        df   = fetch_stock(selected_ticker, start_dt, end_dt)
        info = fetch_quote(selected_ticker)

    if df.empty:
        st.warning(f"No data returned for **{selected_ticker}**. Try a different ticker or date range.")
    else:
        # ── KPI Metrics ──
        price      = info["price"]     or df["Close"].iloc[-1]
        prev_close = info["prev_close"] or df["Close"].iloc[-2]
        chg        = price - prev_close
        chg_pct    = chg / prev_close * 100

        m1, m2, m3, m4, m5 = st.columns(5)
        m1.metric("Price",          f"${price:,.2f}",
                  f"{chg:+.2f}  ({chg_pct:+.2f}%)",
                  delta_color="normal")
        m2.metric("52-Week High",   f"${info['52w_high']:,.2f}" if info["52w_high"] else "—")
        m3.metric("52-Week Low",    f"${info['52w_low']:,.2f}"  if info["52w_low"]  else "—")
        m4.metric("Market Cap",
                  f"${info['market_cap']/1e9:,.1f}B" if info["market_cap"] else "—")
        m5.metric("Volume",
                  f"{info['volume']/1e6:,.2f}M" if info["volume"] else "—")

        st.write("")

        # ── Compute SMAs & Bollinger ──
        df["SMA20"] = df["Close"].rolling(20).mean()
        df["SMA50"] = df["Close"].rolling(50).mean()
        if show_bb:
            df["BB_mid"]   = df["Close"].rolling(20).mean()
            df["BB_upper"] = df["BB_mid"] + 2 * df["Close"].rolling(20).std()
            df["BB_lower"] = df["BB_mid"] - 2 * df["Close"].rolling(20).std()

        # ── Price chart ──
        fig = go.Figure()

        if chart_type == "Candlestick":
            fig.add_trace(go.Candlestick(
                x=df.index, open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                name=selected_ticker,
                increasing_line_color="#26a69a",
                decreasing_line_color="#ef5350",
                increasing_fillcolor="#26a69a",
                decreasing_fillcolor="#ef5350",
            ))
        elif chart_type == "OHLC":
            fig.add_trace(go.Ohlc(
                x=df.index, open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                name=selected_ticker,
                increasing_line_color="#26a69a",
                decreasing_line_color="#ef5350",
            ))
        else:  # Line
            fig.add_trace(go.Scatter(
                x=df.index, y=df["Close"],
                name=selected_ticker,
                line=dict(color="#58a6ff", width=2),
            ))

        if show_sma20:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["SMA20"],
                name="SMA 20", line=dict(color="#f39c12", width=1.5, dash="dash"),
            ))
        if show_sma50:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["SMA50"],
                name="SMA 50", line=dict(color="#8e44ad", width=1.5, dash="dot"),
            ))
        if show_bb:
            fig.add_trace(go.Scatter(
                x=df.index, y=df["BB_upper"],
                name="BB Upper", line=dict(color="#888", width=1), showlegend=False,
            ))
            fig.add_trace(go.Scatter(
                x=df.index, y=df["BB_lower"],
                name="BB Lower", line=dict(color="#888", width=1),
                fill="tonexty", fillcolor="rgba(136,136,136,0.08)", showlegend=False,
            ))

        fig.update_layout(
            paper_bgcolor="#0d1117",
            plot_bgcolor="#0d1117",
            font=dict(family="Inter", color="#e6edf3"),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(
                gridcolor="#21262d", showline=False, rangeslider=dict(visible=False),
            ),
            yaxis=dict(gridcolor="#21262d", showline=False, tickprefix="$"),
            legend=dict(bgcolor="#161b22", bordercolor="#30363d", borderwidth=1),
            height=420,
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        # ── Volume sub-chart ──
        if show_volume:
            vol_colors = [
                "#26a69a" if c >= o else "#ef5350"
                for c, o in zip(df["Close"], df["Open"])
            ]
            vol_fig = go.Figure(go.Bar(
                x=df.index, y=df["Volume"],
                name="Volume", marker_color=vol_colors, opacity=0.8,
            ))
            vol_fig.update_layout(
                paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
                font=dict(family="Inter", color="#e6edf3"),
                margin=dict(l=0, r=0, t=4, b=0),
                xaxis=dict(gridcolor="#21262d", showline=False),
                yaxis=dict(gridcolor="#21262d", showline=False,
                           tickformat=".2s", title="Volume"),
                height=180, showlegend=False,
            )
            st.plotly_chart(vol_fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — INDEX OVERVIEW
# ══════════════════════════════════════════════════════════════════════════════
with tab_overview:
    st.info("⚠️ Loading live quotes for all 101 tickers takes ~60 seconds on first load. Data is cached for 10 minutes.")

    if st.button("🔄 Load / Refresh Index Overview"):
        st.cache_data.clear()

    with st.spinner("Fetching quotes for all NASDAQ-100 tickers…"):
        ov_df = fetch_overview(list(NASDAQ100.keys()))

    if not ov_df.empty:
        # ── Sector summary ──
        st.markdown("#### Sector Breakdown")
        sector_summary = (
            ov_df.groupby("Sector")
            .agg(Count=("Ticker", "count"), Avg_Change=("Change%", "mean"))
            .reset_index()
            .sort_values("Avg_Change", ascending=False)
        )
        sec_fig = go.Figure(go.Bar(
            x=sector_summary["Sector"],
            y=sector_summary["Avg_Change"],
            marker_color=[
                "#26a69a" if v >= 0 else "#ef5350"
                for v in sector_summary["Avg_Change"]
            ],
            text=sector_summary["Avg_Change"].map("{:+.2f}%".format),
            textposition="outside",
        ))
        sec_fig.update_layout(
            paper_bgcolor="#0d1117", plot_bgcolor="#0d1117",
            font=dict(family="Inter", color="#e6edf3"),
            margin=dict(l=0, r=0, t=10, b=0),
            xaxis=dict(gridcolor="#21262d"),
            yaxis=dict(gridcolor="#21262d", title="Avg Daily Change %"),
            height=280,
        )
        st.plotly_chart(sec_fig, use_container_width=True)

        # ── All tickers table ──
        st.markdown("#### All Tickers")
        display_df = ov_df.copy()
        display_df["Price"]   = display_df["Price"].map(lambda x: f"${x:,.2f}" if x else "—")
        display_df["Change%"] = display_df["Change%"].map(lambda x: f"{x:+.2f}%" if x else "—")
        st.dataframe(
            display_df,
            hide_index=True,
            use_container_width=True,
            column_config={
                "Ticker":  st.column_config.TextColumn("Ticker", width=80),
                "Company": st.column_config.TextColumn("Company", width=240),
                "Sector":  st.column_config.TextColumn("Sector"),
                "Price":   st.column_config.TextColumn("Price",   width=90),
                "Change%": st.column_config.TextColumn("Change%", width=90),
            },
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — RAW DATA
# ══════════════════════════════════════════════════════════════════════════════
with tab_data:
    try:
        raw = df.copy()
    except NameError:
        raw = fetch_stock(selected_ticker, start_dt, end_dt)

    if not raw.empty:
        # ── Summary stats ──
        st.markdown(f"#### {selected_ticker} · {period_option} Summary Statistics")
        summary = raw[["Open", "High", "Low", "Close", "Volume"]].describe().round(2)
        st.dataframe(summary, use_container_width=True)

        # ── Raw OHLCV ──
        st.markdown("#### OHLCV Data")
        raw_display = raw[["Open", "High", "Low", "Close", "Volume"]].copy()
        raw_display.index = raw_display.index.strftime("%Y-%m-%d")
        raw_display = raw_display.sort_index(ascending=False)
        st.dataframe(raw_display, use_container_width=True)

        # ── Download ──
        csv = raw_display.to_csv().encode("utf-8")
        st.download_button(
            label="⬇️ Download CSV",
            data=csv,
            file_name=f"{selected_ticker}_{period_option}.csv",
            mime="text/csv",
        )

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — BEGINNER GUIDE
# ══════════════════════════════════════════════════════════════════════════════
with tab_guide:
    st.markdown("""
## 📚 Beginner's Guide to This App

### What is the NASDAQ-100?
The **NASDAQ-100 (NDX)** is a stock market index tracking the **100 largest
non-financial companies** listed on the Nasdaq exchange.  
It's dominated by technology but also covers healthcare, consumer goods,
and industrial companies.

---

### Chart Types
| Type | When to use |
|---|---|
| **Candlestick** | Most popular — shows Open, High, Low, Close in one bar |
| **OHLC** | Similar to candlestick, preferred by some traders |
| **Line** | Simplest — just the closing price over time |

---

### Indicators Explained
| Indicator | What it tells you |
|---|---|
| **SMA 20** | Average closing price over the last 20 days — short-term trend |
| **SMA 50** | Average closing price over the last 50 days — medium-term trend |
| **Bollinger Bands** | Bands 2 standard deviations above/below the SMA. Wide = volatile |

**Golden Cross 🟡** — SMA 20 crosses *above* SMA 50: often a bullish signal  
**Death Cross ☠️** — SMA 20 crosses *below* SMA 50: often a bearish signal

---

### Metrics
- **Market Cap** — total value of all shares (Price × Shares Outstanding)
- **52-Week High/Low** — the highest and lowest prices in the past year
- **Volume** — number of shares traded today

---

### How to use this app
1. 🔍 **Filter** sectors in the sidebar to narrow down the companies
2. 📌 **Select** any NASDAQ-100 ticker
3. 📅 **Choose** a date range (1M → 5Y)
4. 📊 **Toggle** overlays (SMAs, Bollinger Bands, Volume)
5. 🌐 Go to **Index Overview** to compare all 100 companies at once
6. 📋 Visit **Raw Data** to download the OHLCV CSV for further analysis

---

### Tech Stack
```
streamlit   — web UI framework
yfinance    — live & historical stock data from Yahoo Finance
pandas      — data manipulation
plotly      — interactive charts
```
    """)
