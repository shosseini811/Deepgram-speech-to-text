# Deepgram Real-Time Transcription

This project demonstrates how to use the Deepgram API for real-time audio transcription using Python. The script captures audio from the microphone and sends it to Deepgram for transcription, displaying the results in real-time.

## Requirements

- Python 3.10 or higher
- Deepgram API key

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/yourusername/deepgram-speech-to-text.git
   cd deepgram-speech-to-text
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   Make sure to uncomment the lines in `requirements.txt`:

   ```text
   deepgram-sdk>=3.0.0
   pyaudio
   python-dotenv
   websockets
   numpy
   ```

   Then run:

   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables:**

   Create a `.env` file in the root directory of the project and add your Deepgram API key:

   ```env
   DEEPGRAM_API_KEY="your_deepgram_api_key_here"
   ```

## Usage

1. **Run the transcription script:**

   ```bash
   python realtime_transcription.py
   ```

2. **Start speaking into your microphone.** The script will capture your audio and display the transcriptions in real-time.

3. **Stop the transcription:**

   Press `Ctrl+C` to stop the script.

## Code Explanation

- **Imports:**
  - The script imports necessary libraries, including `asyncio`, `dotenv`, and `deepgram` SDK components.

- **Event Handlers:**
  - The script defines several event handlers to manage WebSocket events:
    - `on_open`: Triggered when the connection is opened.
    - `on_message`: Handles incoming transcription results.
    - `on_metadata`: Handles metadata messages.
    - `on_speech_started`: Triggered when speech is detected.
    - `on_utterance_end`: Triggered when the utterance ends.
    - `on_close`: Triggered when the connection is closed.
    - `on_error`: Handles errors that occur during the connection.

- **Microphone Input:**
  - The script uses the `Microphone` class to capture audio input and send it to Deepgram.

- **Configuration:**
  - The `LiveOptions` class is used to configure the transcription settings, including the model, language, and whether to enable interim results.

- **Graceful Shutdown:**
  - The script handles shutdown signals (like `SIGINT` and `SIGTERM`) to ensure that resources are cleaned up properly.

## Troubleshooting

- Ensure your microphone is set as the default input device and is functioning correctly.
- Check that your Deepgram API key is valid and has the necessary permissions.
- If you encounter issues, add print statements in the event handlers to debug the flow of data.


