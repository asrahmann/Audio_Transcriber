# Whisper Transcription API

This is a simple Flask-based API for transcribing audio files using OpenAI's [Whisper](https://github.com/openai/whisper) speech recognition model.

## Features

- Accepts audio file uploads (`.wav`, `.mp3`, etc.)
- Uses Whisper to transcribe the audio
- Returns the transcription as JSON
- CORS-enabled for frontend integration

## Requirements

- Python 3.8+
- `ffmpeg` installed and available in system PATH (required by Whisper)

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/asrahmann/Audio_Transcriber.git
   cd whisper-api
