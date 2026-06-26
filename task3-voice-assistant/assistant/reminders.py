"""
reminders.py
------------
Simple reminder management: add, list, delete, and background-check
for reminders that have come due. Reminders persist to a JSON file
so they survive restarts.
"""

import json
import os
import re
import threading
import time
import uuid
from datetime import datetime, timedelta

from assistant import config


class ReminderManager:
    def __init__(self, on_due_callback=None):
        """
        on_due_callback: optional function(reminder_dict) called from a
        background thread whenever a reminder becomes due.
        """
        self.file_path = config.REMINDERS_FILE
        self.on_due_callback = on_due_callback
        self._lock = threading.Lock()
        self._reminders = self._load()
        self._stop_event = threading.Event()
        self._checker_thread = threading.Thread(target=self._check_loop, daemon=True)
        self._checker_thread.start()

    # ---------- persistence ----------

    def _load(self):
        if os.path.exists(self.file_path):
            try:
                with open(self.file_path, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return []
        return []

    def _save(self):
        with open(self.file_path, "w") as f:
            json.dump(self._reminders, f, indent=2)

    # ---------- public API ----------

    def add_reminder(self, text: str, when: datetime) -> dict:
        reminder = {
            "id": str(uuid.uuid4())[:8],
            "text": text,
            "time": when.isoformat(),
            "notified": False,
        }
        with self._lock:
            self._reminders.append(reminder)
            self._save()
        return reminder

    def list_reminders(self):
        with self._lock:
            upcoming = [r for r in self._reminders if not r["notified"]]
        upcoming.sort(key=lambda r: r["time"])
        return upcoming

    def delete_reminder(self, reminder_id: str) -> bool:
        with self._lock:
            before = len(self._reminders)
            self._reminders = [r for r in self._reminders if r["id"] != reminder_id]
            changed = len(self._reminders) < before
            if changed:
                self._save()
        return changed

    def stop(self):
        self._stop_event.set()

    # ---------- background due-checking ----------

    def _check_loop(self):
        while not self._stop_event.is_set():
            now = datetime.now()
            with self._lock:
                for reminder in self._reminders:
                    if reminder["notified"]:
                        continue
                    due_time = datetime.fromisoformat(reminder["time"])
                    if now >= due_time:
                        reminder["notified"] = True
                        if self.on_due_callback:
                            self.on_due_callback(reminder)
                self._save()
            time.sleep(5)


# ---------- natural language time parsing ----------

_NUMBER_WORDS = {
    "a": 1, "an": 1, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5,
    "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10, "fifteen": 15,
    "twenty": 20, "thirty": 30, "forty": 40, "forty-five": 45, "sixty": 60,
}


def _word_to_number(word: str) -> int:
    word = word.strip().lower()
    if word.isdigit():
        return int(word)
    return _NUMBER_WORDS.get(word, 1)


def parse_reminder_command(command: str):
    """
    Parse phrases like:
      "remind me to call mom in 10 minutes"
      "remind me to take out the trash in 2 hours"
      "set a reminder to drink water in 30 minutes"
    Returns (task_text, datetime) or (None, None) if it can't be parsed.
    """
    command = command.lower().strip()

    time_pattern = re.search(
        r"in\s+(a|an|one|two|three|four|five|six|seven|eight|nine|ten|"
        r"fifteen|twenty|thirty|forty(?:-five)?|sixty|\d+)\s*"
        r"(second|minute|hour|day)s?",
        command,
    )
    if not time_pattern:
        return None, None

    amount = _word_to_number(time_pattern.group(1))
    unit = time_pattern.group(2)

    unit_to_kwargs = {
        "second": "seconds",
        "minute": "minutes",
        "hour": "hours",
        "day": "days",
    }
    delta = timedelta(**{unit_to_kwargs[unit]: amount})
    due_time = datetime.now() + delta

    task_match = re.search(r"(?:remind me to|reminder to|remind me)\s+(.*?)\s+in\s+", command)
    if task_match:
        task_text = task_match.group(1).strip()
    else:
        task_text = command
        for phrase in ("set a reminder to", "remind me to", "reminder to", "remind me"):
            task_text = task_text.replace(phrase, "")
        task_text = task_text[: time_pattern.start()].strip()

    if not task_text:
        task_text = "your reminder"

    return task_text, due_time
