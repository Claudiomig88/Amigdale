from anthropic import Anthropic
from anthropic.types import TextBlock
from agents.research_agent import VideoProductionState
from utils.config import Config

def script_agent(state: VideoProductionState) -> dict:
    client = Anthropic(api_key=Config.ANTHROPIC_API_KEY)
    
    research = state.get('research_data', {})
    topic = state.get('topic', '')
    
    prompt = f"""Scrivi uno script per un video educativo YouTube di 5 minuti sull'evento storico: {topic}

Informazioni di ricerca:
{research.get('summary', '')}

REQUISITI FONDAMENTALI:
1. Lingua: Italiano perfetto, fluente e naturale
2. Lunghezza: 600-800 parole (5 minuti di narrazione)
3. Stile: Educativo ma coinvolgente, adatto a YouTube
4. Struttura:
   - INTRODUZIONE HOOK (30 secondi): Cattura l'attenzione con una domanda provocatoria o fatto sorprendente
   - CONTESTO STORICO (1 minuto): Situazione prima dell'evento
   - EVENTI PRINCIPALI (2-2.5 minuti): Cronologia dettagliata con date e fatti specifici
   - CONSEGUENZE (1 minuto): Impatto immediato e a lungo termine
   - CONCLUSIONE (30 secondi): Riflessione finale memorabile

5. Include:
   - Date precise e numeri specifici
   - Nomi di persone chiave coinvolte
   - Dettagli visivi che possiamo illustrare
   - Transizioni fluide tra le sezioni

6. Evita:
   - Riferimenti a "questo video" o "guardate qui"
   - Chiamate all'azione (like, subscribe, ecc.)
   - Linguaggio troppo accademico

SCRIVI SOLO LO SCRIPT, senza titoli di sezione o note aggiuntive."""

    message = client.messages.create(
        model=Config.CLAUDE_MODEL,
        max_tokens=2500,
        messages=[{
            "role": "user",
            "content": prompt
        }]
    )
    
    content_block = message.content[0]
    if isinstance(content_block, TextBlock):
        script = content_block.text.strip()
    else:
        script = str(content_block).strip()
    
    return {"script": script}
