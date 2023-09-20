import os
from gtts import gTTS
import logging

# Configure the logging settings
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def text_to_speech(text, speed=1.25):  # Adjust the speed value as needed
    # Create a gTTS object with the specified speed
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

    from pydub import AudioSegment

    audio = AudioSegment.from_file("assets/voice_over.mp3", format="mp3")
    # # or
    # audio = AudioSegment.from_mp3("test.mp3")

    final = audio.speedup(playback_speed=speed)  # speed up by 2x

    # Export the sped-up audio to a new file
    output_speed_file = f"assets/voice_over_{speed}.mp3"
    final.export(output_speed_file, format="mp3")

    return output_speed_file


def main():
    text = "Hello, this is a test. This text will be converted to audio."
    text_to_speech(text, speed=2.0)


if __name__ == "__main__":
    main()
