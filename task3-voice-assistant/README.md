# Task 3 — Voice-Activated Personal Assistant

A Python personal assistant that listens for a wake word, then responds to
voice commands for setting reminders, checking the weather, reading news
headlines, and telling the time/date — all through speech recognition and
text-to-speech.

## Features

- **Wake-word activation** — say "jarvis" (configurable) to start listening
- **Reminders** — "remind me to call mom in 10 minutes" (persisted to disk, fires in the background even mid-conversation)
- **Weather** — "what's the weather in Paris?" (via OpenWeatherMap)
- **News** — "tell me the news" or "what's the technology news?" (via NewsAPI)
- **Time & date** — "what time is it?", "what's today's date?"
- **Text mode** — fully testable without a microphone or speakers

## Project structure

```
task3-voice-assistant/
├── main.py                 # entry point (voice or text mode)
├── requirements.txt
├── .env.example             # copy to .env and fill in API keys
└── assistant/
    ├── config.py            # settings loaded from .env
    ├── speech_io.py         # speech-to-text + text-to-speech wrapper
    ├── commands.py          # routes recognized text to the right feature
    ├── reminders.py         # reminder storage, parsing, and background checks
    ├── weather.py           # OpenWeatherMap integration
    └── news.py              # NewsAPI integration
```

## Setup

### 1. Install system audio dependencies

`PyAudio` (needed for the microphone) requires a system library called
PortAudio. Install it **before** `pip install`:

**macOS:**
```bash
brew install portaudio
```

**Ubuntu/Debian:**
```bash
sudo apt-get install python3-pyaudio portaudio19-dev
```

**Windows:** PyAudio usually installs from a prebuilt wheel via pip with no
extra steps. If it fails, install from
[this guide](https://pypi.org/project/PyAudio/).

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure API keys

```bash
cp .env.example .env
```

Then edit `.env` and add free API keys from:
- [OpenWeatherMap](https://openweathermap.org/api) — for weather
- [NewsAPI](https://newsapi.org) — for news headlines

The assistant works without these keys too — it'll just tell you that
weather/news aren't configured, while reminders, time, and date still work.

### 4. Run it

**Voice mode** (microphone + speakers):
```bash
python main.py
```

**Text mode** (keyboard, no audio hardware needed — great for testing):
```bash
python main.py --text
```

## Example commands

| You say | Assistant does |
|---|---|
| "jarvis, what's the weather?" | Reports weather for your default city |
| "jarvis, what's the weather in Tokyo?" | Reports weather for Tokyo |
| "jarvis, remind me to take out the trash in 20 minutes" | Saves a reminder, confirms the time |
| "jarvis, list my reminders" | Reads back all upcoming reminders |
| "jarvis, tell me the news" | Reads top headlines |
| "jarvis, what's the sports news?" | Reads top sports headlines |
| "jarvis, what time is it?" | Tells the current time |
| "jarvis, goodbye" | Exits the program |

## How it works

1. **`SpeechIO.listen()`** uses the `speech_recognition` library, which
   captures microphone audio and sends it to Google's free speech-to-text
   web API to get text back.
2. **`CommandHandler.handle()`** does simple keyword/pattern matching on
   that text to decide which feature to invoke — no ML model needed for
   intent classification, keeping it lightweight and fully offline-debuggable
   in text mode.
3. **`ReminderManager`** runs a background thread that checks every 5
   seconds whether any saved reminder is due, and fires a callback (which
   speaks the reminder aloud) when it is. Reminders are saved to
   `reminders.json` so they aren't lost on restart.
4. **`SpeechIO.speak()`** uses `pyttsx3`, which performs text-to-speech
   completely offline using your OS's built-in voices.

## Extending it

- **Add a new skill**: write a new module (like `weather.py`), then add a
  matching `if` branch in `CommandHandler.handle()` in `commands.py`.
- **Change the wake word**: edit `WAKE_WORD` in `.env`.
- **Use a different STT engine**: swap `recognize_google` in `speech_io.py`
  for `recognize_whisper`, `recognize_sphinx` (fully offline), or a cloud
  provider supported by `SpeechRecognition`.
- **Use a different voice**: list available system voices with
  `pyttsx3.init().getProperty('voices')` and set one via
  `tts_engine.setProperty('voice', voice_id)` in `speech_io.py`.

## Troubleshooting

- **"No module named 'pyaudio'" or install fails** — you're missing the
  PortAudio system library; see step 1 above.
- **Assistant never hears the wake word** — try lowering
  `RECOGNIZER_ENERGY_THRESHOLD` in `config.py`, or check your OS microphone
  permissions for the terminal/IDE you're running from.
- **No sound output** — on Linux, `pyttsx3` needs `espeak` installed
  (`sudo apt-get install espeak`).
- **Weather/news say "not configured"** — double check `.env` exists
  (not just `.env.example`) and contains valid keys, and that you're
  running `python main.py` from the project root so `.env` is found.
