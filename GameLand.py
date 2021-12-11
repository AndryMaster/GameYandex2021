import pygame
import pygame_widgets
import pygame_widgets.button as btn

from Snake.Game import run_snake
from Tetris.Game import run_tetris
from GoogleDino.Game import run_dino
from TicTacToe.Game import run_tic_tac_toe


# Запаомнить!!! Экран игры создавать в функции!
# Надо сделать(добавить)!!!
# 1. Поменять шрифт
# 2. Главный экран с градиентом
pygame.init()

SIZE = width, height = (800, 600)

screen = pygame.display.set_mode(SIZE)
clock = pygame.time.Clock()
FPS = 30

font_btn = pygame.font.Font('fonts/font_pixel.ttf', 50)

button_snake = btn.Button(
        screen, 75, 75, 300, 150, text='Snake',
        font=font_btn, fontSize=font_btn.get_ascent(),
        inactiveColour=(130, 255, 0),
        hoverColour=(0, 255, 170),
        # pressedColour=(255, 255, 255),
        margin=20, radius=20,
        onClick=run_snake)

button_tetris = btn.Button(
        screen, 425, 75, 300, 150, text='Tetris',
        font=font_btn, fontSize=font_btn.get_ascent(),
        inactiveColour=(200, 100, 150),
        hoverColour=(200, 200, 0),
        # pressedColour=(255, 255, 255),
        margin=20, radius=20,
        onClick=run_tetris)

button_dino = btn.Button(
        screen, 75, 275, 300, 150, text='Dino',
        font=font_btn, fontSize=font_btn.get_ascent(),
        inactiveColour=(190, 190, 190),
        hoverColour=(140, 140, 140),
        # pressedColour=(255, 255, 255),
        margin=20, radius=20,
        onClick=run_dino)

button_tic_tac = btn.Button(
        screen, 425, 275, 300, 150, text='Tic Tac',
        font=font_btn, fontSize=font_btn.get_ascent(),
        inactiveColour=(255, 50, 50),
        hoverColour=(50, 50, 255),
        # pressedColour=(255, 255, 255),
        margin=20, radius=20,
        onClick=run_tic_tac_toe)

BUTTONS = [button_snake, button_tetris, button_dino, button_tic_tac]


RUN = True
while RUN:
    screen = pygame.display.set_mode(SIZE)
    # pygame.display.set_icon()
    screen.fill((200, 255, 230))  # Сюда картинку градиента
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
