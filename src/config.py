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

    @staticmethod
    def validate_api_keys():
        """Validate that all required API keys are set"""
        missing_keys = []

        if not Config.ANTHROPIC_API_KEY:
            missing_keys.append("ANTHROPIC_API_KEY")
        if not Config.OPENAI_API_KEY:
            missing_keys.append("OPENAI_API_KEY")
        if not Config.LEONARDO_API_KEY:
            missing_keys.append("LEONARDO_API_KEY")
        if not Config.MUBERT_ACCESS_TOKEN:
            missing_keys.append("MUBERT_ACCESS_TOKEN")
        if not Config.DATABASE_URL:
            missing_keys.append("DATABASE_URL")

        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}\n"
                "Please set them in your .env file. See .env.example for reference."
            )

        return True
