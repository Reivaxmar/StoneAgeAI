"""
Stone Age AI Player Module

This module implements a simple heuristic-based AI player for Stone Age.
The AI uses a greedy evaluation function to choose actions.
"""

from typing import List, Tuple, Optional
import random
from game_state import GameState, Player, ActionSpace, ResourceType, Building, CivilizationCard


class AIPlayer:
    """Simple heuristic-based AI player"""
    
    def __init__(self, player_index: int):
        self.player_index = player_index
    
    def decide_worker_placement(self, game_state: GameState) -> List[Tuple[ActionSpace, int]]:
        """
        Decide where to place workers for this round.
        Returns a list of (ActionSpace, worker_count) tuples.
        """
        player = game_state.players[self.player_index]
        available_workers = player.workers
        placements = []
        
        # Calculate utilities for each action space
        action_utilities = self._calculate_action_utilities(game_state)
        
        # Sort actions by utility (highest first)
        sorted_actions = sorted(action_utilities.items(), key=lambda x: x[1], reverse=True)
        
        # Greedily place workers on highest utility actions
        for action, utility in sorted_actions:
            if available_workers <= 0:
                break
            
            # Determine how many workers to place
            workers_to_place = self._decide_worker_count(game_state, action, available_workers)
            
            if workers_to_place > 0 and game_state.board.can_place_workers(action, workers_to_place):
                placements.append((action, workers_to_place))
                available_workers -= workers_to_place
        
        return placements
    
    def _calculate_action_utilities(self, game_state: GameState) -> dict:
        """Calculate utility scores for each action space"""
        player = game_state.players[self.player_index]
        utilities = {}
        
        # Resource gathering utilities
        utilities[ActionSpace.HUNTING_GROUNDS] = self._evaluate_hunting_grounds(game_state)
        utilities[ActionSpace.FOREST] = self._evaluate_resource_gathering(game_state, ResourceType.WOOD)
        utilities[ActionSpace.CLAY_PIT] = self._evaluate_resource_gathering(game_state, ResourceType.BRICK)
        utilities[ActionSpace.QUARRY] = self._evaluate_resource_gathering(game_state, ResourceType.STONE)
        utilities[ActionSpace.RIVER] = self._evaluate_resource_gathering(game_state, ResourceType.GOLD)
        
        # Special action utilities
        utilities[ActionSpace.FARM] = self._evaluate_farm(game_state)
        utilities[ActionSpace.TOOL_MAKER] = self._evaluate_tool_maker(game_state)
        utilities[ActionSpace.HUT] = self._evaluate_hut(game_state)
        utilities[ActionSpace.CIVILIZATION_CARD] = self._evaluate_civilization_card(game_state)
        utilities[ActionSpace.BUILDING] = self._evaluate_building(game_state)
        
        return utilities
    
    def _evaluate_hunting_grounds(self, game_state: GameState) -> float:
        """Evaluate hunting grounds (food gathering)"""
        player = game_state.players[self.player_index]
        
        # High priority if we need food to feed workers
        food_needed = player.workers
        current_food = player.resources.food + player.food_track
        
        if current_food < food_needed:
            return 100.0  # Critical priority
        elif current_food < food_needed * 1.5:
            return 50.0  # High priority
        else:
            return 20.0  # Low priority
    
    def _evaluate_resource_gathering(self, game_state: GameState, resource_type: ResourceType) -> float:
        """Evaluate resource gathering spaces"""
        player = game_state.players[self.player_index]
        
        # Check if we need this resource for buildings
        utility = 30.0  # Base utility
        
        for building in game_state.board.buildings:
            if resource_type in building.cost:
                # Higher utility if we need this resource
                utility += 20.0
        
        # Bonus for gold and stone (more valuable)
        if resource_type == ResourceType.GOLD:
            utility += 15.0
        elif resource_type == ResourceType.STONE:
            utility += 10.0
        
        return utility
    
    def _evaluate_farm(self, game_state: GameState) -> float:
        """Evaluate farm (increase food production)"""
        player = game_state.players[self.player_index]
        
        # Good investment early game, less valuable later
        if game_state.current_round < 5:
            return 80.0
        else:
            return 30.0
    
    def _evaluate_tool_maker(self, game_state: GameState) -> float:
        """Evaluate tool maker"""
        player = game_state.players[self.player_index]
        
        # Good if we don't have many tools
        if len(player.tools) < 2:
            return 70.0
        elif len(player.tools) < 3:
            return 40.0
        else:
            return 20.0
    
    def _evaluate_hut(self, game_state: GameState) -> float:
        """Evaluate hut (get more workers)"""
        player = game_state.players[self.player_index]
        
        # Good investment early game if we have food production
        if game_state.current_round < 4 and player.workers < 8:
            if player.food_track >= 2:
                return 85.0
            else:
                return 40.0
        else:
            return 10.0
    
    def _evaluate_civilization_card(self, game_state: GameState) -> float:
        """Evaluate taking a civilization card"""
        if game_state.board.civilization_cards:
            # Civilization cards give good points
            return 60.0
        return 0.0
    
    def _evaluate_building(self, game_state: GameState) -> float:
        """Evaluate building a building"""
        player = game_state.players[self.player_index]
        
        # Check if we can afford any building
        for building in game_state.board.buildings:
            if player.resources.can_afford(building.cost):
                # Higher utility for more valuable buildings
                return 90.0 + building.points
        
        # Lower utility if we can't afford yet
        return 25.0
    
    def _decide_worker_count(self, game_state: GameState, action: ActionSpace, 
                            available_workers: int) -> int:
        """Decide how many workers to place on an action"""
        # Resource gathering: place multiple workers
        if action in [ActionSpace.FOREST, ActionSpace.CLAY_PIT, ActionSpace.QUARRY, 
                     ActionSpace.RIVER, ActionSpace.HUNTING_GROUNDS]:
            # Place 2-4 workers on resource spaces
            count = min(random.randint(2, 4), available_workers)
            return count
        
        # Single worker spaces
        elif action in [ActionSpace.FARM, ActionSpace.TOOL_MAKER, 
                       ActionSpace.CIVILIZATION_CARD, ActionSpace.BUILDING]:
            return 1
        
        # Hut can take up to 2 workers
        elif action == ActionSpace.HUT:
            return min(2, available_workers)
        
        return 1
    
    def resolve_action(self, game_state: GameState, action: ActionSpace, 
                      worker_count: int) -> str:
        """
        Resolve an action for this player.
        Returns a log message describing what happened.
        """
        player = game_state.players[self.player_index]
        log = f"{player.name} resolves {action.value} with {worker_count} worker(s): "
        
        if action == ActionSpace.HUNTING_GROUNDS:
            food = self._gather_resource(worker_count, 2, player)
            player.resources.add(ResourceType.FOOD, food)
            log += f"collected {food} food"
        
        elif action == ActionSpace.FOREST:
            wood = self._gather_resource(worker_count, 3, player)
            player.resources.add(ResourceType.WOOD, wood)
            log += f"collected {wood} wood"
        
        elif action == ActionSpace.CLAY_PIT:
            brick = self._gather_resource(worker_count, 4, player)
            player.resources.add(ResourceType.BRICK, brick)
            log += f"collected {brick} brick"
        
        elif action == ActionSpace.QUARRY:
            stone = self._gather_resource(worker_count, 5, player)
            player.resources.add(ResourceType.STONE, stone)
            log += f"collected {stone} stone"
        
        elif action == ActionSpace.RIVER:
            gold = self._gather_resource(worker_count, 6, player)
            player.resources.add(ResourceType.GOLD, gold)
            log += f"collected {gold} gold"
        
        elif action == ActionSpace.FARM:
            player.food_track += 1
            log += f"increased food production to {player.food_track}"
        
        elif action == ActionSpace.TOOL_MAKER:
            player.add_tool()
            log += f"gained a tool (tools: {player.tools})"
        
        elif action == ActionSpace.HUT:
            for _ in range(worker_count):
                player.add_worker()
            log += f"gained {worker_count} worker(s) (total: {player.workers})"
        
        elif action == ActionSpace.CIVILIZATION_CARD:
            card = game_state.board.get_available_civilization_card()
            if card:
                player.civilization_cards.append(card)
                log += f"took {card}"
            else:
                log += "no cards available"
        
        elif action == ActionSpace.BUILDING:
            building = self._choose_building(game_state)
            if building:
                player.resources.spend(building.cost)
                player.buildings.append(building)
                log += f"built {building}"
            else:
                log += "couldn't afford any building"
        
        return log
    
    def _gather_resource(self, worker_count: int, dice_sides: int, player: Player) -> int:
        """
        Simulate resource gathering with dice rolls.
        Each worker rolls a die, and we can use tools to improve results.
        """
        total = 0
        
        # Roll dice for each worker
        for _ in range(worker_count):
            roll = random.randint(1, dice_sides)
            total += roll
        
        # Optionally use tools to improve results
        if player.tools:
            # Use the best tool available
            tool_bonus = max(player.tools)
            total += tool_bonus
        
        # Divide by dice sides to get resource count
        resources = total // dice_sides
        return max(1, resources)  # At least 1 resource
    
    def _choose_building(self, game_state: GameState) -> Optional[Building]:
        """Choose which building to build (if affordable)"""
        player = game_state.players[self.player_index]
        
        # Find the most valuable affordable building
        best_building = None
        best_index = -1
        best_points = 0
        
        for i, building in enumerate(game_state.board.buildings):
            if player.resources.can_afford(building.cost):
                if building.points > best_points:
                    best_building = building
                    best_index = i
                    best_points = building.points
        
        if best_building:
            return game_state.board.get_available_building(best_index)
        
        return None
