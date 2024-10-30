# Copyright 2023-2024 Deepgram SDK contributors. All Rights Reserved.
# Use of this source code is governed by a MIT license that can be found in the LICENSE file.
# SPDX-License-Identifier: MIT

from signal import SIGINT, SIGTERM
import asyncio
from dotenv import load_dotenv
import logging
from deepgram.utils import verboselogs
from time import sleep

from deepgram import (
    DeepgramClient,
    DeepgramClientOptions,
    LiveTranscriptionEvents,
    LiveOptions,
    Microphone,
)

load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def main():
    try:
        print("\nInitializing Deepgram transcription...\n")
        
        loop = asyncio.get_event_loop()
        
        # Configure Deepgram client
        config = DeepgramClientOptions(options={"keepalive": "true"})
        
        # Make sure you have your API key in .env file
        deepgram = DeepgramClient()  # It will automatically read from DEEPGRAM_API_KEY env variable
        
        print("Connecting to Deepgram...")
        dg_connection = deepgram.listen.asyncwebsocket.v("1")
        
        # Dictionary to store transcripts
        transcripts_by_speaker = {}

        async def on_message(self, result, **kwargs):
            try:
                if len(result.channel.alternatives) > 0:
                    alternative = result.channel.alternatives[0]
                    sentence = alternative.transcript
                    
                    if len(sentence) > 0 and result.is_final:
                        words = alternative.words
                        if not words:
                            return
                        
                        current_speaker = words[0].speaker
                        current_segment = []
                        
                        for word in words:
                            if word.speaker == current_speaker:
                                current_segment.append(word.word)
                            else:
                                if current_speaker not in transcripts_by_speaker:
                                    transcripts_by_speaker[current_speaker] = []
                                transcripts_by_speaker[current_speaker].append(" ".join(current_segment))
                                
                                current_speaker = word.speaker
                                current_segment = [word.word]
                        
                        if current_segment:
                            if current_speaker not in transcripts_by_speaker:
                                transcripts_by_speaker[current_speaker] = []
                            transcripts_by_speaker[current_speaker].append(" ".join(current_segment))
                        
                        print("\033[H\033[J", end="")  # Clear screen
                        for spk, texts in transcripts_by_speaker.items():
                            print(f"Speaker {spk + 1}: {' '.join(texts)}")
                            print()  # Add blank line between speakers
            except Exception as e:
                logger.error(f"Error in message handler: {e}")

        # Register event handlers
        print("Setting up event handlers...")
        dg_connection.on(LiveTranscriptionEvents.Transcript, on_message)

        options = LiveOptions(
            model="nova-2",
            language="en-US",
            smart_format=True,
            encoding="linear16",
            channels=1,
            sample_rate=16000,
            endpointing=500,
            interim_results=True,
            vad_events=True,
            diarize=True,
            punctuate=True,
        )

        addons = {
            "no_delay": "true",
            "low_latency": "true",
            "min_speakers": 2,
            "max_speakers": 6
        }

        print("\nStarting connection...")
        if await dg_connection.start(options, addons=addons) is False:
            print("Failed to connect to Deepgram")
            return

        print("\nInitializing microphone...")
        microphone = Microphone(dg_connection.send)

        print("\n\nReady! Start speaking (Press Ctrl+C to stop)...\n")
        microphone.start()

        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            pass
        finally:
            print("\nStopping microphone...")
            microphone.finish()
            print("Closing connection...")
            await dg_connection.finish()

    except Exception as e:
        logger.error(f"Main error: {e}")
        return

async def shutdown(signal, loop, dg_connection, microphone):
    print(f"\nReceived exit signal {signal.name}...")
    microphone.finish()
    await dg_connection.finish()
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
    [task.cancel() for task in tasks]
    print(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()
    print("Shutdown complete.")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nProgram terminated by user")
    except Exception as e:
        logger.error(f"Program error: {e}")