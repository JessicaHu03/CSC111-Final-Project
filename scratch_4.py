import pygame as pg
import pygame_gui as pg_gui

pg.init()

pg.display.set_caption('Quick Start')
window_surface = pg.display.set_mode((800, 600))

background = pg.Surface((800, 600))
background.fill(pg.Color('#000000'))

manager = pg_gui.UIManager((800, 600))

hello_button = pg_gui.elements.UIButton(relative_rect=pg.Rect((350, 275), (100, 50)),
                                        text='Say Hello',
                                        manager=manager)
text_entry = pg_gui.elements.UITextEntryLine(relative_rect=pg.Rect((350, 400), (100, 50)), manager=manager)

clock = pg.time.Clock()
is_running = True

while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pg.event.get():
        if event.type == pg.QUIT:
            is_running = False

        if event.type == pg.USEREVENT:
            if event.user_type == pg_gui.UI_BUTTON_PRESSED:
                if event.ui_element == hello_button:
                    print('Hello World!')
            if event.user_type == pg_gui.UI_TEXT_ENTRY_FINISHED:
                print("Entered text:", type(event.text))

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pg.display.update()

pg.quit()
