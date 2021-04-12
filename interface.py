"""
This is the main game file contains the relevant execution of a PyGame
interface for the game.
"""

import pygame
from pygame.colordict import THECOLORS

pygame.init()
SCREEN = pygame.display.set_mode((1200, 1000))
GRID_SIZE = 8
EXIT = False


def draw_grid(screen: pygame.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    """
    color = THECOLORS['grey']
    width, height = screen.get_size()

    for col in range(1, GRID_SIZE):
        x = col * (width // GRID_SIZE)
        pygame.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, GRID_SIZE):
        y = row * (height // GRID_SIZE)
        pygame.draw.line(screen, color, (0, y), (width, y))

def run_game() -> None:
    # TODO: Finish this module
    while not EXIT:
        for event in pygame.event.get():
            draw_grid(SCREEN)
            if event.type == pygame.QUIT:
                EXIT = True
        pygame.display.flip()

    pygame.quit()
