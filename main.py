
import logging
import os
from scrap_press_release import scrape_web_page
from text_to_script import get_clean_text_for_t2s
from google_t2s import text_to_speech
from generate_video import edit_video_with_voiceover

# Set up logging
logging.basicConfig(level=logging.INFO)

from fastapi import APIRouter

endpoint_router = APIRouter()


STATUS = "NO_STATUS"

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
        update_status("Scraping press release web page...")
        print("Scraping press release web page...")
        scrape_web_page(url_to_scrape)

        print("Extracting and cleaning text...")
        update_status("Extracting and cleaning text...")

        file_path = 'assets/webpage_text.txt'  # Replace with the path to your text file
        cleaned_voiceover = get_clean_text_for_t2s(file_path)

        update_status("Generating voiceover...")
        print("Generating voiceover...")
        cleaned_voiceover = read_voice_over_text()
        voice_file = text_to_speech(cleaned_voiceover, speed=1.25)

        update_status("Editing video with voiceover...")
        print("Editing video with voiceover...")
        image_folder = 'Scrapped_Images'
        video_path = edit_video_with_voiceover(voice_file, image_folder)

        update_status("Video has been saved!")
        print("Video has been saved!")

        return video_path

    except Exception as e:
        print(f"Error: {str(e)}")
        return None


def main(url_to_scrape):
    video_path = text_to_video(url_to_scrape)
    from upload_to_drive import auth_drive, upload_video_to_drive
    gauth = auth_drive()  # Authenticate with Google Drive
    video_link = upload_video_to_drive(gauth, video_path)
    response = {"video_id": 1, "generated_video_url": video_link}
    return response


from fastapi import HTTPException

from pydantic import BaseModel
class PressRelease(BaseModel):
    pressReleaseLink: str


@endpoint_router.get("/get_status")
def get_status():
    return STATUS

def update_status(status: str):
    global STATUS
    STATUS = status

@endpoint_router.post("/generate_video")
def generate_video(pressReleaseLink: PressRelease):
    try:
        response = main(pressReleaseLink.pressReleaseLink)
        update_status("FINISHED")
        return response
    except Exception as e:
        # Handle the exception and return a 500 status code
        error_message = f"An error occurred: {str(e)}"
        error_response = {"error": error_message, "status": 500}
        update_status("NO_STATUS")
        # return error_response  # Return the error response with 500 status code
        raise HTTPException(status_code=500, detail=error_message)


if __name__ == "__main__":
    url_to_scrape = "https://pib.gov.in/PressReleasePage.aspx?PRID=1958748"
    main(url_to_scrape)
