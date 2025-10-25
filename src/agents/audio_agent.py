from openai import OpenAI
import os
from src.pipeline.state import VideoProductionState
from src.config import Config
from src.utils.helpers import clean_filename

def audio_agent(state: VideoProductionState) -> dict:
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    
    script = state.get('script', '')
    topic = state.get('topic') or 'untitled'
    
    topic_clean = clean_filename(topic)
    audio_path = os.path.join(Config.AUDIO_DIR, f"{topic_clean}_narration.mp3")
    
    response = client.audio.speech.create(
        model=Config.OPENAI_TTS_MODEL,
        voice=Config.OPENAI_TTS_VOICE,
        input=script,
        response_format="mp3"
    )
    
    response.stream_to_file(audio_path)
    
    return {"audio_path": audio_path}
