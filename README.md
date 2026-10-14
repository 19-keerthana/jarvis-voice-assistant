# J.A.R.V.I.S. — Personal Voice Assistant

A Python desktop voice assistant featuring a modern dark-themed GUI, offline speech recognition, local AI responses, text-to-speech, and productivity commands.

## Features

- **Modern GUI:** Dark-themed desktop interface built with CustomTkinter.
- **Offline speech recognition:** Uses Vosk with a downloaded local speech model.
- **Local AI:** Integrates with Ollama and the Llama 3.2 model.
- **Text-to-speech:** Uses pyttsx3 to speak responses.
- **Productivity commands:** Supports time, date, notes, and other built-in commands.
- **Web search:** Opens Google Search when requested.

## Technology Stack

- Python 3.13
- Vosk
- SpeechRecognition
- PyAudio
- pyttsx3
- CustomTkinter
- Requests
- Ollama with Llama 3.2

## Prerequisites

- Python 3.13
- Git
- A working microphone for voice input
- A compatible Vosk speech model
- Ollama for local AI responses

## Installation

Clone the repository:

```bash
git clone https://github.com/19-keerthana/jarvis-voice-assistant/tree/main
cd jarvis-voice-assistant
```

Create a virtual environment on Windows:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the Python dependencies:

```bash
python -m pip install -r requirements.txt
```

## Configure Vosk

Download a compatible speech-recognition model from the official Vosk website:

https://alphacephei.com/vosk/models

Extract the model into the directory expected by `main.py`. The folder name and location must match the path used in your code.

## Configure Ollama

Install Ollama from:

https://ollama.com/download

Download the model:

```bash
ollama pull llama3.2
```

Make sure Ollama is running before using the local AI feature.

## Run the Application

Activate your virtual environment, then run:

```bash
python main.py
```

## Screenshots

Application screenshots are available in the `screenshots/` directory.

## Privacy and Connectivity

- Vosk can recognize speech locally after its model has been downloaded.
- Ollama runs AI models locally after the model download.
- Google Search requires an internet connection.
- Initial installation and model downloads require internet access.

Actual connectivity requirements depend on the code paths enabled in your configuration.

## Testing

Run the available automated tests:

```bash
python -m unittest -v test_commands.py
```

## Future Improvements

- Expand automated tests for the actual application command handler.
- Improve error handling and logging.
- Add configurable commands and settings.
- Improve offline operation and packaging for Windows.

## License

A license has not been specified yet. Add a `LICENSE` file if you intend to publish the project for reuse by others.