"""
This is the main game file contains the relevant execution of a Pygame
interface for the game.
"""
from game import Game
import pygame as pg
from pygame.locals import *
from typing import Tuple
import menu
from path import Path
from player import Player
from map import GameMap
import os
import copy


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
        color = (255, 255, 255)
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
        pg.display.set_caption("Treasure Hunt game!")
        line_color = pg.Color('#8c8c91')

        # Initializes game loop booleans
        draw_path = False
        draw_grid = True
        show_all = False
        exit_game = False
        game_start = False
        player_set = False
        is_paused = False
        # Create Game Menu Objects
        name_entry = menu.NameEntry(self.screen_size, self.screen)
        settings_menu = menu.Settings(self.screen_size, self.screen)
        main_menu = menu.MainMenu(self.screen_size, self.screen)
        pause = menu.Pause(self.screen_size, self.screen)

        # Initializes player rect object
        rect_size = (8, 8)
        rect_pos = (0, 0)
        player_rect = pg.Rect(rect_pos, rect_size)

        # Sets default map and path
        game.set_map(1)
        game.reset_path()

        while not exit_game:
            name_on = not player_set
            settings_on = False

            name_input = name_entry.display(name_on)
            if not player_set:
                game.player = Player(name_input)
                game.player.set_vision_radius(20)

            vision_radius = game.player.get_vision_radius()
            player_set = True

            if game_start:
                menu_on = False
            else:
                menu_on = True

            main_option = main_menu.display(menu_on)
            if main_option == 'Start':
                game.reset_path()

                rect_pos = game.path.initial_pos

                player_rect = pg.Rect(rect_pos, rect_size)

                game_start = True

                main_menu.return_option = ''
            elif main_option == 'Settings':
                settings_on = True
            elif main_option == 'Quit':
                exit_game = True
            else:
                pass

            settings_option = settings_menu.display(settings_on)
            if settings_option == 'logout':
                player_set = False
                settings_menu.option = ''
            map_id = settings_menu.map_id
            # TODO Implement Shortest Path function as a mod
            current_mode = settings_menu.mode

            # Sets game map id given by settings
            game.set_map(map_id)
            game.path.set_map(map_id)
            # Defines player movement step size
            h_step, v_step = game.game_map.get_step()

            # Obtains game objects from the map
            obstacle_list_type = [(x[0], x[1]) for x in game.game_map.get_obstacles()]
            obstacle_list = [x[0] for x in game.game_map.get_obstacles()]
            treasure_list = game.game_map.get_treasures()
            fragment_list = game.game_map.get_fragments()

            # Retrieves object types and their relevant information
            object_type = game.game_map.get_object_types()

            # Change in position according to movement event
            dir_key = {K_LEFT: (-h_step, 0), K_RIGHT: (h_step, 0), K_UP: (0, -v_step), K_DOWN: (0, v_step)}
            # Assign keys to movement names
            dir_name = {K_LEFT: 'left', K_RIGHT: 'right', K_UP: 'up', K_DOWN: 'down'}
            # Assign keys to those for opposite direction. This is for reversing a move
            dir_opposite = {K_LEFT: K_RIGHT, K_RIGHT: K_LEFT, K_UP: K_DOWN, K_DOWN: K_UP}

            # Game window
            if game_start:
                # Checks for possible movements given obstacles in the current map
                possible_movements = ['left', 'right', 'up', 'down']
                margins = [0, 800]
                available_movements = []
                for move in possible_movements:
                    new_pos = next_pos(rect_pos, move, h_step, v_step)
                    center_pos = [new_pos[0] + rect_size[0] / 2, new_pos[1] + rect_size[1] / 2]
                    new_rect = pg.Rect(new_pos, rect_size)
                    if new_rect.collidelist(obstacle_list) == -1 and \
                            all(x not in margins for x in center_pos):
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

                        if event.key == K_ESCAPE:
                            is_paused = not is_paused

                        if event.key == K_g:
                            draw_grid = not draw_grid

                        if event.key == K_q:
                            draw_path = not draw_path

                # Fills screen
                self.screen.fill((248, 186, 182))

                # Draws player rectangle object onto screen
                pg.draw.rect(self.screen, (255, 255, 255), player_rect)

                # Sets color for fragment and treasures
                treasure_color = pg.Color('#fdcc33')
                fragment_color = pg.Color('#f25805')

                if show_all:
                    # Draws all game objects onto screen if show_all is True
                    for o in obstacle_list_type:
                        pg.draw.rect(self.screen, object_type[o[1]][0], o[0])
                    for treasure in treasure_list:
                        pg.draw.rect(self.screen, treasure_color, treasure)
                    for fragment in fragment_list:
                        pg.draw.rect(self.screen, fragment_color, fragment)
                else:
                    # Otherwise, utilizes vision field function
                    path_pos = game.path.all_pos

                    vision_rect_size = (rect_size[0] + 2 * vision_radius, rect_size[1] + 2 * vision_radius)
                    vision_rect_pos = [(pos[0] - vision_radius, pos[1] - vision_radius) for pos in path_pos]

                    vision_rects = [pg.Rect(pos, vision_rect_size) for pos in vision_rect_pos]

                    for o in obstacle_list_type:
                        if o[0].collidelist(vision_rects) != -1:
                            pg.draw.rect(self.screen, object_type[o[1]][0], o[0])
                    for treasure in treasure_list:
                        if treasure.collidelist(vision_rects) != -1:
                            pg.draw.rect(self.screen, treasure_color, treasure)
                    for fragment in fragment_list:
                        if fragment.collidelist(vision_rects) != -1:
                            pg.draw.rect(self.screen, '#ea4915', fragment)

                # Adds grid to the screen
                if draw_grid:
                    self.draw_grid(40)

                if pause.display(is_paused) == 'exit':
                    player_rect.topleft = game.path.initial_pos
                    game.reset_path()
                    game.player.reset()
                    game.game_map.reset()
                    game_start = False
                    pause.reset()

                # Showing the path of the player
                if draw_path:
                    path_vertices = game.path.get_graph().get_vertices().values()
                    for vertex in path_vertices:
                        pos = vertex.pos
                        neighbours = vertex.neighbours
                        for neighbour in neighbours:
                            init_pos = (pos[0] + rect_size[0] / 2, pos[1] + rect_size[1] / 2)
                            end_pos = (neighbour.pos[0] + rect_size[0] / 2, neighbour.pos[1] + rect_size[1] / 2)
                            pg.draw.line(self.screen, line_color, init_pos, end_pos)

                is_paused = False
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
                    # Keeps record of move_count
                    move_count = copy.deepcopy(game.path.move_count)
                    # Reset player position
                    player_rect.topleft = game.path.initial_pos
                    # Saves current game score to player data and resets player
                    game.player.update_data(game.game_map.get_difficulty())
                    game.player.reset()

                    # Saves the current path to file
                    game.path.write_path()
                    # The reset path function is part of the Game class, contrary to GameMap and Player
                    # This is path requires a given map and player, which are obtained from game.
                    game.reset_path()

                    # Resets the game objects in the current GameMap
                    game.game_map.reset()

                    self.game_end(move_count)

                    game_start = False

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


def run():
    """Runs the game"""
    # Initializes player
    ply = Player('Test')

    # New GameMap object with generated game objects
    map1 = GameMap((800, 800), 40, True)
    # Save map to file
    map1.write_map()

    # Retrieve the name of the map that was just saved
    map_num = len([m for m in os.listdir('maps/')])
    map_name = 'map{}.csv'.format(map_num)
    map_path = os.path.join(r'maps\\', map_name)
    # New GameMap object without any game objects: autogen = False
    map2 = GameMap((800, 800), 40, False)
    # Reads from the map that was just saved
    map2.read_map(map_path)

    # Assign map and player to the Path
    p = Path((int(20 - 8 / 2), int(400 - 8 / 2)), 1, '1')
    # Initializes game
    game = Game()

    # Initializes Game Display
    display = GameDisplay((800, 800))
    display.run_game(game)
