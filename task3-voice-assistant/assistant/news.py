"""
news.py
-------
Fetches top headlines from NewsAPI.org.
Requires NEWS_API_KEY to be set (see .env.example).
"""

import requests

from assistant import config

BASE_URL = "https://newsapi.org/v2/top-headlines"


def get_news(category: str = None, country: str = "us", max_headlines: int = 5) -> str:
    """
    Return a spoken-friendly summary of the top headlines.
    category: optional NewsAPI category (business, technology, sports, etc.)
    """
    if not config.NEWS_API_KEY or config.NEWS_API_KEY == "your_newsapi_key_here":
        return (
            "I can't read the news yet because no NewsAPI key is configured. "
            "Please add NEWS_API_KEY to your .env file."
        )

    params = {
        "apiKey": config.NEWS_API_KEY,
        "country": country,
        "pageSize": max_headlines,
    }
    if category:
        params["category"] = category

    try:
        response = requests.get(BASE_URL, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException:
        return "I couldn't reach the news service. Please try again later."

    articles = data.get("articles", [])
    if not articles:
        return "I couldn't find any news headlines right now."

    headlines = [article.get("title", "").split(" - ")[0] for article in articles if article.get("title")]
    headlines = headlines[:max_headlines]

    if not headlines:
        return "I couldn't find any news headlines right now."

    spoken = "Here are the top headlines. " + ". ".join(headlines) + "."
    return spoken
