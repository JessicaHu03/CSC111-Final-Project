"""
This file contains the necessary classes and methods for a game map.
Incorporating the generation and placement of game objects
"""
import pygame as pg
from typing import Iterable, Tuple, Any


class GameMap:
    """This represents a game map with the indicated obstacles and "difficulty" of the game.

    The difficulty attribute indicates how much the obstacles will occupy the map, or in other
    words how much of the map is not available for the path, and also how many treasures are
    needed to be found.
    """
    _width: int
    _height: int
    _difficulty: int
    _step_size: int
    _state: dict[str, int]

    def __init__(self, difficulty: int,
                 step_size: int,
                 screen_size: Tuple[int, int]):
        """Initializes GameMap object with the given game difficulty, movement step size,
        and window size"""
        self._width = screen_size[0]
        self._height = screen_size[1]
        self._difficulty = difficulty
        self._step_size = step_size
        self._state = {
            'keys': 0,
            'fragments': 0,
            'treasure': 1
        }

    def get_difficulty(self) -> int:
        """Return the difficulty of this map"""
        return self._difficulty

    def get_game_state(self, score_type: str) -> Any:
        """Return the game_state of this map"""
        if score_type == 'all':
            return self._state
        else:
            if score_type in self._state:
                return self._state[score_type]
            else:
                print("Invalid score type")

    def update_game_state(self, score_type: str, change: int) -> None:
        """Update game_state of this map"""
        if score_type in self._state:
            self._state[score_type] += change
        else:
            print("Invalid score type")

    def generate_obstacles(self):
        """Generates the obstacles on the map with the required obstacle types.

        includes: a list of required obstacle types (mountain, river...)
        """
        map_occupy = self._difficulty * 0.15
        size = self._width * self._height
        obstacle_size = 0

        while obstacle_size <= map_occupy * size:



