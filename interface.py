"""
This is the main game file contains the relevant execution of a Pygame
interface for the game.
"""

import pygame as pg
from pygame.locals import *
from map import GameMap
from player import Player
from path import Path, Graph
from typing import Tuple
from game import Game
import time
import os


class GameDisplay:
    screen_size: Tuple[int, int]
    screen: pg.Surface
    clock: pg.time.Clock
    msg_font: pg.font.Font

    def __init__(self, screen_size: Tuple[int, int]):
        # Initializes PyGame Modules
        pg.init()

        self.screen_size = screen_size
        self.screen = pg.display.set_mode(screen_size)
        self.clock = pg.time.Clock()
        self.msg_font = pg.font.Font(None, 30)

    def draw_grid(self, div: int) -> None:
        """Draws a square grid on the given surface.

        The drawn grid has GRID_SIZE columns and rows.
        """
        color = (0, 0, 0)
        width, height = self.screen.get_size()

        for col in range(1, div):
            x = col * (width // div)
            pg.draw.line(self.screen, color, (x, 0), (x, height))

        for row in range(1, div):
            y = row * (height // div)
            pg.draw.line(self.screen, color, (0, y), (width, y))

    def message(self, text: str, font: pg.font, color: Tuple[int, ...], center_pos: Tuple[int, int]):
        pg.font.init()

        # Creates text object
        text_render = font.render(text, True, color)
        text_rect = text_render.get_rect()
        text_rect.center = center_pos

        # Displays text onto screen
        self.screen.blit(text_render, text_rect)

    def not_enough_fragment(self):
        text_off = False
        delay = 1500

        color = (0, 0, 0)
        center_pos = (int(self.screen_size[0] / 2), int(self.screen_size[1] * 0.25))
        text_str = "You still need more fragments to open this treasure!"

        while not text_off:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            self.message(text_str, self.msg_font, color, center_pos)

            pg.display.update()

            passed = self.clock.tick(60)
            delay -= passed
            if delay <= 0:
                text_off = True

    def show_score(self, game: Game):
        treasures = self.msg_font.render('Treasures:' + str(game.player.backpack['treasures']), True, (255, 255, 255))
        fragments = self.msg_font.render('Fragments:' + str(game.player.backpack['fragments']), True, (255, 255, 255))

        self.screen.blit(treasures, (50, 20))
        self.screen.blit(fragments, (50, 50))

    def game_end(self, num_steps: int):
        game_exit = False
        delay = 5000

        color = (0, 0, 0)
        center_pos1 = (int(self.screen_size[0] / 2), int(self.screen_size[1] / 2))
        center_pos2 = (int(self.screen_size[0] / 2), int(self.screen_size[1] * 0.65))
        text_str = "You have won!"
        text_str2 = "The number of steps you took this game was: {}".format(num_steps)

        while not game_exit:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    pg.quit()

            self.screen.fill((255, 255, 255))
            self.message(text_str, self.msg_font, color, center_pos1)
            self.message(text_str2, self.msg_font, color, center_pos2)

            pg.display.update()

            passed = self.clock.tick(60)
            delay -= passed
            if delay <= 0:
                game_exit = True

    def run_game(self, game: Game) -> None:
        """Runs the game"""

        # Defines player movement step size
        h_step, v_step = game.game_map.get_step()

        # Change in position according to movement event
        dir_key = {K_LEFT: (-h_step, 0), K_RIGHT: (h_step, 0), K_UP: (0, -v_step), K_DOWN: (0, v_step)}
        # Assign keys to movement names
        dir_name = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}
        # Assign keys to those for opposite direction. This is for reversing a move
        dir_opposite = {K_LEFT: K_RIGHT, K_RIGHT: K_LEFT, K_UP: K_DOWN, K_DOWN: K_UP}

        # Obtains game objects from the map
        obstacle_list_type = [(x[0], x[1]) for x in game.game_map.get_obstacles()]
        obstacle_list = [x[0] for x in game.game_map.get_obstacles()]
        treasure_list = game.game_map.get_treasures()
        fragment_list = game.game_map.get_fragments()

        pg.display.set_caption("Treasure Hunt game!")

        # Retrieves object types and their relevant information
        object_type = game.game_map.get_object_types()

        rect_size = (8, 8)
        rect_pos = game.player.initial_pos
        vision_radius = game.player.get_vision_radius()
        # This is for returning the player upon treasure collision with not enough fragments
        player_rect = pg.Rect(rect_pos, rect_size)

        # Game Loop
        show_all = False
        exit_game = False
        while not exit_game:
            game.player.update_pos(rect_pos)

            # Checks for possible movements given obstacles in the current map
            possible_movements = ['left', 'right', 'up', 'down']
            available_movements = []
            for move in possible_movements:
                new_pos = next_pos(rect_pos, move, h_step, v_step)
                new_rect = pg.Rect(new_pos, rect_size)
                if new_rect.collidelist(obstacle_list) == -1:
                    available_movements.append(move)

            event_key = None
            for event in pg.event.get():
                if event.type == QUIT:
                    exit_game = True
                    pg.quit()

                if event.type == KEYDOWN:
                    # Assign rectangle movements according to key event if movement is valid
                    if event.key in dir_key and dir_name[event.key] in available_movements:
                        event_key = event.key

                        pos_change = dir_key[event.key]
                        rect_pos = tuple(map(sum, zip(rect_pos, pos_change)))
                        player_rect.move_ip(pos_change)

                        game.path.update_path((int(rect_pos[0]), int(rect_pos[1])))

                    if event.key == K_f:
                        show_all = not show_all

            # Fills screen
            self.screen.fill((191, 192, 150))

            # Draws player rectangle object onto screen
            pg.draw.rect(self.screen, (255, 255, 255), player_rect)

            if show_all:
                # Draws all game objects onto screen if show_all is True
                for o in obstacle_list_type:
                    pg.draw.rect(self.screen, object_type[o[1]][0], o[0])
                for treasure in treasure_list:
                    pg.draw.rect(self.screen, (248, 188, 49), treasure)
                for fragment in fragment_list:
                    pg.draw.rect(self.screen, (193, 44, 31), fragment)
            else:
                # Otherwise, utilizes vision field function
                path_pos = game.path.all_pos()

                vision_rect_size = (rect_size[0] + 2 * vision_radius, rect_size[1] + 2 * vision_radius)
                vision_rect_pos = [(pos[0] - vision_radius, pos[1] - vision_radius) for pos in path_pos]

                vision_rects = [pg.Rect(pos, vision_rect_size) for pos in vision_rect_pos]

                for o in obstacle_list_type:
                    if o[0].collidelist(vision_rects) != -1:
                        pg.draw.rect(self.screen, object_type[o[1]][0], o[0])
                for treasure in treasure_list:
                    if treasure.collidelist(vision_rects) != -1:
                        pg.draw.rect(self.screen, (248, 188, 49), treasure)
                for fragment in fragment_list:
                    if fragment.collidelist(vision_rects) != -1:
                        pg.draw.rect(self.screen, (193, 44, 31), fragment)

            # Adds grid to the screen
            self.draw_grid(40)

            # Checks for fragment and treasure collision
            # Treasure Collision
            treasure_collision_index = player_rect.collidelist(treasure_list)
            if treasure_collision_index != -1:
                # With at least 3 fragments on treasure collision
                if game.player.backpack['fragments'] >= 3:
                    # Remove collided treasure from list
                    del treasure_list[treasure_collision_index]
                    game.player.update_backpack('treasures', 1)
                    game.player.update_backpack('fragments', -3)
                # Not enough fragments on treasure collision
                else:
                    # Moves player back to their last position
                    pos_change = dir_key[dir_opposite[event_key]]
                    rect_pos = tuple(map(sum, zip(rect_pos, pos_change)))
                    player_rect.move_ip(pos_change)
                    # Prints info message
                    self.not_enough_fragment()

            # Fragment Collision
            fragment_collision_index = player_rect.collidelist(fragment_list)
            if fragment_collision_index != -1:
                # remove collided fragment from list
                del fragment_list[fragment_collision_index]
                game.player.update_backpack('fragments', 1)

            # On winning game
            if game.player.backpack['treasures'] == game.game_map.get_difficulty():
                self.game_end(game.path.move_count)
                exit_game = True

            # Display current number of fragments and treasures the player has found
            self.show_score(game)

            pg.display.flip()

            self.clock.tick(60)

        pg.quit()


def next_pos(cur_pos: Tuple[int, int], move: str, h_step, v_step) -> Tuple[int, int]:
    """Helper function for analyzing next position coordinate by a given step"""
    possible_next_pos = {'left': (cur_pos[0] - h_step, cur_pos[1]),
                         'right': (cur_pos[0] + h_step, cur_pos[1]),
                         'up': (cur_pos[0], cur_pos[1] - v_step),
                         'down': (cur_pos[0], cur_pos[1] + v_step)}

    return possible_next_pos[move]


def test() -> None:
    """Tests all relevant functions from each modules"""
    # TODO implement this to the Game Class
    # Initializes empty graph
    graph = Graph()
    # Initializes player with default position
    ply = Player('Test', (int(20 - 8 / 2), int(400 - 8 / 2)), 20)

    # New GameMap object with generated game objects
    map1 = GameMap((800, 800), 40, True)
    # Save map to file
    map1.save_map()
    print("Saving map")
    time.sleep(2)
    # Retrieve the name of the map that was just saved
    map_num = len([m for m in os.listdir('maps/')])
    map_name = 'map{}.csv'.format(map_num)
    map_path = os.path.join(r'maps\\', map_name)
    # New GameMap object without any game objects: autogen = False
    map2 = GameMap((800, 800), 40, False)
    # Reads from the map that was just saved
    map2.read_map(map_path)

    # Assign map and player to the Path
    p = Path(map1, graph, ply)
    # Initializes game
    game = Game(map2, p, ply)

    # Initializes Game Display
    display = GameDisplay((800, 800))
    display.run_game(game)
