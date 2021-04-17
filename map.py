"""
This file contains the necessary classes and methods for a game map.
Incorporating the generation and placement of game objects
"""
from typing import Tuple, Any, Dict, List, Optional
import pygame as pg
import numpy as np
import pandas as pd
import random
import os


class GameMap:
    """This represents a game map with the indicated obstacles and "difficulty" of the game.

    The difficulty attribute indicates the number of obstacles that will occupy the map,
    and how many fragments and treasures are needed to be found.
    """
    id: int
    _width: int
    _height: int
    _difficulty: int
    _h_step: int
    _v_step: int
    _div: int
    _obstacles: List[Tuple[pg.Rect, str]]
    _fragments: List[pg.Rect]
    _treasures: List[pg.Rect]
    _obstacle_info: List[Tuple[Tuple[int, ...], str]]
    _fragment_info: List[Tuple[int, ...]]
    _treasure_info: List[Tuple[int, ...]]
    _object_type: Dict[str, Any]

    def __init__(self, screen_size: Tuple[int, int], div: int, autogen: bool, difficulty: Optional[int] = 4):
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
        self._obstacles = list()
        self._treasures = list()
        self._fragments = list()
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
        """Returns the relevant information for each type of game object"""
        return self._object_type

    def get_object_info(self) -> Tuple[Any, ...]:
        """Returns the rect object information for each type"""
        return self._obstacle_info, self._fragment_info, self._treasure_info

    def get_step(self) -> Tuple[int, int]:
        return self._h_step, self._v_step

    def get_difficulty(self) -> int:
        """Return the difficulty of this map"""
        return self._difficulty

    def get_screen_size(self) -> Tuple[int, int]:
        """Return the width and height of the screen"""
        return self._width, self._height

    def generate_objects_from_info(self) -> None:
        """This is for using the information read from a map file to generate relevant
        game objects. However it uses its own attributes(e.g. self._obstacle_info) as
        that's where the information is saved to"""
        # Iterates through the obstacle object information to generate
        # new obstacle rectangles with their relevant type assigned.
        obstacles = []
        for rect, types in self.get_object_info()[0]:
            obstacle_rect = pg.Rect(rect)
            obstacles.append((obstacle_rect, types))
        self._obstacles = obstacles
        # Iterates through the fragment objects information to generate
        # new fragment rectangles.
        fragments = []
        for rect in self.get_object_info()[1]:
            fragment_rect = pg.Rect(rect)
            fragments.append(fragment_rect)
        self._fragments = fragments
        # Iterates through the treasure objects information to generate
        # new treasure rectangles.
        treasures = []
        for rect in self.get_object_info()[2]:
            treasure_rect = pg.Rect(rect)
            treasures.append(treasure_rect)
        self._treasures = treasures

    def generate_obstacles(self) -> None:
        """Generates the obstacles on the map with the required obstacle types.

        Calling this function updates the obstacles attribute of the map. This is only
        meant to be called in the initialization of the game map with autogen=True.
        """
        col_width = (6 - self._difficulty) * self._h_step * 2
        col_num = int(self._width / col_width) + 1
        col_count = 1
        obstacles = []
        obstacles_list = []
        obstacle_col = []
        obstacle_heights = []
        obstacle_col_info = []
        obstacle_info = []

        while col_count < col_num:

            obstacle = random.choice(['rock', 'river'])

            rect_gen, rect_info = self._generate_helper(col_count, obstacle)

            obstacle_heights.append((rect_info[1], rect_info[3]))

            # Generates a new list from 0 to height (0, 1, 2, 3,...,height).
            y = np.arange(0, self._height)
            # For each rectangle generated, its height range is removed from the list.
            # e.g. Rectangle that occupies from y = 200 to y = 400 will remove that range,
            # which then becomes (0, 1, 2,...,198,199, 401, 402,...,height)
            for x in obstacle_heights:
                y = remove_range(x[0], x[0] + x[1], y)

            # Checks whether total number of obstacles is reached either by game difficulty settings
            # or if there is no space left for the player to go through if the rectangle is added.
            if len(obstacle_col) >= (self._difficulty * 2) or len(y) <= ((6 - self._difficulty) * self._v_step):
                # Adds the column of obstacles to the list of all obstacles
                obstacle_info.extend(obstacle_col_info)
                obstacles.extend(obstacle_col)
                col_count += 1
                # Resets the column
                print("col num:" + str(col_count))
                print(y)
                obstacle_col.clear()
                obstacle_col_info.clear()
                obstacle_heights.clear()
            else:
                # If above conditions are not met, add a new obstacle to the column
                if rect_gen.collidelist(obstacles_list) == -1:
                    obstacle_col_info.append((rect_info, obstacle))
                    obstacle_col.append((rect_gen, obstacle))
                    print(len(obstacle_col))
                    obstacles_list.append(rect_gen)

        self._obstacle_info = obstacle_info
        self._obstacles = obstacles

    def generate_treasures(self):
        """Generates treasure objects (fragments and treasure chests)

        Note that contrary to obstacle generation, where each rect is generated
        in columns, this is random, and takes range for almost the entire map.
        """
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
            # Generating Key fragments
            # All object generations start at a certain point a few steps from the left

            # All this does is putting the fragments in the middle of the grid lines
            x = int((col_width + 2 * self._h_step + self._h_step / 2) +
                    random.randint(1, int(self._div - (col_width + 2 * self._h_step) / self._h_step - 2))
                    * self._h_step)
            y = int(self._v_step / 2 + random.randint(1, self._div - 2) * self._v_step)

            rect_x = int(self._h_step)
            rect_y = int(rect_x * self._object_type['fragment'][1])

            # Generate Rectangle object from given coordinates and size
            fragment_rect = pg.Rect(x, y, rect_x, rect_y)

            # Check collision with existing game objects
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

            # Generate Rectangle object from given coordinates and size
            treasure_rect = pg.Rect(x, y, rect_x, rect_y)

            # Check collision with existing game objects
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
        """Generates a single obstacle object in the given column. This is for obstacles only"""
        col_width = (6 - self._difficulty) * self._h_step * 2

        x = col_count * col_width + 2 * self._h_step
        y = random.randrange(0, int(0.9 * self._height), self._v_step)

        rect_x = col_width - self._h_step * 2
        rect_y = random.randint(1, self._object_type[obstacle][1]) * rect_x

        # Generate Rectangle object from given coordinates and size
        obstacle_rect = pg.Rect(x, y, rect_x, rect_y)

        return obstacle_rect, (x, y, rect_x, rect_y)

    def write_map(self) -> None:
        """Save the current map information to a new file under directory 'maps', with name map[num].csv"""
        # Returns number of existing maps from directory
        map_num = len([m for m in os.listdir('maps/')])
        self.id = map_num + 1
        # Retrieves specific object information, save to dataframe
        obstacle_info = pd.DataFrame({'obstacle': [x[0] for x in self.get_object_info()[0]]})
        obstacle_type = pd.DataFrame({'obstacle_type': [x[1] for x in self.get_object_info()[0]]})
        fragment_info = pd.DataFrame({'fragment': self.get_object_info()[1]})
        treasure_info = pd.DataFrame({'treasure': self.get_object_info()[2]})

        # Retrieves difficulty setting
        settings_info = pd.DataFrame({'difficulty': self.get_difficulty()}, index=[0])

        # Concatenate all information to a single dataframe. This may be bad practice, for that
        # the elements from one row aren't correlated, and there is a different number of observations
        # per variable. Using Pandas here is just for code cleanliness and computational simplicity.
        object_info = pd.concat([obstacle_info, obstacle_type, treasure_info, fragment_info, settings_info],
                                axis=1, ignore_index=False)

        # Sets new map name. This is given by 'maps' + the map index.
        map_name = 'map{}.csv'.format(self.id)
        # Saves map file to directory
        object_info.to_csv(os.path.join(r'maps\\', map_name), index=False)

    def read_map(self, map_file: str):
        """Reads a game map from file, retrieving all relevant information required
        to generate a map"""
        # Reading game_map type file
        df = pd.read_csv(map_file, index_col=False)

        # Retrieve game objects and settings for map, indexing by column name
        # The concatenation of different length DataFrames result in NA values,
        # thus they need to be removed.
        obstacles = df['obstacle'].dropna().tolist()
        obstacle_type = df['obstacle_type'].dropna().tolist()
        treasures = df['treasure'].dropna().tolist()
        fragments = df['fragment'].dropna().tolist()
        difficulty = int(df['difficulty'][0])

        # Each value of the DataFrame is of type string, except for the difficulty.
        # Thus, by evaluating each returns the tuple objects.
        obstacle_info = [eval(rect) for rect in obstacles]
        treasure_info = [eval(rect) for rect in treasures]
        fragment_info = [eval(rect) for rect in fragments]

        # Concatenate the obstacle rect to their relevant type
        assert len(obstacle_info) == len(obstacle_type)
        obstacle_concat = []
        for i in range(len(obstacle_info)):
            obstacle_concat.append((obstacle_info[i], obstacle_type[i]))

        # Save the game objects and settings to the current game map
        obstacle_info_concat = obstacle_concat
        self._obstacle_info = obstacle_info_concat
        self._treasure_info = treasure_info
        self._fragment_info = fragment_info
        self._difficulty = difficulty
        self.generate_objects_from_info()


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



