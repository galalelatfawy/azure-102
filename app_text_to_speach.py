import azure.cognitiveservices.speech as speechsdk
from dotenv import load_dotenv
import os
import sys
from datetime import datetime

load_dotenv()

# Get environment variables
speech_key = os.getenv("AZURE_SPEECH_KEY")
region = os.getenv("AZURE_SPEECH_REGION", "eastus")
endpoint = os.getenv("AZURE_SPEECH_ENDPOINT")

# Validate environment variables
if not speech_key or not endpoint:
    print("Error: Missing required environment variables!")
    print("Please set the following in your .env file:")
    print("  AZURE_SPEECH_KEY=your_speech_key_here")
    print("  AZURE_SPEECH_ENDPOINT=your_speech_endpoint_here")
    exit(1)

# Get text file from command line argument or use default
translate_dir = os.path.join(os.path.dirname(__file__), "translate")

if len(sys.argv) > 1:
    # User provided a filename
    filename = sys.argv[1]
    # If it's just a filename, look in translate directory
    if not os.path.dirname(filename):
        text_file = os.path.join(translate_dir, filename)
    else:
        # Full path provided
        text_file = filename
else:
    # Default to text.txt in translate directory
    text_file = os.path.join(translate_dir, "text.txt")

# Check if text file exists
if not os.path.exists(text_file):
    print(f"Error: Text file not found: {text_file}")
    print(f"\nUsage: {sys.argv[0]} [filename]")
    print(f"  filename: Name of file in translate/ directory (default: text.txt)")
    print(f"\nAvailable files in translate/ directory:")
    if os.path.exists(translate_dir):
        files = [f for f in os.listdir(translate_dir) if os.path.isfile(os.path.join(translate_dir, f))]
        for f in files:
            print(f"  - {f}")
    exit(1)

speech_config = speechsdk.SpeechConfig(subscription=speech_key, endpoint=endpoint)

# Configure audio output to save to a file
# Use timestamp to create unique filenames
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_file = f"output_audio_{timestamp}.wav"
audio_config = speechsdk.audio.AudioOutputConfig(filename=output_file)


# The neural multilingual voice can speak different languages based on the input text.
speech_config.speech_synthesis_voice_name='en-US-Ava:DragonHDLatestNeural'

speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)

# Read text from file
print(f"Reading text from: {text_file}")
with open(text_file, "r", encoding="utf-8") as f:
    text = f.read().strip()

if not text:
    print(f"Error: Text file is empty: {text_file}")
    exit(1)

speech_synthesis_result = speech_synthesizer.speak_text_async(text).get()

if speech_synthesis_result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
    print("Speech synthesized for text [{}]".format(text))
    print("Audio saved to: {}".format(output_file))
elif speech_synthesis_result.reason == speechsdk.ResultReason.Canceled:
    cancellation_details = speech_synthesis_result.cancellation_details
    print("Speech synthesis canceled: {}".format(cancellation_details.reason))
    if cancellation_details.reason == speechsdk.CancellationReason.Error:
        if cancellation_details.error_details:
            print("Error details: {}".format(cancellation_details.error_details))
            print("Did you set the speech resource key and endpoint values?")