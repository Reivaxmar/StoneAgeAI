# Stone Age AI Simulation

A Python implementation of the board game *Stone Age* where two AI players compete against each other using heuristic-based decision making.

## Overview

This project simulates a complete game of Stone Age with AI players that make decisions based on a greedy evaluation function. The AI balances food production, resource collection, and point generation to win the game.

## Features

- **Complete Game State**: Full implementation of board setup including resource pools, civilization cards, and building tiles
- **Player Management**: Tracks workers, resources, tools, food production, civilization cards, buildings, and scores
- **AI Players**: Simple heuristic-based AI that evaluates actions and makes strategic decisions
- **Game Loop**: Implements all phases of the game:
  1. Worker placement phase
  2. Action resolution phase
  3. Feeding phase
- **Detailed Logging**: Full game progression logs showing each decision and outcome
- **Final Scoring**: Calculates final scores including civilization cards, buildings, and resource bonuses

## Installation

No external dependencies required! This project uses only Python standard library.

Requirements:
- Python 3.7 or higher

## Usage

To run a simulation:

```bash
python3 main.py
```

Or:

```bash
python3 game_engine.py
```

## Project Structure

```
StoneAgeAI/
├── game_state.py      # Core game state classes (Board, Player, Resources)
├── ai_player.py       # AI player with heuristic evaluation
├── game_engine.py     # Main game loop and orchestration
├── main.py            # Entry point
└── README.md          # This file
```

## Game Components

### Resources
- **Wood**: Gathered from Forest (3-sided die)
- **Brick**: Gathered from Clay Pit (4-sided die)
- **Stone**: Gathered from Quarry (5-sided die)
- **Gold**: Gathered from River (6-sided die)
- **Food**: Gathered from Hunting Grounds (2-sided die)

### Action Spaces
- **Resource Gathering**: Forest, Clay Pit, Quarry, River, Hunting Grounds
- **Farm**: Increase permanent food production
- **Tool Maker**: Acquire tools to improve dice rolls
- **Hut**: Gain additional workers
- **Civilization Card**: Take a civilization card for points
- **Building**: Build a building tile for points

### AI Strategy

The AI uses a utility-based evaluation function that considers:

1. **Food Priority**: High priority to ensure workers can be fed
2. **Resource Collection**: Balanced gathering based on building requirements
3. **Long-term Investment**: Early-game focus on farms and workers
4. **Point Generation**: Building buildings and taking civilization cards
5. **Tool Usage**: Acquiring tools to improve resource gathering efficiency

### Scoring

Final scores include:
- Base score accumulated during the game
- Points from civilization cards
- Points from buildings
- Bonus points from remaining resources (1 point per resource)

## Example Output

```
================================================================================
STONE AGE - AI SIMULATION
================================================================================
Starting game with 2 players

================================================================================
ROUND 1
================================================================================

--- Phase 1: Worker Placement ---

Player 1's turn to place workers:
  Available workers: 5
  Resources: Wood=0, Brick=0, Stone=0, Gold=0, Food=0
  Placed 3 worker(s) on Hunting Grounds
  Placed 2 worker(s) on Quarry

...

================================================================================
GAME OVER
================================================================================

FINAL SCORES:
--------------------------------------------------------------------------------

Player 1:
  Base score: 0
  Civilization cards (0): +0 points
  Buildings (1): +8 points
    - Field (8pts)
  Resource bonus: +3 points
  TOTAL: 11 points

Player 2:
  Base score: 0
  Civilization cards (0): +0 points
  Buildings (3): +30 points
    - Shelter (10pts)
    - Simple Hut (6pts)
    - Lodge (14pts)
  Resource bonus: +2 points
  TOTAL: 32 points

================================================================================
🏆 WINNER: Player 2 with 32 points! 🏆
================================================================================
```

## Game Rules Simplifications

This implementation includes some simplifications from the full board game rules:
- Simplified civilization card effects (points only)
- Fixed number of rounds (10) instead of ending when cards run out
- Simplified tool usage mechanics
- No multiplier cards or other advanced mechanics

## Customization

You can modify game parameters in the code:

- **Number of rounds**: Change `max_rounds` in `GameState.__init__()` (game_state.py)
- **Number of players**: Pass `num_players` parameter to `GameEngine()` (game_engine.py)
- **AI behavior**: Adjust utility values in `AIPlayer._calculate_action_utilities()` (ai_player.py)
- **Random seed**: Uncomment `random.seed(42)` in `main()` for reproducible games (game_engine.py)

## License

See LICENSE file for details.

## Acknowledgments

Based on the board game *Stone Age* by Bernd Brunnhofer, published by Hans im Glück.
