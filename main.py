import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE
import numpy as np
import random

screen = w, h = 1440, 768
is_working = True

BG_COLOR = (0, 0, 0)
BALL_COLOR = (134, 231, 222)
ENEMY_COLOR = (255, 0, 0)
COIN_COLOR = (229, 186, 14)

BALL_SIZE = (50, 50)
ENEMY_SIZE = (40, 40)
COIN_SIZE = (25, 25)

ball_speed = 5
ENEMY_SPEED_RANGE = (5, 10)
COIN_SPEED_RANGE = (2, 4)

ENEMY_PERIOD = 500
COIN_PERIOD = 5000

pygame.init()

FPS = pygame.time.Clock()
CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_PERIOD)

CREATE_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_COIN, COIN_PERIOD)

main_surface = pygame.display.set_mode(screen)

ball = pygame.Surface(BALL_SIZE)
ball.fill(BALL_COLOR)
ball_rect = ball.get_rect()

def create_enemy():
    enemy = pygame.Surface(ENEMY_SIZE)
    enemy.fill(ENEMY_COLOR)
    enemy_rect = pygame.Rect(w, random.randint(0, h), *enemy.get_size())
    enemy_speed = random.randint(ENEMY_SPEED_RANGE[0], ENEMY_SPEED_RANGE[1])
    return [enemy, enemy_rect, enemy_speed]

def create_coin():
    coin = pygame.Surface(COIN_SIZE)
    coin.fill(COIN_COLOR)
    coin_rect = pygame.Rect(random.randint(0, w), 0, *coin.get_size())
    coin_speed = random.randint(COIN_SPEED_RANGE[0], COIN_SPEED_RANGE[1])
    return [coin, coin_rect, coin_speed]

enemies = []
coins = []

while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_COIN:
            coins.append(create_coin())

    pressed_key = pygame.key.get_pressed()

    main_surface.fill(BG_COLOR)

    main_surface.blit(ball, ball_rect)

    for enemy in enemies:
        main_surface.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(-enemy[2], 0)

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        
        if ball_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))

    for coin in coins:
        main_surface.blit(coin[0], coin[1])
        coin[1] = coin[1].move(0, coin[2])

        if coin[1].bottom > h:
            coins.pop(coins.index(coin))
        
        if ball_rect.colliderect(coin[1]):
            coins.pop(coins.index(coin))

    if pressed_key[K_DOWN] and ball_rect.bottom <= h:
        ball_rect = ball_rect.move(0, ball_speed)

    if pressed_key[K_UP] and ball_rect.top >= 0:
        ball_rect = ball_rect.move(0, -ball_speed)
    
    if pressed_key[K_RIGHT] and ball_rect.right <= w:
        ball_rect = ball_rect.move(ball_speed, 0)

    if pressed_key[K_LEFT] and ball_rect.left >= 0:
        ball_rect = ball_rect.move(-ball_speed, 0)

    pygame.display.flip()


# if ball_rect.bottom >= h or ball_rect.top <= 0:
#     ball_speed[1]= -ball_speed[1]
#     ball.fill(list(np.random.choice(range(256), size=3)))
    
# if ball_rect.right >= w or ball_rect.left <= 0:
#     ball_speed[0]= -ball_speed[0]
#     ball.fill(list(np.random.choice(range(256), size=3)))