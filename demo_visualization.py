"""
Demo script to show the board visualization in action.
Run this to see a sample game board with all features displayed.
"""

import random
from game_engine import GameEngine
from game_state import ActionSpace, CivilizationCard, Building, ResourceType
from board_visualization import display_round_start

random.seed(42)

print("\n" + "=" * 120)
print("STONE AGE - BOARD VISUALIZATION DEMO".center(120))
print("=" * 120)
print("\nThis demo shows the ASCII-based board visualization with all game components.")
print("The visualization displays:")
print("  • 100-point scoring track (0-99) around the board perimeter")
print("  • Resource gathering zones with worker placement status")
print("  • Special action zones (Farm, Tool Maker, Hut)")
print("  • 4 available civilization cards")
print("  • 4 available buildings")
print("  • Player status with resources, tools, and food production")
print("\n" + "=" * 120)

# Create game with visualization
engine = GameEngine(num_players=2, enable_visualization=True)
engine.game_state.current_round = 5

# Simulate active game state with workers placed
engine.game_state.board.place_workers(ActionSpace.HUNTING_GROUNDS, 0, 3)
engine.game_state.board.place_workers(ActionSpace.FOREST, 1, 2)
engine.game_state.board.place_workers(ActionSpace.CLAY_PIT, 0, 2)
engine.game_state.board.place_workers(ActionSpace.QUARRY, 1, 1)
engine.game_state.board.place_workers(ActionSpace.RIVER, 0, 1)
engine.game_state.board.place_workers(ActionSpace.FARM, 1, 1)
engine.game_state.board.place_workers(ActionSpace.TOOL_MAKER, 0, 1)

# Set up interesting player states
p1 = engine.game_state.players[0]
p1.resources.wood = 6
p1.resources.brick = 4
p1.resources.stone = 3
p1.resources.gold = 2
p1.resources.food = 5
p1.food_track = 3
p1.tools = [1, 2, 2]
p1.score = 52
p1.workers = 8

# Add some civilization cards and buildings to Player 1
if engine.game_state.board.civilization_cards:
    card = engine.game_state.board.get_available_civilization_card()
    if card:
        p1.civilization_cards.append(card)

p2 = engine.game_state.players[1]
p2.resources.wood = 3
p2.resources.brick = 8
p2.resources.stone = 1
p2.resources.gold = 4
p2.resources.food = 3
p2.food_track = 2
p2.tools = [1, 3]
p2.score = 48
p2.workers = 7

# Add a building to Player 2
building = Building("Field", {ResourceType.WOOD: 2, ResourceType.BRICK: 2}, 8)
p2.buildings.append(building)

# Display the visualization
display_round_start(engine.game_state, 5)

print("\n" + "=" * 120)
print("END OF DEMO".center(120))
print("=" * 120)
print("\nTo run the game with visualization enabled, use:")
print("  python3 main.py --visualize")
print("  or")
print("  python3 main.py -v")
print("\n")
