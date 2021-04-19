"""
Main execution file for CSC111 Final Project
"""
from interface import GameDisplay
from game import Game


if __name__ == "__main__":
    screen_size = (800, 800)
    rect_size = (8, 8)
    game = Game()
    game.generate_maps(num=0, difficulty=2)
    game.read()

    interface = GameDisplay(screen_size)
    interface.run_game(game)
