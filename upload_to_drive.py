from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
import os
import sys

def auth_drive():
    # Google Authentication
    gauth = GoogleAuth()
    gauth.LoadCredentialsFile("mycreds.txt")
    # You would load credentials from your JSON file like this
    if gauth.credentials is None:
        # Authenticate if they're not there
        gauth.LocalWebserverAuth()
    elif gauth.access_token_expired:
        # Refresh them if expired
        gauth.Refresh()
    else:
        # Initialize the saved creds
        gauth.Authorize()
    # Save the current credentials to a file
    gauth.SaveCredentialsFile("mycreds.txt")
    return gauth

# Function to create or find the "data" folder
def find_or_create_data_folder(drive):
    # Search for the "data" folder in the root of Google Drive
    query = "title='data' and mimeType='application/vnd.google-apps.folder' and trashed=false"
    folder_list = drive.ListFile({'q': query}).GetList()

    if folder_list:
        return folder_list[0]['id']
    else:
        # If the "data" folder doesn't exist, create it
        data_folder = drive.CreateFile({'title': 'assets', 'mimeType': 'application/vnd.google-apps.folder'})
        data_folder.Upload()
        return data_folder['id']
def upload_video_to_drive(gauth, video_path):
    drive = GoogleDrive(gauth)
    try:
        # Get the filename from the video path
        filename = os.path.basename(video_path)

        # Find or create the "data" folder
        data_folder_id = find_or_create_data_folder(drive)

        # Check if the video file exists
        if not os.path.exists(video_path):
            print(f"Error: Video file not found at {video_path}")
            return None  # Return None if the file is not found

        # Before upload, query if the file already exists in the "data" folder on Drive
        exist_query = f"title='{filename}' and '{data_folder_id}' in parents and trashed=false"
        exist_file = drive.ListFile({'q': exist_query}).GetList()

        # If the file already exists, then skip the upload
        if exist_file:
            for file in exist_file:
                print(f"Skipping upload of file: {file['title']}")
                return "https://drive.google.com/file/d/{}/view".format(file['id'])

        # Define a callback function to show the upload progress
        def print_progress(status, remaining, total):
            progress = (total - remaining) / total
            bar_length = 50
            progress_bar = "[" + "=" * int(bar_length * progress) + "-" * (bar_length - int(bar_length * progress)) + "]"
            sys.stdout.write(f"\rUploading: {progress_bar} {int(progress * 100)}%")
            sys.stdout.flush()

        # Upload the new video file to the "data" folder with the progress callback
        file1 = drive.CreateFile({"title": filename, "parents": [{"id": data_folder_id}]})
        file1.SetContentFile(video_path)
        file1.Upload()

        print(f"\nVideo file: {filename} uploaded to Google Drive in the 'data' folder")

        # Return the link to the uploaded file
        return "https://drive.google.com/file/d/{}/view".format(file1['id'])

    except Exception as e:
        print(e)
        return None  # Return None if there's an error during the upload

# Example usage:
def main():
    gauth = auth_drive()  # Authenticate with Google Drive
    video_path = "assets/generated_video.mp4"  # Replace with the path to your video file
    video_link = upload_video_to_drive(gauth, video_path)
    if video_link:
        print(f"Video Link: {video_link}")

if __name__ == "__main__":
    main()