import pygame
import pygame_gui
from main import run
from typing import List
pygame.init()


def toggle_dataset(interval_increases: List[float], selected: List[int],
                   button, increase_box, dataset: int):
    if not selected[dataset]:
        selected[dataset] = True
        button.select()
        change_interval(interval_increases, increase_box, 0, dataset)
    else:
        selected[dataset] = False
        button.unselect()
        increase_box.html_text = ''
        increase_box.rebuild()


def change_interval(interval_increases: List[float], textbox, delta: float, dataset: int) -> None:
    units = ['°C', ' Disasters', ' ppm']
    interval_increases[dataset] += delta
    # Always round the Degrees Celsius
    interval_increases[0] = round(interval_increases[0], 1)
    value = str(interval_increases[dataset])
    if value[0] != '-':
        value = '+' + value
    textbox.html_text = value + units[dataset]
    textbox.rebuild()


def run_interface() -> None:
    """ Runs the graphical user interface
    """
    pygame.display.set_caption('Climate Grapher')
    window_surface = pygame.display.set_mode((450, 300))

    background = pygame.Surface((450, 300))
    background.fill(pygame.Color('#CCCCCC'))

    manager = pygame_gui.UIManager((450, 300))

    # Dataset Buttons
    temperature_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 25), (150, 50)),
                                                      text='Temperature',
                                                      manager=manager)

    disasters_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 85), (150, 50)),
                                                    text='Natural Disasters',
                                                    manager=manager)

    co2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 145), (150, 50)),
                                              text='CO2 levels',
                                              manager=manager)

    # Increase Boxes
    temperature_increase = pygame_gui.elements.UITextBox(
        relative_rect=pygame.Rect((225, 25), (200, 50)),
        html_text='+0.1°C',
        manager=manager)

    disasters_increase = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((225, 85), (200, 50)),
                                                       html_text='',
                                                       manager=manager)

    co2_increase = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((225, 145), (200, 50)),
                                                 html_text='',
                                                 manager=manager)
    # Plus Minus Buttons
    temperature_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 25), (50, 25)),
                                                    text='+',
                                                    manager=manager)

    temperature_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 50), (50, 25)),
                                                     text='-',
                                                     manager=manager)

    disasters_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 85), (50, 25)),
                                                  text='+',
                                                  manager=manager)

    disasters_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 110), (50, 25)),
                                                   text='-',
                                                   manager=manager)

    co2_plus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 145), (50, 25)),
                                            text='+',
                                            manager=manager)

    co2_minus = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((175, 170), (50, 25)),
                                             text='-',
                                             manager=manager)
    # Generate Button
    plot_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 205), (400, 70)),
                                               text='Generate',
                                               manager=manager)

    clock = pygame.time.Clock()
    is_running = True

    selected = [True, False, False]
    interval_increases = [0.1, 0, 0]
    temperature_button.select()

    interval_deltas = [0.1, 20, 10]

    while is_running:
        time_delta = clock.tick(60) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    # Dataset buttons
                    if event.ui_element == temperature_button:
                        toggle_dataset(interval_increases, selected, temperature_button, temperature_increase, 0)
                    elif event.ui_element == disasters_button:
                        toggle_dataset(interval_increases, selected, disasters_button, disasters_increase, 1)
                    elif event.ui_element == co2_button:
                        toggle_dataset(interval_increases, selected, co2_button, co2_increase, 2)

                    # Plus minus interval buttons
                    elif event.ui_element == temperature_plus:
                        change_interval(interval_increases, temperature_increase, interval_deltas[0], 0)
                        if not selected[0]:
                            toggle_dataset(interval_increases, selected, temperature_button, temperature_increase, 0)

                    elif event.ui_element == temperature_minus:
                        change_interval(interval_increases, temperature_increase, -interval_deltas[0], 0)
                        if not selected[0]:
                            toggle_dataset(interval_increases, selected, temperature_button, temperature_increase, 0)

                    elif event.ui_element == disasters_plus:
                        change_interval(interval_increases, disasters_increase, interval_deltas[1], 1)
                        if not selected[1]:
                            toggle_dataset(interval_increases, selected, disasters_button, disasters_increase, 1)
                    elif event.ui_element == disasters_minus:
                        change_interval(interval_increases, disasters_increase, -interval_deltas[1], 1)
                        if not selected[1]:
                            toggle_dataset(interval_increases, selected, disasters_button, disasters_increase, 1)

                    elif event.ui_element == co2_plus:
                        change_interval(interval_increases, co2_increase, interval_deltas[2], 2)
                        if not selected[2]:
                            toggle_dataset(interval_increases, selected, co2_button, co2_increase, 2)
                    elif event.ui_element == co2_minus:
                        change_interval(interval_increases, co2_increase, -interval_deltas[2], 2)
                        if not selected[2]:
                            toggle_dataset(interval_increases, selected, co2_button, co2_increase, 2)

                    # Generate Button
                    elif event.ui_element == plot_button:
                        run(selected[0], selected[1], selected[2], interval_increases[0], interval_increases[1],
                            interval_increases[2])

            manager.process_events(event)

        manager.update(time_delta)

        window_surface.blit(background, (0, 0))
        manager.draw_ui(window_surface)

        pygame.display.update()
