"""
Stone Age Web Visualization Module

This module provides a web-based visualization of the Stone Age game board,
using a simple HTTP server and HTML/CSS/JavaScript frontend.
"""

import json
import http.server
import socketserver
import threading
import webbrowser
import time
from pathlib import Path
from typing import Optional
from game_state import GameState, ActionSpace, ResourceType


class GameStateEncoder(json.JSONEncoder):
    """Custom JSON encoder for game state objects"""
    
    def default(self, obj):
        if isinstance(obj, ActionSpace):
            return obj.value
        elif isinstance(obj, ResourceType):
            return obj.value
        elif hasattr(obj, '__dict__'):
            return obj.__dict__
        return super().default(obj)


class WebVisualizer:
    """Handles web-based visualization of the Stone Age game board"""
    
    def __init__(self, game_state: GameState, port: int = 8080):
        self.game_state = game_state
        self.port = port
        self.server = None
        self.server_thread = None
        self.latest_state = None
        
    def export_game_state(self) -> dict:
        """Export game state as JSON-serializable dictionary"""
        state = {
            'current_round': self.game_state.current_round,
            'max_rounds': self.game_state.max_rounds,
            'players': [],
            'board': {
                'civilization_cards': [],
                'buildings': [],
                'action_spaces': {},
                'placed_workers': {}
            }
        }
        
        # Export players
        for i, player in enumerate(self.game_state.players):
            state['players'].append({
                'name': player.name,
                'workers': player.workers,
                'food_track': player.food_track,
                'tools': player.tools,
                'score': player.score,
                'resources': {
                    'wood': player.resources.wood,
                    'brick': player.resources.brick,
                    'stone': player.resources.stone,
                    'gold': player.resources.gold,
                    'food': player.resources.food
                },
                'civilization_cards': [
                    {'name': card.name, 'points': card.points}
                    for card in player.civilization_cards
                ],
                'buildings': [
                    {
                        'name': building.name,
                        'points': building.points,
                        'cost': {res.value: amt for res, amt in building.cost.items()}
                    }
                    for building in player.buildings
                ]
            })
        
        # Export board
        for card in self.game_state.board.civilization_cards[:4]:
            state['board']['civilization_cards'].append({
                'name': card.name,
                'points': card.points
            })
        
        for building in self.game_state.board.buildings[:4]:
            state['board']['buildings'].append({
                'name': building.name,
                'points': building.points,
                'cost': {res.value: amt for res, amt in building.cost.items()}
            })
        
        # Export action spaces and worker placements
        for action, max_workers in self.game_state.board.action_spaces.items():
            state['board']['action_spaces'][action.value] = max_workers
            workers = self.game_state.board.placed_workers[action]
            state['board']['placed_workers'][action.value] = len(workers)
        
        return state
    
    def save_state_to_file(self):
        """Save current game state to a JSON file for the web interface"""
        state = self.export_game_state()
        self.latest_state = state
        
        web_dir = Path(__file__).parent / 'web'
        web_dir.mkdir(exist_ok=True)
        
        state_file = web_dir / 'game_state.json'
        with open(state_file, 'w') as f:
            json.dump(state, f, indent=2)
        
        return state_file
    
    def create_html_file(self):
        """Create the HTML file for the web visualization"""
        web_dir = Path(__file__).parent / 'web'
        web_dir.mkdir(exist_ok=True)
        
        html_content = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stone Age - Game Board</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #8B7355 0%, #D2B48C 100%);
            padding: 20px;
            min-height: 100vh;
        }
        
        .container {
            max-width: 1400px;
            margin: 0 auto;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            box-shadow: 0 10px 40px rgba(0, 0, 0, 0.3);
            padding: 30px;
        }
        
        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
            background: linear-gradient(135deg, #6B4423 0%, #8B7355 100%);
            border-radius: 10px;
            color: white;
        }
        
        h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
            text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        }
        
        .round-info {
            font-size: 1.2em;
            opacity: 0.9;
        }
        
        .board-container {
            display: grid;
            grid-template-columns: 1fr;
            gap: 20px;
            margin-bottom: 30px;
        }
        
        .scoring-track {
            background: linear-gradient(90deg, #2c5f2d 0%, #97bc62 50%, #2c5f2d 100%);
            padding: 20px;
            border-radius: 10px;
            text-align: center;
            color: white;
            font-size: 1.2em;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        }
        
        .score-numbers {
            display: flex;
            justify-content: space-around;
            margin-top: 10px;
            flex-wrap: wrap;
        }
        
        .score-marker {
            padding: 5px 10px;
            background: rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            margin: 2px;
        }
        
        .action-zones {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 15px;
        }
        
        .zone-card {
            background: white;
            border-radius: 10px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }
        
        .zone-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        }
        
        .zone-header {
            display: flex;
            align-items: center;
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 2px solid #f0f0f0;
        }
        
        .zone-icon {
            font-size: 2em;
            margin-right: 10px;
        }
        
        .zone-title {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }
        
        .worker-count {
            margin-left: auto;
            background: #4CAF50;
            color: white;
            padding: 5px 12px;
            border-radius: 20px;
            font-size: 0.9em;
            font-weight: bold;
        }
        
        .worker-count.empty {
            background: #ccc;
        }
        
        .card-list, .building-list {
            list-style: none;
        }
        
        .card-item, .building-item {
            padding: 10px;
            margin: 5px 0;
            background: #f8f9fa;
            border-radius: 5px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        
        .points-badge {
            background: #FFD700;
            color: #333;
            padding: 3px 10px;
            border-radius: 15px;
            font-weight: bold;
            font-size: 0.9em;
        }
        
        .cost-badge {
            background: #e9ecef;
            color: #495057;
            padding: 3px 8px;
            border-radius: 5px;
            font-size: 0.85em;
            margin-right: 5px;
        }
        
        .players-section {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        
        .player-card {
            background: white;
            border-radius: 10px;
            padding: 25px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        .player-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 3px solid #6B4423;
        }
        
        .player-name {
            font-size: 1.5em;
            font-weight: bold;
            color: #6B4423;
        }
        
        .player-score {
            font-size: 2em;
            font-weight: bold;
            color: #4CAF50;
        }
        
        .player-stats {
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 15px;
            margin-bottom: 15px;
        }
        
        .stat-item {
            background: #f8f9fa;
            padding: 10px;
            border-radius: 5px;
        }
        
        .stat-label {
            font-size: 0.85em;
            color: #666;
            margin-bottom: 5px;
        }
        
        .stat-value {
            font-size: 1.2em;
            font-weight: bold;
            color: #333;
        }
        
        .resources-grid {
            display: grid;
            grid-template-columns: repeat(5, 1fr);
            gap: 10px;
            margin-top: 15px;
        }
        
        .resource-item {
            text-align: center;
            padding: 10px;
            background: #f8f9fa;
            border-radius: 5px;
        }
        
        .resource-icon {
            font-size: 1.5em;
            margin-bottom: 5px;
        }
        
        .resource-amount {
            font-weight: bold;
            color: #333;
        }
        
        .owned-items {
            margin-top: 15px;
            padding-top: 15px;
            border-top: 2px solid #f0f0f0;
        }
        
        .owned-items-title {
            font-weight: bold;
            color: #666;
            margin-bottom: 10px;
        }
        
        .refresh-btn {
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #4CAF50;
            color: white;
            border: none;
            padding: 15px 30px;
            border-radius: 50px;
            font-size: 1em;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            transition: all 0.3s;
        }
        
        .refresh-btn:hover {
            background: #45a049;
            transform: scale(1.05);
        }
        
        .section-title {
            font-size: 1.5em;
            font-weight: bold;
            margin: 20px 0 15px 0;
            color: #6B4423;
            padding-bottom: 10px;
            border-bottom: 2px solid #D2B48C;
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🏛️ STONE AGE 🏛️</h1>
            <div class="round-info">Loading game state...</div>
        </header>
        
        <div id="game-board">
            <div class="scoring-track">
                <div>Scoring Track (0-99 Points)</div>
                <div class="score-numbers" id="score-markers"></div>
            </div>
            
            <h2 class="section-title">Resource Gathering Zones</h2>
            <div class="action-zones" id="resource-zones"></div>
            
            <h2 class="section-title">Special Action Zones</h2>
            <div class="action-zones" id="special-zones"></div>
            
            <h2 class="section-title">Civilization Cards</h2>
            <div class="action-zones" id="civ-cards"></div>
            
            <h2 class="section-title">Buildings</h2>
            <div class="action-zones" id="buildings"></div>
        </div>
        
        <h2 class="section-title">Players</h2>
        <div class="players-section" id="players"></div>
    </div>
    
    <button class="refresh-btn" onclick="loadGameState()">🔄 Refresh</button>
    
    <script>
        const resourceIcons = {
            'Wood': '🌲',
            'Brick': '🧱',
            'Stone': '🪨',
            'Gold': '💰',
            'Food': '🍖'
        };
        
        const actionZones = {
            'Hunting Grounds': { icon: '🍖', resource: 'Food' },
            'Forest': { icon: '🌲', resource: 'Wood' },
            'Clay Pit': { icon: '🧱', resource: 'Brick' },
            'Quarry': { icon: '🪨', resource: 'Stone' },
            'River': { icon: '💰', resource: 'Gold' },
            'Farm': { icon: '🌾', special: true },
            'Tool Maker': { icon: '🔨', special: true },
            'Hut': { icon: '🏠', special: true }
        };
        
        async function loadGameState() {
            try {
                const response = await fetch('game_state.json');
                const data = await response.json();
                renderGameBoard(data);
            } catch (error) {
                console.error('Error loading game state:', error);
                document.querySelector('.round-info').textContent = 'Error loading game state';
            }
        }
        
        function renderGameBoard(data) {
            // Update header
            document.querySelector('.round-info').textContent = 
                `Round ${data.current_round} of ${data.max_rounds}`;
            
            // Render scoring track markers
            const scoreMarkers = document.getElementById('score-markers');
            scoreMarkers.innerHTML = '';
            for (let i = 0; i <= 95; i += 5) {
                const marker = document.createElement('div');
                marker.className = 'score-marker';
                marker.textContent = i;
                scoreMarkers.appendChild(marker);
            }
            
            // Render resource zones
            const resourceZones = document.getElementById('resource-zones');
            resourceZones.innerHTML = '';
            ['Hunting Grounds', 'Forest', 'Clay Pit', 'Quarry', 'River'].forEach(zone => {
                const workers = data.board.placed_workers[zone] || 0;
                const maxWorkers = data.board.action_spaces[zone] || 7;
                resourceZones.appendChild(createZoneCard(zone, workers, maxWorkers));
            });
            
            // Render special zones
            const specialZones = document.getElementById('special-zones');
            specialZones.innerHTML = '';
            ['Farm', 'Tool Maker', 'Hut'].forEach(zone => {
                const workers = data.board.placed_workers[zone] || 0;
                const maxWorkers = data.board.action_spaces[zone] || 1;
                specialZones.appendChild(createZoneCard(zone, workers, maxWorkers));
            });
            
            // Render civilization cards
            const civCards = document.getElementById('civ-cards');
            civCards.innerHTML = '';
            const civWorkers = data.board.placed_workers['Civilization Card'] || 0;
            const civCard = createZoneCard('Civilization Card', civWorkers, 1);
            const cardList = document.createElement('ul');
            cardList.className = 'card-list';
            data.board.civilization_cards.forEach((card, i) => {
                const li = document.createElement('li');
                li.className = 'card-item';
                li.innerHTML = `
                    <span>📜 ${i + 1}. ${card.name}</span>
                    <span class="points-badge">${card.points} pts</span>
                `;
                cardList.appendChild(li);
            });
            civCard.appendChild(cardList);
            civCards.appendChild(civCard);
            
            // Render buildings
            const buildings = document.getElementById('buildings');
            buildings.innerHTML = '';
            const buildWorkers = data.board.placed_workers['Building'] || 0;
            const buildCard = createZoneCard('Building', buildWorkers, 1);
            const buildList = document.createElement('ul');
            buildList.className = 'building-list';
            data.board.buildings.forEach((building, i) => {
                const li = document.createElement('li');
                li.className = 'building-item';
                const costStr = Object.entries(building.cost)
                    .map(([res, amt]) => {
                        const abbrev = {'Wood': 'W', 'Brick': 'B', 'Stone': 'S', 'Gold': 'G', 'Food': 'F'}[res] || res[0];
                        return `<span class="cost-badge">${amt}${abbrev}</span>`;
                    })
                    .join('');
                li.innerHTML = `
                    <div>
                        <div>🏛️ ${i + 1}. ${building.name}</div>
                        <div style="margin-top: 5px;">${costStr}</div>
                    </div>
                    <span class="points-badge">${building.points} pts</span>
                `;
                buildList.appendChild(li);
            });
            buildCard.appendChild(buildList);
            buildings.appendChild(buildCard);
            
            // Render players
            const playersDiv = document.getElementById('players');
            playersDiv.innerHTML = '';
            data.players.forEach(player => {
                playersDiv.appendChild(createPlayerCard(player));
            });
        }
        
        function createZoneCard(zoneName, workers, maxWorkers) {
            const card = document.createElement('div');
            card.className = 'zone-card';
            
            const zoneInfo = actionZones[zoneName] || { icon: '📋' };
            const workerClass = workers > 0 ? '' : 'empty';
            
            card.innerHTML = `
                <div class="zone-header">
                    <span class="zone-icon">${zoneInfo.icon}</span>
                    <span class="zone-title">${zoneName}</span>
                    <span class="worker-count ${workerClass}">${workers}/${maxWorkers}</span>
                </div>
            `;
            
            return card;
        }
        
        function createPlayerCard(player) {
            const card = document.createElement('div');
            card.className = 'player-card';
            
            const toolsStr = player.tools.length > 0 ? player.tools.join(', ') : 'None';
            
            card.innerHTML = `
                <div class="player-header">
                    <div class="player-name">${player.name}</div>
                    <div class="player-score">${player.score} pts</div>
                </div>
                
                <div class="player-stats">
                    <div class="stat-item">
                        <div class="stat-label">Workers</div>
                        <div class="stat-value">👷 ${player.workers}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Food/Turn</div>
                        <div class="stat-value">🌾 ${player.food_track}</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-label">Tools</div>
                        <div class="stat-value">🔨 [${toolsStr}]</div>
                    </div>
                </div>
                
                <div class="resources-grid">
                    <div class="resource-item">
                        <div class="resource-icon">🌲</div>
                        <div class="resource-amount">${player.resources.wood}</div>
                    </div>
                    <div class="resource-item">
                        <div class="resource-icon">🧱</div>
                        <div class="resource-amount">${player.resources.brick}</div>
                    </div>
                    <div class="resource-item">
                        <div class="resource-icon">🪨</div>
                        <div class="resource-amount">${player.resources.stone}</div>
                    </div>
                    <div class="resource-item">
                        <div class="resource-icon">💰</div>
                        <div class="resource-amount">${player.resources.gold}</div>
                    </div>
                    <div class="resource-item">
                        <div class="resource-icon">🍖</div>
                        <div class="resource-amount">${player.resources.food}</div>
                    </div>
                </div>
                
                ${renderOwnedItems(player)}
            `;
            
            return card;
        }
        
        function renderOwnedItems(player) {
            let html = '<div class="owned-items">';
            
            if (player.civilization_cards.length > 0) {
                html += '<div class="owned-items-title">Civilization Cards:</div>';
                html += '<ul class="card-list">';
                player.civilization_cards.forEach(card => {
                    html += `<li class="card-item">
                        <span>📜 ${card.name}</span>
                        <span class="points-badge">${card.points} pts</span>
                    </li>`;
                });
                html += '</ul>';
            }
            
            if (player.buildings.length > 0) {
                html += '<div class="owned-items-title" style="margin-top: 10px;">Buildings:</div>';
                html += '<ul class="building-list">';
                player.buildings.forEach(building => {
                    html += `<li class="building-item">
                        <span>🏛️ ${building.name}</span>
                        <span class="points-badge">${building.points} pts</span>
                    </li>`;
                });
                html += '</ul>';
            }
            
            html += '</div>';
            return html;
        }
        
        // Load initial state
        loadGameState();
        
        // Auto-refresh every 3 seconds
        setInterval(loadGameState, 3000);
    </script>
</body>
</html>'''
        
        html_file = web_dir / 'index.html'
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return html_file
    
    def start_server(self):
        """Start the web server in a background thread"""
        web_dir = Path(__file__).parent / 'web'
        
        class MyHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def __init__(self, *args, **kwargs):
                super().__init__(*args, directory=str(web_dir), **kwargs)
            
            def translate_path(self, path):
                """Restrict access to web directory only"""
                path = super().translate_path(path)
                # Ensure path is within web_dir
                real_path = Path(path).resolve()
                real_web_dir = Path(web_dir).resolve()
                if not str(real_path).startswith(str(real_web_dir)):
                    return str(real_web_dir / 'index.html')
                return path
            
            def log_message(self, format, *args):
                # Suppress server logs
                pass
        
        self.server = socketserver.TCPServer(("127.0.0.1", self.port), MyHTTPRequestHandler)
        self.server_thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        self.server_thread.start()
        
        print(f"\n🌐 Web visualization server started at http://localhost:{self.port}")
        print("The browser will open automatically. Keep this window open.")
        print("Press Ctrl+C to stop the server.\n")
    
    def stop_server(self):
        """Stop the web server"""
        if self.server:
            self.server.shutdown()
            self.server.server_close()
    
    def open_browser(self):
        """Open the web browser to view the visualization"""
        time.sleep(0.5)  # Give server time to start
        webbrowser.open(f'http://localhost:{self.port}')
    
    def display_round(self, round_num: int):
        """Update and display the game board for a round"""
        self.save_state_to_file()
        print(f"Round {round_num} - Game state updated. View at http://localhost:{self.port}")


def start_web_visualization(game_state: GameState, port: int = 8080) -> WebVisualizer:
    """
    Start web visualization for the game.
    Returns the visualizer instance.
    """
    visualizer = WebVisualizer(game_state, port)
    
    # Create HTML file
    visualizer.create_html_file()
    
    # Save initial state
    visualizer.save_state_to_file()
    
    # Start server
    visualizer.start_server()
    
    # Open browser
    visualizer.open_browser()
    
    return visualizer
