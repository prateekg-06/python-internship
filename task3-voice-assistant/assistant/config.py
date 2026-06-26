"""
config.py
---------
Centralized configuration for the voice assistant. Loads API keys and
settings from environment variables (via a .env file if present).
"""

import os
from dotenv import load_dotenv

load_dotenv()

OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY", "")
NEWS_API_KEY = os.getenv("NEWS_API_KEY", "")
DEFAULT_CITY = os.getenv("DEFAULT_CITY", "New York")
WAKE_WORD = os.getenv("WAKE_WORD", "jarvis").lower()

# Speech recognition tuning
RECOGNIZER_ENERGY_THRESHOLD = 300
RECOGNIZER_PAUSE_THRESHOLD = 0.8
LISTEN_TIMEOUT = 5
PHRASE_TIME_LIMIT = 8

# Text-to-speech tuning
TTS_RATE = 175
TTS_VOLUME = 1.0

# Reminder storage file
REMINDERS_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "reminders.json")
