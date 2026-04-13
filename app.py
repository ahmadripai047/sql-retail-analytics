"""
app.py — Online Retail SQL Analytics Dashboard
Tema: Deep Ocean Tech — Dark Navy dengan aksen Cyan & Teal
Muhammad Rifai | Portfolio | Analytifai
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import sqlite3
import warnings
warnings.filterwarnings("ignore")

# ─── Page Config ──────────────────────────────────────────────────────
st.set_page_config(
    page_title="Retail SQL Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── TEMA: Deep Ocean Tech ────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
}
.stApp {
    background: #050d1a;
    color: #c8d8e8;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #07142b 0%, #050d1a 100%);
    border-right: 1px solid rgba(0,200,200,0.15);
}
[data-testid="stSidebar"] * { color: #a8c8d8 !important; }

/* Hero */
.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 2.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #00d4ff 0%, #00ffcc 50%, #0099cc 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -0.5px;
    line-height: 1.1;
}
.hero-sub {
    font-size: 0.82rem;
    color: #4a8a9a;
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 6px;
}

/* KPI Cards */
.kpi-card {
    background: linear-gradient(135deg, rgba(0,212,255,0.06) 0%, rgba(0,100,150,0.04) 100%);
    border: 1px solid rgba(0,212,255,0.2);
    border-top: 2px solid #00d4ff;
    border-radius: 12px;
    padding: 20px 16px;
    text-align: center;
}
.kpi-number {
    font-family: 'JetBrains Mono', monospace;
    font-size: 2rem;
    font-weight: 600;
    color: #00d4ff;
    line-height: 1;
}
.kpi-label {
    font-size: 0.68rem;
    color: #4a8a9a;
    text-transform: uppercase;
    letter-spacing: 2px;
    margin-top: 6px;
}
.kpi-sub {
    font-size: 0.78rem;
    color: #7ab8c8;
    margin-top: 4px;
}

/* Section Headers */
.section-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: #00d4ff;
    letter-spacing: 0.5px;
    border-left: 3px solid #00d4ff;
    padding-left: 10px;
    margin: 20px 0 14px;
}

/* Insight Box */
.insight-box {
    background: rgba(0,212,255,0.04);
    border: 1px solid rgba(0,212,255,0.15);
    border-left: 3px solid #00ffcc;
    border-radius: 8px;
    padding: 12px 16px;
    margin: 10px 0;
    font-size: 0.85rem;
    color: #a8c8d8;
    line-height: 1.6;
}

/* SQL Badge */
.sql-badge {
    display: inline-block;
    background: rgba(0,212,255,0.1);
    border: 1px solid rgba(0,212,255,0.3);
    border-radius: 4px;
    padding: 2px 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.7rem;
    color: #00d4ff;
    margin-right: 4px;
}

/* Segment Badge Colors */
.seg-champions    { background:rgba(0,255,180,0.15); border:1px solid rgba(0,255,180,0.4); color:#00ffb4; border-radius:6px; padding:3px 10px; font-size:0.78rem; }
.seg-loyal        { background:rgba(0,212,255,0.15); border:1px solid rgba(0,212,255,0.4); color:#00d4ff; border-radius:6px; padding:3px 10px; font-size:0.78rem; }
.seg-potential    { background:rgba(100,180,255,0.15); border:1px solid rgba(100,180,255,0.4); color:#64b4ff; border-radius:6px; padding:3px 10px; font-size:0.78rem; }
.seg-atrisk       { background:rgba(255,180,0,0.15); border:1px solid rgba(255,180,0,0.4); color:#ffb400; border-radius:6px; padding:3px 10px; font-size:0.78rem; }
.seg-lost         { background:rgba(255,80,80,0.12); border:1px solid rgba(255,80,80,0.3); color:#ff5050; border-radius:6px; padding:3px 10px; font-size:0.78rem; }

hr { border-color: rgba(0,212,255,0.1) !important; }

.stTabs [data-baseweb="tab"] {
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.5px;
    color: #4a8a9a;
}
.stTabs [aria-selected="true"] {
    color: #00d4ff !important;
    border-bottom: 2px solid #00d4ff !important;
}
[data-testid="stDataFrame"] {
    border: 1px solid rgba(0,212,255,0.12);
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# ─── Plotly Theme ──────────────────────────────────────────────────────
PLOT_THEME = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(5,13,26,0.8)",
    font=dict(family="Space Grotesk, sans-serif", color="#a8c8d8", size=11),
    title_font=dict(family="Space Grotesk, sans-serif", color="#00d4ff", size=14),
    colorway=["#00d4ff","#00ffcc","#0099ff","#7b68ee","#ff6b9d","#ffaa00","#00ff87"],
)
CYAN  = "#00d4ff"
TEAL  = "#00ffcc"
BLUE  = "#0099ff"
PURPLE= "#7b68ee"
WARN  = "#ffaa00"
DANGER= "#ff5050"

COLORSCALE_OCEAN = [[0,"#050d1a"],[0.3,"#003d5c"],[0.6,"#006d8a"],[0.85,"#00b4cc"],[1,"#00d4ff"]]
COLORSCALE_TEAL  = [[0,"#050d1a"],[0.4,"#00403a"],[0.7,"#00806e"],[1,"#00ffcc"]]

# ─── Load Data ─────────────────────────────────────────────────────────
@st.cache_data
def load_all():
    conn = sqlite3.connect("retail.db")

    df_raw = pd.read_sql("SELECT * FROM transactions", conn)

    # KPI
    kpi = pd.read_sql("""
        SELECT
            COUNT(*) AS total_transactions,
            COUNT(DISTINCT InvoiceNo) AS unique_invoices,
            COUNT(DISTINCT CustomerID) AS unique_customers,
            COUNT(DISTINCT StockCode) AS unique_products,
            COUNT(DISTINCT Country) AS countries,
            ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS total_revenue,
            ROUND(AVG(CAST(Revenue AS FLOAT)),2) AS avg_transaction
        FROM transactions
    """, conn).iloc[0]

    # Country revenue
    country = pd.read_sql("""
        SELECT Country,
            COUNT(DISTINCT InvoiceNo) AS orders,
            COUNT(DISTINCT CustomerID) AS customers,
            ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue,
            ROUND(SUM(CAST(Revenue AS FLOAT))*100.0/
                  SUM(SUM(CAST(Revenue AS FLOAT))) OVER(),2) AS pct
        FROM transactions
        GROUP BY Country ORDER BY revenue DESC
    """, conn)

    # Monthly trend
    monthly = pd.read_sql("""
        WITH m AS (
            SELECT SUBSTR(InvoiceDate,1,7) AS month,
                COUNT(DISTINCT InvoiceNo) AS orders,
                COUNT(DISTINCT CustomerID) AS customers,
                ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue
            FROM transactions GROUP BY month
        ),
        lag AS (
            SELECT *, LAG(revenue) OVER (ORDER BY month) AS prev_rev FROM m
        )
        SELECT month, orders, customers, revenue,
            ROUND((revenue-prev_rev)*100.0/prev_rev, 1) AS mom_growth
        FROM lag ORDER BY month
    """, conn)

    # Top products
    products = pd.read_sql("""
        SELECT Description,
            COUNT(DISTINCT InvoiceNo) AS orders,
            SUM(Quantity) AS total_qty,
            ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue,
            ROUND(AVG(CAST(UnitPrice AS FLOAT)),2) AS avg_price
        FROM transactions
        GROUP BY Description ORDER BY revenue DESC LIMIT 15
    """, conn)

    # RFM
    rfm = pd.read_sql("""
        WITH b AS (
            SELECT CustomerID, Country,
                CAST((JULIANDAY('2011-12-10')-JULIANDAY(MAX(InvoiceDate))) AS INT) AS recency,
                COUNT(DISTINCT InvoiceNo) AS frequency,
                ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS monetary
            FROM transactions GROUP BY CustomerID
        ),
        s AS (
            SELECT *, 
                NTILE(5) OVER (ORDER BY recency DESC) AS r,
                NTILE(5) OVER (ORDER BY frequency ASC) AS f,
                NTILE(5) OVER (ORDER BY monetary ASC)  AS m
            FROM b
        )
        SELECT CustomerID, Country, recency, frequency, monetary,
            r, f, m, (r+f+m) AS rfm_total,
            CASE
                WHEN (r+f+m)>=13 THEN 'Champions'
                WHEN (r+f+m)>=10 THEN 'Loyal Customers'
                WHEN (r+f+m)>=7  THEN 'Potential Loyalists'
                WHEN (r+f+m)>=4  THEN 'At Risk'
                ELSE 'Lost'
            END AS segment
        FROM s ORDER BY rfm_total DESC
    """, conn)

    # Frequency dist
    freq = pd.read_sql("""
        WITH f AS (
            SELECT CustomerID, COUNT(DISTINCT InvoiceNo) AS cnt FROM transactions GROUP BY CustomerID
        )
        SELECT
            CASE
                WHEN cnt=1 THEN '1 order'
                WHEN cnt<=3 THEN '2–3 orders'
                WHEN cnt<=6 THEN '4–6 orders'
                WHEN cnt<=10 THEN '7–10 orders'
                ELSE '10+ orders'
            END AS segment,
            COUNT(*) AS customers,
            ROUND(COUNT(*)*100.0/SUM(COUNT(*)) OVER(),1) AS pct
        FROM f GROUP BY segment ORDER BY MIN(cnt)
    """, conn)

    # Pareto
    pareto = pd.read_sql("""
        WITH pr AS (
            SELECT Description, ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS rev
            FROM transactions GROUP BY Description
        ),
        ranked AS (
            SELECT Description, rev,
                RANK() OVER (ORDER BY rev DESC) AS rnk,
                ROUND(SUM(rev) OVER (ORDER BY rev DESC
                      ROWS UNBOUNDED PRECEDING)*100.0/SUM(rev) OVER(),2) AS cum_pct
            FROM pr
        )
        SELECT rnk, Description, rev, cum_pct,
            CASE WHEN cum_pct<=80 THEN 'Top 80%' ELSE 'Tail 20%' END AS pareto_group
        FROM ranked ORDER BY rnk LIMIT 20
    """, conn)

    # AOV by country
    aov = pd.read_sql("""
        SELECT Country,
            COUNT(DISTINCT InvoiceNo) AS orders,
            ROUND(SUM(CAST(Revenue AS FLOAT))/COUNT(DISTINCT InvoiceNo),2) AS aov
        FROM transactions
        GROUP BY Country HAVING orders>=50
        ORDER BY aov DESC
    """, conn)

    # Cohort
    cohort = pd.read_sql("""
        WITH fp AS (
            SELECT CustomerID, SUBSTR(MIN(InvoiceDate),1,7) AS cohort
            FROM transactions GROUP BY CustomerID
        ),
        cd AS (
            SELECT f.cohort, SUBSTR(t.InvoiceDate,1,7) AS om, t.CustomerID
            FROM transactions t JOIN fp f ON t.CustomerID=f.CustomerID
        )
        SELECT cohort,
            COUNT(DISTINCT CustomerID) AS cohort_size,
            COUNT(DISTINCT CASE WHEN om>cohort THEN CustomerID END) AS returned,
            ROUND(COUNT(DISTINCT CASE WHEN om>cohort THEN CustomerID END)*100.0
                  /COUNT(DISTINCT CustomerID),1) AS retention_pct
        FROM cd GROUP BY cohort ORDER BY cohort
    """, conn)

    conn.close()
    return df_raw, kpi, country, monthly, products, rfm, freq, pareto, aov, cohort

df_raw, kpi, df_country, df_monthly, df_products, df_rfm, df_freq, df_pareto, df_aov, df_cohort = load_all()

# ─── Sidebar ───────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding:20px 0 10px;'>
        <div style='font-family:JetBrains Mono,monospace; font-size:1.1rem;
                    color:#00d4ff; letter-spacing:2px;'>◈ RETAIL SQL</div>
        <div style='font-size:0.62rem; color:#2a6a7a; letter-spacing:3px;
                    text-transform:uppercase; margin-top:4px;'>Analytics Dashboard</div>
    </div>""", unsafe_allow_html=True)
    st.divider()

    st.markdown("**◈ Navigate**")
    page = st.radio("", [
        "Overview",
        "Revenue & Country",
        "Product Performance",
        "Customer Behaviour",
        "RFM Segmentation",
        "Time Analysis",
        "SQL Explorer",
    ], label_visibility="collapsed")

    st.divider()
    st.markdown("**◈ Filters**")
    all_countries = ["All"] + sorted(df_raw["Country"].unique().tolist())
    sel_country = st.selectbox("Country", all_countries)

    all_months = sorted(df_raw["InvoiceDate"].str[:7].unique().tolist())
    sel_months = st.select_slider("Period",
        options=all_months,
        value=(all_months[0], all_months[-1])
    )

    st.divider()
    st.markdown(f"""
    <div style='font-size:0.68rem; color:#2a6a7a; text-align:center; line-height:1.9;'>
    Dataset: Online Retail UCI<br>
    {int(kpi['total_transactions']):,} transactions<br>
    {int(kpi['unique_customers']):,} customers · {int(kpi['countries'])} countries
    </div>""", unsafe_allow_html=True)

