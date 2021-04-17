import pygame as pg
from pygame.locals import *
import pygame_gui as pg_gui
from typing import Tuple, List, Any
from map import GameMap


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
        self.manager = pg_gui.UIManager(screen_size, 'themes/themes.json')
        self.clock = pg.time.Clock()
        pg.mouse.set_cursor(pg.cursors.diamond)

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
                                          manager=self.manager)

        info_rect_pos = (int(screen_size[0] / 2 - 150 - 5), int(screen_size[1] / 2 - 70))
        info_rect = pg.Rect(info_rect_pos, (218, 48))
        info_text = pg_gui.elements.UITextBox(relative_rect=info_rect,
                                              html_text='Please enter your name:',
                                              manager=self.manager)
        self._name_entry = text_entry
        self._enter_button = button
        self._player_name = ''

    def display(self, on):
        while on:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
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

            self.screen.fill((223, 206, 180))
            self.manager.draw_ui(self.screen)

            pg.display.update()


start_game = False
settings_on = False


class MainMenu(Menu):
    options: list
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
        self.option_rects = []
        self.option_info = []

        default_color = (154, 167, 177)
        options_font = pg.font.Font('themes/fonts/Prodelt Co.ttf', 40)
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

    def display(self, on) -> None:
        global start_game
        global settings_on
        on = True
        while on:
            mouse_pos = pg.mouse.get_pos()
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                    pg.quit()
                if event.type == pg.MOUSEBUTTONDOWN:
                    for option_info in self.option_info:
                        if option_info[0].collidepoint(mouse_pos):
                            if option_info[1] == 'Start':
                                start_game = not start_game
                                on = False
                            if option_info[1] == 'Settings':
                                settings_on = not settings_on
                                on = False

            self.screen.fill((191, 192, 150))

            default_color = (154, 167, 177)
            hover_color = (243, 166, 148)

            options_font = pg.font.Font('themes/fonts/Prodelt Co.ttf', 40)

            for option in self.options:
                text_surface = options_font.render(option[0], True, default_color)
                text_rect = text_surface.get_rect()
                text_rect.center = option[1]

                if text_rect.collidepoint(mouse_pos):
                    text_surface = options_font.render(option[0], True, hover_color)

                self.screen.blit(text_surface, text_rect)

            pg.display.update()


class Settings(Menu):
    map_id: int
    _map_menu: pg_gui.elements.UIDropDownMenu
    _mode: pg_gui.elements.UIDropDownMenu
    _exit: pg_gui.elements.UIButton

    def __init__(self, screen_size: Tuple[int, int], screen: pg.Surface):
        """Initializes Settings menu with given screen"""
        Menu.__init__(self, 'main', screen_size, screen)
        # Create Map Dropdown List
        map_menu_pos = (int(screen_size[0] * 0.3 - 75), int(screen_size[1] / 2 - 100))
        map_menu_rect = pg.Rect(map_menu_pos, (150, 50))
        map_menu = pg_gui.elements.UIDropDownMenu(options_list=['map1', 'map2'], starting_option='map1',
                                                  relative_rect=map_menu_rect, manager=self.manager)
        # Create Settings Button
        mode_pos = (int(screen_size[0] * 0.7 - 75), int(screen_size[1] / 2 - 100))
        mode_rect = pg.Rect(mode_pos, (150, 50))
        mode = pg_gui.elements.UIDropDownMenu(options_list=['Shortest Path', 'User Control'],
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
        self._mode = mode
        self._exit = exit_button
        self.map_id = 1

    def display(self, on):
        while on:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        on = False

                if event.type == pg.USEREVENT:
                    if event.user_type == pg_gui.UI_DROP_DOWN_MENU_CHANGED:
                        if event.ui_element == self._map_menu:
                            self.map_id = int(event.text[-1])
                            print(self.map_id)
                        if event.ui_element == self._mode:
                            print(event.text)
                    if event.user_type == pg_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self._exit:
                            on = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self.screen.fill((223, 206, 180))
            self.manager.draw_ui(self.screen)

            pg.display.update()


class Pause(Menu):
    _exit: pg_gui.elements.UIButton
    _continue: pg_gui.elements.UIButton
    _cover: pg.Surface

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

    def display(self, on):
        while on:
            time_delta = self.clock.tick(60) / 1000.0
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    on = False
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        on = False

                if event.type == pg.USEREVENT:
                    if event.user_type == pg_gui.UI_BUTTON_PRESSED:
                        if event.ui_element == self._exit:
                            on = False
                            main_on = True
                        else:
                            on = False

                self.manager.process_events(event)

            self.manager.update(time_delta)

            self._cover.fill(color=(214, 218, 217))
            self._cover.set_alpha(10)
            self.screen.blit(self._cover, (0, 0))

            self.manager.draw_ui(self.screen)

            pg.display.update()


def run():
    pg.init()
    pg.font.init()

    screen_size = (800, 800)
    screen = pg.display.set_mode(screen_size)
    name_menu_on = True
    main_menu_on = True

    name_entry = NameEntry(screen_size, screen)
    name_entry.display(name_menu_on)

    main_menu = MainMenu(screen_size, screen)
    main_menu.display(main_menu_on)

    settings = Settings(screen_size, screen)
    settings.display(settings_on)

    pause = Pause(screen_size, screen)
    pause.display(True)

    pg.quit()

