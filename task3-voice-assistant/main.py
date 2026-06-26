"""
main.py
-------
Entry point for the voice-activated personal assistant.

Usage:
    python main.py            # voice mode (microphone + speakers)
    python main.py --text     # text mode for testing without a mic/speaker

Voice mode flow:
    1. Wait for the wake word (default: "jarvis", configurable in .env).
    2. Listen for a command.
    3. Dispatch the command and speak the response.
    4. Repeat until an exit phrase is heard or Ctrl+C is pressed.
"""

import argparse
import sys

from assistant import config
from assistant.commands import CommandHandler
from assistant.reminders import ReminderManager


def on_reminder_due(reminder, speech_io):
    speech_io.speak(f"Reminder: {reminder['text']}")


def run_voice_mode():
    # Import here so text-mode users don't need pyaudio/pyttsx3 installed.
    from assistant.speech_io import SpeechIO

    speech_io = SpeechIO(use_voice_output=True)
    reminder_manager = ReminderManager(
        on_due_callback=lambda r: on_reminder_due(r, speech_io)
    )
    handler = CommandHandler(reminder_manager)

    speech_io.speak(
        f"Hello! I'm ready. Say '{config.WAKE_WORD}' followed by your command."
    )

    try:
        while True:
            heard = speech_io.listen(timeout=None, phrase_time_limit=4)
            if config.WAKE_WORD not in heard:
                continue

            speech_io.speak("Yes?")
            command = speech_io.listen()
            if not command:
                speech_io.speak("I didn't catch that.")
                continue

            response, should_exit = handler.handle(command)
            speech_io.speak(response)
            if should_exit:
                break
    except KeyboardInterrupt:
        speech_io.speak("Goodbye!")
    finally:
        reminder_manager.stop()


def run_text_mode():
    """Text-based mode: useful for testing logic without audio hardware."""
    reminder_manager = ReminderManager(
        on_due_callback=lambda r: print(f"\n[Reminder] {r['text']}\n")
    )
    handler = CommandHandler(reminder_manager)

    print("Voice Assistant (text mode). Type 'exit' to quit.")
    print("Try: 'what's the weather', 'remind me to call mom in 1 minute', 'tell me the news'\n")

    try:
        while True:
            command = input("You: ").strip()
            if not command:
                continue
            response, should_exit = handler.handle(command)
            print(f"Assistant: {response}")
            if should_exit:
                break
    except KeyboardInterrupt:
        print("\nAssistant: Goodbye!")
    finally:
        reminder_manager.stop()


def main():
    parser = argparse.ArgumentParser(description="Voice-Activated Personal Assistant")
    parser.add_argument(
        "--text", action="store_true", help="Run in text mode (no microphone/speaker needed)"
    )
    args = parser.parse_args()

    if args.text:
        run_text_mode()
    else:
        try:
            run_voice_mode()
        except Exception as e:
            print(f"Voice mode failed to start: {e}")
            print("This usually means a microphone/audio dependency (e.g. PyAudio) isn't installed.")
            print("Falling back to text mode.\n")
            run_text_mode()


if __name__ == "__main__":
    sys.exit(main())
