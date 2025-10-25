# 🎬 YouTube History Bot

Sistema multi-agente autonomo per la produzione e pubblicazione automatica di video documentari storici in italiano su YouTube.

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![LangGraph](https://img.shields.io/badge/LangGraph-Latest-green.svg)](https://github.com/langchain-ai/langgraph)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## 🚀 Caratteristiche Principali

- **✨ Generazione Automatica Topic**: Claude seleziona eventi storici interessanti
- **📚 Research Intelligente**: Wikipedia API (IT/EN) per contenuti accurati
- **✍️ Script AI**: Claude 3.5 Sonnet scrive script educativi in italiano perfetto
- **🎨 Immagini Coerenti**: Leonardo.ai PhotoReal con Character Reference per stile uniforme
- **🎤 Voce Italiana**: OpenAI TTS-1-HD con voce Nova naturale
- **🎵 Musica Originale**: Mubert genera colonne sonore royalty-free
- **🎞️ Ken Burns Effect**: Animazioni dinamiche zoom+pan sulle immagini
- **📤 Upload Automatico**: Pubblicazione YouTube con metadata SEO-ottimizzati
- **🗄️ Tracking Database**: PostgreSQL per monitorare produzione e costi

---

## 📊 Workflow Pipeline

```
┌─────────┐    ┌──────────┐    ┌────────┐    ┌───────┐    ┌───────┐    ┌───────┐    ┌────────┐
│Research │ ─▶ │  Script  │ ─▶ │ Images │ ─▶ │ Audio │ ─▶ │ Music │ ─▶ │ Video │ ─▶ │ Upload │
│  Agent  │    │  Agent   │    │ Agent  │    │ Agent │    │ Agent │    │ Agent │    │ Agent  │
└─────────┘    └──────────┘    └────────┘    └───────┘    └───────┘    └───────┘    └────────┘
    │               │               │             │             │            │             │
Wikipedia       Claude         Leonardo      OpenAI        Mubert      MoviePy        YouTube
  API            API             AI           TTS           API        Render          API
```

---

## 💰 Costi per Video

| Servizio | Costo | Descrizione |
|----------|-------|-------------|
| Leonardo.ai | €1.10 | 25 immagini PhotoReal 1024x576 |
| OpenAI TTS | €0.14 | Narrazione 5 minuti voce italiana |
| Mubert | €0.10 | Musica di sottofondo cinematic |
| Claude | €0.01 | Generazione topic + script |
| **TOTALE** | **€1.35** | **per video** |

**Costo mensile stimato (30 video)**: €40.50

---

## 📁 Struttura del Progetto

```
youtube-history-bot/
│
├── src/                        # Codice sorgente
│   ├── agents/                 # 7 agenti specializzati
│   │   ├── research_agent.py   # Wikipedia + topic generation
│   │   ├── script_agent.py     # Script writing
│   │   ├── images_agent.py     # Leonardo.ai image generation
│   │   ├── audio_agent.py      # OpenAI TTS
│   │   ├── music_agent.py      # Mubert music
│   │   ├── video_agent.py      # MoviePy assembly
│   │   └── upload_agent.py     # YouTube upload
│   │
│   ├── pipeline/               # LangGraph orchestration
│   │   ├── graph.py            # Workflow DAG
│   │   ├── state.py            # VideoProductionState
│   │   └── executor.py         # Execution + error handling
│   │
│   ├── database/               # PostgreSQL persistence
│   │   └── repository.py       # CRUD operations
│   │
│   ├── utils/                  # Helper functions
│   │   └── helpers.py          # Download, cleanup, etc.
│   │
│   └── config.py               # Configuration centrale
│
├── data/                       # File generati (gitignored)
│   ├── videos/                 # Video finali MP4
│   ├── audio/                  # Narrazione + musica MP3
│   ├── images/                 # Frame generati
│   ├── temp/                   # File temporanei
│   └── cache/                  # Cache API responses
│
├── logs/                       # Application logs
├── assets/                     # Static files
│   └── style_reference.jpg     # Leonardo Character Reference
│
├── docs/                       # Documentation
│   ├── SETUP.md                # Setup guide
│   ├── API_KEYS.md             # Come ottenere API keys
│   └── ARCHITECTURE.md         # Architettura sistema
│
├── tests/                      # Test suite
├── scripts/                    # Utility scripts
├── main.py                     # Entry point CLI
├── requirements.txt            # Python dependencies
├── .env.example                # Template environment variables
└── README.md                   # This file
```

---

## 🔧 Setup Veloce

### 1. Clona il Repository
```bash
git clone https://github.com/yourusername/youtube-history-bot.git
cd youtube-history-bot
```

### 2. Installa Dipendenze
```bash
pip install -r requirements.txt
```

### 3. Configura API Keys
Crea file `.env` nella root:
```bash
cp .env.example .env
```

Aggiungi le tue API keys (vedi [docs/API_KEYS.md](docs/API_KEYS.md)):
```env
ANTHROPIC_API_KEY=sk-ant-...
OPENAI_API_KEY=sk-...
LEONARDO_API_KEY=...
MUBERT_CUSTOMER_ID=...
MUBERT_ACCESS_TOKEN=...
```

### 4. Setup YouTube OAuth
1. Scarica `credentials.json` da Google Cloud Console
2. Mettilo nella root del progetto
3. Al primo upload, autorizzerai l'app (genera `token.pickle`)

Guida completa: [docs/API_KEYS.md#5-youtube-data-api-v3](docs/API_KEYS.md)

### 5. Carica Style Reference (Opzionale)
Per mantenere stile visivo consistente:
```bash
cp tua-immagine-stile.jpg assets/style_reference.jpg
```

---

## 🎯 Utilizzo

### CLI - Genera Singolo Video

**Topic Automatico:**
```bash
python main.py
```

**Topic Specifico:**
```bash
python main.py "Battaglia di Waterloo"
python main.py "Scoperta della penicillina"
python main.py "Caduta del Muro di Berlino"
```

### Output
```
✅ VIDEO PRODUCTION COMPLETED!
============================================================
Topic: Battaglia di Waterloo
YouTube URL: https://www.youtube.com/watch?v=ABC123XYZ
YouTube ID: ABC123XYZ
Video Path: data/videos/Battaglia_di_Waterloo.mp4
============================================================
```

---

## 📖 Documentazione Completa

- **[Setup Guide](docs/SETUP.md)**: Configurazione passo-passo
- **[API Keys](docs/API_KEYS.md)**: Come ottenere tutte le chiavi API
- **[Architecture](docs/ARCHITECTURE.md)**: Design sistema e workflow

---

## 🛠️ Stack Tecnologico

| Categoria | Tecnologie |
|-----------|-----------|
| **Orchestrazione** | LangGraph, LangChain |
| **AI/ML** | Anthropic Claude 3.5 Sonnet, OpenAI TTS-1-HD, Leonardo.ai PhotoReal |
| **Video** | MoviePy, FFmpeg |
| **Database** | PostgreSQL (Replit managed) |
| **APIs** | Wikipedia API, Mubert API, YouTube Data API v3 |
| **Linguaggio** | Python 3.11+ |
| **Deployment** | Replit (con supporto Docker/Railway) |

---

## 🔍 Esempio Video Generato

**Topic**: "Sbarco in Normandia - D-Day"

1. **Research**: Wikipedia IT fornisce contesto storico
2. **Script**: Claude genera script 750 parole in italiano:
   - Intro coinvolgente: "6 giugno 1944. Le spiagge della Normandia..."
   - Eventi cronologici dettagliati
   - Impatto storico e conseguenze
3. **Images**: 25 immagini PhotoReal:
   - "Barche da sbarco che si avvicinano alla spiaggia, atmosfera drammatica, cinematic"
   - "Soldati alleati durante lo sbarco, fotografia storica professionale"
4. **Audio**: Voce italiana narrativa naturale (5 min)
5. **Music**: Musica documentaristica orchestrale sottofondo
6. **Video**: Ken Burns effect su ogni immagine, transizioni fluide
7. **Upload**: YouTube con:
   - Titolo: "Storia: Sbarco in Normandia - D-Day"
   - Tag: storia, educazione, seconda guerra mondiale, d-day
   - Categoria: Education (27)

---

## ⚙️ Configurazione Avanzata

### Personalizzare Parametri Video

Modifica `src/config.py`:

```python
class Config:
    # Numero immagini per video
    NUM_IMAGES_PER_VIDEO = 25  # Aumenta per video più lunghi
    
    # Lunghezza script
    SCRIPT_WORD_COUNT_MIN = 600
    SCRIPT_WORD_COUNT_MAX = 800
    
    # Video settings
    VIDEO_FPS = 24             # Frame per secondo
    VIDEO_BITRATE = "5000k"    # Qualità video
    
    # Durata musica (secondi)
    MUBERT_DURATION = 300      # 5 minuti
```

### Cambiare Voce TTS

Voci disponibili OpenAI: `alloy`, `echo`, `fable`, `onyx`, `nova`, `shimmer`

```python
# In src/config.py
OPENAI_TTS_VOICE = "shimmer"  # Voce femminile italiana
```

---

## 🐛 Troubleshooting

### "Database connection failed"
```bash
# Verifica DATABASE_URL nelle secrets
echo $DATABASE_URL
```

### "Leonardo API 429 Too Many Requests"
→ Hai superato il rate limit. Attendi 60 secondi e riprova.

### "YouTube upload permission denied"
→ Rigenera OAuth eliminando `token.pickle` e riautorizzando:
```bash
rm token.pickle
python main.py
```

### "MoviePy render crash"
→ Verifica RAM disponibile (richiede almeno 2GB). Su Replit, upgrade a piano Hacker.

Per altre domande: [docs/ARCHITECTURE.md#troubleshooting](docs/ARCHITECTURE.md)

---

## 📈 Metriche Database

Query video pubblicati:
```sql
SELECT 
    topic_name, 
    youtube_url, 
    total_cost,
    created_at
FROM videos 
WHERE status = 'published' 
ORDER BY created_at DESC 
LIMIT 10;
```

Statistiche produzione:
```python
from src.database.repository import DatabaseRepository

db = DatabaseRepository()
stats = db.get_statistics()

print(f"Video totali: {stats['total_videos']}")
print(f"Pubblicati: {stats['published']}")
print(f"Costo medio: €{stats['avg_cost']:.2f}")
print(f"Costo totale: €{stats['total_cost']:.2f}")
```

---

## 🚦 Roadmap

- [x] Pipeline multi-agente LangGraph
- [x] Generazione automatica topic
- [x] Character Reference per stile coerente
- [x] Ken Burns effect animazioni
- [x] Upload YouTube automatico
- [ ] **Scheduler giornaliero** (APScheduler)
- [ ] **Dashboard web monitoring** (Flask/Streamlit)
- [ ] **Notifications** (Telegram/Email su completamento)
- [ ] **A/B testing** (generare multiple versioni per stesso topic)
- [ ] **Thumbnail auto-generation** (DALL-E o Ideogram)
- [ ] **Sottotitoli automatici** (Whisper)
- [ ] **Multi-lingua** (EN, ES, FR oltre a IT)

---

## 🤝 Contributi

I contributi sono benvenuti! Per favore:

1. Fork il progetto
2. Crea branch feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambiamenti (`git commit -m 'Add AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Apri Pull Request

---

## 📄 License

Distribuito sotto licenza MIT. Vedi `LICENSE` per informazioni.

---

## 👤 Autore

Creato con ❤️ da [Your Name]

- GitHub: [@yourusername](https://github.com/yourusername)
- Twitter: [@yourusername](https://twitter.com/yourusername)

---

## 🙏 Ringraziamenti

- [LangGraph](https://github.com/langchain-ai/langgraph) - Orchestrazione multi-agente
- [Anthropic Claude](https://anthropic.com/) - AI per script generation
- [Leonardo.ai](https://leonardo.ai/) - Generazione immagini
- [OpenAI](https://openai.com/) - Text-to-Speech
- [Mubert](https://mubert.com/) - Music generation
- [MoviePy](https://zulko.github.io/moviepy/) - Video editing

---

## 📞 Supporto

Se hai domande o problemi:
1. Controlla [docs/](docs/) per guide dettagliate
2. Apri una [Issue](https://github.com/yourusername/youtube-history-bot/issues)
3. Contattami via email: your.email@example.com

---

**Made with ❤️ and 🤖 AI**
