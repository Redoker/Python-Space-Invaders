import pygame
import keyboard
import sys
import random
from os import path

running = True

# базовые настройки экрана игры
WIDTH = 600
HEIGHT = 700
FPS = 60

# Цвет
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Определение файлов игры
imgDir = path.join(path.dirname(__file__), 'img')

# объект игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = playerImg
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.bottom = (HEIGHT - 50)
        self.rect.centerx = (WIDTH / 2)

    def update(self):
        # начальная скорость передвижения
        self.speedx = 0
        self.speedy = 0

        # нажатие кнопки управления
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speedx -= 5
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speedx += 5
        if keystate[pygame.K_UP] or keystate[pygame.K_w]:
            self.speedy -= 5
        if keystate[pygame.K_DOWN] or keystate[pygame.K_s]:
            self.speedy += 5
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)

# объект врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        # спрайт врага
        self.imageOrig = random.choice(meteorImages)
        self.image = self.imageOrig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rotSpeed = random.randrange(-9, 9)
        self.lastUpdate = pygame.time.get_ticks()

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speedx = -self.speedx

        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)

    # вращение астероида
    def rotate(self):
        now = pygame.time.get_ticks()
        if now - self.lastUpdate > 50:
            self.lastUpdate = now
            self.rot = (self.rot + self.rotSpeed) % 360
            new_image = pygame.transform.rotate(self.imageOrig, self.rot)
            oldCenter = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = oldCenter

# объект пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bulletImg
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            # Если пуля заходит за верхний край, то убить
            self.kill()

# инициализация игры и окна
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders by Yaroslav")
clock = pygame.time.Clock()

# Загрузка файлов графики
background = pygame.image.load('img/Backgrounds/blue.png')
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
backgroundRect = background.get_rect()
playerImg = pygame.image.load('img/player/playerShip3_green.png')
playerImg = pygame.transform.scale(playerImg, (50, 45))
bulletImg = pygame.image.load('img/player/laserRed05.png')
meteorImages = []
meteorList = ['meteorBrown_big2.png', 'meteorBrown_med1.png',
              'meteorBrown_med3.png', 'meteorBrown_small1.png',
              'meteorBrown_small2.png', 'meteorBrown_tiny2.png',
              'meteorGrey_big4.png', 'meteorGrey_med1.png',
              'meteorGrey_med2.png', 'meteorGrey_small1.png',
              'meteorGrey_small2.png', 'meteorGrey_tiny1.png']
for img in meteorList:
    meteorImages.append(pygame.image.load('img/enemy/' + img))

# спрайты
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
for i in range(15):
    e = Enemy()
    all_sprites.add(e)
    enemies.add(e)

while running:
    # цикл обновления экрана
    clock.tick(FPS)

    # событие игры
    for event in pygame.event.get():
        key = pygame.key.get_pressed()
        if event.type == pygame.QUIT or key[pygame.K_ESCAPE]:
            running = False
        elif key[pygame.K_SPACE]:
          player.shoot()

    # обновление спрайтов
    all_sprites.update()

    # проверка попадания
    hits = pygame.sprite.spritecollide(player, enemies, False, pygame.sprite.collide_circle)
    if hits:
        running = False

    # проверка попадания выстрело
    shootHits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for shootHit in shootHits:
        e = Enemy()
        all_sprites.add(e)
        enemies.add(e)

    # заполнение (рендеринг) экрана
    screen.fill(BLACK)
    screen.blit(background, backgroundRect)
    all_sprites.draw(screen)

    # показываем экран после отрисовки
    pygame.display.flip()

pygame.quit()