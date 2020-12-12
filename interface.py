import pygame
import pygame_gui

pygame.init()

pygame.display.set_caption('Climate Grapher')
window_surface = pygame.display.set_mode((400, 500))

background = pygame.Surface((400, 500))
background.fill(pygame.Color('#CCCCCC'))

manager = pygame_gui.UIManager((400, 500))

# Dataset Buttons
temperature_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 25), (350, 50)),
                                                  text='Temperature',
                                                  manager=manager)

disasters_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 85), (350, 50)),
                                                text='Natural Disasters',
                                                manager=manager)

co2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 145), (350, 50)),
                                          text='CO2 levels',
                                          manager=manager)

# Interval of Increases
increase_text = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((25, 235), (180, 50)),
                                              html_text='0.1°C',
                                              manager=manager)

minus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((215, 235), (75, 50)),
                                            text='-',
                                            manager=manager)

plus_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((300, 235), (75, 50)),
                                           text='+',
                                           manager=manager)
# Generate Button
plot_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 325), (350, 150)),
                                           text='Generate',
                                           manager=manager)

clock = pygame.time.Clock()
is_running = True

selected_dataset = 0
interval_increase = 0.1
temperature_button.select()

units = ['°C', ' Disasters', ' ppm']
interval_deltas = [0.1, 20, 10]


def change_interval(textbox, interval):
    textbox.html_text = str(interval) + units[selected_dataset]
    textbox.rebuild()


def deselect_datasets():
    temperature_button.unselect()
    disasters_button.unselect()
    co2_button.unselect()


while is_running:
    time_delta = clock.tick(60) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                # Dataset buttons
                if event.ui_element == temperature_button:
                    deselect_datasets()
                    temperature_button.select()
                    selected_dataset = 0
                    interval_increase = 0.1
                    change_interval(increase_text, interval_increase)
                elif event.ui_element == disasters_button:
                    deselect_datasets()
                    disasters_button.select()
                    selected_dataset = 1
                    interval_increase = 20
                    change_interval(increase_text, interval_increase)
                elif event.ui_element == co2_button:
                    deselect_datasets()
                    co2_button.select()
                    selected_dataset = 2
                    interval_increase = 10
                    change_interval(increase_text, interval_increase)

                # Plus minus interval buttons
                elif event.ui_element == minus_button:
                    interval_increase -= interval_deltas[selected_dataset]
                    if selected_dataset == 0:
                        interval_increase = round(interval_increase, 1)
                    change_interval(increase_text, interval_increase)
                elif event.ui_element == plus_button:
                    interval_increase += interval_deltas[selected_dataset]
                    if selected_dataset == 0:
                        interval_increase = round(interval_increase, 1)
                    change_interval(increase_text, interval_increase)

                # Generate Button
                elif event.ui_element == plot_button:
                    # PLOT... selected_dataset & interval_increase
                    pass

        manager.process_events(event)

    manager.update(time_delta)

    window_surface.blit(background, (0, 0))
    manager.draw_ui(window_surface)

    pygame.display.update()
