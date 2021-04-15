"""
This is the main game file contains the relevant execution of a PyGame
interface for the game.
"""

import pygame as pg
from pygame.colordict import THECOLORS
from map import GameMap
from player import Player
from path import Path
from typing import Tuple, Any, List

GRID_SIZE: 40


def draw_grid(screen: pg.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    """
    color = THECOLORS['grey']
    width, height = screen.get_size()

    for col in range(1, GRID_SIZE):
        x = col * (width // GRID_SIZE)
        pg.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, GRID_SIZE):
        y = row * (height // GRID_SIZE)
        pg.draw.line(screen, color, (0, y), (width, y))


def run_game() -> None:
    screen = pg.display.set_mode((800, 800))
    screen.fill((191, 192, 150))
    exit_game = False
    pg.init()

    # TODO: Finish this module
    while not exit_game:
        for event in pg.event.get():
            draw_grid(screen)
            if event.type == pg.QUIT:
                exit_game = True

        for o in obstacles:
            pg.draw.rect(screen, object_types[o[1]][0], o[0])
        for t in treasures:
            pg.draw.rect(screen, object_types[t[1]][0], t[0])
        for f in fragments:
            pg.draw.rect(screen, object_types[f[1]][0], f[0])

        pg.display.flip()

    pg.quit()
