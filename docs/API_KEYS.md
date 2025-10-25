# Come Ottenere le API Keys

Questa guida spiega passo-passo come ottenere tutte le API keys necessarie per il sistema.

## 1. Anthropic Claude API ⚡

**Utilizzo**: Generazione topic storici e script video  
**Costo stimato**: ~€0.01 per video

### Setup:
1. Vai su https://console.anthropic.com/
2. Crea un account (richiede email)
3. Vai su "API Keys"
4. Clic su "Create Key"
5. Copia la chiave (inizia con `sk-ant-`)
6. In Replit: Settings → Secrets → Aggiungi `ANTHROPIC_API_KEY`

### Nota sui costi:
- Claude 3.5 Sonnet: $3/1M input tokens, $15/1M output tokens
- Utilizzo per video: ~800 token output → $0.01 per video

---

## 2. OpenAI API 🎤

**Utilizzo**: Sintesi vocale italiana (TTS-1-HD)  
**Costo stimato**: ~€0.14 per video (5 minuti)

### Setup:
1. Vai su https://platform.openai.com/
2. Crea un account o accedi
3. Vai su "API Keys" nel menu
4. Clic su "Create new secret key"
5. Copia la chiave (inizia con `sk-`)
6. In Replit: Settings → Secrets → Aggiungi `OPENAI_API_KEY`

### Nota sui costi:
- TTS-1-HD: $0.03 per 1K caratteri
- Script medio: 700 parole = ~4500 caratteri → $0.135 per video

---

## 3. Leonardo.ai API 🎨

**Utilizzo**: Generazione immagini con Character Reference  
**Costo stimato**: ~€1.10 per video (25 immagini)

### Setup:
1. Vai su https://leonardo.ai/
2. Crea un account gratuito
3. Vai su "User Settings" (icona profilo)
4. Seleziona "API Access"
5. Clic su "Generate API Key"
6. Copia la chiave
7. In Replit: Settings → Secrets → Aggiungi `LEONARDO_API_KEY`

### Nota sui costi:
- Leonardo usa un sistema a "token" (crediti)
- 1 immagine PhotoReal = ~40 token
- 25 immagini per video = ~1000 token
- Piano base: $12/mese = 8500 token

### Character Reference (Opzionale):
Per mantenere uno stile visivo consistente:
1. Carica un'immagine di riferimento stilistico
2. Salvala come `assets/style_reference.jpg`
3. Il sistema la userà automaticamente per tutte le generazioni

---

## 4. Mubert API 🎵

**Utilizzo**: Musica di sottofondo royalty-free  
**Costo stimato**: ~€0.10 per video

### Setup:
1. Vai su https://mubert.com/render/api
2. Compila il form di richiesta accesso API
3. Attendi l'email con Customer ID e Access Token (1-2 giorni)
4. In Replit: Settings → Secrets → Aggiungi:
   - `MUBERT_CUSTOMER_ID`
   - `MUBERT_ACCESS_TOKEN`

### Nota sui costi:
- Piano Starter: $10/mese per 10 tracce
- Video a 5 minuti = 1 traccia → $1 per video
- (Alternative gratuite: Pixabay, Bensound - ma richiedono gestione manuale)

---

## 5. YouTube Data API v3 📹

**Utilizzo**: Upload automatico su YouTube  
**Costo**: GRATUITO

### Setup OAuth 2.0:
1. Vai su https://console.cloud.google.com/
2. Crea un nuovo progetto
3. Vai su "APIs & Services" → "Enable APIs"
4. Cerca "YouTube Data API v3" e abilitala
5. Vai su "Credentials" → "Create Credentials" → "OAuth client ID"
6. Tipo applicazione: "Desktop app"
7. Scarica il file JSON delle credenziali
8. Rinomina il file in `credentials.json`
9. Caricalo nella root del progetto Replit: `/home/runner/workspace/credentials.json`

### Prima Autorizzazione:
Al primo upload, il sistema:
1. Aprirà un URL di autenticazione
2. Ti chiederà di autenticarti con il tuo account YouTube
3. Salverà il token in `token.pickle` per utilizzi futuri

---

## Verifica Configurazione

Usa questo script per verificare che tutte le API keys siano configurate:

```python
import os

required_secrets = {
    'ANTHROPIC_API_KEY': 'Claude API',
    'OPENAI_API_KEY': 'OpenAI TTS',
    'LEONARDO_API_KEY': 'Leonardo.ai',
    'MUBERT_CUSTOMER_ID': 'Mubert Customer',
    'MUBERT_ACCESS_TOKEN': 'Mubert Token',
    'DATABASE_URL': 'PostgreSQL'
}

print("Verifica Configurazione API Keys:\n")
all_configured = True

for secret, name in required_secrets.items():
    if os.getenv(secret):
        print(f"✓ {name}: Configurato")
    else:
        print(f"✗ {name}: MANCANTE")
        all_configured = False

if all_configured:
    print("\n✅ Tutte le API keys sono configurate!")
else:
    print("\n⚠️  Alcune API keys mancano. Vedi docs/API_KEYS.md")
```

---

## Costi Mensili Stimati

**Per 30 video al mese (1 al giorno)**:

| Servizio | Costo per video | Costo mensile |
|----------|----------------|---------------|
| Leonardo.ai | €1.10 | €33.00 |
| OpenAI TTS | €0.14 | €4.20 |
| Mubert | €0.10 | €3.00 |
| Claude | €0.01 | €0.30 |
| **TOTALE** | **€1.35** | **€40.50** |

**+ Hosting Replit**: €0-25/mese (dipende dal piano)

---

## Supporto

Se hai problemi con una API:
- **Anthropic**: https://support.anthropic.com/
- **OpenAI**: https://help.openai.com/
- **Leonardo.ai**: support@leonardo.ai
- **Mubert**: api@mubert.com
- **YouTube**: https://support.google.com/youtube/

---

## Alternative Gratuite (con limiti)

- **Claude**: Tier gratuito con limiti stringenti
- **OpenAI TTS**: $5 di credito iniziale gratuito
- **Leonardo.ai**: 150 token/giorno gratuiti (3-4 immagini)
- **Mubert**: Nessun tier gratuito per API
- **YouTube**: Completamente gratuito (quota 10K unit/giorno)
