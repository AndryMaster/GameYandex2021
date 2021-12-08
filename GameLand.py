import pygame
import pygame_widgets
import pygame_widgets.button as btn

from Snake.Game import run_snake
from Tetris.Game import run_tetris


# Запаомнить!!! Экран игры создавать в функции!
pygame.init()

SIZE = width, height = (800, 600)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FPS = 30

font_btn = pygame.font.Font('font_pixel.ttf', 50)

button_snake = btn.Button(
        screen, 75, 75, 300, 150, text='Snake',
        font=font_btn, fontSize=font_btn.get_ascent(),
        inactiveColour=(255, 0, 0),
        hoverColour=(0, 255, 0),
        pressedColour=(0, 255, 0),
        margin=20, radius=20,
        onClick=run_snake)

button_tetris = btn.Button(
        screen, 425, 75, 300, 150, text='Tetris',
        font=font_btn, fontSize=font_btn.get_ascent(),
        inactiveColour=(255, 0, 255),
        hoverColour=(200, 255, 0),
        pressedColour=(200, 255, 0),
        margin=20, radius=20,
        onClick=run_tetris)

BUTTONS = [button_snake, button_tetris]


RUN = True
while RUN:
    screen = pygame.display.set_mode(SIZE)
    screen.fill('white')
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            RUN = False

    # Выполнение действий
    pygame_widgets.update(events)
    # Корректный запуск и отписовука окон игр
    [btn.listen(events) for btn in BUTTONS]
    [btn.draw() for btn in BUTTONS]

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
