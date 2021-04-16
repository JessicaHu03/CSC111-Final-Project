"""This file contains the main game"""
from player import Player
from map import GameMap
from path import Path


class Game:
    """Game class"""
    path: Path
    player: Player
    game_map: GameMap

    def __init__(self, game_map: GameMap, path: Path, player: Player):
        self.path = path
        self.player = player
        self.game_map = game_map
        self.show_all = False
        
    def set_show(self, value: bool):
        self.show_all = value
