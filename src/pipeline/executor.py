from typing import Optional
from src.pipeline.graph import create_video_workflow
from src.pipeline.state import VideoProductionState
from src.database.repository import DatabaseRepository
from src.config import Config

def run_video_production(topic: Optional[str] = None):
    Config.ensure_dirs()
    
    db = DatabaseRepository()
    
    app = create_video_workflow()
    
    input_topic = topic
    
    initial_state = VideoProductionState(
        topic=topic,
        status="starting"
    )
    
    if topic:
        video_id = db.create_video(topic)
    else:
        video_id = db.create_video("Auto-generated")
    
    initial_state['video_id'] = video_id
    
    try:
        db.add_log(video_id, "workflow", "started", f"Starting production for topic: {topic or 'auto-generated'}")
        
        result = app.invoke(initial_state)
        
        final_topic = result.get('topic', topic)
        
        if input_topic is None:
            db.update_video(video_id, topic_name=final_topic)
        
        db.mark_topic_used(final_topic)
        
        total_cost = sum([
            Config.COSTS['images'],
            Config.COSTS['audio'],
            Config.COSTS['music'],
            Config.COSTS['script']
        ])
        
        db.update_video(
            video_id,
            youtube_id=result.get('youtube_id'),
            youtube_url=result.get('youtube_url'),
            script=result.get('script'),
            status='published',
            cost_images=Config.COSTS['images'],
            cost_audio=Config.COSTS['audio'],
            cost_music=Config.COSTS['music'],
            cost_script=Config.COSTS['script'],
            total_cost=total_cost
        )
        
        db.add_log(video_id, "workflow", "completed", f"Video published: {result.get('youtube_url')}")
        
        return result
        
    except Exception as e:
        db.update_video(
            video_id,
            status='error',
            error_message=str(e)
        )
        db.add_log(video_id, "workflow", "error", str(e))
        raise
