"""
Demo script for web-based board visualization.
Run this to see the game board in your web browser.
"""

import random
import time
from game_engine import GameEngine
from game_state import ActionSpace, Building, ResourceType

print("=" * 80)
print("STONE AGE - WEB VISUALIZATION DEMO".center(80))
print("=" * 80)
print()
print("This demo will:")
print("  1. Start a local web server")
print("  2. Open your browser to view the game board")
print("  3. Simulate a few rounds of gameplay")
print("  4. Update the visualization in real-time")
print()
print("=" * 80)
print()

random.seed(42)

# Create game with web visualization
engine = GameEngine(num_players=2, enable_visualization=True)

# Start the web visualization
from web_visualization import start_web_visualization
engine.web_visualizer = start_web_visualization(engine.game_state)

# Simulate round 1
print("\nSimulating Round 1...")
engine.game_state.current_round = 1
engine.game_state.board.place_workers(ActionSpace.HUNTING_GROUNDS, 0, 3)
engine.game_state.board.place_workers(ActionSpace.FOREST, 1, 2)

p1 = engine.game_state.players[0]
p1.resources.wood = 2
p1.resources.food = 3

p2 = engine.game_state.players[1]
p2.resources.food = 2
p2.resources.wood = 1

engine.web_visualizer.save_state_to_file()
time.sleep(3)

# Clear workers for next round
engine.game_state.board.clear_workers()

# Simulate round 2
print("Simulating Round 2...")
engine.game_state.current_round = 2
engine.game_state.board.place_workers(ActionSpace.HUNTING_GROUNDS, 0, 2)
engine.game_state.board.place_workers(ActionSpace.QUARRY, 1, 2)
engine.game_state.board.place_workers(ActionSpace.FARM, 0, 1)

p1.resources.wood = 2
p1.resources.food = 5
p1.resources.stone = 0
p1.food_track = 1
p1.score = 10

p2.resources.wood = 1
p2.resources.food = 2
p2.resources.stone = 2

engine.web_visualizer.save_state_to_file()
time.sleep(3)

# Clear workers for next round
engine.game_state.board.clear_workers()

# Simulate round 5 (mid-game)
print("Simulating Round 5 (mid-game)...")
engine.game_state.current_round = 5
engine.game_state.board.place_workers(ActionSpace.HUNTING_GROUNDS, 0, 2)
engine.game_state.board.place_workers(ActionSpace.FOREST, 1, 3)
engine.game_state.board.place_workers(ActionSpace.QUARRY, 0, 2)
engine.game_state.board.place_workers(ActionSpace.RIVER, 1, 1)
engine.game_state.board.place_workers(ActionSpace.CIVILIZATION_CARD, 0, 1)
engine.game_state.board.place_workers(ActionSpace.TOOL_MAKER, 1, 1)

p1.resources.wood = 8
p1.resources.brick = 4
p1.resources.stone = 5
p1.resources.gold = 2
p1.resources.food = 6
p1.food_track = 3
p1.tools = [1, 2, 2]
p1.score = 45
p1.workers = 8

# Add a civilization card to Player 1
if engine.game_state.board.civilization_cards:
    card = engine.game_state.board.civilization_cards[0]
    p1.civilization_cards.append(card)

p2.resources.wood = 5
p2.resources.brick = 7
p2.resources.stone = 3
p2.resources.gold = 3
p2.resources.food = 4
p2.food_track = 2
p2.tools = [1, 3]
p2.score = 38
p2.workers = 7

# Add a building to Player 2
building = Building("Field", {ResourceType.WOOD: 2, ResourceType.BRICK: 2}, 8)
p2.buildings.append(building)

engine.web_visualizer.save_state_to_file()

print()
print("=" * 80)
print("Demo is running!")
print("=" * 80)
print()
print("The web visualization is now showing the game state.")
print("Open your browser to: http://localhost:8080")
print()
print("The page auto-refreshes every 3 seconds.")
print()
print("Press Ctrl+C to stop the server and exit.")
print()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\n\nShutting down web server...")
    engine.web_visualizer.stop_server()
    print("Done!")
