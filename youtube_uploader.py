import os
import google.auth.transport.requests
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload


def upload_video(video_path, title, description, tags):
    print("📤 Preparing YouTube upload...")

    creds = Credentials(
        None,
        refresh_token=os.environ["YOUTUBE_REFRESH_TOKEN"],
        token_uri="https://oauth2.googleapis.com/token",
        client_id=os.environ["YOUTUBE_CLIENT_ID"],
        client_secret=os.environ["YOUTUBE_CLIENT_SECRET"],
        scopes=["https://www.googleapis.com/auth/youtube.upload"],
    )

    request = google.auth.transport.requests.Request()
    creds.refresh(request)

    youtube = build("youtube", "v3", credentials=creds)

    # ✅ FIXED INDENTATION + Shorts optimization
    body = {
        "snippet": {
            "title": title + " #Shorts",
            "description": description + "\n\n#Shorts #AI #Story",
            "tags": tags + ["shorts", "ai video", "story"],
            "categoryId": "24",
        },
        "status": {
            "privacyStatus": "public",
            "selfDeclaredMadeForKids": False,
        },
    }

    media = MediaFileUpload(video_path, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media,
    )

    response = request.execute()

    print("✅ Video uploaded successfully!")
    print("🔗 Video ID:", response.get("id"))
