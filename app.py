import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import datetime

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Global Real Estate Daily Dashboard",
    page_icon="🏢",
    layout="wide"
)

# --- 2. LIVE NEWS ENGINE (VIA NEWS API) ---
@st.cache_data(ttl=600)
def fetch_all_daily_news(country):
    """
    Fetches real-time property market news using a robust 
    JSON API infrastructure instead of raw scraping.
    """
    # Fallback default news if API limit is reached
    fallback_news = {
        'India': [{"title": "Premium residential complexes driving capital interest across Mumbai", "source": "Property Monitor", "time": "Today"}],
        'Dubai': [{"title": "Off-plan luxury developments report strong transactional velocity", "source": "Emirates Property Review", "time": "Today"}],
        'United States': [{"title": "Mortgage metrics hover near multi-year high as buyer demand adapts", "source": "US Market Gauge", "time": "Today"}],
        'Singapore': [{"title": "Private residential valuations stabilize following structural policy checks", "source": "Lion City Insights", "time": "Today"}],
        'China': [{"title": "Liquidity focus sharpens around completing tier-1 housing projects", "source": "Asia Real Estate Journal", "time": "Today"}]
    }

    # PASTE YOUR TOKEN HERE INSIDE THE QUOTES
    API_TOKEN = "7c2452f2-5ab0-42c3-a680-a0d9cffeccd5"
    
    if API_TOKEN == "7c2452f2-5ab0-42c3-a680-a0d9cffeccd5" or not API_TOKEN:
        return fallback_news.get(country)

    query_mapping = {
        'India': 'india real estate property',
        'Dubai': 'dubai property real estate',
        'United States': 'usa housing real estate',
        'Singapore': 'singapore property residential',
        'China': 'china property real estate'
    }
    
    search_term = query_mapping.get(country, 'real estate')
    url = f"https://thenewsapi.com{API_TOKEN}&search={search_term}&language=en&limit=5"
    
    articles = []
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            for item in data.get('data', []):
                articles.append({
                    "title": item.get('title'),
                    "link": item.get('url'),
                    "source": item.get('source', 'Web Feed'),
                    "time": item.get('published_at')[:10] if item.get('published_at') else "Recent"
                })
        if articles:
            return articles
    except Exception:
        pass
        
    return fallback_news.get(country)

# --- 3. HARD DATA STRUCTURAL ENGINE ---
@st.cache_data(ttl=3600)
def load_market_metrics():
    regions = ['India', 'Dubai', 'United States', 'Singapore', 'China']
    metrics_data = {
        'Region': regions,
        'YoY Capital Appreciation (%)': [11.2, 14.5, 3.8, 2.5, -4.5],
        'Avg Gross Rental Yield (%)': [3.2, 7.2, 4.1, 4.3, 1.8],
        'Market Sentiment': ['Bullish', 'Very Bullish', 'Neutral', 'Stable', 'Cautious'],
        'Primary Driver': ['Luxury Residential', 'Foreign Capital', 'High Mortgage Rates', 'Domestic Upgraders', 'Policy Support']
    }
    return pd.DataFrame(metrics_data)

df_metrics = load_market_metrics()

# --- 4. SIDEBAR NAVIGATION ---
st.sidebar.title("🏢 Global Property Hub")
st.sidebar.markdown(f"**Live Feed Matrix**\nAs of: {datetime.date.today().strftime('%B %d, %Y')}")
selected_region = st.sidebar.selectbox(
    "Select Target Market Filter",
    options=["All Regions", "India", "Dubai", "United States", "Singapore", "China"]
)

# --- 5. DASHBOARD HEADER ---
st.title("🌐 Global Real Estate Live News Aggregator")
st.markdown("Streaming comprehensive property market press, transaction reports, and cross-border performance trends.")
st.markdown("---")

# --- 6. KPI FLASH CARDS ---
st.subheader("📊 Cross-Border Performance Flash")
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

# --- 7. DATA VISUALIZATION MATRIX ---
st.subheader("📈 Capital Appreciation vs Yield Analysis")
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

fig.update_layout(title_text="Macro Performance Metrics", hovermode="x unified")
st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# --- 8. COMPREHENSIVE DAILY NEWS FEED GENERATOR ---
st.subheader("📰 Scrollable Daily Real Estate News Streams")

regions_to_display = df_metrics['Region'].tolist() if selected_region == "All Regions" else [selected_region]

for region in regions_to_display:
    st.markdown(f"### {flags[region]} {region} Comprehensive Market Stream")
    
    news_stream = fetch_all_daily_news(region)
    col_stats, col_feed = st.columns(2)
    
    with col_stats:
        reg_row = df_metrics[df_metrics['Region'] == region].iloc[0] if selected_region != "All Regions" else df_metrics[df_metrics['Region'] == region].iloc[0]
        st.info(f"**Core Market Indicators:**\n* **Primary Vector:** {reg_row['Primary Driver']}\n* **Sentiment Structure:** {reg_row['Market Sentiment']}")
        if reg_row['YoY Capital Appreciation (%)'] > 0:
            st.success("Demand environment remains constructive for core transactions.")
        else:
            st.warning("Asset repricing conditions present entry value opportunities.")
            
    with col_feed:
        with st.container(height=380):
            for article in news_stream:
                if "link" in article:
                    st.markdown(f"🔗 **[{article['title']}]({article['link']})**")
                else:
                    st.markdown(f"🔹 **{article['title']}**")
                st.caption(f"📰 {article['source']} • 🕒 {article['time']}")
                st.markdown("<hr style='margin:4px 0px; opacity:0.15;'>", unsafe_allow_html=True)
                
    st.markdown("<br>", unsafe_allow_html=True)





