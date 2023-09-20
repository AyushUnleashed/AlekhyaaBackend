from gradio_client import Client

def sad_talker(image_url, audio_url):
    try:
        client = Client("https://kevinwang676-sadtalker.hf.space/")
        result = client.predict(
            "https://raw.githubusercontent.com/gradio-app/gradio/main/test/test_files/bus.png",	# str (filepath or URL to image) in 'Source image' Image component
            "https://github.com/gradio-app/gradio/raw/main/test/test_files/audio_sample.wav",	#
            "crop",
            True,
            True,
            0,
            "256",
            0,
            fn_index=0
        )
        print(result)
        # Save the result to a file
        with open("assets/sadtalker_inference.txt", "w") as file:
            file.write(result)

        print("Inference result saved successfully.")
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    # Take user input for image and audio URLs
    image_url = "assets/grace.png"
    audio_url = "assets/voice_over_1.25.mp3"

    # Call the sad_talker function with user-provided inputs
    sad_talker(image_url, audio_url)