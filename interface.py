"""
This is the main game file contains the relevant execution of a Pygame
interface for the game.
"""

import pygame as pg
from pygame.colordict import THECOLORS
from map import GameMap
from player import Player
from path import Path, Graph
from typing import Tuple, Any, List
from game import Game

GRID_SIZE = 40


def draw_grid(screen: pg.Surface) -> None:
    """Draws a square grid on the given surface.

    The drawn grid has GRID_SIZE columns and rows.
    """
    color = (0, 0, 0)
    width, height = screen.get_size()

    for col in range(1, GRID_SIZE):
        x = col * (width // GRID_SIZE)
        pg.draw.line(screen, color, (x, 0), (x, height))

    for row in range(1, GRID_SIZE):
        y = row * (height // GRID_SIZE)
        pg.draw.line(screen, color, (0, y), (width, y))


#
# def meet_treasure(game_map: gameMap, cur_pos: Tuple[int, int]) -> bool:
#     """Return whether the player has met a treasure with current movement."""
#     if _player.collidelist(game_map.get_treasures()):
#         return True
#     return False
# 
# 
# def meet_fragment(game_map: gameMap, step: int) -> bool:
#     """Return whether the player has met a key fragment with current movement."""


def run_game(game: Game) -> None:
    """Run game"""
    pg.display.set_caption("Treasure Hunt game!")
    screen = pg.display.set_mode((800, 800))
    exit_game = False
    pg.init()
    screen.fill((191, 192, 150))
    draw_grid(screen)

    pg.font.init()
    font1 = pg.font.SysFont('Comic Sans MS', 30)
    not_enough_fragments = 'You still need more fragments to open this treasure!'

    h_step, v_step = game.game_map.get_step()
    obstacle_list = [x[0] for x in game.game_map.get_obstacles()]
    treasure_list = [x[0] for x in game.game_map.get_treasures()]
    fragment_list = [x[0] for x in game.game_map.get_fragments()]

    object_type = game.game_map.get_object_types()
    for o in game.game_map.get_obstacles():
        pg.draw.rect(screen, object_type[o[1]][0], o[0])
    for t in game.game_map.get_treasures():
        pg.draw.rect(screen, object_type[t[1]][0], t[0])
    for f in game.game_map.get_fragments():
        pg.draw.rect(screen, object_type[f[1]][0], f[0])

    cur_pos = game.player.get_pos()
    possible_mov = []

    possible_next_pos = {'left': (cur_pos[0] - h_step - 4, cur_pos[1] - 4),
                         'right': (cur_pos[0] + h_step - 4, cur_pos[1] - 4),
                         'up': (cur_pos[0] - v_step - 4, cur_pos[1] - 4),
                         'down': (cur_pos[0] + v_step - 4, cur_pos[1] - 4)}

    for move in possible_next_pos:
        next_pos = possible_next_pos[move]
        next_rect = pg.Rect(next_pos, (8, 8))
        if next_rect.collidelistall(obstacle_list) == -1:
            possible_mov.append(move)

    rect_pos = (cur_pos[0] - 4, cur_pos[1] - 4)

    player_rect = pg.Rect(rect_pos, (8, 8))
    pg.draw.rect(screen, (154, 167, 177), player_rect)
    new_pos = []

    while not exit_game:
        for event in pg.event.get():
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
                game.path.update_path(new_pos)
                game.player.update_pos(new_pos)

                # if we meet a treasure
                if player_rect.collidelist(treasure_list):
                    # if we have more than 3 fragments when meet a treasure
                    if game.player.backpack['fragments'] >= 3:
                        game.player.update_backpack('treasures', 1)
                        game.player.update_backpack('fragments', -3)
                    # if we don't have enough fragments when meet a treasure
                    else:
                        text = font1.render(not_enough_fragments, False, (0, 0, 0))
                        screen.blit(text, (400, 200))
                # if we meet a fragment
                if player_rect.collidelist(fragment_list):
                    game.player.update_backpack('fragments', 1)

        pg.display.flip()

    pg.quit()
