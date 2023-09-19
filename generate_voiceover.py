'''
The function in here takes two parameters: 
1. the voice narration artist you want to use & 
2. the script you want to get narrated

Name of shorlisted narrater : voice_id
Bella: (super sexy voice, crips and clear): EXAVITQu4vr4xnSDxMaL
Rachel: (normal fast speaking american): 21m00Tcm4TlvDq8ikWAM

'''


import os
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
import requests

app = FastAPI()

# Load environment variables from the .env file
load_dotenv()

# Get the ElevenLabs API key from sthe environment variables
elevenlabs_api_key = os.getenv("ELEVENLABS_API_KEY")

if not elevenlabs_api_key:
    raise ValueError("ELEVENLABS_API_KEY not found in .env file")

# Define the base URL for ElevenLabs API
base_url = "https://api.elevenlabs.io/v1/text-to-speech"

# @app.post("/generate-voiceover/{voice_id}")
@app.post("/generate-voiceover/EXAVITQu4vr4xnSDxMaL")
async def generate_voiceover(voice_id: str, text: str):
    # Define the API endpoint
    endpoint = f"{base_url}/{voice_id}"
    
    # Define the request headers with the API key
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": elevenlabs_api_key
    }

    # Define the request body
    request_data = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style": 0,
            "use_speaker_boost": True
        }
    }

    # Make a POST request to the ElevenLabs API
    response = requests.post(endpoint, headers=headers, json=request_data)

    if response.status_code == 200:
        # The request was successful, save the audio file to the assets folder
        audio_content = response.content
        file_name = f"assets/voiceover_{voice_id}.mp3"

        with open(file_name, "wb") as audio_file:
            audio_file.write(audio_content)

        return {"location": file_name}
    else:
        # Handle API error responses
        error_message = response.json()["detail"][0]["msg"]
        raise HTTPException(status_code=response.status_code, detail=error_message)
