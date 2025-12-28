# Xenofont

Xenofont is a lightweight, fully offline voice assistant written in pure Python, created around 2020 — long before the widespread adoption of large language models.

It operates entirely without internet connection (except for optional "what is" queries that use Yandex search), relies on no external AI services, and runs locally on your machine. All speech recognition is handled by SpeechRecognition with pocketsphinx or Google fallback, while text-to-speech uses pyttsx3.

### Key Features
- Voice commands for basic tasks (time, date, weather via OpenWeatherMap)
- Simple conversational responses and one classic Russian joke
- Radio stream playback
- Web search fallback for unknown questions
- Background listening mode
- Immediate shutdown on the command "stop"

### Philosophy
This project was built as a personal experiment to create a functional voice-controlled desktop assistant using only traditional programming techniques and publicly available libraries — no neural networks, no cloud APIs, no telemetry.

It represents an era when building a talking program still felt like real hacking.

Today it serves as a nostalgic artifact and a minimal base for further development (such as integration with local LLMs like Ollama).

Pre-pre-alpha quality. Expect bugs, hard-coded Russian responses, and questionable code style. It works — sometimes surprisingly well.