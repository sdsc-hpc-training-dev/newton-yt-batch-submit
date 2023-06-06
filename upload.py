from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from json import load
import argparse
import os

# You will have to setup your own API_KEY and other credentials
API_KEY = load(open("creds.json", 'r'))['youtubeAPI']
YOUTUBE_UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

def upload_to_youtube(video_path, title, description):
    try:
        youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=API_KEY)

        # Create the MediaFileUpload object for the video
        media = MediaFileUpload(video_path, chunksize=-1, resumable=True)

        # Create the video on YouTube
        video = youtube.videos().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": title,
                    "description": description,
                },
                "status": {
                    "privacyStatus": "private",
                },
            },
            media_body=media,
        ).execute()

        print(f'Uploaded video: {video["id"]}')

    except HttpError as e:
        print(f'An error occurred: {e}')
        return False
    return True

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # Args
    parser.add_argument("--path", help="Path to video")
    parser.add_argument("--title", help="Title of YT Video")
    parser.add_argument("--description", help="Description of YT Video")
    args = parser.parse_args()

    video_path = args.path
    title = args.title
    description = args.description
    
    upload_to_youtube(video_path, title, description)