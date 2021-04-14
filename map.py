"""
This file contains the necessary classes and methods for a game map.
Incorporating the generation and placement of game objects
"""
from typing import Tuple, Any, Dict
from pygame import THECOLORS
import pygame as pg
import numpy as np
import random
import time


class GameMap:
    """This represents a game map with the indicated obstacles and "difficulty" of the game.

    The difficulty attribute indicates how much the obstacles will occupy the map, or in other
    words how much of the map is not available for the path, and also how many treasures are
    needed to be found.
    """
    _width: int
    _height: int
    _difficulty: int
    _h_step: int
    _v_step: int
    _state: dict[str, int]
    _obstacle_type: dict[str, Any]

    def __init__(self, difficulty: int, screen_size: Tuple[int, int], div: int):
        """Initializes GameMap object with the given game difficulty, movement step size,
        and window size"""
        self._width = screen_size[0]
        self._height = screen_size[1]
        self._difficulty = difficulty
        self._h_step = int(self._width / div)
        self._v_step = int(self._height / div)
        self._state = {
            'keys': 0,
            'fragments': 0,
            'treasure': 1
        }
        self._obstacle_type = {
            'rock': (THECOLORS['brown'], 2),
            'river': (THECOLORS['blue'], 3)
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
        """
        col_width = (6 - self._difficulty) * self._h_step * 2
        col_num = int(self._width / col_width) + 1
        col_count = 1
        obstacles_ret = []
        obstacle_col = []
        obstacle_info = []

        while col_count < col_num:
            print("Generating obstacles on column:" + str(col_count), end='\r')
            time.sleep(0.1)
            obstacle = random.choice(list(self._obstacle_type.keys()))

            rect_gen, rect_height = self._generate_helper(col_count, obstacle)
            obstacle_col.append((rect_gen, obstacle))
            obstacle_info.append(rect_height)

            temp_col = [rect[0] for rect in obstacle_col]
            counter = 0
            for r in temp_col:
                if r.collidelistall(temp_col) != -1:
                    counter += 1
                    temp_col.remove(r)

            y = np.arange(0, self._height)
            for x in obstacle_info:
                remove_range(x[0], x[1], y)

            if counter >= self._difficulty * 2 or len(y) <= self._difficulty / 2 * self._v_step:
                obstacles_ret.extend(obstacle_col)
                col_count += 1
                obstacle_col.clear()
                obstacle_info.clear()

        return obstacles_ret

    def _generate_helper(self, col_count: int, obstacle: str):
        """Generates a single obstacle object in the given column"""
        col_width = (6 - self._difficulty) * self._h_step * 2

        x = col_count * col_width + 2 * self._h_step
        y = random.randrange(0, int(0.9 * self._height), self._v_step)

        rect_x = col_width - self._h_step * 2
        rect_y = random.randrange(rect_x, self._obstacle_type[obstacle][1] * rect_x, self._v_step)

        obstacle_rect = pg.Rect(x, y, rect_x, rect_y)

        return obstacle_rect, [y, y + rect_y]


# Helper functions
def remove_range(start: int, stop: int, lst: np.array) -> np.array:
    """Removes elements from the list that satisfy start <= element <= stop"""
    i = 0
    while i < len(lst):
        if start <= lst[i] <= stop:
            lst = np.delete(lst, i)
            i -= 1
        i += 1

    return lst


def len_largest_interval(lst: np.array) -> int:
    """Return the continuous interval(increment of 1) of greatest length from a
    given list"""
    counter = 1
    max_len = 0

    for i in range(len(lst) - 1):
        if lst[i+1] - lst[i] == 1:
            counter += 1
        else:
            if counter > max_len:
                max_len = counter
            counter = 1

    return max_len



