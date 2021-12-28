import pygame
import sqlite3
from random import randrange, choice


class Cactus:
    def __init__(self, number, flor, c_speed, up=False):
        self.number = number
        if number == BIRD:
            self.bird = True
            self.up = up
            self.anim = 18
            self.picture = dino_bird[0]
        else:
            self.bird = False
            self.picture = plant[number]
        self.speed = c_speed + number // BIRD
        self.size = size_plant[number]
        self.pos = [width + 35, flor]

    def update(self):
        if not n_win:
            self.pos[0] -= self.speed

            if self.bird:
                self.anim -= 1
                if self.anim <= 0:
                    self.anim = 18
                    self.picture = dino_bird[abs(dino_bird.index(self.picture)) - 1]

    def test_dead(self):
        global n_win, high_score
        x_pers, y_pers = x, y
        if y_pers + 43 > self.pos[1]:
            c_width = self.size[0]
            if not self.bird or (self.bird and not self.up):
                if (self.pos[0] < x_pers < (self.pos[0] + c_width)) or \
                        (self.pos[0] < (x_pers + 40) < (self.pos[0] + c_width)):
                    n_win = True
                    GameStop()
                    high_score = max(high_score, score)
            else:
                if (self.pos[0] < x_pers < (self.pos[0] + c_width)) or \
                        (self.pos[0] < (x_pers + 40) < (self.pos[0] + c_width)):
                    if (not dino_low and self.pos[1] == floor - size_plant[BIRD][1] - 37) or \
                            (isJump and self.pos[1] == floor - size_plant[BIRD][1] - 60):
                        n_win = True
                        GameStop()
                        high_score = max(high_score, score)

    def __repr__(self):
        return f'SpriteObject №{self.number} size:{self.size} pos:{self.pos}'


def GameStop():
    global speed, isJump, pr_restart
    speed = 0
    isJump = False
    pr_restart = True


def Make_Cactus():
    global cactus_time_game_out, wait_bird
    cactus_time_game_out = int(fps * 0.75)  # number of sec
    number = random_number(7)
    if number == BIRD:
        number = random_number(6)
        if not random_number(3):
            wait_bird = True
            return
    flor = floor - size_plant[number][1]

    if wait_bird:
        wait_bird = False
        flor = floor - size_plant[BIRD][1]
        flor = choice([flor - 37, flor - 12, flor - 60])
        up = True if flor <= floor - size_plant[BIRD][1] - 37 else False
        cact = Cactus(BIRD, flor, speed, up=up)
        cactus.append(cact)
        return

    cact = Cactus(number, flor, speed)
    cactus.append(cact)

    if len(cactus) > 0:
        if cactus[0].pos[0] < -60:
            del cactus[0]


def Restart_Game():
    global n_win, speed, isJump, pr_restart, y, attempts
    global cactus_time_game_out, cactus, JumpCount, score

    speed, y, cactus_time_game_out, JumpCount, score = copy_sp, floor - 44, 180, JK, 0
    n_win = pr_restart = False
    attempts += 1
    cactus.clear()


def save_record(path):
    try:
        connection = sqlite3.connect(path)
        cursor = connection.cursor()
        try:
            cursor.execute(f"""INSERT INTO stat (`date`,attempts,hiscore,jumps)
                               VALUES(datetime('now', '+3 hours'),{attempts},
                               {max(high_score, score)},{total_jumps})""")
            # print('Saved successfully')
            connection.commit()
        except Exception as e:
            print('Save error...', e)
    except Exception:
        print('Connecting error...')


