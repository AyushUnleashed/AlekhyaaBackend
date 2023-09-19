import os
from gtts import gTTS
import logging

# Configure the logging settings
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def text_to_speech(text):
    # Create a gTTS object
    tts = gTTS(text)

    # Define the path for the assets folder and the output file name
    assets_folder = "assets"
    output_file = os.path.join(assets_folder, "voice_over.mp3")

    # Create the assets folder if it doesn't exist
    if not os.path.exists(assets_folder):
        os.makedirs(assets_folder)

    # Log a loading message
    logging.info("Loading...")

    # Save the generated audio to the specified file
    tts.save(output_file)

    # Log a message when the audio is saved
    logging.info(f"Audio saved to {output_file}")
    return output_file

def main():
    text = "Hello, this is a test. This text will be converted to audio."
    text_to_speech(text)

if __name__ == "__main__":
    main()