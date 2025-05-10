
import requests

API_URL = "https://cryptopanic.com/api/v1/posts/"
API_KEY = "c61180e0b531b0c266add9888bf138dca4712261"  # Replace with your actual API key

def fetch_news_for_symbols(symbols, min_score=0.0):
    query = ",".join(symbols)
    params = {
        "auth_token": API_KEY,
        "currencies": query,
        "public": "true"
    }
    response = requests.get(API_URL, params=params)
    data = response.json()

    news = []
    for item in data.get("results", []):
        risk_score = 1.0  # Stub risk logic — customize as needed
        if risk_score >= min_score:
            news.append({
                "title": item["title"],
                "risk_score": risk_score,
                "published_at": item["published_at"]
            })

    return news
