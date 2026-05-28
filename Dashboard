import requests
import streamlit as st

# Securely fetch your API key from Streamlit secrets or default string
NEWS_API_KEY = st.secrets.get("NEWS_API_KEY", "YOUR_NEWS_API_KEY_HERE")

def fetch_live_news(country_keyword):
    """Fetches real-time real estate news from Google News index via NewsAPI"""
    # Build query focused strictly on property/real estate markets
    query = f'"{country_keyword}" AND ("real estate" OR "property market" OR "housing")'
    url = f'https://newsapi.org{query}&sortBy=publishedAt&pageSize=3&language=en&apiKey={NEWS_API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        articles = []
        if data.get("status") == "ok":
            for art in data.get("articles", []):
                articles.append({
                    "title": art.get("title"),
                    "source": art.get("source", {}).get("name"),
                    "time": art.get("publishedAt")[:10]  # Extracts YYYY-MM-DD
                })
        return articles if articles else [{"title": "No recent updates found.", "source": "Search Engine", "time": "Today"}]
    except Exception as e:
        return [{"title": "Error connecting to search feed.", "source": "System", "time": "Now"}]

# Update your dashboard loading function to use the live search engine
@st.cache_data(ttl=1800)  # Cache results for 30 minutes to save API limits
def load_dashboard_data():
    regions = ['India', 'Dubai', 'United States', 'Singapore', 'China']
    
    # Keep your static performance metrics
    metrics_data = {
        'Region': regions,
        'YoY Capital Appreciation (%)': [11.2, 14.5, 3.8, 2.5, -4.5],
        'Avg Gross Rental Yield (%)': [3.2, 7.2, 4.1, 4.3, 1.8],
        'Market Sentiment': ['Bullish', 'Very Bullish', 'Neutral', 'Stable', 'Cautious'],
        'Primary Driver': ['Luxury Residential', 'Foreign Capital', 'High Mortgage Rates', 'Domestic Upgraders', 'Policy Support']
    }
    df_metrics = pd.DataFrame(metrics_data)
    
    # Dynamic live search feed mapping
    news_feed = {
        'India': fetch_live_news('India'),
        'Dubai': fetch_live_news('Dubai'),
        'United States': fetch_live_news('United States'),
        'Singapore': fetch_live_news('Singapore'),
        'China': fetch_live_news('China')
    }
    
    return df_metrics, news_feed