# ─── Apply Filters ─────────────────────────────────────────────────────
dff = df_raw.copy()
if sel_country != "All":
    dff = dff[dff["Country"] == sel_country]
dff = dff[
    (dff["InvoiceDate"].str[:7] >= sel_months[0]) &
    (dff["InvoiceDate"].str[:7] <= sel_months[1])
]

# ─── Helper: recompute KPIs dari filtered data ─────────────────────────
def kpi_from(df):
    return {
        "revenue": df["Revenue"].astype(float).sum(),
        "orders":  df["InvoiceNo"].nunique(),
        "customers": df["CustomerID"].nunique(),
        "aov":     df["Revenue"].astype(float).sum() / max(df["InvoiceNo"].nunique(), 1),
        "products": df["StockCode"].nunique(),
    }

k = kpi_from(dff)

# ══════════════════════════════════════════════════════════════════
# PAGE: OVERVIEW
# ══════════════════════════════════════════════════════════════════
if page == "Overview":
    st.markdown("""
    <div style='padding:24px 0 16px;'>
        <div class='hero-title'>RETAIL SQL<br>ANALYTICS</div>
        <div class='hero-sub'>Online Retail · UK-Based E-Commerce · 2010–2011</div>
    </div>""", unsafe_allow_html=True)
    st.markdown(f"<div style='font-size:0.78rem; color:#2a6a7a;'>Showing <b style='color:#00d4ff'>{len(dff):,}</b> of {len(df_raw):,} transactions after filters</div>", unsafe_allow_html=True)
    st.divider()

    # KPIs
    c1,c2,c3,c4,c5 = st.columns(5)
    kpis = [
        (f"£{k['revenue']:,.0f}", "Total Revenue", "filtered period"),
        (f"{k['orders']:,}", "Unique Invoices", "transaction count"),
        (f"{k['customers']:,}", "Customers", "unique buyers"),
        (f"£{k['aov']:,.1f}", "Avg Order Value", "revenue per invoice"),
        (f"{k['products']:,}", "Products", "unique SKUs"),
    ]
    for col, (num, label, sub) in zip([c1,c2,c3,c4,c5], kpis):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-number'>{num}</div>
                <div class='kpi-label'>{label}</div>
                <div class='kpi-sub'>{sub}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    col_a, col_b = st.columns([1.3, 0.7])

    with col_a:
        st.markdown("<div class='section-title'>Monthly Revenue Trend</div>", unsafe_allow_html=True)
        st.markdown("<span class='sql-badge'>LAG()</span><span class='sql-badge'>GROUP BY</span>", unsafe_allow_html=True)
        m_filt = df_monthly[
            (df_monthly["month"] >= sel_months[0]) &
            (df_monthly["month"] <= sel_months[1])
        ]
        fig = go.Figure()
        fig.add_trace(go.Bar(x=m_filt["month"], y=m_filt["revenue"],
                             name="Revenue", marker_color=CYAN, opacity=0.7))
        fig2_ax = go.Scatter(x=m_filt["month"], y=m_filt["customers"],
                              name="Customers", yaxis="y2",
                              line=dict(color=TEAL, width=2.5), mode="lines+markers",
                              marker=dict(size=5))
        fig.add_trace(fig2_ax)
        fig.update_layout(**PLOT_THEME, height=300,
                          margin=dict(l=0,r=60,t=10,b=0),
                          yaxis=dict(title="Revenue (£)", tickformat="£,.0f"),
                          yaxis2=dict(title="Customers", overlaying="y", side="right"),
                          legend=dict(orientation="h", y=1.08))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Revenue by Country</div>", unsafe_allow_html=True)
        c_filt = dff.groupby("Country").agg(
            revenue=("Revenue", lambda x: x.astype(float).sum())
        ).reset_index().sort_values("revenue", ascending=False).head(6)
        fig = go.Figure(go.Pie(
            labels=c_filt["Country"], values=c_filt["revenue"],
            hole=0.6,
            marker=dict(colors=[CYAN,TEAL,BLUE,PURPLE,"#ff6b9d",WARN],
                        line=dict(color="#050d1a", width=2)),
            textinfo="percent", textfont=dict(size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=300,
                          margin=dict(l=0,r=0,t=10,b=0),
                          legend=dict(font=dict(size=9)),
                          annotations=[dict(text="Market<br>Share", x=0.5, y=0.5,
                                           font=dict(size=12, color=CYAN), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    # Business problem
    st.markdown("<div class='section-title'>Business Problem & Key Questions</div>", unsafe_allow_html=True)
    cols = st.columns(3)
    questions = [
        ("Revenue Driver", "Faktor apa yang paling mempengaruhi total revenue — negara, produk, atau timing?"),
        ("Customer Loyalty", "Berapa banyak pelanggan yang kembali beli? Segmen mana yang paling bernilai?"),
        ("Product Strategy", "Produk mana yang harus diprioritaskan? Apakah berlaku aturan Pareto 80/20?"),
        ("Seasonal Pattern", "Apakah ada pola musiman yang bisa dimanfaatkan untuk inventory planning?"),
        ("Market Expansion", "Negara mana yang punya growth potential terbesar selain UK?"),
        ("Churn Prevention", "Pelanggan mana yang at-risk dan butuh win-back campaign segera?"),
    ]
    for i, (title, desc) in enumerate(questions):
        with cols[i % 3]:
            st.markdown(f"""
            <div style='background:rgba(0,212,255,0.04); border:1px solid rgba(0,212,255,0.12);
                        border-radius:10px; padding:14px; margin-bottom:10px; min-height:100px;'>
                <div style='color:#00d4ff; font-weight:600; font-size:0.85rem;
                            margin-bottom:5px;'>{title}</div>
                <div style='color:#7aa8b8; font-size:0.8rem; line-height:1.5;'>{desc}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: REVENUE & COUNTRY
# ══════════════════════════════════════════════════════════════════
elif page == "Revenue & Country":
    st.markdown("<div class='hero-title' style='font-size:2rem;'>REVENUE & COUNTRY</div>", unsafe_allow_html=True)
    st.markdown("<span class='sql-badge'>SUM() OVER()</span><span class='sql-badge'>RANK() OVER()</span><span class='sql-badge'>GROUP BY</span>", unsafe_allow_html=True)
    st.divider()

    c1,c2,c3,c4 = st.columns(4)
    for col, (num, label) in zip([c1,c2,c3,c4], [
        (f"£{k['revenue']:,.0f}", "Total Revenue"),
        (f"{k['orders']:,}", "Total Orders"),
        (f"£{k['aov']:,.1f}", "Avg Order Value"),
        (f"{k['customers']:,}", "Unique Customers"),
    ]):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-number'>{num}</div>
                <div class='kpi-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    c_filt = dff.groupby("Country").agg(
        orders=("InvoiceNo","nunique"),
        customers=("CustomerID","nunique"),
        revenue=("Revenue", lambda x: round(x.astype(float).sum(), 2))
    ).reset_index().sort_values("revenue", ascending=False)
    c_filt["pct"] = (c_filt["revenue"] / c_filt["revenue"].sum() * 100).round(2)

    col_a, col_b = st.columns([1.4, 0.6])
    with col_a:
        st.markdown("<div class='section-title'>Revenue by Country</div>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=c_filt["revenue"], y=c_filt["Country"],
            orientation="h",
            marker=dict(color=c_filt["revenue"],
                        colorscale=COLORSCALE_OCEAN, showscale=False),
            text=c_filt["revenue"].apply(lambda x: f"£{x:,.0f}"),
            textposition="outside",
            textfont=dict(color=CYAN, size=9)
        ))
        fig.update_layout(**PLOT_THEME, height=380,
                          margin=dict(l=0,r=90,t=10,b=0),
                          xaxis=dict(tickformat="£,.0f"),
                          yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Order Count</div>", unsafe_allow_html=True)
        fig = go.Figure(go.Bar(
            x=c_filt["orders"], y=c_filt["Country"],
            orientation="h",
            marker=dict(color=TEAL, opacity=0.75),
            text=c_filt["orders"],
            textposition="outside",
            textfont=dict(color=TEAL, size=9)
        ))
        fig.update_layout(**PLOT_THEME, height=380,
                          margin=dict(l=0,r=50,t=10,b=0),
                          yaxis=dict(categoryorder="total ascending"))
        st.plotly_chart(fig, use_container_width=True)

    # AOV comparison
    st.markdown("<div class='section-title'>Average Order Value per Country</div>", unsafe_allow_html=True)
    aov_filt = dff.groupby("Country").apply(
        lambda x: pd.Series({
            "orders": x["InvoiceNo"].nunique(),
            "aov": round(x["Revenue"].astype(float).sum() / x["InvoiceNo"].nunique(), 2)
        })
    ).reset_index().query("orders >= 30").sort_values("aov", ascending=False)

    fig = px.bar(aov_filt, x="Country", y="aov",
                 color="aov", color_continuous_scale=COLORSCALE_TEAL,
                 text=aov_filt["aov"].apply(lambda x: f"£{x:,.1f}"))
    fig.update_traces(textposition="outside", textfont=dict(color=TEAL, size=10))
    fig.update_layout(**PLOT_THEME, height=320,
                      margin=dict(l=0,r=0,t=10,b=0),
                      yaxis_title="AOV (£)", coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
    ◈ <b>Insight:</b> UK mendominasi volume transaksi, namun negara lain bisa menunjukkan
    AOV lebih tinggi — target ideal untuk <b>upselling & premium bundle strategy</b>.
    Diversifikasi pasar di luar UK penting untuk mitigasi risiko konsentrasi revenue.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: PRODUCT PERFORMANCE
# ══════════════════════════════════════════════════════════════════
elif page == "Product Performance":
    st.markdown("<div class='hero-title' style='font-size:2rem;'>PRODUCT PERFORMANCE</div>", unsafe_allow_html=True)
    st.markdown("<span class='sql-badge'>RANK() OVER()</span><span class='sql-badge'>HAVING</span><span class='sql-badge'>CTE</span>", unsafe_allow_html=True)
    st.divider()

    prod_filt = dff.groupby("Description").agg(
        orders=("InvoiceNo","nunique"),
        qty=("Quantity","sum"),
        revenue=("Revenue", lambda x: round(x.astype(float).sum(), 2)),
        avg_price=("UnitPrice", lambda x: round(x.astype(float).mean(), 2))
    ).reset_index().sort_values("revenue", ascending=False)

    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("<div class='section-title'>Top 12 Products by Revenue</div>", unsafe_allow_html=True)
        top12 = prod_filt.head(12)
        fig = go.Figure(go.Bar(
            x=top12["revenue"], y=top12["Description"],
            orientation="h",
            marker=dict(color=top12["revenue"],
                        colorscale=COLORSCALE_OCEAN, showscale=False),
            text=top12["revenue"].apply(lambda x: f"£{x:,.0f}"),
            textposition="outside",
            textfont=dict(color=CYAN, size=9)
        ))
        fig.update_layout(**PLOT_THEME, height=420,
                          margin=dict(l=0,r=90,t=10,b=0),
                          xaxis=dict(tickformat="£,.0f"),
                          yaxis=dict(categoryorder="total ascending",
                                     tickfont=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Price vs Volume Scatter</div>", unsafe_allow_html=True)
        top20 = prod_filt.head(20)
        fig = px.scatter(top20, x="avg_price", y="qty",
                         size="revenue", color="revenue",
                         hover_name="Description",
                         size_max=50,
                         color_continuous_scale=COLORSCALE_OCEAN,
                         labels={"avg_price":"Avg Price (£)","qty":"Total Qty Sold","revenue":"Revenue"})
        fig.update_layout(**PLOT_THEME, height=420,
                          margin=dict(l=0,r=0,t=10,b=0),
                          coloraxis_colorbar=dict(title="Revenue", tickformat="£,.0f",
                                                  tickfont=dict(size=9)))
        st.plotly_chart(fig, use_container_width=True)

    # Pareto
    st.markdown("<div class='section-title'>Pareto Analysis — 80/20 Rule</div>", unsafe_allow_html=True)
    st.markdown("<span class='sql-badge'>SUM() OVER(ROWS UNBOUNDED)</span>", unsafe_allow_html=True)

    prod_pareto = prod_filt.copy().reset_index(drop=True)
    prod_pareto["cum_pct"] = prod_pareto["revenue"].cumsum() / prod_pareto["revenue"].sum() * 100
    prod_pareto["rank"] = range(1, len(prod_pareto)+1)
    prod_pareto["pareto"] = prod_pareto["cum_pct"].apply(
        lambda x: "Top 80% Revenue" if x <= 80 else "Tail 20%"
    )
    top_pareto = prod_pareto.head(20)

    fig = go.Figure()
    colors_p = [CYAN if g == "Top 80% Revenue" else "#1a3a4a" for g in top_pareto["pareto"]]
    fig.add_trace(go.Bar(x=top_pareto["rank"].astype(str),
                         y=top_pareto["revenue"], name="Revenue",
                         marker_color=colors_p, opacity=0.85))
    fig.add_trace(go.Scatter(x=top_pareto["rank"].astype(str),
                             y=top_pareto["cum_pct"], name="Cumulative %",
                             yaxis="y2", line=dict(color=TEAL, width=2.5),
                             mode="lines+markers", marker=dict(size=5)))
    fig.add_hline(y=80, line_dash="dash", line_color=WARN,
                  annotation_text="80% threshold", annotation_font_color=WARN,
                  yref="y2")
    fig.update_layout(**PLOT_THEME, height=340,
                      margin=dict(l=0,r=60,t=10,b=0),
                      xaxis_title="Product Rank",
                      yaxis=dict(title="Revenue (£)", tickformat="£,.0f"),
                      yaxis2=dict(title="Cumulative %", overlaying="y", side="right",
                                  ticksuffix="%", range=[0,105]),
                      legend=dict(orientation="h", y=1.08))
    st.plotly_chart(fig, use_container_width=True)

    n80 = len(prod_pareto[prod_pareto["cum_pct"] <= 80])
    total_prod = len(prod_pareto)
    st.markdown(f"""
    <div class='insight-box'>
    ◈ <b>Pareto Insight:</b> Hanya <b style='color:#00d4ff'>{n80} dari {total_prod} produk</b>
    ({n80/total_prod*100:.0f}%) menghasilkan 80% total revenue —
    terapkan aturan 80/20 untuk fokus inventory & marketing budget.
    Produk di "Tail 20%" perlu evaluasi apakah masih layak dipertahankan di katalog.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: CUSTOMER BEHAVIOUR
# ══════════════════════════════════════════════════════════════════
elif page == "Customer Behaviour":
    st.markdown("<div class='hero-title' style='font-size:2rem;'>CUSTOMER BEHAVIOUR</div>", unsafe_allow_html=True)
    st.markdown("<span class='sql-badge'>NTILE()</span><span class='sql-badge'>COUNT DISTINCT</span><span class='sql-badge'>CASE WHEN</span>", unsafe_allow_html=True)
    st.divider()

    cust_stats = dff.groupby("CustomerID").agg(
        orders=("InvoiceNo","nunique"),
        revenue=("Revenue", lambda x: round(x.astype(float).sum(),2)),
        country=("Country","first")
    ).reset_index()
    cust_stats["aov"] = (cust_stats["revenue"] / cust_stats["orders"]).round(2)

    c1,c2,c3,c4 = st.columns(4)
    for col, (num, label) in zip([c1,c2,c3,c4], [
        (f"{len(cust_stats):,}", "Total Customers"),
        (f"£{cust_stats['revenue'].mean():,.1f}", "Avg CLV"),
        (f"{cust_stats['orders'].mean():.1f}x", "Avg Order Freq"),
        (f"£{cust_stats['aov'].mean():,.1f}", "Avg Order Value"),
    ]):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-number'>{num}</div>
                <div class='kpi-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-title'>Purchase Frequency Distribution</div>", unsafe_allow_html=True)

        def freq_seg(n):
            if n == 1:   return "1 order"
            elif n <= 3: return "2–3 orders"
            elif n <= 6: return "4–6 orders"
            elif n <= 10:return "7–10 orders"
            else:        return "10+ orders"

        freq_df = cust_stats["orders"].apply(freq_seg).value_counts().reset_index()
        freq_df.columns = ["segment","count"]
        order_map = {"1 order":0,"2–3 orders":1,"4–6 orders":2,"7–10 orders":3,"10+ orders":4}
        freq_df["sort"] = freq_df["segment"].map(order_map)
        freq_df = freq_df.sort_values("sort")

        colors_f = [CYAN, TEAL, BLUE, PURPLE, WARN]
        fig = go.Figure(go.Bar(
            x=freq_df["segment"], y=freq_df["count"],
            marker_color=colors_f[:len(freq_df)], opacity=0.85,
            text=freq_df["count"], textposition="outside",
            textfont=dict(color=CYAN, size=11)
        ))
        fig.update_layout(**PLOT_THEME, height=320,
                          margin=dict(l=0,r=0,t=10,b=0),
                          yaxis_title="Customers",
                          xaxis=dict(tickangle=15))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>CLV Distribution (Top Customers)</div>", unsafe_allow_html=True)
        top30 = cust_stats.nlargest(30, "revenue")
        fig = go.Figure(go.Bar(
            x=top30["CustomerID"].astype(str),
            y=top30["revenue"],
            marker=dict(color=top30["revenue"],
                        colorscale=COLORSCALE_TEAL, showscale=False),
        ))
        fig.update_layout(**PLOT_THEME, height=320,
                          margin=dict(l=0,r=0,t=10,b=0),
                          xaxis_title="Customer ID",
                          yaxis=dict(tickformat="£,.0f"),
                          xaxis=dict(tickangle=45, tickfont=dict(size=8)))
        st.plotly_chart(fig, use_container_width=True)

    # Top 10 customer table
    st.markdown("<div class='section-title'>Top 10 Customers by Lifetime Value</div>", unsafe_allow_html=True)
    top10 = cust_stats.nlargest(10, "revenue")[
        ["CustomerID","country","orders","revenue","aov"]
    ].rename(columns={
        "CustomerID":"Customer ID","country":"Country",
        "orders":"Orders","revenue":"Total Revenue (£)","aov":"AOV (£)"
    })
    st.dataframe(top10.set_index("Customer ID"), use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
    ◈ <b>Insight:</b> Mayoritas pelanggan hanya melakukan 1–3 pembelian —
    indikasi kuat perlunya <b>re-engagement strategy</b>.
    Pelanggan dengan 10+ orders adalah segmen paling bernilai dan harus mendapat
    <b>VIP treatment & loyalty program</b> khusus.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: RFM SEGMENTATION
# ══════════════════════════════════════════════════════════════════
elif page == "RFM Segmentation":
    st.markdown("<div class='hero-title' style='font-size:2rem;'>RFM SEGMENTATION</div>", unsafe_allow_html=True)
    st.markdown("<span class='sql-badge'>NTILE(5)</span><span class='sql-badge'>CTE</span><span class='sql-badge'>CASE WHEN</span>", unsafe_allow_html=True)
    st.divider()

    # Recompute RFM dari filtered data
    snapshot = "2011-12-10"
    rfm_filt = dff.groupby("CustomerID").agg(
        recency=("InvoiceDate", lambda x: (
            pd.Timestamp(snapshot) - pd.to_datetime(x.max())
        ).days),
        frequency=("InvoiceNo","nunique"),
        monetary=("Revenue", lambda x: round(x.astype(float).sum(), 2))
    ).reset_index()

    rfm_filt["r"] = pd.qcut(rfm_filt["recency"].rank(method="first"),
                              5, labels=[5,4,3,2,1]).astype(int)
    rfm_filt["f"] = pd.qcut(rfm_filt["frequency"].rank(method="first"),
                              5, labels=[1,2,3,4,5]).astype(int)
    rfm_filt["m"] = pd.qcut(rfm_filt["monetary"].rank(method="first"),
                              5, labels=[1,2,3,4,5]).astype(int)
    rfm_filt["rfm_total"] = rfm_filt["r"] + rfm_filt["f"] + rfm_filt["m"]

    def seg(s):
        if s >= 13: return "Champions"
        elif s >= 10: return "Loyal Customers"
        elif s >= 7:  return "Potential Loyalists"
        elif s >= 4:  return "At Risk"
        else:         return "Lost"

    rfm_filt["segment"] = rfm_filt["rfm_total"].apply(seg)

    seg_summary = rfm_filt.groupby("segment").agg(
        count=("CustomerID","count"),
        avg_recency=("recency","mean"),
        avg_frequency=("frequency","mean"),
        avg_monetary=("monetary","mean")
    ).reset_index().round(1)
    seg_summary["pct"] = (seg_summary["count"] / seg_summary["count"].sum() * 100).round(1)

    # KPIs per segment
    seg_colors = {
        "Champions": TEAL, "Loyal Customers": CYAN,
        "Potential Loyalists": BLUE, "At Risk": WARN, "Lost": DANGER
    }
    seg_order = ["Champions","Loyal Customers","Potential Loyalists","At Risk","Lost"]

    cols = st.columns(5)
    for col, seg_name in zip(cols, seg_order):
        row = seg_summary[seg_summary["segment"] == seg_name]
        if len(row):
            cnt = int(row["count"].iloc[0])
            pct = float(row["pct"].iloc[0])
            color = seg_colors[seg_name]
            with col:
                st.markdown(f"""
                <div style='background:rgba(0,0,0,0.3); border:1px solid {color}33;
                            border-top:2px solid {color}; border-radius:10px;
                            padding:16px 12px; text-align:center;'>
                    <div style='font-family:JetBrains Mono,monospace; font-size:1.6rem;
                                font-weight:600; color:{color};'>{cnt}</div>
                    <div style='font-size:0.65rem; color:{color}99; letter-spacing:1.5px;
                                text-transform:uppercase; margin-top:4px;'>{seg_name}</div>
                    <div style='font-size:0.78rem; color:{color}cc; margin-top:2px;'>{pct}%</div>
                </div>""", unsafe_allow_html=True)

    st.markdown("")
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown("<div class='section-title'>Segment Distribution</div>", unsafe_allow_html=True)
        seg_plot = seg_summary.set_index("segment").reindex(seg_order).reset_index().dropna()
        fig = go.Figure(go.Pie(
            labels=seg_plot["segment"], values=seg_plot["count"],
            hole=0.6,
            marker=dict(
                colors=[seg_colors[s] for s in seg_plot["segment"]],
                line=dict(color="#050d1a", width=2)
            ),
            textinfo="percent+label",
            textfont=dict(size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=340,
                          margin=dict(l=0,r=0,t=10,b=0),
                          showlegend=False,
                          annotations=[dict(text="RFM<br>Segments", x=0.5, y=0.5,
                                           font=dict(size=12, color=CYAN), showarrow=False)])
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        st.markdown("<div class='section-title'>Avg Monetary per Segment</div>", unsafe_allow_html=True)
        seg_plot2 = seg_summary.set_index("segment").reindex(seg_order).reset_index().dropna()
        fig = go.Figure(go.Bar(
            x=seg_plot2["segment"], y=seg_plot2["avg_monetary"],
            marker_color=[seg_colors[s] for s in seg_plot2["segment"]],
            opacity=0.85,
            text=seg_plot2["avg_monetary"].apply(lambda x: f"£{x:,.0f}"),
            textposition="outside",
            textfont=dict(size=10)
        ))
        fig.update_layout(**PLOT_THEME, height=340,
                          margin=dict(l=0,r=0,t=10,b=20),
                          yaxis=dict(tickformat="£,.0f"),
                          xaxis=dict(tickangle=15))
        st.plotly_chart(fig, use_container_width=True)

    # RFM scatter
    st.markdown("<div class='section-title'>RFM Scatter — Recency vs Monetary (size = Frequency)</div>", unsafe_allow_html=True)
    fig = px.scatter(rfm_filt.sample(min(500, len(rfm_filt))),
                     x="recency", y="monetary",
                     size="frequency", color="segment",
                     color_discrete_map=seg_colors,
                     size_max=25, opacity=0.75,
                     labels={"recency":"Recency (days)","monetary":"Monetary (£)","frequency":"Frequency"})
    fig.update_layout(**PLOT_THEME, height=380,
                      margin=dict(l=0,r=0,t=10,b=0),
                      yaxis=dict(tickformat="£,.0f"))
    st.plotly_chart(fig, use_container_width=True)

    # Strategy table
    st.markdown("<div class='section-title'>Action Strategy per Segment</div>", unsafe_allow_html=True)
    strategies = {
        "Champions":          ("🏆", TEAL,   "VIP program, early access produk baru, brand ambassador"),
        "Loyal Customers":    ("💛", CYAN,   "Loyalty reward, upsell bundle, referral program"),
        "Potential Loyalists":("🔄", BLUE,   "Onboarding email series, personalized recommendation"),
        "At Risk":            ("⚠️", WARN,   "Win-back campaign, diskon personal, survey kepuasan"),
        "Lost":               ("❌", DANGER, "Re-activation campaign atau stop invest marketing"),
    }
    cols = st.columns(5)
    for col, seg_name in zip(cols, seg_order):
        icon, color, strategy = strategies[seg_name]
        row = seg_summary[seg_summary["segment"] == seg_name]
        avg_m = float(row["avg_monetary"].iloc[0]) if len(row) else 0
        with col:
            st.markdown(f"""
            <div style='background:rgba(0,0,0,0.2); border:1px solid {color}22;
                        border-radius:10px; padding:14px 10px; min-height:150px;'>
                <div style='font-size:16px; margin-bottom:6px;'>{icon}</div>
                <div style='color:{color}; font-weight:600; font-size:0.82rem;
                            margin-bottom:6px;'>{seg_name}</div>
                <div style='font-size:0.75rem; color:#6a9aaa; line-height:1.5;'>{strategy}</div>
                <div style='margin-top:8px; font-family:JetBrains Mono,monospace;
                            font-size:0.75rem; color:{color}aa;'>Avg £{avg_m:,.0f}</div>
            </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: TIME ANALYSIS
# ══════════════════════════════════════════════════════════════════
elif page == "Time Analysis":
    st.markdown("<div class='hero-title' style='font-size:2rem;'>TIME ANALYSIS</div>", unsafe_allow_html=True)
    st.markdown("<span class='sql-badge'>LAG() OVER()</span><span class='sql-badge'>SUM() OVER(ROWS)</span><span class='sql-badge'>JULIANDAY()</span>", unsafe_allow_html=True)
    st.divider()

    m_filt = df_monthly[
        (df_monthly["month"] >= sel_months[0]) &
        (df_monthly["month"] <= sel_months[1])
    ].copy()

    c1,c2,c3 = st.columns(3)
    for col, (num, label) in zip([c1,c2,c3],[
        (f"£{m_filt['revenue'].sum():,.0f}", "Total Revenue"),
        (f"{m_filt['orders'].sum():,}", "Total Orders"),
        (f"{m_filt['mom_growth'].mean():+.1f}%", "Avg MoM Growth"),
    ]):
        with col:
            st.markdown(f"""
            <div class='kpi-card'>
                <div class='kpi-number'>{num}</div>
                <div class='kpi-label'>{label}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("")

    # MoM Growth
    st.markdown("<div class='section-title'>Month-over-Month Revenue Growth</div>", unsafe_allow_html=True)
    bar_colors = [TEAL if v >= 0 else DANGER for v in m_filt["mom_growth"].fillna(0)]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=m_filt["month"], y=m_filt["revenue"],
                         name="Revenue", marker_color=CYAN, opacity=0.5, yaxis="y"))
    fig.add_trace(go.Scatter(x=m_filt["month"],
                             y=m_filt["mom_growth"],
                             name="MoM Growth %", yaxis="y2",
                             mode="lines+markers+text",
                             line=dict(color=TEAL, width=2.5),
                             marker=dict(size=7, color=bar_colors),
                             text=m_filt["mom_growth"].apply(
                                 lambda x: f"{x:+.1f}%" if pd.notna(x) else ""),
                             textposition="top center",
                             textfont=dict(size=9, color=TEAL)))
    fig.add_hline(y=0, line_color=WARN, line_dash="dash", line_width=1, yref="y2")
    fig.update_layout(**PLOT_THEME, height=360,
                      margin=dict(l=0,r=60,t=20,b=0),
                      yaxis=dict(title="Revenue (£)", tickformat="£,.0f"),
                      yaxis2=dict(title="MoM Growth %", overlaying="y",
                                  side="right", ticksuffix="%"),
                      legend=dict(orientation="h", y=1.1))
    st.plotly_chart(fig, use_container_width=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Cumulative revenue
        st.markdown("<div class='section-title'>Cumulative Revenue (Running Total)</div>", unsafe_allow_html=True)
        m_filt["cumulative"] = m_filt["revenue"].cumsum()
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=m_filt["month"], y=m_filt["cumulative"],
            fill="tozeroy", fillcolor="rgba(0,212,255,0.08)",
            line=dict(color=CYAN, width=2.5), mode="lines",
            name="Cumulative Revenue"
        ))
        fig.update_layout(**PLOT_THEME, height=300,
                          margin=dict(l=0,r=0,t=10,b=0),
                          yaxis=dict(tickformat="£,.0f"),
                          xaxis=dict(tickangle=30))
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        # Cohort retention
        st.markdown("<div class='section-title'>Cohort Retention Rate</div>", unsafe_allow_html=True)
        cohort_filt = df_cohort[
            (df_cohort["cohort"] >= sel_months[0]) &
            (df_cohort["cohort"] <= sel_months[1])
        ]
        bar_ret = [TEAL if v >= 50 else (WARN if v >= 25 else DANGER)
                   for v in cohort_filt["retention_pct"]]
        fig = go.Figure(go.Bar(
            x=cohort_filt["cohort"], y=cohort_filt["retention_pct"],
            marker_color=bar_ret, opacity=0.85,
            text=cohort_filt["retention_pct"].apply(lambda x: f"{x:.0f}%"),
            textposition="outside",
            textfont=dict(size=9)
        ))
        fig.add_hline(y=cohort_filt["retention_pct"].mean(),
                      line_dash="dash", line_color=CYAN,
                      annotation_text=f"Avg {cohort_filt['retention_pct'].mean():.1f}%",
                      annotation_font_color=CYAN)
        fig.update_layout(**PLOT_THEME, height=300,
                          margin=dict(l=0,r=0,t=10,b=0),
                          yaxis=dict(ticksuffix="%"),
                          xaxis=dict(tickangle=30))
        st.plotly_chart(fig, use_container_width=True)

    st.markdown(f"""
    <div class='insight-box'>
    ◈ <b>Time Insight:</b> Perhatikan bulan dengan MoM growth negatif —
    apakah bersamaan dengan event tertentu atau masalah supply chain?
    Cohort dengan retention tinggi menunjukkan kualitas akuisisi yang lebih baik di bulan tersebut.
    Gunakan pola ini untuk menentukan <b>kapan & di mana mengalokasikan budget marketing</b>.
    </div>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════
# PAGE: SQL EXPLORER
# ══════════════════════════════════════════════════════════════════
elif page == "SQL Explorer":
    st.markdown("<div class='hero-title' style='font-size:2rem;'>SQL EXPLORER</div>", unsafe_allow_html=True)
    st.markdown("Jalankan SQL query langsung ke database retail.", unsafe_allow_html=True)
    st.divider()

    preset_queries = {
        "-- Pilih template query --": "",
        "Top 10 Products by Revenue": """SELECT Description,
    COUNT(DISTINCT InvoiceNo) AS orders,
    SUM(Quantity) AS total_qty,
    ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue
FROM transactions
GROUP BY Description
ORDER BY revenue DESC
LIMIT 10""",
        "Revenue by Country": """SELECT Country,
    COUNT(DISTINCT InvoiceNo) AS orders,
    ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue,
    ROUND(SUM(CAST(Revenue AS FLOAT))*100.0/
          SUM(SUM(CAST(Revenue AS FLOAT))) OVER(),2) AS pct
FROM transactions
GROUP BY Country
ORDER BY revenue DESC""",
        "Monthly Trend": """SELECT SUBSTR(InvoiceDate,1,7) AS month,
    COUNT(DISTINCT InvoiceNo) AS orders,
    ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue
FROM transactions
GROUP BY month
ORDER BY month""",
        "RFM Summary": """WITH b AS (
    SELECT CustomerID,
        CAST((JULIANDAY('2011-12-10')-JULIANDAY(MAX(InvoiceDate))) AS INT) AS recency,
        COUNT(DISTINCT InvoiceNo) AS frequency,
        ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS monetary
    FROM transactions GROUP BY CustomerID
),
s AS (
    SELECT *,
        NTILE(5) OVER (ORDER BY recency DESC) AS r,
        NTILE(5) OVER (ORDER BY frequency ASC) AS f,
        NTILE(5) OVER (ORDER BY monetary ASC)  AS m
    FROM b
)
SELECT CustomerID, recency, frequency, monetary,
    (r+f+m) AS rfm_score,
    CASE
        WHEN (r+f+m)>=13 THEN 'Champions'
        WHEN (r+f+m)>=10 THEN 'Loyal Customers'
        WHEN (r+f+m)>=7  THEN 'Potential Loyalists'
        WHEN (r+f+m)>=4  THEN 'At Risk'
        ELSE 'Lost'
    END AS segment
FROM s ORDER BY rfm_score DESC LIMIT 20""",
        "MoM Growth (LAG)": """WITH m AS (
    SELECT SUBSTR(InvoiceDate,1,7) AS month,
        ROUND(SUM(CAST(Revenue AS FLOAT)),2) AS revenue
    FROM transactions GROUP BY month
),
l AS (
    SELECT *, LAG(revenue) OVER (ORDER BY month) AS prev FROM m
)
SELECT month, revenue, prev AS prev_month,
    ROUND((revenue-prev)*100.0/prev,1) AS mom_growth_pct
FROM l ORDER BY month""",
    }

    selected = st.selectbox("Template Query", list(preset_queries.keys()))
    default_sql = preset_queries[selected]

    sql_input = st.text_area("SQL Query", value=default_sql, height=180,
                             placeholder="SELECT * FROM transactions LIMIT 10")

    col1, col2 = st.columns([1,5])
    with col1:
        run = st.button("▶ Run Query", type="primary")

    if run and sql_input.strip():
        try:
            conn = sqlite3.connect("retail.db")
            result = pd.read_sql_query(sql_input, conn)
            conn.close()
            st.markdown(f"<div style='font-size:0.78rem; color:#2a6a7a; margin-bottom:8px;'>"
                        f"<b style='color:#00d4ff'>{len(result):,}</b> rows returned</div>",
                        unsafe_allow_html=True)
            st.dataframe(result, use_container_width=True, height=400)
        except Exception as e:
            st.error(f"SQL Error: {e}")

    st.markdown("""
    <div class='insight-box' style='margin-top:1rem;'>
    ◈ <b>Tabel tersedia:</b> <code style='color:#00d4ff;'>transactions</code>
    &nbsp;|&nbsp; Kolom: <code style='color:#7ec8c8;'>InvoiceNo, StockCode, Description,
    Quantity, InvoiceDate, UnitPrice, CustomerID, Country, Revenue</code>
    </div>""", unsafe_allow_html=True)

# ─── Footer ───────────────────────────────────────────────────────
st.divider()
st.markdown("""
<div style='text-align:center; padding:8px 0;
     font-family:JetBrains Mono,monospace;
     font-size:0.65rem; color:#1a4a5a; letter-spacing:2px;'>
◈ RETAIL SQL ANALYTICS ◈ MUHAMMAD RIFAI ◈ ANALYTIFAI ◈
</div>""", unsafe_allow_html=True)
