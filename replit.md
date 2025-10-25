# Sistema Multi-Agente per Produzione Video YouTube Automatizzata

## Overview
Sistema automatizzato per la creazione e pubblicazione di video educativi storici su YouTube in italiano. Utilizza LangGraph per orchestrare 7 agenti specializzati che gestiscono l'intero processo di produzione video.

**Budget per video**: €1.35
- Leonardo.ai (immagini): €1.10
- OpenAI TTS-1-HD: €0.14
- Mubert (musica): €0.10
- Claude Sonnet 4: €0.01

## Architettura

### Stack Tecnologico
- **Framework Multi-Agente**: LangGraph
- **LLM**: Claude Sonnet 4 (Anthropic)
- **Text-to-Speech**: OpenAI TTS-1-HD (voce Nova italiana)
- **Generazione Immagini**: Leonardo.ai con Character Reference
- **Musica**: Mubert API
- **Video Editing**: MoviePy + FFmpeg
- **Database**: PostgreSQL (tracking topic duplicati)
- **Upload**: YouTube Data API v3
- **Dashboard**: Flask

### 7 Agenti del Sistema
1. **Research Agent**: Genera topic storici con Claude + ricerca Wikipedia
2. **Script Agent**: Crea script educativo italiano (600-800 parole)
3. **Images Agent**: Genera 20-30 immagini con Leonardo.ai + Character Reference
4. **Audio Agent**: Sintesi vocale italiana con OpenAI TTS-1-HD
5. **Music Agent**: Genera musica di sottofondo con Mubert
6. **Video Agent**: Assembla video con MoviePy (Ken Burns effect, transizioni)
7. **Upload Agent**: Pubblica su YouTube con metadata ottimizzati

## Struttura Progetto
```
/
├── agents/
│   ├── research_agent.py
│   ├── script_agent.py
│   ├── images_agent.py
│   ├── audio_agent.py
│   ├── music_agent.py
│   ├── video_agent.py
│   └── upload_agent.py
├── workflow/
│   └── langgraph_workflow.py
├── database/
│   └── db_manager.py
├── dashboard/
│   └── app.py
├── utils/
│   ├── config.py
│   └── helpers.py
├── data/
│   ├── videos/
│   ├── audio/
│   └── images/
├── main.py
└── requirements.txt
```

## Recent Changes
- **2025-10-25**: Progetto inizializzato con struttura base e dipendenze

## API Keys Necessarie
- `ANTHROPIC_API_KEY`: Per Claude Sonnet 4 (script e topic generation)
- `OPENAI_API_KEY`: Per TTS-1-HD (sintesi vocale italiana)
- `LEONARDO_API_KEY`: Per generazione immagini
- `MUBERT_CUSTOMER_ID` e `MUBERT_ACCESS_TOKEN`: Per musica di sottofondo
- YouTube OAuth configurato tramite Replit connector

## Configurazione
1. Caricare immagine Character Reference in `data/style_reference_image.jpg`
2. Configurare YouTube OAuth tramite dashboard Replit
3. Impostare tutte le API keys come secrets

## Funzionalità Dashboard
- Visualizzazione stato pipeline in tempo reale
- Lista video pubblicati con link YouTube
- Tracking costi per video
- Log errori e debugging
- Statistiche produzione (video/giorno, topic usati)
