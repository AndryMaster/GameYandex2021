import pygame
from copy import deepcopy
from random import choice, randint

pygame.init()

W, H = 10, 20
CELL = 45
SIZE = W * CELL, H * CELL
SIZE_WINDOW = 750, 940
BORDER_COLOR = (40, 40, 40)
# FIGURE_COLORS = ['red', 'green', 'lightgreen', 'purple', 'yellow', 'lightblue', 'blue', 'orange', 'white']

window_screen = pygame.display.set_mode(SIZE_WINDOW)
screen = pygame.Surface(SIZE)
pygame.display.set_caption('Tetris')

title_font = pygame.font.Font('font.ttf', 65)
font = pygame.font.Font('font.ttf', 45)
title_tetris = title_font.render('TETRIS', True, 'darkorange')
title_score = font.render('score:', True, 'green')
title_record = font.render('record:', True, 'purple')

random_color = lambda: (randint(80, 255), randint(80, 255), randint(80, 255))  # choice(FIGURE_COLORS)

clock = pygame.time.Clock()
FPS = 60

figures_pos = [[(-1, 0), (-2, 0), (0, 0), (1, 0)],
               [(0, -1), (-1, -1), (-1, 0), (0, 0)],
               [(-1, 0), (-1, 1), (0, 0), (0, -1)],
               [(0, 0), (-1, 0), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, -1)],
               [(0, 0), (0, -1), (0, 1), (1, -1)],
               [(0, 0), (0, -1), (0, 1), (-1, 0)]]

grid = [pygame.Rect(x * CELL, y * CELL, CELL, CELL) for x in range(W) for y in range(H)]
figures = [[pygame.Rect(x + W // 2, y + 1, 1, 1) for x, y in fig_pos] for fig_pos in figures_pos]
figure_rect = pygame.Rect(0, 0, CELL - 2, CELL - 2)
board = [[0 for _ in range(W)] for _ in range(H)]

anim_count, anim_speed, anim_limit = 0, 60, 2000

color, next_color = random_color(), random_color()
figure, next_figure = deepcopy(choice(figures)), deepcopy(choice(figures))

bg_window = pygame.image.load('img/bg.jpg')
bg_game = pygame.image.load('img/bg2.jpg')

score = full_lines = 0
score_lines = {0: 0, 1: 100, 2: 300, 3: 700, 4: 1500}


def check_borders():
    if figure[i].x < 0 or figure[i].x > W - 1:
        return False
    elif figure[i].y >= H or board[figure[i].y][figure[i].x]:
        return False
    return True


def get_record():
    try:
        with open('record.txt') as f:
            return int(f.readline())
    except FileNotFoundError:
        with open('record.txt', "w") as f:
            f.write('0')
            return 0


def save_record(record_, score_):
    rec = max(record_, score_)
    with open('record.txt', "w") as f:
        f.write(str(rec))


RUN = True
while RUN:
    record = get_record()
    window_screen.blit(bg_window, (0, 0))
    window_screen.blit(screen, (20, 20))
    screen.blit(bg_game, (0, 0))
    # delay for score
    for _ in range(full_lines):
        pygame.time.wait(200)
    dx = 0
    rotate = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                dx = -1
            elif event.key == pygame.K_RIGHT:
                dx = 1
            elif event.key == pygame.K_DOWN:
                anim_limit = 160
            elif event.key == pygame.K_UP:
                rotate = True

    # move x
    old_figure = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_borders():
            figure = deepcopy(old_figure)
            break
    # move y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        old_figure = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_borders():
                for j in range(4):
                    board[old_figure[j].y][old_figure[j].x] = color
                color, next_color = next_color, random_color()
                figure, next_figure = next_figure, deepcopy(choice(figures))
                anim_limit = 2000
                break
    # rotate figure
    if rotate:
        center = figure[0]
        old_figure = deepcopy(figure)
        for i in range(4):
            x = figure[i].y - center.y
            y = figure[i].x - center.x
            figure[i].x = center.x - x
            figure[i].y = center.y + y
            if not check_borders():
                figure = deepcopy(old_figure)
                break
    # check lines
    line = H - 1
    full_lines = 0
    for row in range(line, -1, -1):
        board[line] = board[row]
        if not all(board[row]):
            line -= 1
        else:
            anim_speed += 3
            full_lines += 1
    # get score
    score += score_lines[full_lines]
    # draw grid
    for cord in grid:
        pygame.draw.rect(screen, BORDER_COLOR, cord, 1)
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * CELL
        figure_rect.y = figure[i].y * CELL
        pygame.draw.rect(screen, color, figure_rect)
    # draw board
    for y, row in enumerate(board):
        for x, col_or in enumerate(row):
            if col_or:
                figure_rect.x, figure_rect.y = x * CELL, y * CELL
                pygame.draw.rect(screen, col_or, figure_rect)
    # draw next figure
    for i in range(4):
        figure_rect.x = next_figure[i].x * CELL + 380
        figure_rect.y = next_figure[i].y * CELL + 185
        pygame.draw.rect(window_screen, next_color, figure_rect)
    # draw titles
    window_screen.blit(title_tetris, (485, -10))
    window_screen.blit(title_score, (535, 780))
    window_screen.blit(font.render(str(score), True, 'white'), (550, 840))
    window_screen.blit(title_record, (525, 650))
    window_screen.blit(font.render(str(record), True, pygame.Color('gold')), (550, 710))
    # over game
    for i in range(W):
        if board[0][i]:
            save_record(record, score)
            board = [[0 for _ in range(W)] for _ in range(H)]
            anim_count, anim_speed, anim_limit = 0, 60, 2000
            score = 0
            for cord in grid:
                pygame.draw.rect(screen, random_color(), cord)
                window_screen.blit(screen, (20, 20))
                pygame.display.flip()
                clock.tick(200)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
