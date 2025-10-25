from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from database.db_manager import DatabaseManager
from workflow.langgraph_workflow import run_video_production
import threading

app = Flask(__name__)
CORS(app)
db = DatabaseManager()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="it">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Produzione Video YouTube</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 1400px;
            margin: 0 auto;
        }
        h1 {
            color: white;
            text-align: center;
            margin-bottom: 30px;
            font-size: 2.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .stat-card h3 {
            color: #667eea;
            font-size: 0.9rem;
            text-transform: uppercase;
            margin-bottom: 10px;
        }
        .stat-card .value {
            font-size: 2.5rem;
            font-weight: bold;
            color: #333;
        }
        .stat-card .label {
            color: #666;
            font-size: 0.9rem;
            margin-top: 5px;
        }
        .controls {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            display: flex;
            gap: 15px;
            align-items: center;
        }
        .btn {
            background: #667eea;
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 1rem;
            font-weight: 600;
            transition: all 0.3s;
        }
        .btn:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }
        .btn:disabled {
            background: #ccc;
            cursor: not-allowed;
            transform: none;
        }
        input[type="text"] {
            flex: 1;
            padding: 12px 20px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1rem;
        }
        .videos-section {
            background: white;
            padding: 25px;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        .videos-section h2 {
            color: #667eea;
            margin-bottom: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
        }
        th, td {
            padding: 15px;
            text-align: left;
            border-bottom: 1px solid #e0e0e0;
        }
        th {
            background: #f8f9fa;
            color: #667eea;
            font-weight: 600;
            text-transform: uppercase;
            font-size: 0.85rem;
        }
        tr:hover {
            background: #f8f9fa;
        }
        .status {
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.85rem;
            font-weight: 600;
        }
        .status.published {
            background: #d4edda;
            color: #155724;
        }
        .status.error {
            background: #f8d7da;
            color: #721c24;
        }
        .status.pending {
            background: #fff3cd;
            color: #856404;
        }
        .youtube-link {
            color: #667eea;
            text-decoration: none;
            font-weight: 600;
        }
        .youtube-link:hover {
            text-decoration: underline;
        }
        .loading {
            text-align: center;
            padding: 40px;
            color: #666;
        }
        .cost {
            font-weight: 600;
            color: #28a745;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎬 Dashboard Produzione Video YouTube</h1>
        
        <div class="stats-grid" id="stats">
            <div class="stat-card">
                <h3>Video Totali</h3>
                <div class="value" id="total-videos">-</div>
                <div class="label">prodotti</div>
            </div>
            <div class="stat-card">
                <h3>Pubblicati</h3>
                <div class="value" id="published-videos">-</div>
                <div class="label">su YouTube</div>
            </div>
            <div class="stat-card">
                <h3>Costo Medio</h3>
                <div class="value" id="avg-cost">-</div>
                <div class="label">€ per video</div>
            </div>
            <div class="stat-card">
                <h3>Costo Totale</h3>
                <div class="value" id="total-cost">-</div>
                <div class="label">€ spesi</div>
            </div>
        </div>
        
        <div class="controls">
            <input type="text" id="topic-input" placeholder="Inserisci un topic specifico (opzionale, lascia vuoto per generazione automatica)">
            <button class="btn" onclick="startProduction()">🚀 Avvia Produzione</button>
            <button class="btn" onclick="loadData()">🔄 Aggiorna</button>
        </div>
        
        <div class="videos-section">
            <h2>📹 Video Prodotti</h2>
            <div id="videos-list">
                <div class="loading">Caricamento...</div>
            </div>
        </div>
    </div>
    
    <script>
        function loadData() {
            fetch('/api/stats')
                .then(r => r.json())
                .then(data => {
                    document.getElementById('total-videos').textContent = data.total_videos || 0;
                    document.getElementById('published-videos').textContent = data.published || 0;
                    document.getElementById('avg-cost').textContent = data.avg_cost ? '€' + data.avg_cost.toFixed(2) : '€0.00';
                    document.getElementById('total-cost').textContent = data.total_cost ? '€' + data.total_cost.toFixed(2) : '€0.00';
                });
            
            fetch('/api/videos')
                .then(r => r.json())
                .then(videos => {
                    let html = '<table><thead><tr><th>Topic</th><th>Status</th><th>YouTube</th><th>Costo</th><th>Data</th></tr></thead><tbody>';
                    
                    videos.forEach(v => {
                        html += '<tr>';
                        html += '<td><strong>' + v.topic_name + '</strong></td>';
                        html += '<td><span class="status ' + v.status + '">' + v.status + '</span></td>';
                        html += '<td>' + (v.youtube_url ? '<a href="' + v.youtube_url + '" target="_blank" class="youtube-link">Guarda su YouTube</a>' : '-') + '</td>';
                        html += '<td class="cost">€' + (v.total_cost || 0).toFixed(2) + '</td>';
                        html += '<td>' + new Date(v.created_at).toLocaleDateString('it-IT') + '</td>';
                        html += '</tr>';
                    });
                    
                    html += '</tbody></table>';
                    document.getElementById('videos-list').innerHTML = html;
                });
        }
        
        function startProduction() {
            const topic = document.getElementById('topic-input').value.trim();
            const btn = event.target;
            btn.disabled = true;
            btn.textContent = '⏳ Produzione in corso...';
            
            fetch('/api/produce', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({topic: topic || null})
            })
            .then(r => r.json())
            .then(data => {
                alert(data.message);
                btn.disabled = false;
                btn.textContent = '🚀 Avvia Produzione';
                document.getElementById('topic-input').value = '';
                loadData();
            })
            .catch(err => {
                alert('Errore: ' + err.message);
                btn.disabled = false;
                btn.textContent = '🚀 Avvia Produzione';
            });
        }
        
        loadData();
        setInterval(loadData, 10000);
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/stats')
def stats():
    return jsonify(db.get_statistics())

@app.route('/api/videos')
def videos():
    return jsonify(db.get_all_videos())

@app.route('/api/produce', methods=['POST'])
def produce():
    data = request.json or {}
    topic = data.get('topic')
    
    def produce_async():
        try:
            run_video_production(topic)
        except Exception as e:
            print(f"Production error: {e}")
    
    thread = threading.Thread(target=produce_async)
    thread.start()
    
    return jsonify({
        'message': 'Produzione avviata! Controlla la dashboard per gli aggiornamenti.',
        'topic': topic or 'auto-generato'
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
