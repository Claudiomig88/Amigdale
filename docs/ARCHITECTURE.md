# Architettura del Sistema

## Panoramica

Sistema multi-agente basato su **LangGraph** per la produzione automatica di video documentari storici in italiano, con pubblicazione su YouTube.

```
┌──────────────────────────────────────────────────────────┐
│                     main.py                              │
│              (Entry Point CLI)                           │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│          src/pipeline/executor.py                        │
│       (Gestione esecuzione e database)                   │
└────────────────────┬─────────────────────────────────────┘
                     │
                     ▼
┌──────────────────────────────────────────────────────────┐
│           src/pipeline/graph.py                          │
│          (LangGraph Workflow DAG)                        │
└────────────────────┬─────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        ▼                         ▼
   Sequential Flow           State Management
(research → script →      (VideoProductionState)
images → audio →
music → video →
upload)
```

---

## Moduli Principali

### 1. **Pipeline** (`src/pipeline/`)

Orchestrazione del workflow multi-agente.

#### `state.py`
```python
class VideoProductionState(TypedDict):
    topic: Optional[str]           # Topic storico
    research_data: dict             # Dati da Wikipedia
    script: str                     # Script italiano
    images: list                    # Lista path immagini
    audio_path: str                 # Path file audio
    music_path: str                 # Path file musica
    video_path: str                 # Path video finale
    youtube_id: str                 # ID video YouTube
    youtube_url: str                # URL video YouTube
    status: str                     # Stato corrente
    error: str                      # Errore se presente
    video_id: int                   # ID database
```

#### `graph.py`
Definisce il grafo di esecuzione sequenziale:
```
START → research_step → script_step → images_step → audio_step 
      → music_step → video_step → upload_step → END
```

**Nota**: I nomi dei nodi hanno suffisso `_step` per evitare conflitti con le chiavi di stato di LangGraph.

#### `executor.py`
- Inizializza database e directory
- Crea stato iniziale
- Invoca workflow LangGraph
- Gestisce errori e logging
- Salva metadata e costi

---

### 2. **Agents** (`src/agents/`)

7 agenti specializzati, ognuno con una responsabilità specifica.

#### `research_agent.py`
**Input**: `topic` (opzionale)  
**Output**: `research_data`, `topic`

- Se topic non fornito: genera con Claude
- Cerca su Wikipedia IT/EN
- Estrae summary, title, URL

#### `script_agent.py`
**Input**: `research_data`, `topic`  
**Output**: `script`

- Prompt a Claude 3.5 Sonnet
- 600-800 parole in italiano
- Struttura: intro, contesto, eventi, conseguenze, conclusione

#### `images_agent.py`
**Input**: `script`, `topic`  
**Output**: `images` (lista di 25 path)

- Analizza script per scene
- Leonardo.ai PhotoReal + Alchemy
- Character Reference per consistenza stile
- 1024x576 px (16:9 orizzontale)

#### `audio_agent.py`
**Input**: `script`, `topic`  
**Output**: `audio_path`

- OpenAI TTS-1-HD
- Voce "Nova" (italiana)
- Formato MP3

#### `music_agent.py`
**Input**: `topic`  
**Output**: `music_path`

- Mubert API
- Tag: calm, cinematic, documentary, ambient
- 300 secondi (5 minuti)
- Mode: loop, Bitrate: 320

#### `video_agent.py`
**Input**: `images`, `audio_path`, `music_path`, `topic`  
**Output**: `video_path`

- **Ken Burns Effect**: zoom + pan dinamico su ogni immagine
- MoviePy compositing
- Durata immagini = durata_audio / num_immagini
- Musica al 15% volume, fadeout finale
- Export: H.264, AAC, 24fps, 5000k bitrate

#### `upload_agent.py`
**Input**: `video_path`, `topic`, `research_data`, `script`  
**Output**: `youtube_id`, `youtube_url`

- OAuth 2.0 con refresh token
- Metadata ottimizzati (titolo, descrizione, tag)
- Categoria: Education (27)
- Privacy: public
- Upload chunked resumable

---

### 3. **Database** (`src/database/`)

#### `repository.py` (`DatabaseRepository`)

**Tabelle PostgreSQL**:

