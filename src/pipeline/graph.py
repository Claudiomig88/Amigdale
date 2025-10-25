from langgraph.graph import StateGraph, START, END
from src.pipeline.state import VideoProductionState
from src.agents.research_agent import research_agent
from src.agents.script_agent import script_agent
from src.agents.images_agent import images_agent
from src.agents.audio_agent import audio_agent
from src.agents.music_agent import music_agent
from src.agents.video_agent import video_agent
from src.agents.upload_agent import upload_agent

def create_video_workflow():
    workflow = StateGraph(VideoProductionState)
    
    workflow.add_node("research_step", research_agent)
    workflow.add_node("script_step", script_agent)
    workflow.add_node("images_step", images_agent)
    workflow.add_node("audio_step", audio_agent)
    workflow.add_node("music_step", music_agent)
    workflow.add_node("video_step", video_agent)
    workflow.add_node("upload_step", upload_agent)
    
    workflow.add_edge(START, "research_step")
    workflow.add_edge("research_step", "script_step")
    workflow.add_edge("script_step", "images_step")
    workflow.add_edge("images_step", "audio_step")
    workflow.add_edge("audio_step", "music_step")
    workflow.add_edge("music_step", "video_step")
    workflow.add_edge("video_step", "upload_step")
    workflow.add_edge("upload_step", END)
    
    return workflow.compile()
