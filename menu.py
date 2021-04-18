import os
import pygame as pg
from pygame.locals import *
import pygame_gui as pg_gui
from typing import Tuple, List, Any
from pygame_gui.core import IncrementalThreadedResourceLoader


class Menu:
    menu_type: str
    screen: pg.Surface
    screen_size: Tuple[int, int]
    manager: pg_gui.UIManager
    clock: pg.time.Clock

    def __init__(self, menu_type: str, screen_size: Tuple[int, int], screen: pg.Surface):
        """Initializes menu screen with given menu type and screen_size"""
        self.menu_type = menu_type
        self.screen_size = screen_size
        self.screen = screen

        pg.init()
        pg.mouse.set_cursor(pg.cursors.diamond)

        loader = IncrementalThreadedResourceLoader()
        self.manager = pg_gui.UIManager(screen_size, 'themes/themes.json', resource_loader=loader)

        self.manager.add_font_paths(font_name='IndieFlower', regular_path='fonts/IndieFlower-Regular.ttf')

        font_list = [{'name': 'IndieFlower', 'point_size': 18, 'style': 'regular'}]
        self.manager.preload_fonts(font_list)

        loader.start()

        self.clock = pg.time.Clock()

    def display(self, on: bool) -> None:
        """Display module for all menus"""
        raise NotImplementedError


class NameEntry(Menu):
    _name_entry: pg_gui.elements.UITextEntryLine
    _enter_button: pg_gui.elements.UIButton
    _player_name: str

    def __init__(self, screen_size: Tuple[int, int], screen: pg.Surface):
        """Initializes NameEntry menu with given screen"""
        Menu.__init__(self, 'main', screen_size, screen)
        # Create Text Entry Field
        text_rect_pos = (int(screen_size[0] / 2 - 150), int(screen_size[1] / 2))
        text_rect = pg.Rect(text_rect_pos, (200, 60))
        text_entry = pg_gui.elements.UITextEntryLine(relative_rect=text_rect,
                                                     manager=self.manager)

        # Create Enter Button
        button_rect_pos = (int(screen_size[0] / 2 + 100), int(screen_size[1] / 2 - 5))
        button_rect = pg.Rect(button_rect_pos, (80, 40))
        button = pg_gui.elements.UIButton(relative_rect=button_rect,
                                          text='Enter',
                                          manager=self.manager,
                                          object_id='#' + str(1) + ',' + str(1))

        info_rect_pos = (int(screen_size[0] / 2 - 150 - 5), int(screen_size[1] / 2 - 70))
        info_rect = pg.Rect(info_rect_pos, (230, 50))
        info_text = pg_gui.elements.UITextBox(relative_rect=info_rect,
                                              html_text="Please enter your name:",
                                              manager=self.manager)
        self._name_entry = text_entry
        self._enter_button = button
        self._player_name = ''

    def display(self, on) -> str:
        while on:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                    pg.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        on = False

                if event.type == pg.USEREVENT:
                    if event.user_type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                        if event.text != '':
                            self._player_name = event.text
                            on = False
                    if event.user_type == pg_gui.UI_BUTTON_PRESSED:
                        if self._name_entry.text != '':
                            self._player_name = self._name_entry.text
                            on = False
                        else:
                            print("Please enter a name")

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.screen.fill((243, 166, 148))
            self.manager.draw_ui(self.screen)

            pg.display.update()
        return self._player_name


class MainMenu(Menu):
    options: list
    return_option: str
    option_rects: List[pg.Rect]
    option_info: List[Tuple[pg.Rect, str]]

    def __init__(self, screen_size: Tuple[int, int], screen: pg.Surface):
        """Initializes Main Menu with given screen"""
        Menu.__init__(self, 'main', screen_size, screen)
        self.options = []
        self.screen_size = screen_size
        self.screen = screen
        self.add_options('Start')
        self.add_options('Settings')
        self.add_options('Quit')
        self.option_rects = []
        self.option_info = []
        self.return_option = ''

        default_color = (154, 167, 177)
        options_font = pg.font.Font('fonts/Prodelt Co.ttf', 40)
        for option in self.options:
            text_surface = options_font.render(option[0], True, default_color)
            text_rect = text_surface.get_rect()
            text_rect.center = option[1]
            self.option_rects.append(text_rect)
            self.option_info.append((text_rect, option[0]))

    def add_options(self, option: str) -> None:
        # Use the existing number of options to calculate text y-pos offset
        num_options = len(self.options)
        off_set = self.screen_size[1] * 0.5 + num_options * (self.screen_size[1] / 10)
        # Set text position
        text_pos = (int(self.screen_size[0] / 2), int(off_set))
        # Generate new text info
        text = (option, text_pos)
        # Add text info to options list
        self.options.append(text)

    def display(self, on) -> str:
        while on:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for option_info in self.option_info:
                        if option_info[0].collidepoint(mouse_pos):
                            self.return_option = option_info[1]
                            on = False
            self.screen.fill((191, 192, 150))

            default_color = (154, 167, 177)
            hover_color = (243, 166, 148)

            options_font = pg.font.Font('fonts/Prodelt Co.ttf', 40)

            for option in self.options:
                text_surface = options_font.render(option[0], True, default_color)
                text_rect = text_surface.get_rect()
                text_rect.center = option[1]

                if text_rect.collidepoint(mouse_pos):
                    text_surface = options_font.render(option[0], True, hover_color)

                self.screen.blit(text_surface, text_rect)

            pg.display.update()

        return self.return_option


