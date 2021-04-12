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

    def generate_obstacles():
        """Generates the obstacles on the map with the required obstacle types.
        """
        difficulty = 2
        width = 800
        height = 800
        step = int(width / 40)
        obstacle_col = difficulty * 4
        obstacle_type = ['mountain', 'river']
        origin_x = 0
        col_num = 1
        obstacles = []
        finish_gen = False
        x = 0

        while col_num <= obstacle_col and not finish_gen:
            # obstacle = random.choice(obstacle_type)

            col_left = obstacle_col

            # rect_x = 0
            x = round_ten(random.randint(origin_x + int(step),
                                         origin_x + int(step) + int(width / (difficulty * 10))))
            y = round_ten(random.randint(int(step * 3), int(height * 0.5)))

            if x < width * 0.9:
                rect_x = round_ten(random.randint(int(width / obstacle_col * 0.2), int(width / obstacle_col)))
                rect_y = round_ten(random.randint(int(height * 0.2), int(height * 0.75)))
                if x + rect_x > 800:
                    rect_x = 800 - x

                obstacle_rect = pg.Rect(x, y, rect_x, rect_y)
                obstacles.append(obstacle_rect)

                origin_x = (x + rect_x)
                col_num += 1
                col_left -= 1
            else:
                finish_gen = True

        return obstacles



