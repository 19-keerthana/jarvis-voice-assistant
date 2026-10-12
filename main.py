import os
import threading
import webbrowser
import subprocess
import platform
from datetime import datetime
from urllib.parse import quote_plus
from pathlib import Path

import customtkinter as ctk
import pyttsx3
import requests
import speech_recognition as sr

APP_NAME = "J.A.R.V.I.S."
OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL = "llama3.2"

BASE_DIR = Path(__file__).resolve().parent
NOTES_FILE = BASE_DIR / "notes.txt"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class JarvisAssistant:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("J.A.R.V.I.S. | Personal AI")
        self.root.geometry("950x680")
        self.root.minsize(750, 560)

        self.recognizer = sr.Recognizer()
        self.listening = False
        self.busy = False
        self.alive = True
        self.history = []

        self.build_ui()
        self.log("SYSTEM", "JARVIS initialized. Systems ready.")
        self.log("SYSTEM", "Press LISTEN or type a command below.")
        self.root.protocol("WM_DELETE_WINDOW", self.close)

    def build_ui(self):
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)

        header = ctk.CTkFrame(self.root, corner_radius=15)
        header.grid(row=0, column=0, padx=18, pady=(18, 10), sticky="ew")
        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="J.A.R.V.I.S.",
            font=ctk.CTkFont(size=30, weight="bold"),
            text_color="#42C8FF",
        ).grid(row=0, column=0, padx=20, pady=(14, 2))

        ctk.CTkLabel(
            header,
            text="PERSONAL VOICE ASSISTANT  •  PYTHON",
            font=ctk.CTkFont(size=11),
            text_color="#9BAFC4",
        ).grid(row=1, column=0, pady=(0, 14))

        self.status = ctk.CTkLabel(
            header,
            text="● SYSTEM ONLINE",
            text_color="#5BE7A9",
            font=ctk.CTkFont(size=12, weight="bold"),
        )
        self.status.grid(row=0, column=1, padx=20, pady=15)

        self.console = ctk.CTkTextbox(
            self.root,
            corner_radius=12,
            font=ctk.CTkFont(family="Consolas", size=13),
            wrap="word",
        )
        self.console.grid(row=1, column=0, padx=18, pady=8, sticky="nsew")
        self.console.configure(state="disabled")

        controls = ctk.CTkFrame(self.root, corner_radius=15)
        controls.grid(row=2, column=0, padx=18, pady=(8, 18), sticky="ew")
        controls.grid_columnconfigure(0, weight=1)

        self.command_input = ctk.CTkEntry(
            controls,
            placeholder_text="Type a command, e.g. what time is it?",
            height=42,
        )
        self.command_input.grid(row=0, column=0, padx=(12, 6), pady=12, sticky="ew")
        self.command_input.bind("<Return>", self.submit_text)

        ctk.CTkButton(
            controls, text="EXECUTE", width=100, command=self.submit_text
        ).grid(row=0, column=1, padx=6, pady=12)

        self.listen_button = ctk.CTkButton(
            controls,
            text="🎙 LISTEN",
            width=115,
            fg_color="#087FA5",
            hover_color="#096582",
            command=self.listen_once,
        )
        self.listen_button.grid(row=0, column=2, padx=(6, 12), pady=12)

        ctk.CTkLabel(
            controls,
            text="All systems running completely offline via local models.",
            text_color="#9BAFC4",
            font=ctk.CTkFont(size=10),
        ).grid(row=1, column=0, columnspan=3, pady=(0, 10))

    def ui(self, callback, *args, **kwargs):
        if self.alive:
            self.root.after(0, lambda: callback(*args, **kwargs))

    def log(self, sender, message):
        if not self.alive:
            return
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.console.configure(state="normal")
        self.console.insert("end", f"[{timestamp}] {sender}: {message}\n\n")
        self.console.see("end")
        self.console.configure(state="disabled")

    def set_status(self, message, color="#42C8FF"):
        self.status.configure(text=f"● {message}", text_color=color)

    def speak(self, message):
        try:
            engine = pyttsx3.init()
            engine.setProperty("rate", 180)
            engine.setProperty("volume", 0.9)
            engine.say(message)
            engine.runAndWait()
            engine.stop()
        except Exception as exc:
            self.ui(self.log, "TTS ERROR", str(exc))

    def respond(self, message):
        self.ui(self.log, "JARVIS", message)
        self.speak(message)

    def listen_once(self):
        if self.busy:
            self.log("SYSTEM", "Please wait for the current task.")
            return

        self.busy = True
        self.ui(self.listen_button.configure, state="disabled")
        self.ui(self.set_status, "LISTENING...", "#FFCB69")
        self.ui(self.log, "SYSTEM", "Listening for up to 6 seconds...")

        threading.Thread(target=self._listen_worker, daemon=True).start()

    def _listen_worker(self):
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=7)

            self.ui(self.set_status, "PROCESSING OFFLINE...", "#FFCB69")
            
            # Using local offline Vosk recognition
            text = self.recognizer.recognize_vosk(audio)
            
            import json
            text_data = json.loads(text)
            clean_text = text_data.get("text", "").strip()

            if clean_text:
                self.ui(self.log, "YOU", clean_text)
                self.process_command(clean_text)
            else:
                self.ui(self.log, "SYSTEM", "I couldn't understand that.")

        except sr.WaitTimeoutError:
            self.ui(self.log, "SYSTEM", "No speech detected. Try again.")
        except Exception as exc:
            self.ui(self.log, "ERROR", str(exc))
        finally:
            self.busy = False
            self.ui(self.listen_button.configure, state="normal")
            self.ui(self.set_status, "SYSTEM ONLINE", "#5BE7A9")

    def submit_text(self, event=None):
        if self.busy:
            self.log("SYSTEM", "Please wait for the current task.")
            return

        text = self.command_input.get().strip()
        if not text:
            return

        self.command_input.delete(0, "end")
        self.log("YOU", text)
        self.busy = True

        threading.Thread(
            target=self._command_worker,
            args=(text,),
            daemon=True,
        ).start()

    def _command_worker(self, text):
        try:
            self.process_command(text)
        except Exception as exc:
            self.ui(self.log, "ERROR", str(exc))
        finally:
            self.busy = False
            self.ui(self.set_status, "SYSTEM ONLINE", "#5BE7A9")

    def process_command(self, text):
        command = text.lower().strip()
        if not command:
            return

        # 1. Local command: current time
        if "time" in command:
            self.respond("The time is " + datetime.now().strftime("%I:%M %p"))

        # 2. Local command: current date
        elif "date" in command or "today" in command:
            self.respond("Today is " + datetime.now().strftime("%A, %d %B %Y"))

        # 3. Local command: save a note
        elif command.startswith(("take a note", "remember this", "note ")):
            note = text
            for prefix in ("take a note", "remember this", "note"):
                if command.startswith(prefix):
                    note = text[len(prefix) :].strip(" :,-")
                    break

            if not note:
                self.respond("What would you like me to note down?")
                return

            with open(NOTES_FILE, "a", encoding="utf-8") as f:
                f.write(
                    f"[{datetime.now().strftime('%Y-%m-%d %H:%M')}] {note}\n"
                )
            self.respond("I've saved that note for you.")

        # 4. Local command: search the web
        elif command.startswith(("search", "google ")):
            query = text
            for prefix in ("search", "google"):
                if command.startswith(prefix):
                    query = text[len(prefix) :].strip(" :,-")
                    break
            self.respond(f"Searching the web for {query}")
            webbrowser.open(f"https://google.com{quote_plus(query)}")

        # 5. Fallback: Local AI via Ollama
        else:
            self.query_ollama(text)

    def query_ollama(self, prompt):
        self.ui(self.set_status, "AI IS THINKING...", "#42C8FF")
        try:
            self.history.append({"role": "user", "content": prompt})

            payload = {
                "model": OLLAMA_MODEL,
                "messages": self.history,
                "stream": False,
            }
            response = requests.post(OLLAMA_URL, json=payload, timeout=30)

            if response.status_code == 200:
                ai_response = (
                    response.json().get("message", {}).get("content", "")
                )
                self.history.append({"role": "assistant", "content": ai_response})
                self.respond(ai_response)
            else:
                self.respond(
                    "I encountered an error communicating with my AI core."
                )

        except requests.exceptions.ConnectionError:
            self.respond(
                "My AI core is currently offline. Please ensure Ollama is running."
            )
        except Exception as e:
            self.ui(self.log, "AI ERROR", str(e))

    def close(self):
        self.alive = False
        self.root.destroy()

if __name__ == "__main__":
    app = JarvisAssistant()
    app.root.mainloop()
