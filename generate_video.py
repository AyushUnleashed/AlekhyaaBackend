import os
import moviepy.editor as mp
import logging

def edit_video_with_voiceover(voiceover_path, image_folder):
    # Set up logging
    logging.basicConfig(filename='video_edit_log.txt', level=logging.INFO)

    try:
        # Find voice_over.mp3 in the assets folder
        # voiceover_path = 'assets/voice_over.mp3'

        if not os.path.exists(voiceover_path):
            raise FileNotFoundError("Voiceover file not found.")

        # Get the length of the voiceover in seconds
        voiceover_clip = mp.AudioFileClip(voiceover_path)
        voiceover_duration = voiceover_clip.duration

        # Find Scrapped_Images folder and count total images
        # image_folder = 'Scrapped_Images'

        if not os.path.exists(image_folder) or not os.path.isdir(image_folder):
            raise FileNotFoundError("Scrapped_Images folder not found.")

        image_files = [f for f in os.listdir(image_folder) if os.path.isfile(os.path.join(image_folder, f))]
        total_images = len(image_files)

        if total_images == 0:
            raise ValueError("No images found in Scrapped_Images folder.")

        # Calculate time for each image
        time_per_image = voiceover_duration / total_images

        # Create clips for each image
        video_clips = []
        for image_file in image_files:
            image_path = os.path.join(image_folder, image_file)
            image_clip = mp.ImageClip(image_path, duration=time_per_image)
            video_clips.append(image_clip)

        # Concatenate the clips into one video
        final_video = mp.concatenate_videoclips(video_clips, method="compose")

        # Set the audio to the voiceover
        final_video = final_video.set_audio(voiceover_clip)

        # Save the final video
        output_path = 'assets/generated_video.mp4'
        final_video.write_videofile(output_path, codec='libx264',fps=24 )

        logging.info("Video editing completed successfully.")

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    voiceover_path = 'assets/voice_over.mp3'
    image_folder = 'Scrapped_Images'
    edit_video_with_voiceover(voiceover_path=voiceover_path,image_folder=image_folder)