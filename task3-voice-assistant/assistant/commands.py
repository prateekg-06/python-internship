"""
commands.py
-----------
Interprets recognized text and dispatches it to the right feature
(weather, news, reminders, time/date, or general chit-chat).
"""

import re
from datetime import datetime

from assistant import weather, news, reminders


EXIT_PHRASES = ("exit", "quit", "stop", "goodbye", "bye", "shut down")


class CommandHandler:
    def __init__(self, reminder_manager: reminders.ReminderManager):
        self.reminder_manager = reminder_manager

    def handle(self, command: str) -> tuple[str, bool]:
        """
        Process a recognized command string.
        Returns (response_text, should_exit).
        """
        command = command.lower().strip()

        if not command:
            return "I didn't catch that. Could you say it again?", False

        if self._matches_any(command, EXIT_PHRASES):
            return "Goodbye! Have a great day.", True

        if "weather" in command:
            return self._handle_weather(command), False

        if "news" in command or "headline" in command:
            return self._handle_news(command), False

        if "list" in command and "reminder" in command:
            return self._handle_list_reminders(), False

        if "remind" in command or "reminder" in command:
            return self._handle_reminder(command), False

        if "time" in command and "what" in command:
            return self._handle_time(), False

        if "date" in command or ("what" in command and "day" in command):
            return self._handle_date(), False

        if "your name" in command or "who are you" in command:
            return "I'm your personal voice assistant, here to help with reminders, weather, and news.", False

        if "thank" in command:
            return "You're welcome!", False

        return (
            "I'm not sure how to help with that yet. You can ask me about the weather, "
            "the news, or to set a reminder.",
            False,
        )

    # ---------- individual handlers ----------

    def _handle_weather(self, command: str) -> str:
        city = self._extract_city(command)
        return weather.get_weather(city)

    def _handle_news(self, command: str) -> str:
        category = None
        for cat in ("business", "technology", "sports", "health", "science", "entertainment"):
            if cat in command:
                category = cat
                break
        return news.get_news(category=category)

    def _handle_reminder(self, command: str) -> str:
        task_text, due_time = reminders.parse_reminder_command(command)
        if not due_time:
            return (
                "I can set a reminder if you tell me what to remind you about and when, "
                "for example: remind me to call mom in 10 minutes."
            )
        self.reminder_manager.add_reminder(task_text, due_time)
        time_str = due_time.strftime("%I:%M %p").lstrip("0")
        return f"Okay, I'll remind you to {task_text} at {time_str}."

    def _handle_list_reminders(self) -> str:
        upcoming = self.reminder_manager.list_reminders()
        if not upcoming:
            return "You have no upcoming reminders."
        parts = []
        for r in upcoming:
            due_time = datetime.fromisoformat(r["time"])
            time_str = due_time.strftime("%I:%M %p").lstrip("0")
            parts.append(f"{r['text']} at {time_str}")
        return "Here are your upcoming reminders: " + "; ".join(parts) + "."

    def _handle_time(self) -> str:
        now = datetime.now().strftime("%I:%M %p").lstrip("0")
        return f"It's currently {now}."

    def _handle_date(self) -> str:
        today = datetime.now().strftime("%A, %B %d, %Y")
        return f"Today is {today}."

    # ---------- helpers ----------

    @staticmethod
    def _matches_any(command: str, phrases) -> bool:
        return any(phrase in command for phrase in phrases)

    @staticmethod
    def _extract_city(command: str) -> str:
        """Extract a city name from phrases like 'weather in Paris'."""
        match = re.search(r"weather (?:in|for|at)\s+([a-zA-Z\s]+)", command)
        if match:
            return match.group(1).strip().rstrip("?.!")
        return None
