import pygame

pygame.init()

SIZE = WIDTH, HEIGHT = 500, 500

screen = pygame.display.set_mode(SIZE)
# pygame.display.set_caption('Name')
clock = pygame.time.Clock()
FPS = 60

RUN = True
while RUN:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUN = False

    screen.fill(pygame.Color('black'))

    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
