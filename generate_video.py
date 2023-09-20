import math
import os
import moviepy.editor as mp
import logging

import numpy
from PIL import Image


def zoom_in_effect(clip, zoom_ratio=0.04):
    def effect(get_frame, t):
        img = Image.fromarray(get_frame(t))
        base_size = img.size

        new_size = [
            math.ceil(img.size[0] * (1 + (zoom_ratio * t))),
            math.ceil(img.size[1] * (1 + (zoom_ratio * t)))
        ]

        # The new dimensions must be even.
        new_size[0] = new_size[0] + (new_size[0] % 2)
        new_size[1] = new_size[1] + (new_size[1] % 2)

        img = img.resize(new_size, Image.LANCZOS)

        x = math.ceil((new_size[0] - base_size[0]) / 2)
        y = math.ceil((new_size[1] - base_size[1]) / 2)

        img = img.crop([
            x, y, new_size[0] - x, new_size[1] - y
        ]).resize(base_size, Image.LANCZOS)

        result = numpy.array(img)
        img.close()

        return result

    return clip.fl(effect)

size = (1920, 1080)

def edit_video_with_voiceover(voiceover_path, image_folder):
    # Set up logging
    logging.basicConfig(filename='video_edit_log.txt', level=logging.INFO)

    try:
        # Find voice_over.mp3 in the assets folder
        # voiceover_path = 'assets/voice_over.mp3'
        output_path = 'assets/generated_video.mp4'
        if os.path.exists(output_path):
            return output_path

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

        N = 3
        # Calculate time for each image
        time_per_image = voiceover_duration / total_images
        time_per_image = time_per_image/N
        # Create clips for each image
        video_clips = []
        for i in range(1, N+1):
            for image_file in image_files:
                image_path = os.path.join(image_folder, image_file)
                image_clip = mp.ImageClip(image_path, duration=time_per_image).resize(size)

                # adding zoom
                image_clip = zoom_in_effect(image_clip, zoom_ratio=0.04)

                video_clips.append(image_clip)

        # Add transition
        # transitioned_clips = [demo_clip.crossfadein(2) for demo_clip in video_clips]

        # Concatenate the clips into one video
        final_video = mp.concatenate_videoclips(video_clips, method="compose")

        # Set the audio to the voiceover
        final_video = final_video.set_audio(voiceover_clip)

        # Save the final video
        output_path = 'assets/generated_video.mp4'
        final_video.write_videofile(output_path, codec='libx264',fps=24 )

        logging.info("Video editing completed successfully.")
        return output_path

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        print(f"Error: {str(e)}")
        return None

if __name__ == "__main__":
    voiceover_path = 'assets/voice_over.mp3'
    image_folder = 'Scrapped_Images'
    edit_video_with_voiceover(voiceover_path=voiceover_path,image_folder=image_folder)