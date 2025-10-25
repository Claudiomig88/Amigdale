import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    LEONARDO_API_KEY = os.getenv('LEONARDO_API_KEY')
    MUBERT_CUSTOMER_ID = os.getenv('MUBERT_CUSTOMER_ID')
    MUBERT_ACCESS_TOKEN = os.getenv('MUBERT_ACCESS_TOKEN')
    DATABASE_URL = os.getenv('DATABASE_URL')
    
    CLAUDE_MODEL = "claude-3-5-sonnet-20241022"
    
    LEONARDO_MODEL_ID = "aa77f04e-3eec-4034-9c07-d0f619684628"
    
    OPENAI_TTS_MODEL = "tts-1-hd"
    OPENAI_TTS_VOICE = "nova"
    
    MUBERT_DURATION = 300
    
    VIDEO_FPS = 24
    VIDEO_BITRATE = "5000k"
    VIDEO_AUDIO_BITRATE = "192k"
    
    COSTS = {
        'images': 1.10,
        'audio': 0.14,
        'music': 0.10,
        'script': 0.01
    }
    
    DATA_DIR = "data"
    VIDEOS_DIR = os.path.join(DATA_DIR, "videos")
    AUDIO_DIR = os.path.join(DATA_DIR, "audio")
    IMAGES_DIR = os.path.join(DATA_DIR, "images")
    TEMP_DIR = os.path.join(DATA_DIR, "temp")
    CACHE_DIR = os.path.join(DATA_DIR, "cache")
    
    LOGS_DIR = "logs"
    ASSETS_DIR = "assets"
    
    NUM_IMAGES_PER_VIDEO = 25
    
    SCRIPT_WORD_COUNT_MIN = 600
    SCRIPT_WORD_COUNT_MAX = 800
    
    @staticmethod
    def ensure_dirs():
        os.makedirs(Config.VIDEOS_DIR, exist_ok=True)
        os.makedirs(Config.AUDIO_DIR, exist_ok=True)
        os.makedirs(Config.IMAGES_DIR, exist_ok=True)
        os.makedirs(Config.TEMP_DIR, exist_ok=True)
        os.makedirs(Config.CACHE_DIR, exist_ok=True)
        os.makedirs(Config.LOGS_DIR, exist_ok=True)
        os.makedirs(Config.ASSETS_DIR, exist_ok=True)
