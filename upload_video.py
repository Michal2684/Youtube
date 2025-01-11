import os
import requests
import google.auth
import google.auth.transport.requests
import google.oauth2.credentials
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload

def main():
    # 1. Get secrets from environment variables
    client_id = os.environ["YOUTUBE_CLIENT_ID"]
    client_secret = os.environ["YOUTUBE_CLIENT_SECRET"]
    refresh_token = os.environ["YOUTUBE_REFRESH_TOKEN"]
    video_url = os.environ.get("VIDEO_URL")  # If you have a direct URL
    video_path = "I_am_nobodys_master.mp4"       # Where we'll temporarily store it

    # 2. Download the video file (if needed). 
    #    Alternatively, if your repo includes the video file, skip this step.

    """
    if video_url:
        print("Downloading video from:", video_url)
        response = requests.get(video_url)
        with open(video_path, "wb") as f:
            f.write(response.content)
    else:
        print("Using local file:", video_path)
        """

    # 3. Build credentials object manually using refresh token
    creds_data = {
        "token": None,  # Access token (will be obtained via refresh token)
        "refresh_token": refresh_token,
        "token_uri": "https://oauth2.googleapis.com/token",
        "client_id": client_id,
        "client_secret": client_secret,
        "scopes": ["https://www.googleapis.com/auth/youtube.upload"]
    }
    creds = google.oauth2.credentials.Credentials(**creds_data)

    # 4. Refresh the token if needed
    request = google.auth.transport.requests.Request()
    creds.refresh(request)

    # 5. Build the YouTube service
    youtube = googleapiclient.discovery.build(
        "youtube", "v3", credentials=creds
    )

    # 6. Define request body (metadata)
    request_body = {
        "snippet": {
            "title": "I am no nobody's master got it! #shorts #animated #memes #bird #birdie",
            "description": "#Shorts #comedy #memes #funny #bird #up #daily #dog #fyp #animated #kids #movie #cartoons #viral #cute #cool #joke #friends #birdie #goofy #clips #scene #wow",
            "tags": ["Shorts", "comedy", "memes", "funny"],
            "categoryId": "23"  # "People & Blogs" as an example
        },
        "status": {
            "privacyStatus": "public"  # or "public", "private"
        }
    }

    # 7. Upload
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    request_upload = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = None
    while response is None:
        status, response = request_upload.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
        if response is not None:
            print("Upload completed!")
            print("Video ID:", response.get("id"))

if __name__ == "__main__":
    main()
