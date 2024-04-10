import pygame as pg
import pygame.freetype
import sys
import time
import random
from pygame import mixer

from pygame import Surface, SurfaceType

FPS = 80
pg.init()  # просто надо

white = (250, 250, 250)
blue = (0, 0, 255)
green = (0, 255, 0)
W = 900  # длина по х
H = 500  # высота по y
screen = pg.display.set_mode((W, H))  # создание игрового окна

# скорость прыжка вертикально
pg.display.set_caption('Динозаврик')  # надпись сверху на панельке
clock = pg.time.Clock()
fon = pg.image.load('dino/fon_dino.jpg')
dino_imgs = [pg.image.load(f'dino/Run ({i}).png') for i in range(1, 9)]
dino_imgs = [pg.transform.scale(elem, (110, 110)) for elem in dino_imgs]

dino_deads = [pg.image.load(f'death/Dead ({i}).png') for i in range(1, 4)]
dino_deads = [pg.transform.scale(elem, (110, 110)) for elem in dino_deads]

cactus_img = [pg.image.load('кактусы/кактус.png').convert_alpha(screen),
              pg.image.load('кактусы/Cactus_Sprite_Sheet2.png').convert_alpha(screen),
              pg.image.load('кактусы/Cactus_Sprite_Sheet1.png')]

cactus = pg.transform.scale(random.choice(cactus_img), (80, 80))

hearts_imgs = [pg.image.load(f'жизни/green ({i}).png') for i in range(1, 5)]
hearts_imgs = [pg.transform.scale(elem, (180, 100)) for elem in hearts_imgs]
hearts = pg.transform.scale((hearts_imgs[1]), (30, 30))


class Dinozavr:
    score = 0

    def __init__(self, image, position):
        self.image = image
        for elem in self.image:
            self.rect = elem.get_rect()
            self.rect.center = position
        self.y = 0  # Счетчик
        self.max_jump = 35
        self.in_jump = False
        self.number_sprite = 0
        self.k = 1
        self.in_dead = False
        self.number_picture = 0
        self.count = 1
        self.screen = pygame.display.set_mode((W, H))

    def jump(self):  # операции с прыжком
        if self.in_jump:
            if self.y < self.max_jump:
                self.y += 1
                self.rect.y -= 5
            elif self.y < self.max_jump * 2:
                self.y += 1
                self.rect.y += 5
            else:
                self.in_jump = False
                self.y = 0

    def dead_draw(self):
        self.count = 1
        self.number_picture = 1
        screen.blit(self.image[self.number_picture], self.rect)
        if self.in_dead == True:
            if dino_object.rect.colliderect(cactus_object.rect) == True and self.count % 4 == 0:
                if self.in_dead == True:
                    self.number_picture += 1
                    if self.number_picture == len(self.image):
                        self.number_picture = 0
            self.count += 1

    def draw(self):  # для отображения всего необходимого
        # screen.blit(self.image, self.rect)
        screen.blit(self.image[self.number_sprite], self.rect)
        if self.k % 6 == 0:

            self.number_sprite += 1
            if self.number_sprite == len(self.image):
                if not self.in_dead:
                    self.number_sprite = 0
                else:
                    self.number_sprite = 2
        self.k += 1


class Cactus:
    def __init__(self, image, position):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.y = 0  # Счетчик
        self.speed = 5

    def stand(self):  # Движение
        global random_symbol
        self.rect.x -= self.speed
        if self.rect.x <= 0:
            Dinozavr.score += 1
            random_symbol = get_sentence()
            sound = pygame.mixer.Sound(f"music/{random_symbol[0]}.mp3")
            sound.play()
            self.image = pg.transform.scale(random.choice(cactus_img), (80, 80))
            self.rect.x = 900
        if self.y % 1000 == 0:
            self.speed += 1

    def draw(self):  # для отображения всего необходимого
        screen.blit(self.image, self.rect)


class Hearts:
    def __init__(self, image, position):
        self.image = image
        self.count = 0
        self.position = position

    def draw_lifes(self):
        screen.blit(self.image[self.count], self.position)


def draw_line():  # для отображения всего необходимого
    pg.draw.rect(screen, "black", (0, 450, 900, 20))


def get_sentence():
    with open("alfavit.txt", encoding="utf-8") as f:
        text = f.read()
    sentences = text.split('\n')
    sentence = random.choice(sentences)
    return sentence


