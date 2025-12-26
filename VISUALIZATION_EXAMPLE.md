# Stone Age Board Visualization Example

This file shows an example of the ASCII-based board visualization created for the Stone Age game.

## Running the Visualization

To run the game with visualization enabled:
```bash
python3 main.py --visualize
# or
python3 main.py -v
```

To see a demo of all features:
```bash
python3 demo_visualization.py
```

## Example Output

```
████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████
                                                        ROUND 5                                                         
████████████████████████████████████████████████████████████████████████████████████████████████████████████████████████

========================================================================================================================
                                                 STONE AGE - GAME BOARD                                                 
========================================================================================================================
┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Points:  0  .  .  .  .  5  .  .  .  . 10  .  .  .  . 15  .  .  .  . 20  .  .  .  .                                  │
│25│ RESOURCE GATHERING ZONES                                                                                    │75│
│26│ 🍖 Hunting Grounds (Food)    [3/7 workers]                                                                   │76│
│27│ 🌲 Forest (Wood)             [2/7 workers]                                                                   │77│
│28│ 🧱 Clay Pit (Brick)          [2/7 workers]                                                                   │78│
│29│ 🪨 Quarry (Stone)            [1/7 workers]                                                                   │79│
│30│ 💰 River (Gold)              [1/7 workers]                                                                   │80│
│31│ ──────────────────────────────────────────────────                                                          │81│
│32│ SPECIAL ACTION ZONES                                                                                        │82│
│33│ 🌾 Farm (Food Production)         [1/1 workers]                                                              │83│
│34│ 🔨 Tool Maker                     [1/1 workers]                                                              │84│
│35│ 🏠 Hut (Get Workers)              [0/2 workers]                                                              │85│
│36│ ──────────────────────────────────────────────────                                                          │86│
│37│ CIVILIZATION CARDS [0/1 workers]                                                                            │87│
│38│   📜 1. Music                (15 pts)                                                                        │88│
│39│   📜 2. Weaving              ( 9 pts)                                                                        │89│
│40│   📜 3. Transport            (11 pts)                                                                        │90│
│41│   📜 4. Medicine             (10 pts)                                                                        │91│
│42│ ──────────────────────────────────────────────────                                                          │92│
│43│ BUILDINGS [0/1 workers]                                                                                     │93│
│44│   🏛️  1. House           Cost:[2W, 2S      ] (11 pts)                                                       │94│
│45│   🏛️  2. Field           Cost:[2W, 2B      ] ( 8 pts)                                                       │95│
│46│   🏛️  3. Shelter         Cost:[3S          ] (10 pts)                                                       │96│
│47│   🏛️  4. Lodge           Cost:[3B, 2S      ] (14 pts)                                                       │97│
│48│                                                                                                             │98│
│49│                                                                                                             │99│
│        50  .  .  .  . 55  .  .  .  . 60  .  .  .  . 65  .  .  .  . 70  .  .  .  .                                  │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
  Points 75-99 on right edge ↑
========================================================================================================================

========================================================================================================================
                                                     PLAYER STATUS                                                      
========================================================================================================================

Player 1:
  Score: 52 pts
  Workers: 8
  Food/Turn: 3 🌾
  Tools: [1, 2, 2]
  Resources: Wood=6🌲 Brick=4🧱 Stone=3🪨 Gold=2💰 Food=5🍖
  Civilization Cards: 1
    - Pottery (8pts)
  Buildings: 0

Player 2:
  Score: 48 pts
  Workers: 7
  Food/Turn: 2 🌾
  Tools: [1, 3]
  Resources: Wood=3🌲 Brick=8🧱 Stone=1🪨 Gold=4💰 Food=3🍖
  Civilization Cards: 0
  Buildings: 1
    - Field (8pts)

========================================================================================================================
```

## Features Shown in the Visualization

### Scoring Track (0-99 points)
- Points 0-24 shown at the top
- Points 25-49 shown on the left edge  
- Points 50-74 shown at the bottom
- Points 75-99 shown on the right edge

### Resource Gathering Zones
Each zone displays:
- Icon (emoji) representing the resource
- Zone name
- Current worker count / maximum capacity
- Examples: 🍖 Hunting Grounds, 🌲 Forest, 🧱 Clay Pit, 🪨 Quarry, 💰 River

### Special Action Zones  
- 🌾 Farm (Food Production) - Increase permanent food production
- 🔨 Tool Maker - Acquire tools to improve dice rolls
- 🏠 Hut (Get Workers) - Gain additional workers

### Civilization Cards
Shows up to 4 available civilization cards with:
- Card icon (📜)
- Card name
- Point value
- Worker placement status for the zone

### Buildings
Shows up to 4 available buildings with:
- Building icon (🏛️)
- Building name
- Resource cost (W=Wood, B=Brick, S=Stone, G=Gold)
- Point value
- Worker placement status for the zone

### Player Status
For each player:
- Current score
- Number of workers
- Food production per turn (🌾)
- Available tools
- Current resources with icons
- Owned civilization cards with details
- Owned buildings with details
