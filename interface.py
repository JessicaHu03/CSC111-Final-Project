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
from game import Game

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

def meet_treasure(game_map: GameMap, cur_pos: Tuple[int, int]) -> bool:
    """Return whether the player has met a treasure with current movement."""
    if self._player.collidelist(game_map.get_treasures()):
        return True
    return False


def meet_fragment(game_map: GameMap, step: int) -> bool:
    """Return whether the player has met a key fragment with current movement."""


def get_possible_movement(game_map: GameMap, h_step: int, v_step: int) -> List[str]:
    """Calculate possible movement the player can make based on
    current position in the given game map."""
    movements = ['right', 'left', 'up', 'down']
    possible_movements = []
    for move in movements:
        next_pos = Game.path.next_pos(move, h_step, v_step)
        check = []


    return possible_movements


def run_game() -> None:
    # TODO: Finish this module
    pg.display.set_caption("Treasure Hunt Game!")
    screen = pg.display.set_mode((800, 800))
    screen.fill((191, 192, 150))
    exit_game = False
    pg.init()

    cur_pos = Game.player.get_pos()
    h_step, v_step = Game.map.get_step()
    possible_mov = []

    possible_next_pos = {'left': (cur_pos[0] - h_step - 4, cur_pos[1] - 4),
                         'right': (cur_pos[0] + h_step - 4, cur_pos[1] - 4),
                         'up': (cur_pos[0] - v_step - 4, cur_pos[1] - 4),
                         'down': (cur_pos[0] + v_step - 4, cur_pos[1] - 4)}
    obstacle_list = Game.map.get_obstacles()[0]
    for move in possible_next_pos:
        next_pos = possible_next_pos[move]
        next_rect = pg.Rect(next_pos, (8, 8))
        if next_rect.collidelistall(obstacle_list) == -1:
            possible_mov.append(move)

    rect_pos = (cur_pos[0] - 4, cur_pos - 4)

    player_rect = pg.Rect(rect_pos, (8, 8))
    pg.draw.rect(Game.map, (154, 167, 177), player_rect)
    new_pos = []

    while not exit_game:
        for event in pg.event.get():
            draw_grid(screen)
            if event.type == pg.QUIT:
                exit_game = True
            if event.type in possible_mov:
                if event.type == pg.K_LEFT:
                    new_pos = (cur_pos[0] - h_step, cur_pos[1])
                    player_rect.move(new_pos)
                if event.type == pg.K_RIGHT:
                    new_pos = (cur_pos[0] + h_step, cur_pos[1])
                    player_rect.move(new_pos)
                if event.type == pg.K_UP:
                    new_pos = (cur_pos[0] - v_step, cur_pos[1])
                    player_rect.move(new_pos)
                if event.type == pg.K_DOWN:
                    new_pos = (cur_pos[0] + v_step, cur_pos[1])
                    player_rect.move(new_pos)
                Game.path.update_path(new_pos)
                Game.player.update_pos(new_pos)

        for o in Game.obstacles:
            pg.draw.rect(screen, object_types[o[1]][0], o[0])
        for t in Game.treasures:
            pg.draw.rect(screen, object_types[t[1]][0], t[0])
        for f in Game.fragments:
            pg.draw.rect(screen, object_types[f[1]][0], f[0])

        pg.display.flip()

    pg.quit()



