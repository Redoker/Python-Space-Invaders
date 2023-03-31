import pygame
import keyboard
import sys
import random
import time

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

# объект игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((25, 25))
        self.image.fill(GREEN)
        self.rect = self.image.get_rect()
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
        # размер врага
        self.image = pygame.Surface((40, 30))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.right > WIDTH or self.rect.left < 0:
            self.speedx = -self.speedx

        if self.rect.top > HEIGHT + 10:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

# объект пули
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
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

# спрайты
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
bullets = pygame.sprite.Group()
for i in range(8):
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
        #elif key[pygame.K_SPACE]:
        #   player.shoot()

    for _ in range(10):
        player.shoot()
        time.sleep(1)

    # обновление спрайтов
    all_sprites.update()

    # проверка попадания
    hits = pygame.sprite.spritecollide(player, enemies, False)
    if hits:
        running = False

    # заполнение (рендеринг) экрана
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # показываем экран после отрисовки
    pygame.display.flip()

pygame.quit()