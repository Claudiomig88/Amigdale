from moviepy.editor import (
    ImageClip, AudioFileClip,
    concatenate_videoclips, CompositeAudioClip
)
import os
from src.pipeline.state import VideoProductionState
from src.config import Config
from src.utils.helpers import clean_filename

def video_agent(state: VideoProductionState) -> dict:
    images = state.get('images', [])
    audio_path = state.get('audio_path', '')
    music_path = state.get('music_path', '')
    topic = state.get('topic') or 'untitled'

    if not images:
        raise ValueError("No images provided for video creation")

    audio = AudioFileClip(audio_path)
    total_duration = audio.duration

    duration_per_image = total_duration / len(images)
    
    clips = []
    for img_path in images:
        clip = create_ken_burns_clip(img_path, duration_per_image)
        clips.append(clip)
    
    video = concatenate_videoclips(clips, method="compose")
    
    music = AudioFileClip(music_path)
    music = music.fx(lambda clip: clip.multiply_volume(0.15)).audio_fadeout(2)
    music = music.set_duration(total_duration)
    
    final_audio = CompositeAudioClip([
        audio,
        music
    ])
    
    video = video.set_audio(final_audio)
    
    topic_clean = clean_filename(topic)
    output_path = os.path.join(Config.VIDEOS_DIR, f"{topic_clean}.mp4")
    
    video.write_videofile(
        output_path,
        fps=Config.VIDEO_FPS,
        codec='libx264',
        audio_codec='aac',
        preset='medium',
        bitrate=Config.VIDEO_BITRATE,
        audio_bitrate=Config.VIDEO_AUDIO_BITRATE,
        threads=4,
        logger=None
    )
    
    # Cleanup resources
    audio.close()
    music.close()
    final_audio.close()
    for clip in clips:
        clip.close()
    video.close()

    return {"video_path": output_path, "status": "video_ready"}

def create_ken_burns_clip(image_path: str, duration: float) -> ImageClip:
    clip = ImageClip(image_path).set_duration(duration)

    w, h = clip.size
    zoom_factor = 1.2

    def zoom_in_effect(get_frame, t):
        progress = t / duration if duration > 0 else 0
        current_zoom = 1 + (zoom_factor - 1) * progress

        new_w = int(w * current_zoom)
        new_h = int(h * current_zoom)

        resized_clip = clip.resize((new_w, new_h))
        return resized_clip.get_frame(t)

    zoomed_clip = clip.fl(zoom_in_effect)

    zoomed_clip = zoomed_clip.resize(height=720)

    zoomed_clip = zoomed_clip.crossfadein(0.5).crossfadeout(0.5)

    return zoomed_clip