##### `topics`
```sql
id SERIAL PRIMARY KEY
topic_name VARCHAR(500) UNIQUE NOT NULL
created_at TIMESTAMP
used BOOLEAN DEFAULT FALSE
```

##### `videos`
```sql
id SERIAL PRIMARY KEY
topic_id INTEGER REFERENCES topics(id)
topic_name VARCHAR(500) NOT NULL
script TEXT
youtube_id VARCHAR(100)
youtube_url VARCHAR(500)
status VARCHAR(50) DEFAULT 'pending'
cost_images DECIMAL(10, 2)
cost_audio DECIMAL(10, 2)
cost_music DECIMAL(10, 2)
cost_script DECIMAL(10, 2)
total_cost DECIMAL(10, 2)
error_message TEXT
created_at TIMESTAMP
completed_at TIMESTAMP
```

##### `production_logs`
```sql
id SERIAL PRIMARY KEY
video_id INTEGER REFERENCES videos(id)
agent_name VARCHAR(100)
status VARCHAR(50)
message TEXT
created_at TIMESTAMP
```

**Metodi principali**:
- `create_video(topic)` → video_id
- `update_video(video_id, **kwargs)`
- `add_log(video_id, agent, status, message)`
- `mark_topic_used(topic)`
- `get_all_videos()` → lista video
- `get_statistics()` → metriche aggregate

---

### 4. **Configuration** (`src/config.py`)

Gestione centralizzata di:
- API keys (Anthropic, OpenAI, Leonardo, Mubert, YouTube)
- Model IDs e parametri
- Directory paths
- Costi per servizio
- Parametri video (FPS, bitrate, numero immagini)

**Metodo chiave**: `Config.ensure_dirs()` - crea data/, logs/, assets/

---

### 5. **Utils** (`src/utils/`)

#### `helpers.py`
- `download_file(url, path)`: Download con retry
- `wait_for_leonardo_generation(gen_id, api_key)`: Polling async Leonardo
- `analyze_script_for_scenes(script, num)`: Genera prompt immagini da script
- `clean_filename(name)`: Sanitizza nomi file

---

## Flusso di Esecuzione Completo

### 1. Inizializzazione
```python
Config.ensure_dirs()          # Crea directory
db = DatabaseRepository()     # Connessione DB
app = create_video_workflow() # Compila grafo LangGraph
```

### 2. Creazione Stato Iniziale
```python
initial_state = VideoProductionState(
    topic=topic or None,
    status="starting"
)
video_id = db.create_video(topic or "Auto-generated")
initial_state['video_id'] = video_id
```

### 3. Esecuzione Pipeline
```python
result = app.invoke(initial_state)
```

**Flusso interno**:
1. **research_step**: topic + research_data
2. **script_step**: script italiano 700 parole
3. **images_step**: 25 immagini PhotoReal
4. **audio_step**: narrazione MP3
5. **music_step**: background music MP3
6. **video_step**: assembly + Ken Burns → MP4
7. **upload_step**: upload YouTube → youtube_id, youtube_url

### 4. Salvataggio Risultati
```python
db.update_video(
    video_id,
    youtube_id=result['youtube_id'],
    youtube_url=result['youtube_url'],
    script=result['script'],
    status='published',
    cost_images=1.10,
    cost_audio=0.14,
    cost_music=0.10,
    cost_script=0.01,
    total_cost=1.35
)
db.mark_topic_used(final_topic)
```

---

## Gestione Errori

### Livello Agente
Ogni agente gestisce errori specifici:
- `research_agent`: ValueError se topic non trovato
- `images_agent`: Retry su API error, fallisce se < 10 immagini
- `upload_agent`: FileNotFoundError se manca credentials.json

### Livello Executor
```python
try:
    result = app.invoke(initial_state)
except Exception as e:
    db.update_video(video_id, status='error', error_message=str(e))
    db.add_log(video_id, "workflow", "error", str(e))
    raise
```

### Livello Database
```python
try:
    self.init_database()
except Exception as e:
    raise ValueError(f"Failed to initialize database: {e}. Check DATABASE_URL.")
```

---

## Estensibilità

### Aggiungere un Nuovo Agente

