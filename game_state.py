"""
Stone Age Game State Module

This module defines the core game state including board setup, player state,
and resource management for the Stone Age board game simulation.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
import random


class ResourceType(Enum):
    """Types of resources in the game"""
    WOOD = "Wood"
    BRICK = "Brick"
    STONE = "Stone"
    GOLD = "Gold"
    FOOD = "Food"


class ActionSpace(Enum):
    """Available action spaces on the board"""
    FOREST = "Forest"  # Collect wood
    CLAY_PIT = "Clay Pit"  # Collect brick
    QUARRY = "Quarry"  # Collect stone
    RIVER = "River"  # Collect gold
    HUNTING_GROUNDS = "Hunting Grounds"  # Collect food
    FARM = "Farm"  # Increase food production
    TOOL_MAKER = "Tool Maker"  # Get tools
    HUT = "Hut"  # Get more workers
    CIVILIZATION_CARD = "Civilization Card"  # Take a civilization card
    BUILDING = "Building"  # Build a building


@dataclass
class Resources:
    """Player's resource inventory"""
    wood: int = 0
    brick: int = 0
    stone: int = 0
    gold: int = 0
    food: int = 0

    def add(self, resource_type: ResourceType, amount: int):
        """Add resources"""
        if resource_type == ResourceType.WOOD:
            self.wood += amount
        elif resource_type == ResourceType.BRICK:
            self.brick += amount
        elif resource_type == ResourceType.STONE:
            self.stone += amount
        elif resource_type == ResourceType.GOLD:
            self.gold += amount
        elif resource_type == ResourceType.FOOD:
            self.food += amount

    def can_afford(self, cost: Dict[ResourceType, int]) -> bool:
        """Check if player has enough resources"""
        for resource_type, amount in cost.items():
            if resource_type == ResourceType.WOOD and self.wood < amount:
                return False
            elif resource_type == ResourceType.BRICK and self.brick < amount:
                return False
            elif resource_type == ResourceType.STONE and self.stone < amount:
                return False
            elif resource_type == ResourceType.GOLD and self.gold < amount:
                return False
        return True

    def spend(self, cost: Dict[ResourceType, int]):
        """Spend resources"""
        for resource_type, amount in cost.items():
            if resource_type == ResourceType.WOOD:
                self.wood -= amount
            elif resource_type == ResourceType.BRICK:
                self.brick -= amount
            elif resource_type == ResourceType.STONE:
                self.stone -= amount
            elif resource_type == ResourceType.GOLD:
                self.gold -= amount

    def total_value(self) -> int:
        """Calculate total resource value"""
        return self.wood + self.brick + self.stone + self.gold


@dataclass
class CivilizationCard:
    """Represents a civilization card"""
    name: str
    points: int
    immediate_bonus: str = ""
    
    def __repr__(self):
        return f"{self.name} ({self.points}pts)"


@dataclass
class Building:
    """Represents a building tile"""
    name: str
    cost: Dict[ResourceType, int]
    points: int
    
    def __repr__(self):
        return f"{self.name} ({self.points}pts)"


@dataclass
class Player:
    """Represents a player in the game"""
    name: str
    workers: int = 5
    food_track: int = 0  # Permanent food production
    tools: List[int] = field(default_factory=lambda: [])  # Tool values
    resources: Resources = field(default_factory=Resources)
    civilization_cards: List[CivilizationCard] = field(default_factory=list)
    buildings: List[Building] = field(default_factory=list)
    score: int = 0
    
    def available_workers(self) -> int:
        """Get number of available workers"""
        return self.workers
    
    def can_feed_workers(self) -> bool:
        """Check if player can feed all workers"""
        required_food = self.workers
        available_food = self.resources.food + self.food_track
        return available_food >= required_food
    
    def feed_workers(self) -> int:
        """Feed workers and return penalty if unable"""
        required_food = self.workers
        available_food = self.resources.food + self.food_track
        
        if available_food >= required_food:
            # Use food track first, then resources
            used_from_track = min(self.food_track, required_food)
            used_from_resources = required_food - used_from_track
            self.resources.food -= used_from_resources
            return 0
        else:
            # Take penalty for each missing food
            penalty = (required_food - available_food) * 10
            self.score = max(0, self.score - penalty)
            self.resources.food = 0
            return penalty
    
    def add_tool(self):
        """Add a new tool"""
        if len(self.tools) < 3:
            self.tools.append(1)
        else:
            # Upgrade existing tools
            for i in range(len(self.tools)):
                if self.tools[i] < 4:
                    self.tools[i] += 1
                    break
    
    def add_worker(self):
        """Add a new worker"""
        if self.workers < 10:
            self.workers += 1
    
    def use_tool(self, index: int) -> int:
        """Use a tool and return its value"""
        if 0 <= index < len(self.tools):
            return self.tools[index]
        return 0
    
    def calculate_final_score(self) -> int:
        """Calculate final score including civilization cards and buildings"""
        total = self.score
        
        # Add points from civilization cards
        for card in self.civilization_cards:
            total += card.points
        
        # Add points from buildings
        for building in self.buildings:
            total += building.points
        
        # Resource bonus: 1 point per resource
        total += self.resources.total_value()
        
        return total


