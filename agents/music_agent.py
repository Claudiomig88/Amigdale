import requests
import os
from agents.research_agent import VideoProductionState
from utils.config import Config
from utils.helpers import download_file, clean_filename

def music_agent(state: VideoProductionState) -> dict:
    topic = state.get('topic', '')
    
    response = requests.post(
        "https://api-b2b.mubert.com/v2/RecordTrack",
        json={
            "method": "RecordTrack",
            "params": {
                "pat": Config.MUBERT_ACCESS_TOKEN,
                "duration": Config.MUBERT_DURATION,
                "tags": "calm,cinematic,documentary,ambient",
                "mode": "loop",
                "bitrate": 320
            }
        }
    )
    
    if response.status_code != 200:
        raise ValueError(f"Mubert API error: {response.text}")
    
    data = response.json()
    
    if data.get('status') != 1:
        raise ValueError(f"Mubert generation failed: {data}")
    
    download_url = data['data']['tasks'][0]['download_link']
    
    topic_clean = clean_filename(topic)
    music_path = os.path.join(Config.AUDIO_DIR, f"{topic_clean}_music.mp3")
    
    download_file(download_url, music_path)
    
    return {"music_path": music_path}
