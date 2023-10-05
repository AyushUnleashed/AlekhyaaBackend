import streamlit as st
import logging
import os
from scrap_press_release import scrape_web_page
from text_to_script import get_clean_text_for_t2s
from google_t2s import text_to_speech
from generate_video import edit_video_with_voiceover

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
        voice_file = text_to_speech(cleaned_voiceover, speed=1.25)

        st.text("Editing video with voiceover...")
        image_folder = 'Scrapped_Images'
        video_path = edit_video_with_voiceover(voice_file, image_folder)

        st.success("Video has been saved!")
        return video_path

    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None
import shutil

def delete_cache():
    # Define the folders to delete
    folders_to_delete = ["assets", "Scrapped_Images"]

    # Loop through the folders and delete them along with their contents
    for folder_name in folders_to_delete:
        if os.path.exists(folder_name):
            shutil.rmtree(folder_name)
            st.text(f"Deleted folder: {folder_name}")

def main():
    st.title("Alekhyaa ")
    st.text("Automated video generation")

    url_to_scrape = st.text_input("Enter press release URL:")

    if st.button("Generate Video"):
        st.text("Generating video, please wait...")
        video_path = text_to_video(url_to_scrape)

        from upload_to_drive import auth_drive, upload_video_to_drive
        gauth = auth_drive()  # Authenticate with Google Drive
        video_link = upload_video_to_drive(gauth, video_path)

        # Display the generated video link
        st.write("Generated Video Link:", video_link)

    if st.button("Delete Cache"):
        delete_cache()

if __name__ == "__main__":
    main()