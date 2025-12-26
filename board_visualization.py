"""
Stone Age Board Visualization Module

This module provides ASCII-based visualization of the Stone Age game board,
including the scoring track, action spaces, and game components.
"""

from game_state import GameState, ActionSpace, Player
from typing import List


class BoardVisualizer:
    """Handles visualization of the Stone Age game board"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.board_width = 120
        self.board_height = 40
    
    def display_full_board(self):
        """Display the complete game board with all components"""
        print("\n" + "=" * self.board_width)
        print("STONE AGE - GAME BOARD".center(self.board_width))
        print("=" * self.board_width)
        
        # Display scoring track
        self._display_scoring_track()
        
        # Display game board interior
        self._display_board_interior()
        
        # Display bottom of scoring track
        self._display_scoring_track_bottom()
        
        print("=" * self.board_width)
    
    def _display_scoring_track(self):
        """Display the top portion of the scoring track (points 0-29)"""
        # Top edge with points 0-24
        points_top = "".join([f"{i:2d} " if i % 5 == 0 else " . " for i in range(25)])
        print("┌" + "─" * (self.board_width - 2) + "┐")
        print(f"│ Points: {points_top.ljust(self.board_width - 12)}│")
        
        # Display left edge (points 25-49)
        left_points = list(range(25, 50))
        return left_points
    
    def _display_board_interior(self):
        """Display the interior of the board with action spaces and game components"""
        # Left side scoring track points (25-49)
        left_start = 25
        right_start = 75
        point_idx = 0
        max_lines = 25  # 25 lines between top and bottom (25-49 on left, 75-99 on right)
        
        lines = []
        
        # Line 1: Resource gathering zones header
        lines.append(("RESOURCE GATHERING ZONES", False))
        
        # Line 2: Separator
        # (removed to save space)
        
        # Lines: Resource zones
        resource_zones = [
            ("Hunting Grounds (Food)", ActionSpace.HUNTING_GROUNDS, "🍖", 7),
            ("Forest (Wood)", ActionSpace.FOREST, "🌲", 7),
            ("Clay Pit (Brick)", ActionSpace.CLAY_PIT, "🧱", 7),
            ("Quarry (Stone)", ActionSpace.QUARRY, "🪨", 7),
            ("River (Gold)", ActionSpace.RIVER, "💰", 7),
        ]
        
        for name, action, icon, max_workers in resource_zones:
            workers_here = len(self.game_state.board.placed_workers.get(action, []))
            worker_display = f"[{workers_here}/{max_workers} workers]"
            text = f"{icon} {name:25s} {worker_display}"
            lines.append((text, False))
        
        # Separator
        lines.append(("─" * 50, False))
        
        # Special action zones
        lines.append(("SPECIAL ACTION ZONES", False))
        
        special_zones = [
            ("Farm (Food Production)", ActionSpace.FARM, "🌾", 1),
            ("Tool Maker", ActionSpace.TOOL_MAKER, "🔨", 1),
            ("Hut (Get Workers)", ActionSpace.HUT, "🏠", 2),
        ]
        
        for name, action, icon, max_workers in special_zones:
            workers_here = len(self.game_state.board.placed_workers.get(action, []))
            worker_display = f"[{workers_here}/{max_workers} workers]"
            text = f"{icon} {name:30s} {worker_display}"
            lines.append((text, False))
        
        # Separator
        lines.append(("─" * 50, False))
        
        # Civilization cards
        workers_here = len(self.game_state.board.placed_workers.get(ActionSpace.CIVILIZATION_CARD, []))
        lines.append((f"CIVILIZATION CARDS [{workers_here}/1 workers]", False))
        
        # Display 4 civilization cards
        cards = self.game_state.board.civilization_cards[:4]
        for i in range(4):
            if i < len(cards):
                card = cards[i]
                text = f"  📜 {i+1}. {card.name:20s} ({card.points:2d} pts)"
            else:
                text = f"     {i+1}. [No card available]"
            lines.append((text, False))
        
        # Separator
        lines.append(("─" * 50, False))
        
        # Buildings
        workers_here = len(self.game_state.board.placed_workers.get(ActionSpace.BUILDING, []))
        lines.append((f"BUILDINGS [{workers_here}/1 workers]", False))
        
        # Display 4 buildings
        buildings = self.game_state.board.buildings[:4]
        for i in range(4):
            if i < len(buildings):
                building = buildings[i]
                cost_str = ", ".join([f"{amt}{res.value[0]}" for res, amt in building.cost.items()])
                text = f"  🏛️  {i+1}. {building.name:15s} Cost:[{cost_str:12s}] ({building.points:2d} pts)"
            else:
                text = f"     {i+1}. [No building available]"
            lines.append((text, False))
        
        # Only show separator and buildings if we have room
        # Print all lines with left and right point numbers
        for i, (text, _) in enumerate(lines):
            if i >= max_lines:
                break
            left_point = left_start + i
            right_point = right_start + i
            
            line = f"│{left_point:2d}│ {text}"
            # Pad to width
            padding = self.board_width - 4 - len(line) - 4
            line += " " * padding + f" │{right_point:2d}│"
            print(line)
        
        # Fill remaining space if needed
        current_line = len(lines)
        while current_line < max_lines:
            left_point = left_start + current_line
            right_point = right_start + current_line
            line = f"│{left_point:2d}│"
            padding = self.board_width - 4 - len(line) - 4
            line += " " * padding + f" │{right_point:2d}│"
            print(line)
            current_line += 1
    
    def _display_scoring_track_bottom(self):
        """Display the bottom portion of the scoring track (points 50-99)"""
        # Bottom edge with points 50-74
        points_bottom = "".join([f"{i:2d} " if i % 5 == 0 else " . " for i in range(50, 75)])
        print(f"│        {points_bottom.ljust(self.board_width - 12)}│")
        print("└" + "─" * (self.board_width - 2) + "┘")
        
        # Display remaining points 75-99 (right side shown in interior)
        remaining = "Points 75-99 on right edge ↑"
        print(f"  {remaining}")
    
    def display_player_status(self):
        """Display current status of all players"""
        print("\n" + "=" * self.board_width)
        print("PLAYER STATUS".center(self.board_width))
        print("=" * self.board_width)
        
        for i, player in enumerate(self.game_state.players):
            print(f"\n{player.name}:")
            print(f"  Score: {player.score} pts")
            print(f"  Workers: {player.workers}")
            print(f"  Food/Turn: {player.food_track} 🌾")
            print(f"  Tools: {player.tools if player.tools else 'None'}")
            print(f"  Resources: Wood={player.resources.wood}🌲 Brick={player.resources.brick}🧱 "
                  f"Stone={player.resources.stone}🪨 Gold={player.resources.gold}💰 Food={player.resources.food}🍖")
            print(f"  Civilization Cards: {len(player.civilization_cards)}")
            if player.civilization_cards:
                for card in player.civilization_cards:
                    print(f"    - {card}")
            print(f"  Buildings: {len(player.buildings)}")
            if player.buildings:
                for building in player.buildings:
                    print(f"    - {building}")
        
        print("\n" + "=" * self.board_width)
    
    def display_round_header(self, round_num: int):
        """Display round header"""
        print("\n" + "█" * self.board_width)
        print(f"ROUND {round_num}".center(self.board_width))
        print("█" * self.board_width)


def display_game_board(game_state: GameState):
    """Convenience function to display the game board"""
    visualizer = BoardVisualizer(game_state)
    visualizer.display_full_board()
    visualizer.display_player_status()


def display_round_start(game_state: GameState, round_num: int):
    """Display round start with board state"""
    visualizer = BoardVisualizer(game_state)
    visualizer.display_round_header(round_num)
    visualizer.display_full_board()
    visualizer.display_player_status()