@dataclass
class Board:
    """Represents the game board"""
    civilization_cards: List[CivilizationCard] = field(default_factory=list)
    buildings: List[Building] = field(default_factory=list)
    action_spaces: Dict[ActionSpace, int] = field(default_factory=dict)  # Space -> max workers
    placed_workers: Dict[ActionSpace, List[int]] = field(default_factory=dict)  # Space -> player indices
    
    def __post_init__(self):
        """Initialize board with default configuration"""
        # Set up action spaces with worker limits
        self.action_spaces = {
            ActionSpace.FOREST: 7,
            ActionSpace.CLAY_PIT: 7,
            ActionSpace.QUARRY: 7,
            ActionSpace.RIVER: 7,
            ActionSpace.HUNTING_GROUNDS: 7,
            ActionSpace.FARM: 1,
            ActionSpace.TOOL_MAKER: 1,
            ActionSpace.HUT: 2,
            ActionSpace.CIVILIZATION_CARD: 1,
            ActionSpace.BUILDING: 1,
        }
        
        # Initialize placed workers tracking
        for space in self.action_spaces:
            self.placed_workers[space] = []
        
        # Initialize civilization cards
        self._setup_civilization_cards()
        
        # Initialize buildings
        self._setup_buildings()
    
    def _setup_civilization_cards(self):
        """Create the civilization card deck"""
        cards = [
            CivilizationCard("Agriculture", 14),
            CivilizationCard("Art", 12),
            CivilizationCard("Medicine", 10),
            CivilizationCard("Pottery", 8),
            CivilizationCard("Music", 15),
            CivilizationCard("Writing", 13),
            CivilizationCard("Weaving", 9),
            CivilizationCard("Transport", 11),
        ]
        random.shuffle(cards)
        self.civilization_cards = cards
    
    def _setup_buildings(self):
        """Create the building tiles"""
        buildings = [
            Building("Simple Hut", {ResourceType.WOOD: 3}, 6),
            Building("Field", {ResourceType.WOOD: 2, ResourceType.BRICK: 2}, 8),
            Building("Shelter", {ResourceType.STONE: 3}, 10),
            Building("House", {ResourceType.WOOD: 2, ResourceType.STONE: 2}, 11),
            Building("Lodge", {ResourceType.BRICK: 3, ResourceType.STONE: 2}, 14),
            Building("Palace", {ResourceType.STONE: 4, ResourceType.GOLD: 2}, 18),
        ]
        random.shuffle(buildings)
        self.buildings = buildings[:4]  # Only 4 buildings available at a time
    
    def can_place_workers(self, space: ActionSpace, count: int) -> bool:
        """Check if workers can be placed on this space"""
        current = len(self.placed_workers[space])
        max_workers = self.action_spaces[space]
        return current + count <= max_workers
    
    def place_workers(self, space: ActionSpace, player_index: int, count: int) -> bool:
        """Place workers on an action space"""
        if self.can_place_workers(space, count):
            for _ in range(count):
                self.placed_workers[space].append(player_index)
            return True
        return False
    
    def clear_workers(self):
        """Clear all placed workers from the board"""
        for space in self.action_spaces:
            self.placed_workers[space] = []
    
    def get_available_civilization_card(self) -> Optional[CivilizationCard]:
        """Get and remove a civilization card from the deck"""
        if self.civilization_cards:
            return self.civilization_cards.pop(0)
        return None
    
    def get_available_building(self, index: int) -> Optional[Building]:
        """Get and remove a building from available tiles"""
        if 0 <= index < len(self.buildings):
            return self.buildings.pop(index)
        return None


class GameState:
    """Main game state class"""
    
    def __init__(self, num_players: int = 2):
        self.players = [Player(f"Player {i+1}") for i in range(num_players)]
        self.board = Board()
        self.current_round = 0
        self.max_rounds = 10
        self.starting_player = 0
    
    def is_game_over(self) -> bool:
        """Check if the game is over"""
        return self.current_round >= self.max_rounds or len(self.board.civilization_cards) == 0
    
    def get_winner(self) -> Player:
        """Determine the winner"""
        winner = None
        max_score = -1
        
        for player in self.players:
            final_score = player.calculate_final_score()
            if final_score > max_score:
                max_score = final_score
                winner = player
        
        return winner
