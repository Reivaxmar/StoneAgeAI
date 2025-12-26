# Stone Age Web Visualization Screenshots

This directory contains screenshots of the web-based game visualization.

## Full Interface

![Full Web Interface](https://github.com/user-attachments/assets/b44ce85e-c785-4cc3-b3f4-4b8fb7839307)

The complete web interface showing:
- **Header**: Stone Age title with current round information
- **Scoring Track**: Points from 0-99 displayed in a green banner
- **Resource Gathering Zones**: Cards showing each resource type (Hunting Grounds, Forest, Clay Pit, Quarry, River) with worker placement counts
- **Special Action Zones**: Farm, Tool Maker, and Hut with worker status
- **Civilization Cards**: Display of 4 available cards with point values in gold badges
- **Buildings**: Display of 4 available buildings with resource costs and point values
- **Player Status**: Two player cards showing:
  - Score (52 pts and 48 pts)
  - Workers count with emoji (👷)
  - Food per turn (🌾)
  - Tool inventory
  - Resource grid with icons (🌲 Wood, 🧱 Brick, 🪨 Stone, 💰 Gold, 🍖 Food)
  - Owned civilization cards and buildings

## Features Shown

### Interactive Elements
- **Hover Effects**: Cards have a subtle lift effect when hovered
- **Worker Count Badges**: Green badges show active workers (e.g., "3/7"), gray badges show empty zones ("0/7")
- **Point Badges**: Gold-colored badges display point values for cards and buildings
- **Refresh Button**: Floating green button in the bottom-right corner for manual refresh

### Visual Design
- **Color Scheme**: Earthy brown/tan gradients for the background, white cards with shadows
- **Typography**: Clear, modern fonts with appropriate sizing
- **Icons**: Emoji icons for visual clarity throughout the interface
- **Layout**: Responsive grid-based layout that adapts to screen size

### Real-Time Updates
The interface automatically refreshes every 3 seconds to show the latest game state as AI players make their moves.

## Usage

To view this interface yourself:

```bash
# Start the game with visualization
python3 main.py --visualize

# Or run the demo
python3 demo_web_visualization.py
```

The browser will open automatically to http://localhost:8080 and display the game board.
