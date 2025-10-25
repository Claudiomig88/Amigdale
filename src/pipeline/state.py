from typing import TypedDict, Optional

class VideoProductionState(TypedDict, total=False):
    topic: Optional[str]
    research_data: dict
    script: str
    images: list
    audio_path: str
    music_path: str
    video_path: str
    youtube_id: str
    youtube_url: str
    status: str
    error: str
    video_id: int
