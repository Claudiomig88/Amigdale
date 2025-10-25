import wikipediaapi
from anthropic import Anthropic
from typing import TypedDict, Optional
import random
from utils.config import Config
from anthropic.types import TextBlock

class VideoProductionState(TypedDict, total=False):
    topic: Optional[str]
    research_data: dict
    script: str
    images: list
    audio_path: str
    music_path: str
    video_path: str
    youtube_id: str
    status: str
    error: str
    video_id: int

def research_agent(state: VideoProductionState) -> dict:
    topic = state.get('topic')
    
    if not topic:
        topic = generate_historical_topic()
        state['topic'] = topic
    
    wiki_it = wikipediaapi.Wikipedia('VideoBot/1.0 (educational@example.com)', 'it')
    page = wiki_it.page(topic)
    
    if not page.exists():
        wiki_en = wikipediaapi.Wikipedia('VideoBot/1.0 (educational@example.com)', 'en')
        page_en = wiki_en.page(topic)
        
        if page_en.exists():
            research = {
                'summary': page_en.summary[:2000],
                'title': page_en.title,
                'url': page_en.fullurl,
                'language': 'en'
            }
        else:
            raise ValueError(f"Topic '{topic}' not found on Wikipedia")
    else:
        research = {
            'summary': page.summary[:2000],
            'title': page.title,
            'url': page.fullurl,
            'language': 'it'
        }
    
    return {"research_data": research, "topic": topic}

def generate_historical_topic() -> str:
    client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    message = client.messages.create(
        model=Config.CLAUDE_MODEL,
        max_tokens=200,
        messages=[{
            "role": "user",
            "content": """Genera UN SOLO evento storico interessante e educativo adatto per un video YouTube di 5 minuti.

Criteri:
- Deve essere un evento specifico (es: "Battaglia di Waterloo", "Scoperta della penicillina")
- Non una persona (evita biografie complete)
- Sufficientemente conosciuto da essere su Wikipedia
- Interessante per un pubblico italiano
- Periodo: dall'anno 1000 d.C. ad oggi

Rispondi SOLO con il nome dell'evento, nient'altro. Esempio: "Caduta del Muro di Berlino" """
        }]
    )
    
    content_block = message.content[0]
    if isinstance(content_block, TextBlock):
        topic = content_block.text.strip().strip('"').strip("'")
    else:
        topic = str(content_block).strip().strip('"').strip("'")
    
    return topic