class Settings(Menu):
    map_id: int
    mode: str
    option: str
    _map_menu: pg_gui.elements.UIDropDownMenu
    _mode_menu: pg_gui.elements.UIDropDownMenu
    _logout_button: pg_gui.elements.UIButton
    _exit: pg_gui.elements.UIButton

    def __init__(self, screen_size: Tuple[int, int], screen: pg.Surface):
        """Initializes Settings menu with given screen"""
        Menu.__init__(self, 'main', screen_size, screen)
        # Create Map Dropdown List
        map_menu_pos = (int(screen_size[0] * 0.3 - 75), int(screen_size[1] / 2 - 100))
        map_menu_rect = pg.Rect(map_menu_pos, (150, 50))

        map_num = len([m for m in os.listdir('maps/')])
        map_list = []
        for i in range(1, map_num + 1):
            map_list.append('map{}'.format(i))

        map_menu = pg_gui.elements.UIDropDownMenu(options_list=map_list, starting_option='map1',
                                                  relative_rect=map_menu_rect, manager=self.manager)
        # Create Settings Button
        mode_pos = (int(screen_size[0] * 0.7 - 75), int(screen_size[1] / 2 - 100))
        mode_rect = pg.Rect(mode_pos, (150, 50))
        mode_menu = pg_gui.elements.UIDropDownMenu(options_list=['Shortest Path', 'User Control'],
                                                   starting_option='User Control',
                                                   relative_rect=mode_rect, manager=self.manager)

        # Create LogOut Button
        logout_button_pos = (int(screen_size[0] * 0.8 - 150), int(screen_size[1] * 0.8))
        logout_button_rect = pg.Rect(logout_button_pos, (120, 40))
        logout_button = pg_gui.elements.UIButton(relative_rect=logout_button_rect,
                                                 text='Logout',
                                                 manager=self.manager)
        # Create exit button
        exit_button_pos = (int(screen_size[0] * 0.8), int(screen_size[1] * 0.8))
        exit_button_rect = pg.Rect(exit_button_pos, (120, 40))
        exit_button = pg_gui.elements.UIButton(relative_rect=exit_button_rect,
                                               text='Exit',
                                               manager=self.manager)
        self._map_menu = map_menu
        self._mode_menu = mode_menu
        self._logout_button = logout_button
        self._exit = exit_button
        self.map_id = 1
        self.mode = 'User Control'
        self.option = ''

    def display(self, on) -> str:
        while on:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                    pg.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        on = False

                if event.type == pg.USEREVENT:
                    if event.user_type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self._map_menu:
                            self.map_id = int(event.text[-1])
                        if event.ui_element == self._mode_menu:
                            self.mode = event.text
                    if event.user_type == pg_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self._exit:
                            self.option = 'exit'
                            on = False
                        if event.ui_element == self._logout_button:
                            on = False
                            self.option = 'logout'

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.screen.fill((223, 206, 180))
            self.manager.draw_ui(self.screen)

            pg.display.update()

        return self.option


class Pause(Menu):
    _exit: pg_gui.elements.UIButton
    _continue: pg_gui.elements.UIButton
    _cover: pg.Surface
    return_option: str

    def __init__(self, screen_size: Tuple[int, int], screen: pg.Surface):
        """Initializes Settings menu with given screen"""
        Menu.__init__(self, 'main', screen_size, screen)
        # Create Background
        back_pos = (int(screen_size[0] * 0.3), int(screen_size[1] * 0.3))
        back_size = (int(screen_size[0] * 0.4), int(screen_size[1] * 0.4))
        off_set = 60
        # Create Exit Button
        exit_button_pos = (back_pos[0] + back_size[0] / 2 - 70, back_pos[1] + off_set * 2)
        exit_button_rect = pg.Rect(exit_button_pos, (140, 60))
        exit_button = pg_gui.elements.UIButton(relative_rect=exit_button_rect,
                                               text='Exit',
                                               manager=self.manager)

        # Created Continue Button
        continue_button_pos = (back_pos[0] + back_size[0] / 2 - 70, exit_button_pos[1] + off_set * 2)
        continue_button_rect = pg.Rect(continue_button_pos, (140, 60))
        continue_button = pg_gui.elements.UIButton(relative_rect=continue_button_rect,
                                                   text='Continue',
                                                   manager=self.manager)
        self._exit = exit_button
        self._continue = continue_button
        self._cover = pg.Surface(screen_size)
        self.return_option = ''

    def display(self, on) -> str:
        while on:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                    pg.quit()
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.return_option = 'continue'
                        on = False

                if event.type == pg.USEREVENT:
                    if event.user_type == pg_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self._exit:
                            self.return_option = 'exit'
                            on = False
                        else:
                            self.return_option = 'continue'
                            on = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self._cover.fill(color=(214, 218, 217))
            self._cover.set_alpha(10)
            self.screen.blit(self._cover, (0, 0))

            self.manager.draw_ui(self.screen)

            pg.display.update()

        return self.return_option

    def reset(self):
        self.return_option = ''

