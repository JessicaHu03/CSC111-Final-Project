"""This file contains the main game"""
from typing import List, Tuple, Optional
from player import Player
from map import GameMap
from path import Path
import os
import pandas as pd


class Game:
    """Game Class

    This is not for a single game instance. Instead, this is the entire collection.
    It is used to save, retrieve, and modify any player, map, paths.
    """
    path: Path
    player: Player
    game_map: GameMap
    map_list: List[GameMap]
    path_list: List[Path]
    player_list: List[Player]
    screen_size: Tuple[int, int]
    player_rect: Tuple[int, int]
    div: int

    def __init__(self, screen_size: Optional[Tuple[int, int]] = (800, 800), div: Optional[int] = 40):
        """Initializes game instance."""
        self.player_rect = (8, 8)
        self.screen_size = screen_size
        self.div = div
        self.map_list = []
        self.path_list = []
        self.player = Player('Default')

    def set_map(self, map_id):
        """Set the current map given the map index"""
        assert map_id < len(self.map_list)
        self.game_map = self.map_list[map_id - 1]

    def reset_path(self):
        """Resets the current path of the game"""
        pos = (int(self.screen_size[0] / self.div - self.player_rect[0] / 2),
               int(self.screen_size[1] / 2 - self.player_rect[1] / 2))
        self.path = Path(initial_pos=pos, map_id=self.game_map.map_id, player_id=self.player.player_id)

    def generate_maps(self, num: int, difficulty: int) -> None:
        """Generates a set number of maps, which are saved to 'maps/'"""
        for _ in range(num):
            new_map = GameMap(self.screen_size, self.div, True, difficulty)
            new_map.write_map()

    def add_player(self, player_id):
        self.player_list.append(player_id)

    def read(self) -> None:
        """Read from all data"""
        map_num = len([m for m in os.listdir('maps/')])
        path_num = len([m for m in os.listdir('paths/')])
        # Reading game maps
        if map_num != 0:
            for i in range(1, map_num + 1):
                map_name = 'map{}'.format(i)

                new_map = GameMap(self.screen_size, self.div, False)
                new_map.read_map(map_name)
                self.map_list.append(new_map)

        # Reading paths
        if path_num != 0:
            for i in range(1, path_num + 1):
                path_name = 'path{}.csv'.format(i)
                path_dir = os.path.join(r'paths\\', path_name)

                pos = (int(self.screen_size[0] / self.div - self.player_rect[0] / 2),
                       int(self.screen_size[1] / 2 - self.player_rect[1] / 2))

                new_path = Path(initial_pos=pos)
                new_path.read_path(path_dir)
                self.path_list.append(new_path)

    def write(self) -> None:
        """Writes all data into file"""
        for game_map in self.map_list:
            game_map.write_map()
        for path in self.path_list:
            path.write_path()




