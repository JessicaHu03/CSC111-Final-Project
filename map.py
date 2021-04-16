"""
This file contains the necessary classes and methods for a game map.
Incorporating the generation and placement of game objects
"""
from typing import Tuple, Any, Dict, List
import pygame as pg
import numpy as np
import random


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
    _div: int
    _obstacles: List[Tuple[pg.Rect, str]]
    _fragments: List[pg.Rect]
    _treasures: List[pg.Rect]
    _obstacle_info: List[Tuple[int, ...]]
    _fragment_info: List[Tuple[int, ...]]
    _treasure_info: List[Tuple[int, ...]]
    _object_type: Dict[str, Any]

    def __init__(self, difficulty: int, screen_size: Tuple[int, int], div: int, autogen: bool):
        """Initializes GameMap object with the given game difficulty, movement step size,
        and window size"""
        self._width = screen_size[0]
        self._height = screen_size[1]
        self._difficulty = difficulty
        self._h_step = int(self._width / div)
        self._v_step = int(self._height / div)
        self._div = div
        self._object_type = {
            'rock': ((236, 217, 199), 2),
            'river': ((90, 164, 174), 3),
            'fragment': ((193, 44, 31), 1),
            'treasure': ((248, 188, 49), 1/2)
        }
        if autogen:
            self.generate_obstacles()
            self.generate_treasures()

    def get_obstacles(self) -> List[Tuple[pg.Rect, str]]:
        """Return the generated obstacles of this map"""
        return self._obstacles

    def get_fragments(self) -> List[pg.Rect]:
        """Return the generated fragments of this map"""
        return self._fragments

    def get_treasures(self) -> List[pg.Rect]:
        """Return the generated treasures of this map"""
        return self._treasures

    def get_object_types(self) -> Dict[str, Any]:
        return self._object_type

    def get_step(self) -> Tuple[int, int]:
        return self._h_step, self._v_step

    def get_difficulty(self) -> int:
        """Return the difficulty of this map"""
        return self._difficulty

    def get_screen_size(self) -> Tuple[int, int]:
        """Return the width and height of the screen"""
        return self._width, self._height

    def generate_obstacles(self) -> None:
        """Generates the obstacles on the map with the required obstacle types.

        Calling this function will not update the obstacles attribute of the map.
        As it is only meant to be called in the initialization of the game map.
        """
        col_width = (6 - self._difficulty) * self._h_step * 2
        col_num = int(self._width / col_width) + 1
        col_count = 1
        obstacles = []
        obstacle_col = []
        obstacle_heights = []
        obstacle_col_info = []
        obstacle_info = []

        while col_count < col_num:

            obstacle = random.choice(['rock', 'river'])

            rect_gen, rect_info = self._generate_helper(col_count, obstacle)

            obstacle_heights.append((rect_info[1], rect_info[3]))

            y = np.arange(0, self._height)
            for x in obstacle_heights:
                remove_range(x[0], x[1], y)

            if len(obstacle_col) >= self._difficulty * 2\
                    or len(y) <= (6 - self._difficulty) * self._v_step:
                obstacle_info.extend(obstacle_col_info)
                obstacles.extend(obstacle_col)
                col_count += 1
                obstacle_col.clear()
                obstacle_col_info.clear()
                obstacle_heights.clear()
            else:
                obstacle_col_info.append(rect_info)
                obstacle_col.append((rect_gen, obstacle))

        self._obstacle_info = obstacle_info
        self._obstacles = obstacles

    def generate_treasures(self):
        """Generates treasure objects (fragments and a treasure chest)"""
        num_fragments = self._difficulty * 3
        num_treasures = self._difficulty
        col_width = (6 - self._difficulty) * self._h_step * 2
        list_obstacles = [o[0] for o in self._obstacles]
        list_fragments = []
        list_treasures = []
        fragments = []
        treasures = []
        fragment_info = []
        treasure_info = []
        frag_count = 0
        treasure_count = 0

        while frag_count < num_fragments:
            """Generating key fragments"""
            # All this does is putting the fragments in the middle of the grid lines
            x = int((col_width + 2 * self._h_step + self._h_step / 2) +
                    random.randint(1, int(self._div - (col_width + 2 * self._h_step) / self._h_step - 2))
                    * self._h_step)
            y = int(self._v_step / 2 + random.randint(1, self._div - 2) * self._v_step)

            rect_x = int(self._h_step)
            rect_y = int(rect_x * self._object_type['fragment'][1])

            fragment_rect = pg.Rect(x, y, rect_x, rect_y)

            if fragment_rect.collidelist(list_obstacles) == -1:
                if fragment_rect.collidelist(list_fragments) == -1:
                    list_fragments.append(fragment_rect)
                    fragment_info.append((x, y, rect_x, rect_y))
                    fragments.append(fragment_rect)
                    frag_count += 1

        while treasure_count < num_treasures:
            x = int((col_width + 2 * self._h_step) +
                    (random.randint(1, int(self._div - (col_width + 2 * self._h_step) / self._h_step - 4)) + 0.5)
                    * self._h_step)
            y = int((random.randint(2, self._div - 2) + 0.5) * self._v_step)

            rect_x = int(self._h_step * 2)
            rect_y = int(rect_x * self._object_type['treasure'][1])

            treasure_rect = pg.Rect(x, y, rect_x, rect_y)

            if treasure_rect.collidelist(list_obstacles) == -1:
                if treasure_rect.collidelist(list_fragments) == -1:
                    if treasure_rect.collidelist(list_treasures) == -1:
                        list_treasures.append(treasure_rect)
                        treasure_info.append((x, y, rect_x, rect_y))
                        treasures.append(treasure_rect)
                        treasure_count += 1

        self._fragments, self._treasures = fragments, treasures
        self._fragment_info, self._treasure_info = fragment_info, treasure_info

    def _generate_helper(self, col_count: int, obstacle: str) -> Tuple[pg.Rect, Tuple[int, ...]]:
        """Generates a single obstacle object in the given column"""
        col_width = (6 - self._difficulty) * self._h_step * 2

        x = col_count * col_width + 2 * self._h_step
        y = random.randrange(0, int(0.9 * self._height), self._v_step)

        rect_x = col_width - self._h_step * 2
        rect_y = random.randint(1, self._object_type[obstacle][1]) * rect_x

        obstacle_rect = pg.Rect(x, y, rect_x, rect_y)

        return obstacle_rect, (x, y, rect_x, rect_y)


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



