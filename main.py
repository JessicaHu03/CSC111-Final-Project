"""
Main execution file for CSC111 Final Project
"""
from interface import GameDisplay
from game import Game
from player import Player
from path import Path


if __name__ == "__main__":
    screen_size = (800, 800)
    game = Game()
    game.generate_maps(num=0, difficulty=2)
    game.read()

    interface = GameDisplay(screen_size)
    interface.run_game(game)