def DrawWindow(screen):
    screen.fill(WHITE)

    screen.blit(clouds, (ob_x, ob_y))
    screen.blit(clouds, (ob_x + 605, ob_y))
    screen.blit(grass, (gr_x, gr_y))
    screen.blit(grass, (gr_x + 509, gr_y))
    screen.blit(grass, (gr_x + 1018, gr_y))

    if not isJump and not n_win:
        personage = dino[anim // (fps // 6) % 2 + 2]
        if dino_low:
            personage = dino[anim // (fps // 6) % 2 + 4]
    elif n_win:
        personage = dino[0]
    else:
        personage = dino[1]

    for cact in cactus:
        cact.update()
        screen.blit(cact.picture, cact.pos)
        if (x + 20) > cact.pos[0] or (x + 60) < (cact.pos[0] + cact.size[0]):
            cact.test_dead()

    if saw_score:
        text_sc = font.render(f'{str(score).rjust(5, "0")}', False, (45, 45, 45))
        text_hig_sc = font.render(f'HI {str(high_score).rjust(5, "0")}', False, (130, 130, 130))
        screen.blit(text_sc, (510, 12))
        screen.blit(text_hig_sc, (365, 12))

    if pr_restart:
        screen.blit(over_game, (width // 2 - 100, height // 2 - 50))

    screen.blit(personage, (x, y))

    pygame.display.update()


pygame.init()

dino = [pygame.image.load('sprite/dino_die.png'), pygame.image.load('sprite/dino_fly.png'),
        pygame.image.load('sprite/dino_shag_1.png'), pygame.image.load('sprite/dino_shag_2.png'),
        pygame.image.load('sprite/dino_low_shag_1.png'), pygame.image.load('sprite/dino_low_shag_2.png')]  # Все 40 x 43
grass = pygame.image.load('sprite/grass.png')  # 605 x 61
clouds = pygame.image.load('sprite/clouds.png')  # 509 x 120
plant = [pygame.image.load('sprite/kakt_1.png'), pygame.image.load('sprite/kakt_2.png'),
         pygame.image.load('sprite/kakt_3.png'), pygame.image.load('sprite/kakt_small.png'),
         pygame.image.load('sprite/kakt_kakts.png'), pygame.image.load('sprite/kakt_big_2.png')]
dino_bird = [pygame.image.load('sprite/dino_bird_1.png'), pygame.image.load('sprite/dino_bird_2.png')]  # 39 x 33
over_game = pygame.image.load('sprite/game_over.png')  # 199 x 74
size_plant = [(23, 46), (32, 33), (49, 33), (15, 33), (73, 47), (48, 46), (39, 33)]

width = 600
height = 221

WHITE = (255, 255, 255)
BIRD = 6

wait_bird = False
font = pygame.font.SysFont('couriernew', 23)
font.set_bold(True)
n_win = pr_restart = False
saw_score = True
dino_low = False

fps = 120
speed = copy_sp = 360 // fps * 1
attempts = 1

anim = sc = 0
total_jumps = 0
floor = 158
isJump = False
JumpCount = JK = 40  # int(fps / 2.85)
random_number = (lambda n: randrange(0, n))
cactus = []
cactus_time_game_out = 360

ob_x, ob_y = 0, 20
gr_x, gr_y = 0, 140
x = 60
y = floor - 44

score = 0
score_de, click_delay = 180, 0
high_score = 0

clock = pygame.time.Clock()
pygame.display.set_caption("SUPER DINO GAME                 by  AndryMaster")
RunGame = True


def run_dino(private=False):
    global anim, click_delay, sc, score, isJump, JumpCount, dino_low, saw_score, cactus_time_game_out
    global x, y, ob_x, ob_y, gr_x, gr_y, RunGame, total_jumps
    screen = pygame.display.set_mode((width, height))

    if private:
        db_path = 'record/dino_statics.db'
    else:
        db_path = 'GoogleDino/record/dino_statics.db'

    while RunGame:
        clock.tick(fps)

        if anim < fps:
            anim += 1
        else:
            anim = 0
        if click_delay > 0:
            click_delay -= 1

        if sc != anim // 12 and not n_win:
            sc = anim // 12
            score += 1

        if cactus_time_game_out > 0:
            cactus_time_game_out -= 1
        if cactus_time_game_out <= 0:
            if not bool(randrange(0, 36)):
                Make_Cactus()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                save_record(db_path)
                RunGame = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and n_win:
                pos = pygame.mouse.get_pos()
                if width // 2 - 80 < pos[0] < width // 2 + 80 and height // 2 - 40 < pos[1] < height // 2 + 14:
                    Restart_Game()

        keys = pygame.key.get_pressed()

        if keys[pygame.QUIT] or keys[pygame.K_ESCAPE] or keys[pygame.K_q]:
            RunGame = False

        if not isJump:
            if (keys[pygame.K_UP] or keys[pygame.K_SPACE]) and not dino_low:
                isJump = True
                total_jumps += 1
        else:
            if JumpCount >= -JK:  # Прыжки
                if JumpCount < 0:
                    y += -JumpCount // 2 // 2 // 2
                elif JumpCount > 0:
                    y -= JumpCount // 2 // 2 // 2
                JumpCount -= 1
            else:
                isJump = False
                JumpCount = JK

        if keys[pygame.K_v] and click_delay <= 0:
            saw_score = not saw_score
            click_delay = 50

        if keys[pygame.K_DOWN]:
            dino_low = True
        else:
            dino_low = False

        if not n_win:
            ob_x -= (speed - 2)
            gr_x -= speed
        if ob_x <= -605:  # Облака
            ob_x = 1
        if gr_x <= -509:  # Грунт
            gr_x = 1

        if n_win and (keys[pygame.K_r] or keys[pygame.K_KP_ENTER]):
            Restart_Game()

        DrawWindow(screen)


if __name__ == '__main__':
    run_dino(private=True)
    pygame.quit()
