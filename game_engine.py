"""
Stone Age Game Engine Module

This module implements the main game loop and orchestrates the game flow.
"""

from game_state import GameState, ActionSpace
from ai_player import AIPlayer
from board_visualization import display_round_start, display_game_board


class GameEngine:
    """Main game engine that runs the Stone Age game"""
    
    def __init__(self, num_players: int = 2, enable_visualization: bool = False):
        self.game_state = GameState(num_players)
        self.ai_players = [AIPlayer(i) for i in range(num_players)]
        self.game_log = []
        self.enable_visualization = enable_visualization
    
    def log(self, message: str):
        """Add a message to the game log"""
        print(message)
        self.game_log.append(message)
    
    def run_game(self):
        """Run the complete game from start to finish"""
        self.log("=" * 80)
        self.log("STONE AGE - AI SIMULATION")
        self.log("=" * 80)
        self.log(f"Starting game with {len(self.game_state.players)} players")
        self.log("")
        
        # Main game loop
        while not self.game_state.is_game_over():
            self.game_state.current_round += 1
            self.run_round()
        
        # Game over
        self.log("")
        self.log("=" * 80)
        self.log("GAME OVER")
        self.log("=" * 80)
        self.display_final_scores()
    
    def run_round(self):
        """Run a single round of the game"""
        self.log("")
        self.log("=" * 80)
        self.log(f"ROUND {self.game_state.current_round}")
        self.log("=" * 80)
        
        # Display visual board if enabled
        if self.enable_visualization:
            display_round_start(self.game_state, self.game_state.current_round)
        
        # Phase 1: Place workers
        self.log("")
        self.log("--- Phase 1: Worker Placement ---")
        self.phase_place_workers()
        
        # Phase 2: Resolve actions
        self.log("")
        self.log("--- Phase 2: Action Resolution ---")
        self.phase_resolve_actions()
        
        # Phase 3: Feed workers
        self.log("")
        self.log("--- Phase 3: Feeding ---")
        self.phase_feed_workers()
        
        # Display round summary
        self.log("")
        self.log("--- Round Summary ---")
        self.display_round_summary()
        
        # Clear workers from board for next round
        self.game_state.board.clear_workers()
    
    def phase_place_workers(self):
        """Phase 1: Each player places workers on action spaces"""
        # Players take turns placing workers
        num_players = len(self.game_state.players)
        start_player = self.game_state.starting_player
        
        # Each player places all their workers
        for i in range(num_players):
            player_index = (start_player + i) % num_players
            player = self.game_state.players[player_index]
            ai = self.ai_players[player_index]
            
            self.log(f"\n{player.name}'s turn to place workers:")
            self.log(f"  Available workers: {player.workers}")
            self.log(f"  Resources: Wood={player.resources.wood}, Brick={player.resources.brick}, "
                    f"Stone={player.resources.stone}, Gold={player.resources.gold}, Food={player.resources.food}")
            
            # AI decides where to place workers
            placements = ai.decide_worker_placement(self.game_state)
            
            # Place workers on chosen spaces
            for action, count in placements:
                if self.game_state.board.place_workers(action, player_index, count):
                    self.log(f"  Placed {count} worker(s) on {action.value}")
                else:
                    self.log(f"  Failed to place {count} worker(s) on {action.value} (space full)")
    
    def phase_resolve_actions(self):
        """Phase 2: Resolve all placed actions"""
        # Resolve each action space in order
        action_order = [
            ActionSpace.HUNTING_GROUNDS,
            ActionSpace.FOREST,
            ActionSpace.CLAY_PIT,
            ActionSpace.QUARRY,
            ActionSpace.RIVER,
            ActionSpace.FARM,
            ActionSpace.TOOL_MAKER,
            ActionSpace.HUT,
            ActionSpace.CIVILIZATION_CARD,
            ActionSpace.BUILDING,
        ]
        
        for action in action_order:
            placed = self.game_state.board.placed_workers[action]
            
            if not placed:
                continue
            
            # Group workers by player
            player_workers = {}
            for player_index in placed:
                if player_index not in player_workers:
                    player_workers[player_index] = 0
                player_workers[player_index] += 1
            
            # Resolve for each player
            for player_index, worker_count in player_workers.items():
                ai = self.ai_players[player_index]
                log_msg = ai.resolve_action(self.game_state, action, worker_count)
                self.log(f"  {log_msg}")
    
    def phase_feed_workers(self):
        """Phase 3: Each player must feed their workers"""
        for i, player in enumerate(self.game_state.players):
            food_needed = player.workers
            available_food = player.resources.food + player.food_track
            
            self.log(f"\n{player.name} feeding phase:")
            self.log(f"  Workers to feed: {food_needed}")
            self.log(f"  Food from track: {player.food_track}")
            self.log(f"  Food from resources: {player.resources.food}")
            self.log(f"  Total available: {available_food}")
            
            penalty = player.feed_workers()
            
            if penalty > 0:
                self.log(f"  ⚠️  Couldn't feed all workers! Penalty: -{penalty} points")
            else:
                self.log(f"  ✓ Successfully fed all workers")
    
    def display_round_summary(self):
        """Display summary of player states after the round"""
        for player in self.game_state.players:
            self.log(f"\n{player.name}:")
            self.log(f"  Workers: {player.workers}")
            self.log(f"  Food production: {player.food_track}/round")
            self.log(f"  Tools: {player.tools}")
            self.log(f"  Resources: W={player.resources.wood} B={player.resources.brick} "
                    f"S={player.resources.stone} G={player.resources.gold} F={player.resources.food}")
            self.log(f"  Civilization cards: {len(player.civilization_cards)}")
            self.log(f"  Buildings: {len(player.buildings)}")
            self.log(f"  Current score: {player.score}")
    
    def display_final_scores(self):
        """Display final scores and determine winner"""
        self.log("")
        self.log("FINAL SCORES:")
        self.log("-" * 80)
        
        final_scores = []
        
        for player in self.game_state.players:
            final_score = player.calculate_final_score()
            final_scores.append((player, final_score))
            
            self.log(f"\n{player.name}:")
            self.log(f"  Base score: {player.score}")
            
            # Civilization card points
            card_points = sum(card.points for card in player.civilization_cards)
            self.log(f"  Civilization cards ({len(player.civilization_cards)}): +{card_points} points")
            for card in player.civilization_cards:
                self.log(f"    - {card}")
            
            # Building points
            building_points = sum(building.points for building in player.buildings)
            self.log(f"  Buildings ({len(player.buildings)}): +{building_points} points")
            for building in player.buildings:
                self.log(f"    - {building}")
            
            # Resource bonus
            resource_bonus = player.resources.total_value()
            self.log(f"  Resource bonus: +{resource_bonus} points")
            
            self.log(f"  TOTAL: {final_score} points")
        
        # Determine winner
        final_scores.sort(key=lambda x: x[1], reverse=True)
        winner = final_scores[0][0]
        winning_score = final_scores[0][1]
        
        self.log("")
        self.log("=" * 80)
        self.log(f"🏆 WINNER: {winner.name} with {winning_score} points! 🏆")
        self.log("=" * 80)
    
    def get_game_summary(self) -> dict:
        """Get a summary of the game results"""
        final_scores = {}
        for player in self.game_state.players:
            final_scores[player.name] = player.calculate_final_score()
        
        winner = self.game_state.get_winner()
        
        return {
            "rounds_played": self.game_state.current_round,
            "final_scores": final_scores,
            "winner": winner.name if winner else None,
            "log": self.game_log,
        }


def main():
    """Main entry point for the Stone Age simulation"""
    import random
    import sys
    
    # Set random seed for reproducibility (optional)
    # random.seed(42)
    
    # Check if visualization is enabled via command line argument
    enable_viz = '--visualize' in sys.argv or '-v' in sys.argv
    
    # Create and run game
    engine = GameEngine(num_players=2, enable_visualization=enable_viz)
    engine.run_game()
    
    # Get summary
    summary = engine.get_game_summary()
    
    print("\n")
    print("=" * 80)
    print("GAME STATISTICS")
    print("=" * 80)
    print(f"Total rounds played: {summary['rounds_played']}")
    print(f"Winner: {summary['winner']}")
    print(f"Final scores: {summary['final_scores']}")


if __name__ == "__main__":
    main()
