import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Global Real Estate Daily Dashboard",
    page_icon="🏢",
    layout="wide"
)

# --- 2. DATA GENERATION ---
@st.cache_data(ttl=3600)
def load_dashboard_data():
    regions = ['India', 'Dubai', 'United States', 'Singapore', 'China']
    metrics_data = {
        'Region': regions,
        'YoY Capital Appreciation (%)': [11.2, 14.5, 3.8, 2.5, -4.5],
        'Avg Gross Rental Yield (%)': [3.2, 7.2, 4.1, 4.3, 1.8],
        'Market Sentiment': ['Bullish', 'Very Bullish', 'Neutral', 'Stable', 'Cautious'],
        'Primary Driver': ['Luxury Residential', 'Foreign Capital', 'High Mortgage Rates', 'Domestic Upgraders', 'Policy Support']
    }
    df_metrics = pd.DataFrame(metrics_data)
    
    news_feed = {
        'India': [
            {"title": "Mumbai luxury residential sales jump 18% YoY", "source": "Livemint", "time": "2 hours ago"},
            {"title": "GCC expansion drives Grade-A office demand in Bangalore", "source": "Economic Times", "time": "5 hours ago"}
        ],
        'Dubai': [
            {"title": "Palm Jumeirah villa breaches record price per sq ft", "source": "Khaleej Times", "time": "1 hour ago"},
            {"title": "DLD reports $1.2B in off-plan transactions today", "source": "Bloomberg Middle East", "time": "4 hours ago"}
        ],
        'United States': [
            {"title": "30-year fixed mortgage rates tick up to 6.8%", "source": "FRED / Reuters", "time": "3 hours ago"},
            {"title": "Commercial real estate workouts rise in NYC and SF", "source": "Wall Street Journal", "time": "7 hours ago"}
        ],
        'Singapore': [
            {"title": "HDB resale prices show steady growth despite global slowdown", "source": "Straits Times", "time": "30 mins ago"},
            {"title": "ABSD impact keeps foreign retail property buyers at bay", "source": "Channel NewsAsia", "time": "6 hours ago"}
        ],
        'China': [
            {"title": "Beijing rolls out new liquidity support for stalled housing projects", "source": "Caixin", "time": "1 hour ago"},
            {"title": "Tier-1 cities show mild stabilization; Tier-3/4 vacancies high", "source": "South China Morning Post", "time": "8 hours ago"}
        ]
    }
    return df_metrics, news_feed

df_metrics, news_feed = load_dashboard_data()

# --- 3. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 Global Property Hub")
st.sidebar.markdown(f"**Last updated:** {datetime.date.today().strftime('%B %d, %Y')}")
selected_region = st.sidebar.selectbox(
    "Filter News Focus",
    options=["All Regions", "India", "Dubai", "United States", "Singapore", "China"]
)

# --- 4. HEADER ---
st.title("🌐 Global Real Estate Daily Dashboard")
st.markdown("Automated strategic cross-border real estate performance and news tracker.")
st.markdown("---")

# --- 5. KPI CARDS ---
st.subheader("📊 Cross-Border Flash Metrics")
kpi_cols = st.columns(5)
flags = {"India": "🇮🇳", "Dubai": "🇦🇪", "United States": "🇺🇸", "Singapore": "🇸🇬", "China": "🇨🇳"}

for idx, row in df_metrics.iterrows():
    with kpi_cols[idx]:
        region_name = row['Region']
        color_sentiment = "🟢" if row['YoY Capital Appreciation (%)'] > 0 else "🔴"
        st.metric(
            label=f"{flags[region_name]} {region_name}", 
            value=f"{row['YoY Capital Appreciation (%)']}% YoY", 
            delta=f"Yield: {row['Avg Gross Rental Yield (%)']}%"
        )
        st.markdown(f"**Status:** {color_sentiment} {row['Market Sentiment']}")

st.markdown("---")

# --- 6. DATA VISUALIZATION ---
st.subheader("📈 Global Market Comparison Matrix")
fig = make_subplots(specs=[[{"secondary_y": True}]])

fig.add_trace(
    go.Bar(
        x=df_metrics['Region'], 
        y=df_metrics['YoY Capital Appreciation (%)'],
        name="Capital Appreciation (% YoY)",
        marker_color='#1f77b4',
        opacity=0.75,
        text=df_metrics['YoY Capital Appreciation (%)'].apply(lambda x: f"{x}%"),
        textposition='auto',
    ),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(
        x=df_metrics['Region'], 
        y=df_metrics['Avg Gross Rental Yield (%)'],
        name="Avg Gross Rental Yield (%)",
        marker=dict(color='#d62728', size=10),
        line=dict(color='#d62728', width=3),
        text=df_metrics['Avg Gross Rental Yield (%)'].apply(lambda x: f"{x}%"),
        mode="text+lines+markers",
        textposition="top center"
    ),
    secondary_y=True,
)

fig.update_layout(
    title_text="Capital Appreciation vs Gross Rental Yields",
    hovermode="x unified"
)
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- 7. NEWS FEEDS ---
st.subheader("📰 Regional News Briefs & Analysis")
regions_to_display = df_metrics['Region'].tolist() if selected_region == "All Regions" else [selected_region]

for region in regions_to_display:
    st.markdown(f"#### {flags[region]} {region} Market Update")
    col_analysis, col_news = st.columns(2)
    reg_row = df_metrics[df_metrics['Region'] == region].iloc[0]
    
    with col_analysis:
        st.markdown(f"**Primary Driver:** `{reg_row['Primary Driver']}`")
        if reg_row['YoY Capital Appreciation (%)'] > 0:
            st.success(f"Market shows steady upward asset expansion.")
        else:
            st.error(f"Market structure undergoing correction cycles.")
            
    with col_news:
        for article in news_feed[region]:
            st.markdown(f"🔹 **{article['title']}**")
            st.caption(f"Source: {article['source']} • {article['time']}")

