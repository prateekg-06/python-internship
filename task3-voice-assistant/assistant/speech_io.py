"""
speech_io.py
------------
Wraps SpeechRecognition (speech-to-text) and pyttsx3 (text-to-speech)
behind a small, simple interface: listen() and speak().
"""

import speech_recognition as sr
import pyttsx3

from assistant import config


class SpeechIO:
    """Handles all audio input/output for the assistant."""

    def __init__(self, use_voice_output=True):
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = config.RECOGNIZER_ENERGY_THRESHOLD
        self.recognizer.pause_threshold = config.RECOGNIZER_PAUSE_THRESHOLD
        self.microphone = sr.Microphone()
        self.use_voice_output = use_voice_output

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1)

        self.tts_engine = pyttsx3.init()
        self.tts_engine.setProperty("rate", config.TTS_RATE)
        self.tts_engine.setProperty("volume", config.TTS_VOLUME)

    def speak(self, text: str):
        """Convert text to speech and print it for visibility/logging."""
        print(f"Assistant: {text}")
        if self.use_voice_output:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()

    def listen(self, timeout=None, phrase_time_limit=None) -> str:
        """
        Listen on the microphone and return recognized text (lowercased),
        or an empty string if nothing could be understood.
        """
        timeout = timeout or config.LISTEN_TIMEOUT
        phrase_time_limit = phrase_time_limit or config.PHRASE_TIME_LIMIT

        with self.microphone as source:
            try:
                audio = self.recognizer.listen(
                    source, timeout=timeout, phrase_time_limit=phrase_time_limit
                )
            except sr.WaitTimeoutError:
                return ""

        try:
            text = self.recognizer.recognize_google(audio)
            print(f"You said: {text}")
            return text.lower()
        except sr.UnknownValueError:
            return ""
        except sr.RequestError as e:
            print(f"Speech recognition service error: {e}")
            return ""