1. Creare `src/agents/my_agent.py`:
```python
from src.pipeline.state import VideoProductionState

def my_agent(state: VideoProductionState) -> dict:
    # Logica dell'agente
    return {"new_key": "value"}
```

2. Aggiornare `src/pipeline/state.py`:
```python
class VideoProductionState(TypedDict, total=False):
    new_key: str
```

3. Aggiornare `src/pipeline/graph.py`:
```python
from src.agents.my_agent import my_agent

workflow.add_node("my_step", my_agent)
workflow.add_edge("previous_step", "my_step")
workflow.add_edge("my_step", "next_step")
```

### Aggiungere Servizio API

Creare `src/services/my_service.py`:
```python
from src.config import Config

class MyService:
    def __init__(self):
        self.api_key = Config.MY_API_KEY
    
    def call_api(self, params):
        # Logica chiamata API
        pass
```

---

## Performance

### Tempi Stimati (per video 5 minuti)

| Fase | Durata | Bottleneck |
|------|--------|------------|
| Research | 2-5s | Wikipedia API |
| Script | 15-30s | Claude generation |
| Images (25) | 5-10min | Leonardo queue |
| Audio | 10-20s | OpenAI TTS |
| Music | 20-40s | Mubert generation |
| Video Assembly | 2-4min | MoviePy rendering |
| Upload | 1-3min | YouTube API |
| **TOTALE** | **10-18 min** | Leonardo images |

### Ottimizzazioni Possibili

1. **Parallelizzazione**: Audio + Music + Images in parallelo (attualmente sequenziale)
2. **Caching**: Riutilizzare immagini simili per topic correlati
3. **Batch Processing**: Generare più script in una chiamata Claude
4. **Video Presets**: Template MoviePy precompilati

---

## Sicurezza

### API Keys
- Tutte le keys in environment variables (`.env`)
- Mai hardcoded nel codice
- `.env` in `.gitignore`

### OAuth YouTube
- `token.pickle` e `credentials.json` in `.gitignore`
- Refresh token automatico
- Scopes minimi richiesti

### Database
- Connessione PostgreSQL con SSL
- Prepared statements per SQL injection prevention
- Validazione input prima di INSERT/UPDATE

---

## Monitoring e Logs

### Database Logs
```python
db.add_log(video_id, "agent_name", "status", "message")
```

Esempio query logs:
```sql
SELECT agent_name, status, message, created_at 
FROM production_logs 
WHERE video_id = 123 
ORDER BY created_at ASC;
```

### File Logs
- `logs/app_YYYY-MM-DD.log`: Log applicativi giornalieri
- Rotazione automatica (1 file per giorno)

---

## Deployment

### Replit (Attuale)
- Environment gestito automaticamente
- PostgreSQL integrato
- Secrets management built-in
- Auto-restart workflows

### Alternative Cloud

#### Railway
```bash
railway init
railway add postgresql
railway deploy
```

#### Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "main.py"]
```

---

## Troubleshooting

### "Database connection failed"
→ Verifica `DATABASE_URL` in secrets

### "Leonardo API 429"
→ Rate limit superato, attendi 60s

### "YouTube upload permission denied"
→ Rigenera OAuth con `credentials.json`

### "MoviePy render crash"
→ Verifica RAM disponibile (richiede 2GB+)

---

## Roadmap Future Features

1. **Scheduler** (`src/scheduler/`): APScheduler per video giornalieri automatici
2. **Services Layer** (`src/services/`): Wrapper API con retry/backoff
3. **Video Processing** (`src/video/`): Moduli separati per Ken Burns, transitions, etc.
4. **Topics Management** (`src/topics/`): Generator, validator, deduplicator intelligenti
5. **Notifications** (`src/notifications/`): Telegram/Email alerts su successo/errore
6. **Dashboard Web**: Monitoring real-time e controllo produzione
7. **A/B Testing**: Generazione multiple versioni video per stesso topic

---

## Contributi

Per contribuire al progetto:
1. Fork repository
2. Branch feature: `git checkout -b feature/my-feature`
3. Commit: `git commit -m "Add my feature"`
4. Push: `git push origin feature/my-feature`
5. Pull Request

---

## License

MIT License - vedi file `LICENSE`
