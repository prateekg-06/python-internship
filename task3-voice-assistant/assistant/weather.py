"""
weather.py
----------
Fetches current weather conditions from the OpenWeatherMap API.
Requires OPENWEATHER_API_KEY to be set (see .env.example).
"""

import requests

from assistant import config

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str = None) -> str:
    """
    Return a natural-language weather summary for the given city
    (or the configured default city if none is given).
    """
    city = city or config.DEFAULT_CITY

    if not config.OPENWEATHER_API_KEY or config.OPENWEATHER_API_KEY == "your_openweathermap_api_key_here":
        return (
            "I can't check the weather yet because no OpenWeatherMap API key "
            "is configured. Please add OPENWEATHER_API_KEY to your .env file."
        )

    params = {
        "q": city,
        "appid": config.OPENWEATHER_API_KEY,
        "units": "metric",
    }

    try:
        response = requests.get(BASE_URL, params=params, timeout=8)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError:
        if response.status_code == 404:
            return f"I couldn't find a city called {city}. Could you try again?"
        return "I had trouble reaching the weather service. Please try again later."
    except requests.exceptions.RequestException:
        return "I couldn't connect to the weather service. Please check your internet connection."

    try:
        description = data["weather"][0]["description"]
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        humidity = data["main"]["humidity"]
        resolved_city = data.get("name", city)
    except (KeyError, IndexError):
        return "I got an unexpected response from the weather service."

    return (
        f"Right now in {resolved_city}, it's {temp} degrees Celsius with {description}, "
        f"feeling like {feels_like} degrees. Humidity is at {humidity} percent."
    )
