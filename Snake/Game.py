import pygame
from random import randrange


def run_snake():
    pygame.init()

    CELL = 35
    SIZE = CELL * 22

    screen = pygame.display.set_mode((SIZE, SIZE))
    pygame.display.set_caption('Snake')
    clock = pygame.time.Clock()
    FPS = 60

    font_score = pygame.font.Font('font_pixel.ttf', round(SIZE / 29.7))
    font_end = pygame.font.Font('font_pixel.ttf', round(SIZE / 12.5))
    # bg_img = pygame.image.load('bg.jpg').convert()

    x, y = randrange(0, SIZE, CELL), randrange(0, SIZE, CELL)
    apple = randrange(0, SIZE, CELL), randrange(0, SIZE, CELL)
    snake = [(x, y)]
    snake_length = 1
    dx = dy = score = 0
    moved = True

    anim_count, anim_speed = 0, 10

    RUN = True
    while RUN:
        screen.fill('black')
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                RUN = False

        # show score
        screen.blit(font_score.render(f'SCORE: {score}', False, "orange"), (15, 5))
        # draw snake
        for pos in snake[:-1]:
            pygame.draw.rect(screen, 'green', (pos[0] + 1, pos[1] + 1, CELL - 2, CELL - 2))
        pygame.draw.rect(screen, (20, 255, 120), (snake[-1][0] + 1, snake[-1][1] + 1, CELL - 2, CELL - 2))
        # draw apple
        pygame.draw.rect(screen, 'red', (apple[0] + 1, apple[1] + 1, CELL - 2, CELL - 2))

        # eat apple
        if snake[-1] == apple:
            while apple in snake: apple = randrange(0, SIZE, CELL), randrange(0, SIZE, CELL)
            snake_length += 1
            score += 1

        # move
        anim_count += 1
        if anim_count >= anim_speed:
            anim_count = 0
            x += dx * CELL
            y += dy * CELL
            snake.append((x, y))
            snake = snake[-snake_length:]
            moved = True

        # game over
        if len(snake) != len(set(snake)) or min(x, y) < 0 or max(x, y) > SIZE - CELL:
            end_text = font_end.render('GAME OVER!', False, "orange")
            screen.blit(end_text, ((SIZE - end_text.get_width()) // 2, (SIZE - end_text.get_height()) // 2))
            pygame.display.flip()
            while pygame.event.wait().type != pygame.QUIT: pass
            RUN = False

        # render frame
        pygame.display.flip()
        clock.tick(FPS)

        # keys
        key = pygame.key.get_pressed()
        if (key[pygame.K_w] or key[pygame.K_UP]) and dy != 1 and moved:
            dx, dy = 0, -1
            moved = False
        elif (key[pygame.K_s] or key[pygame.K_DOWN]) and dy != -1 and moved:
            dx, dy = 0, 1
            moved = False
        elif (key[pygame.K_a] or key[pygame.K_LEFT]) and dx != 1 and moved:
            dx, dy = -1, 0
            moved = False
        elif (key[pygame.K_d] or key[pygame.K_RIGHT]) and dx != -1 and moved:
            dx, dy = 1, 0
            moved = False


if __name__ == '__main__':
    run_snake()
    pygame.quit()
