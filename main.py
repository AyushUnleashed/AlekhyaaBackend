import streamlit as st
import logging
import os
from scrap_press_release import scrape_web_page
from text_to_script import get_clean_text_for_t2s
from google_t2s import text_to_speech
from generate_video import edit_video_with_voiceover

# Set up logging
logging.basicConfig(level=logging.INFO)

def read_voice_over_text():
    try:
        # Open and read the text file
        file_path = 'assets/cleaned_voiceover.txt'

        if not os.path.exists(file_path):
            raise FileNotFoundError("The file 'voice_over.txt' was not found.")

        with open(file_path, 'r') as file:
            voice_over_text = file.read()

        logging.info("Successfully read the voice over text.")

        return voice_over_text

    except Exception as e:
        logging.error(f"Error while reading the voice over text: {str(e)}")
        raise e

def text_to_video(url_to_scrape):
    try:
        st.text("Scraping press release web page...")
        scrape_web_page(url_to_scrape)

        st.text("Extracting and cleaning text...")
        file_path = 'assets/webpage_text.txt'  # Replace with the path to your text file
        cleaned_voiceover = get_clean_text_for_t2s(file_path)

        st.text("Generating voiceover...")
        cleaned_voiceover = read_voice_over_text()
        voice_file = text_to_speech(cleaned_voiceover)

        st.text("Editing video with voiceover...")
        image_folder = 'Scrapped_Images'
        edit_video_with_voiceover(voice_file, image_folder)

        st.success("Video has been saved!")

    except Exception as e:
        st.error(f"Error: {str(e)}")

def main():
    st.title("Alekhyaa ")
    st.text("Automated video generation")

    url_to_scrape = st.text_input("Enter press release URL:")

    if st.button("Generate Video"):
        st.text("Generating video, please wait...")
        text_to_video(url_to_scrape)

if __name__ == "__main__":
    main()