from typing import Optional
from langgraph.graph import StateGraph, START, END
from agents.research_agent import VideoProductionState, research_agent
from agents.script_agent import script_agent
from agents.images_agent import images_agent
from agents.audio_agent import audio_agent
from agents.music_agent import music_agent
from agents.video_agent import video_agent
from agents.upload_agent import upload_agent
from database.db_manager import DatabaseManager
from utils.config import Config

def create_video_workflow():
    workflow = StateGraph(VideoProductionState)
    
    workflow.add_node("research", research_agent)
    workflow.add_node("script", script_agent)
    workflow.add_node("images", images_agent)
    workflow.add_node("audio", audio_agent)
    workflow.add_node("music", music_agent)
    workflow.add_node("video", video_agent)
    workflow.add_node("upload", upload_agent)
    
    workflow.add_edge(START, "research")
    workflow.add_edge("research", "script")
    workflow.add_edge("script", "images")
    workflow.add_edge("images", "audio")
    workflow.add_edge("audio", "music")
    workflow.add_edge("music", "video")
    workflow.add_edge("video", "upload")
    workflow.add_edge("upload", END)
    
    return workflow.compile()

def run_video_production(topic: Optional[str] = None):
    Config.ensure_dirs()
    
    db = DatabaseManager()
    
    app = create_video_workflow()
    
    initial_state = VideoProductionState(
        topic=topic,
        status="starting"
    )
    
    if topic:
        video_id = db.create_video(topic)
    else:
        topic = "Auto-generated"
        video_id = db.create_video(topic)
    
    initial_state['video_id'] = video_id
    
    try:
        db.add_log(video_id, "workflow", "started", f"Starting production for topic: {topic or 'auto-generated'}")
        
        result = app.invoke(initial_state)
        
        final_topic = result.get('topic', topic)
        
        if not topic:
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
