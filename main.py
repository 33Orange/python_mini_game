import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE
from os import listdir
import random

is_working = True

BG_IMG = './assets/background.png'
PLAYER_IMG = './assets/player.png'
COIN_IMG = './assets/bonus.png'
ENEMY_IMG = './assets/enemy.png'
PLAYER_IMGS = './assets/goose'

SCORE_COLOR = (0, 0, 0)

COIN_SIZE = (90, 150)
ENEMY_SIZE = (153, 54)
BG_SPEED = 3
player_speed = 5
ENEMY_SPEED_RANGE = (5, 10)
COIN_SPEED_RANGE = (2, 4)

CHANGE_PLAYER_FRAME_PERIOD = 125
ENEMY_PERIOD = 1500
COIN_PERIOD = 5000

SCORE_TEXT = 'POINTS: '

player_frames_index = 0
player_score = 0
enemies = []
coins = []

pygame.init()

display_info = pygame.display.Info()
screen = w, h = display_info.current_w, display_info.current_h

FPS = pygame.time.Clock()

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, ENEMY_PERIOD)

CREATE_COIN = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_COIN, COIN_PERIOD)

CHANGE_PLAYER_FRAME = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_PLAYER_FRAME, CHANGE_PLAYER_FRAME_PERIOD)

main_surface = pygame.display.set_mode(screen)

font = pygame.font.SysFont('Verdana', 40)

bg = pygame.transform.scale(pygame.image.load(BG_IMG).convert(), screen)

bgX = 0
bgX2 = bg.get_width()

player_frames = [pygame.image.load(PLAYER_IMGS + '/' + file).convert_alpha() for file in listdir(PLAYER_IMGS)]
player = player_frames[player_frames_index]
player_rect = player.get_rect()

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load(ENEMY_IMG).convert_alpha(), ENEMY_SIZE)
    enemy_rect = pygame.Rect(w + enemy.get_width(), random.randint(0, h), *enemy.get_size())
    enemy_speed = random.randint(ENEMY_SPEED_RANGE[0], ENEMY_SPEED_RANGE[1])
    return [enemy, enemy_rect, enemy_speed]

def create_coin():
    coin = pygame.transform.scale(pygame.image.load(COIN_IMG).convert_alpha(), COIN_SIZE)
    coin_rect = pygame.Rect(random.randint(0, w), 0 - coin.get_height(), *coin.get_size())
    coin_speed = random.randint(COIN_SPEED_RANGE[0], COIN_SPEED_RANGE[1])
    return [coin, coin_rect, coin_speed]


while is_working:
    FPS.tick(60)

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_COIN:
            coins.append(create_coin())
        
        if event.type == CHANGE_PLAYER_FRAME:
            player_frames_index += 1
            if player_frames_index == len(player_frames):
                player_frames_index = 0
            player = player_frames[player_frames_index]

    pressed_key = pygame.key.get_pressed()

    bgX -= BG_SPEED
    bgX2 -= BG_SPEED

    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    if bgX < -bg.get_width():
        bgX = bg.get_width()

    if bgX2 < -bg.get_width():
        bgX2 = bg.get_width()  

    main_surface.blit(player, player_rect)

    rendered_text = font.render(SCORE_TEXT + str(player_score), True, SCORE_COLOR)

    main_surface.blit(rendered_text, (w - rendered_text.get_width(), 0))
    for enemy in enemies:
        main_surface.blit(enemy[0], enemy[1])
        enemy[1] = enemy[1].move(-enemy[2], 0)

        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
        
        if player_rect.colliderect(enemy[1]):
            is_working = False

    for coin in coins:
        main_surface.blit(coin[0], coin[1])
        coin[1] = coin[1].move(0, coin[2])

        if coin[1].bottom > h:
            coins.pop(coins.index(coin))
        
        if player_rect.colliderect(coin[1]):
            coins.pop(coins.index(coin))
            player_score += 1

    if pressed_key[K_DOWN] and player_rect.bottom <= h:
        player_rect = player_rect.move(0, player_speed)

    if pressed_key[K_UP] and player_rect.top >= 0:
        player_rect = player_rect.move(0, -player_speed)
    
    if pressed_key[K_RIGHT] and player_rect.right <= w:
        player_rect = player_rect.move(player_speed, 0)

    if pressed_key[K_LEFT] and player_rect.left >= 0:
        player_rect = player_rect.move(-player_speed, 0)

    pygame.display.flip()
