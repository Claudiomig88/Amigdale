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
├── src/                        # Codice sorgente principale
│   ├── agents/                 # 7 agenti specializzati
│   ├── pipeline/               # LangGraph orchestration (graph, state, executor)
│   ├── database/               # PostgreSQL repository
│   ├── utils/                  # Helper functions
│   ├── services/               # API client wrappers (futuro)
│   ├── video/                  # Video processing modules (futuro)
│   ├── topics/                 # Topic management (futuro)
│   ├── scheduler/              # Job scheduling (futuro)
│   ├── notifications/          # Alert system (futuro)
│   └── config.py               # Configurazione centralizzata
├── data/                       # File generati (gitignored)
│   ├── videos/                 # Video finali MP4
│   ├── audio/                  # Narrazione + musica MP3
│   ├── images/                 # Frame generati
│   ├── temp/                   # File temporanei
│   └── cache/                  # Cache API responses
├── docs/                       # Documentazione completa
│   ├── SETUP.md                # Guida setup
│   ├── API_KEYS.md             # Come ottenere API keys
│   └── ARCHITECTURE.md         # Architettura sistema
├── logs/                       # Application logs
├── assets/                     # Static files
├── tests/                      # Test suite
├── scripts/                    # Utility scripts
├── main.py                     # Entry point CLI
├── .env.example                # Template environment variables
└── README.md                   # Project documentation
```

## Recent Changes
- **2025-10-25 16:00**: Ristrutturazione completa a src/-based architecture
  - Migrati tutti i moduli in src/ per migliore organizzazione
  - Separato pipeline in graph.py, state.py, executor.py
  - Rinominato DatabaseManager → DatabaseRepository
  - Creata documentazione completa in docs/
  - Risolto bug topic auto-generation nel executor
  - Configurato workflow Video Production Bot
  - Rimossa dashboard Flask (non più necessaria)
- **2025-10-25 14:00**: Progetto inizializzato con struttura base e dipendenze

## API Keys Necessarie
- `ANTHROPIC_API_KEY`: Per Claude Sonnet 4 (script e topic generation)
- `OPENAI_API_KEY`: Per TTS-1-HD (sintesi vocale italiana)
- `LEONARDO_API_KEY`: Per generazione immagini
- `MUBERT_CUSTOMER_ID` e `MUBERT_ACCESS_TOKEN`: Per musica di sottofondo
- YouTube OAuth configurato tramite Replit connector

## Configurazione

### Quick Start
1. **Configura API Keys** (vedi `docs/API_KEYS.md`)
   - ANTHROPIC_API_KEY
   - OPENAI_API_KEY  
   - LEONARDO_API_KEY
   - MUBERT_CUSTOMER_ID + MUBERT_ACCESS_TOKEN
   
2. **Setup YouTube OAuth**
   - Scarica `credentials.json` da Google Cloud Console
   - Metti nella root: `/home/runner/workspace/credentials.json`
   
3. **Carica Style Reference** (opzionale)
   - Carica un'immagine in `assets/style_reference.jpg`
   - Leonardo.ai la userà per consistenza stile

### Utilizzo

**CLI - Topic Automatico:**
```bash
python main.py
```

**CLI - Topic Specifico:**
```bash
python main.py "Battaglia di Waterloo"
```

## Workflow LangGraph
Flusso sequenziale:
```
START → research_step → script_step → images_step → 
audio_step → music_step → video_step → upload_step → END
```

Ogni step aggiorna `VideoProductionState` con output dell'agente.

## Database PostgreSQL
Tabelle automatiche:
- `topics`: Topic usati per evitare duplicati
- `videos`: Metadata video pubblicati + costi
- `production_logs`: Log dettagliato esecuzione pipeline
