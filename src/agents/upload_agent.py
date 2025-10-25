import pickle
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from src.pipeline.state import VideoProductionState

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def upload_agent(state: VideoProductionState) -> dict:
    video_path = state.get('video_path', '')
    topic = state.get('topic', '')
    research = state.get('research_data', {})
    script = state.get('script', '')
    
    creds = None
    
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json not found. Please download it from Google Cloud Console"
                )
            
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    youtube = build('youtube', 'v3', credentials=creds)
    
    description = f"""Scopri la storia di {topic} in questo video educativo.

{script[:500]}...

Fonti:
{research.get('url', 'N/A')}

#storia #educazione #italia #documentario"""
    
    body = {
        'snippet': {
            'title': f"Storia: {topic}",
            'description': description,
            'tags': ['storia', 'educazione', 'documentario', 'italia', topic],
            'categoryId': '27'
        },
        'status': {
            'privacyStatus': 'public',
            'selfDeclaredMadeForKids': False
        }
    }
    
    media = MediaFileUpload(video_path, chunksize=-1, resumable=True)
    
    request = youtube.videos().insert(
        part='snippet,status',
        body=body,
        media_body=media
    )
    
    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Upload progress: {int(status.progress() * 100)}%")
    
    video_id = response['id']
    youtube_url = f"https://www.youtube.com/watch?v={video_id}"
    
    return {
        "youtube_id": video_id,
        "youtube_url": youtube_url,
        "status": "published"
    }
