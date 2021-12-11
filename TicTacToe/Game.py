import pygame
import random
import sys
from copy import deepcopy


pygame.init()

O = 1
X = 2

WHITE = (255, 255, 255)
PURPLE = (255, 0, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
f1 = pygame.font.Font(None, 35)
f2 = pygame.font.SysFont('serif', 40)
f3 = pygame.font.SysFont('timesnewroman', 37)
f4 = pygame.font.SysFont('calibri', 25)

blocks = 3
size_block = 160
midth = 15
step = bool(random.randrange(0, 2))
width = size_block * blocks + midth * (blocks + 1)
height = width + size_block + 20
title_rec = pygame.Rect(0, 0, width, size_block + 20)
delay_key = 10
score_winner = {'Blue': 0, 'Red': 0}
score = True
win_line = [(0, 0), (0, 0)]
win = False
lines = [[(0, 0)] * 3 for _ in range(3)]
matrix = [[0, 0, 0],
          [0, 0, 0],
          [0, 0, 0]]
pos = 5

RunGame = True


def run_tic_tac_toe():
    global delay_key, step, RunGame, screen, matrix, pos, x, y

    screen = pygame.display.set_mode((width, height))
    # icon = pygame.image.load("icons/tticon.png")
    # pygame.display.set_icon(icon)
    pygame.display.set_caption("КРЕСТики  И  НОЛЬики: X-X-O")
    clock = pygame.time.Clock()

    while RunGame:
        clock.tick(30)
        if delay_key > 0:
            delay_key -= 1

        check_win()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RunGame = False

        keys = pygame.key.get_pressed()
        if win and (keys[pygame.K_r] or keys[pygame.K_BACKSPACE]):
            restart_game()
        if keys[pygame.K_UP] and (pos - 3) >= 1 and delay_key == 0 and not win:
            delay_key += 10
            pos -= 3
        elif keys[pygame.K_DOWN] and (pos + 3) <= 9 and delay_key == 0 and not win:
            delay_key += 10
            pos += 3
        elif keys[pygame.K_RIGHT] and delay_key == 0 and (pos - 1) // blocks == pos // blocks and not win:
            delay_key += 10
            pos += 1
        elif keys[pygame.K_LEFT] and delay_key == 0 and (pos - 2) // blocks == (pos - 1) // blocks and not win:
            delay_key += 10
            pos -= 1

        y = (pos - 1) // blocks
        x = (pos - 1) % blocks

        if (keys[pygame.K_x] or keys[pygame.K_RETURN]) and not step and matrix[y][x] == 0 and not win:
            matrix[y][x] = X
            step = True
        elif (keys[pygame.K_o] or keys[pygame.K_RETURN]) and step and matrix[y][x] == 0 and not win:
            matrix[y][x] = O
            step = False

        RenderWindow()


def restart_game():
    global matrix, win, pos, step, score
    matrix = [[0, 0, 0],
              [0, 0, 0],
              [0, 0, 0]]
    win = False
    pos = 5
    score = True
    step = bool(random.randrange(0, 2))
    screen.fill('black')


def find_win(win_cell, start, end):
    global win_line
    r = win_cell == X
    b = win_cell == O
    win_line = (lines[start[0]][start[1]], lines[end[0]][end[1]])
    return r, b


def check_win():
    global score_winner, win, score, x, y
    blue_win = red_win = False
    m = deepcopy(matrix)

    no_zero = all(all(row) for row in m)
    for i in range(3):
        if m[i][0] == m[i][1] == m[i][2] and m[i][1]:
            red_win, blue_win = find_win(m[i][1], (i, 0), (i, 2))
    for j in range(3):
        if m[0][j] == m[1][j] == m[2][j] and m[1][j]:
            red_win, blue_win = find_win(m[1][j], (0, j), (2, j))
    if m[0][0] == m[1][1] == m[2][2]:
        red_win, blue_win = find_win(m[1][1], (0, 0), (2, 2))
    elif m[0][2] == m[1][1] == m[2][0]:
        red_win, blue_win = find_win(m[1][1], (0, 2), (2, 0))

    if red_win or blue_win or no_zero:
        win = True
        x = y = 3
        if red_win and score:
            score_winner['Red'] += 1
            score = False
        elif blue_win and score:
            score_winner['Blue'] += 1
            score = False


def RenderWindow():
    pygame.draw.rect(screen, (255, 235, 190), title_rec)

    steep = f3.render("Next step:", True, (10, 10, 10))
    text_red = f1.render(f"Red: {score_winner['Red']}", True, (250, 0, 0))
    text_blue = f1.render(f"Blue: {score_winner['Blue']}", True, (0, 0, 250))
    text = f2.render("Score:", True, (0, 0, 0))
    restart = f4.render("Click 'R' to restart", True, (40, 200, 35))

    screen.blit(steep, (240, 110))
    screen.blit(text, (25, 15))
    screen.blit(text_red, (40, 80))
    screen.blit(text_blue, (40, 125))
    if win:
        screen.blit(restart, (330, 15))

    if step:
        pygame.draw.rect(screen, (0, 0, 0), (415, 70, 90, 90))
        pygame.draw.rect(screen, (160, 160, 255), (420, 75, 80, 80))
        pygame.draw.circle(screen, BLUE, (420 + 40, 75 + 40), 35, 10)
    else:
        pygame.draw.rect(screen, (0, 0, 0), (415, 70, 90, 90))
        pygame.draw.rect(screen, (255, 160, 160), (420, 75, 80, 80))
        pygame.draw.line(screen, RED, (435, 85), (485, 145), 8)
        pygame.draw.line(screen, RED, (485, 85), (435, 145), 8)

    for row in range(blocks):
        for column in range(blocks):
            cursor = False
            x_draw = False
            o_draw = False
            color = WHITE

            if row == y and column == x and not win:
                cursor = True
                color = (130, 130, 130)
            if matrix[row][column] == X:
                color = (255, 160, 160)
                if cursor and not win:
                    color = (200, 100, 100)
                x_draw = True
            elif matrix[row][column] == O:
                color = (160, 160, 255)
                if cursor and not win:
                    color = (100, 100, 200)
                o_draw = True

            w = column * size_block + (column + 1) * midth
            h = (row + 1) * size_block + (row + 1) * midth + 20
            pygame.draw.rect(screen, color, (w, h, 160, 160))
            lines[row][column] = (w + 80, h + 80)
            if x_draw:
                pygame.draw.line(screen, RED, (w + 15, h + 10), (w + 145, h + 150), 22)
                pygame.draw.line(screen, RED, (w + 145, h + 10), (w + 15, h + 150), 22)
            elif o_draw:
                pygame.draw.circle(screen, BLUE, (w + 80, h + 80), 70, 24)
            if win and not score:
                pygame.draw.line(screen, PURPLE, win_line[0], win_line[1], 10)

    pygame.display.flip()


if __name__ == '__main__':
    run_tic_tac_toe()
    pygame.quit()
