# Guida alla Configurazione - Sistema Produzione Video YouTube

## Prerequisiti

Il sistema richiede le seguenti API keys per funzionare:

### 1. Anthropic Claude API (RICHIESTO)
- **Uso**: Generazione topic storici e script video
- **Costo**: ~€0.01 per video
- **Setup**:
  1. Vai su https://console.anthropic.com/
  2. Crea un account e ottieni la API key
  3. Aggiungi come secret Replit: `ANTHROPIC_API_KEY`

### 2. OpenAI API (RICHIESTO)
- **Uso**: Sintesi vocale italiana (TTS-1-HD)
- **Costo**: ~€0.14 per video (5 minuti)
- **Setup**:
  1. Vai su https://platform.openai.com/
  2. Crea un account e ottieni la API key
  3. Aggiungi come secret Replit: `OPENAI_API_KEY`

### 3. Leonardo.ai API (RICHIESTO)
- **Uso**: Generazione 25 immagini per video con Character Reference
- **Costo**: ~€1.10 per video
- **Setup**:
  1. Vai su https://leonardo.ai/
  2. Crea un account e ottieni la API key
  3. Aggiungi come secret Replit: `LEONARDO_API_KEY`
  4. OPZIONALE: Carica un'immagine di stile in `data/style_reference_image.jpg` per consistenza visiva

### 4. Mubert API (RICHIESTO)
- **Uso**: Musica di sottofondo royalty-free
- **Costo**: ~€0.10 per video
- **Setup**:
  1. Vai su https://mubert.com/render/api
  2. Richiedi accesso API
  3. Aggiungi come secrets Replit:
     - `MUBERT_CUSTOMER_ID`
     - `MUBERT_ACCESS_TOKEN`

### 5. YouTube Data API v3 (RICHIESTO per upload)
- **Uso**: Upload automatico video su YouTube
- **Costo**: Gratuito
- **Setup**:
  1. Vai su https://console.cloud.google.com/
  2. Crea un nuovo progetto
  3. Abilita "YouTube Data API v3"
  4. Crea credenziali OAuth 2.0
  5. Scarica `credentials.json` e mettilo nella root del progetto
  6. Al primo upload, il sistema chiederà l'autorizzazione

## Configurazione Step-by-Step

### Passo 1: Configura Secrets Replit
1. Vai nelle Impostazioni di questo Repl
2. Sezione "Secrets"
3. Aggiungi tutti i secrets richiesti sopra

### Passo 2: Upload Style Reference (Opzionale)
```bash
# Carica un'immagine di riferimento stilistico
cp tua-immagine-stile.jpg data/style_reference_image.jpg
```

### Passo 3: Configura YouTube OAuth
1. Scarica `credentials.json` da Google Cloud Console
2. Mettilo nella root: `/home/runner/workspace/credentials.json`

### Passo 4: Verifica Database
Il database PostgreSQL è già configurato automaticamente da Replit.

## Utilizzo

### Dashboard Web (Raccoman dato)
1. La dashboard è già in esecuzione su porta 5000
2. Apri il browser integrato Replit
3. Clicca "Avvia Produzione" per generare un video
4. Inserisci un topic specifico (opzionale) o lascia vuoto per generazione automatica

### CLI (Avanzato)
```bash
# Genera video con topic automatico
python main.py

# Genera video su topic specifico
python main.py "Battaglia di Waterloo"
```

## Verifica Configurazione

Puoi verificare che tutti i secrets siano configurati correttamente:

```python
import os

required_secrets = [
    'ANTHROPIC_API_KEY',
    'OPENAI_API_KEY',
    'LEONARDO_API_KEY',
    'MUBERT_CUSTOMER_ID',
    'MUBERT_ACCESS_TOKEN',
    'DATABASE_URL'
]

for secret in required_secrets:
    if os.getenv(secret):
        print(f"✓ {secret} configurato")
    else:
        print(f"✗ {secret} MANCANTE")
```

## Costi Previsti

Per ogni video prodotto:
- Leonardo.ai (25 immagini): €1.10
- OpenAI TTS (5 min): €0.14
- Mubert (musica): €0.10
- Claude (script): €0.01
- **TOTALE: €1.35 per video**

## Troubleshooting

### "ModuleNotFoundError: No module named X"
Assicurati che tutti i pacchetti siano installati:
```bash
pip install -r requirements.txt
```

### "DATABASE_URL environment variable not set"
Il database PostgreSQL dovrebbe essere configurato automaticamente. Se manca:
1. Vai nelle impostazioni Repl
2. Abilita "PostgreSQL Database"

### "Leonardo API error"
Verifica:
- API key corretta
- Credito sufficiente su Leonardo.ai
- Limiti rate non superati

### "YouTube upload failed"
Verifica:
- `credentials.json` presente nella root
- Hai completato il flusso OAuth almeno una volta
- Il file `token.pickle` è stato generato

## Supporto

Per problemi o domande:
1. Controlla i log nella dashboard web
2. Verifica che tutti i secrets siano configurati
3. Controlla i costi e i limiti delle API esterne
