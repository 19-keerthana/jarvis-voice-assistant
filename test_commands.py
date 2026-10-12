
import unittest
from datetime import datetime


def classify_command(text):
    command = text.lower().strip()

    if "time" in command:
        return "time"
    if "date" in command or "today" in command:
        return "date"
    if command.startswith(
        ("take a note", "remember this", "note ")
    ):
        return "note"
    if "read notes" in command or "show notes" in command:
        return "read_notes"
    if "open google" in command:
        return "google"
    if command in ("help", "commands", "what can you do"):
        return "help"
    return "ai"


class TestCommands(unittest.TestCase):
    def test_time(self):
        self.assertEqual(classify_command("What time is it?"), "time")

    def test_date(self):
        self.assertEqual(classify_command("Tell me today's date"), "date")

    def test_note(self):
        self.assertEqual(
            classify_command("take a note buy milk"), "note"
        )

    def test_read_notes(self):
        self.assertEqual(classify_command("read notes"), "read_notes")

    def test_google(self):
        self.assertEqual(classify_command("open google"), "google")

    def test_ai_fallback(self):
        self.assertEqual(
            classify_command("Explain neural networks"), "ai"
        )


if __name__ == "__main__":
    unittest.main()
