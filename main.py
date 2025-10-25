#!/usr/bin/env python3
import sys
import os
from typing import Optional
from workflow.langgraph_workflow import run_video_production
from utils.config import Config

def main():
    Config.ensure_dirs()
    
    topic: Optional[str]
    if len(sys.argv) > 1:
        topic = ' '.join(sys.argv[1:])
        print(f"Starting video production for topic: {topic}")
    else:
        topic = None
        print("Starting video production with auto-generated topic")
    
    try:
        result = run_video_production(topic)
        
        print("\n" + "="*60)
        print("✅ VIDEO PRODUCTION COMPLETED!")
        print("="*60)
        print(f"Topic: {result.get('topic')}")
        print(f"YouTube URL: {result.get('youtube_url')}")
        print(f"YouTube ID: {result.get('youtube_id')}")
        print(f"Video Path: {result.get('video_path')}")
        print("="*60)
        
        return 0
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
