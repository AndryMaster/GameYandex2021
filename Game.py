import pygame
from copy import deepcopy

pygame.init()

W, H = 10, 20
CELL = 35
SIZE = W * CELL, H * CELL

BORDER_COLOR = (40, 40, 40)

screen = pygame.display.set_mode(SIZE)
# pygame.display.set_caption('Name')
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

anim_count, anim_speed, anim_limit = 0, 60, 2000
figure = deepcopy(figures[3])


def check_border(x):
    if 0 <= x <= W - 1:
        return True
    return False


RUN = True
while RUN:
    dx = 0
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

    screen.fill(pygame.Color('black'))

    # move figure x
    old_figure = deepcopy(figure)
    for i in range(4):
        figure[i].x += dx
        if not check_border(figure[i].x):
            figure = deepcopy(old_figure)
            break
    # move figure y
    anim_count += anim_speed
    if anim_count > anim_limit:
        anim_count = 0
        old_figure = deepcopy(figure)
        for i in range(4):
            figure[i].y += 1
            if not check_border(figure[i].x):
                figure = deepcopy(old_figure)
                anim_limit = 2000
                break
    # draw grid
    for cord in grid:
        pygame.draw.rect(screen, BORDER_COLOR, cord, 1)
    # draw figure
    for i in range(4):
        figure_rect.x = figure[i].x * CELL
        figure_rect.y = figure[i].y * CELL
        pygame.draw.rect(screen, "white", figure_rect)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