# def draw_text(self, screen, msg, y, fsize, color):
#     font = pg.font.SysFont('cosmeticians', 50)
#     text = font.render(msg, 1, color)
#     text_rect = text.get_rect(center=(W / 2, H / 2))
#     screen.blit(text, text_rect)
#     pygame.display.update()
#     self.draw_button(self.screen, 315, 450)

mixer.music.load('mus/фоновое.mp3')
mixer.music.set_volume(0.3)
mixer.music.play(-1)

dino_object = Dinozavr(dino_imgs, (100, 405))
lifes_objects = Hearts(hearts_imgs, (685, 130))
cactus_object = Cactus(cactus, (900, 419))
dino_deads_objects = Dinozavr(dino_deads, (100, 405))

run = True  # чтоб удобнее было

"""QUIT - событие, происходящее, когда пользователь закрывает/останавливает
 программу pygame.
 KEYDOWN - событие, происходящее, когда пользователь
 наживает клавишу на клавиатуре."""
random_symbol = ""
is_sound = False
while run:  # делаем следующие действия во время запуска
    for event in pg.event.get():  # получить данные о происходящем в данный момент события
        if event.type == pg.QUIT:  # для удобного закрытия игрового окна без лагов
            run = False # приостановка действий
        if event.type == pg.KEYDOWN:
            if dino_object.in_dead and not (lifes_objects.count == 3 and dino_object.number_sprite == 2):
                dino_object.in_dead = False
                dino_object.image = dino_imgs
                dino_object.number_sprite = 0
            elif event.key == pg.K_SPACE:
                dino_object.in_jump = True
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button in (1, 3) and dino_object.in_dead and lifes_objects.count == 3 \
                    and dino_object.number_sprite == 2:
                x, y = event.pos
                if 360 <= x <= 490 and 280 <= y <= 320:
                    # Рестарт
                    dino_object.in_dead = False
                    dino_object.image = dino_imgs
                    dino_object.number_sprite = 0
                    lifes_objects.count = 0
                    dino_object.number_sprite = 0
                    # follow = font.render(f"Счет: 0}", 1, (0, 0, 0), (0, 255, 0))
                    Dinozavr.score = 0
                    random_symbol = ""
                    is_sound = False
                    mixer.music.play(-1)

    screen.blit(fon, (0, 0))  # заливка фона
    draw_line()
    lifes_objects.draw_lifes()
    dino_object.jump()
    dino_object.draw()

    if not dino_object.in_dead:
        cactus_object.draw()
        cactus_object.stand()
        cactus_object.y += 1

    if dino_object.in_dead and lifes_objects.count == 3 and dino_object.number_sprite == 2:
        if not is_sound:
            mixer.music.stop()
            sound_game_over = pygame.mixer.Sound("mus/game_over1.wav")
            sound_game_over.play()
            is_sound = True
        random_symbol = ""
        screen.fill('black')
        # screen = pygame.display.set_mode((W, H))
        pygame.draw.rect(screen, (50, 205, 50), (360, 280, 130, 40))
        # draw_text(screen, "Перезапуск", 470, 18, (102, 0, 51), (0, 0, 0))
        font = pg.font.SysFont('cosmeticians', 50)
        string = font.render("Game over", 1, (0, 250, 154))
        screen.blit(string, (340, 200))
        font_2 = pg.font.SysFont('cosmeticians', 30)
        string_restart = font_2.render("Перезапуск", 1, (0, 100, 0))
        screen.blit(string_restart, (368, 290))

    if dino_object.rect.colliderect(
            cactus_object.rect) == True:  # номер картинки (на 1 картинке 3 сердечка, на второй на 1 меньше и тд)
        lifes_objects.count += 1
        dino_object.in_dead = True
        dino_object.image = dino_deads
        dino_object.number_sprite = 0
        cactus = pg.transform.scale(random.choice(cactus_img), (80, 80))
        cactus_object = Cactus(cactus, (900, 419))

    font = pg.font.SysFont('cosmeticians', 50)
    follow = font.render(f"Счет: {Dinozavr.score}", 1, (0, 0, 0), (0, 255, 0))
    symbol_tr = font.render(random_symbol, 1, (0, 0, 0))

    screen.blit(follow, (720, 50))
    screen.blit(symbol_tr, (W // 2, H // 2))
    pg.display.flip()  # чтобы отображалось все, что написано выше
    clock.tick(FPS)
