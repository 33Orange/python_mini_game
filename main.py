import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_SPACE, K_q, K_r, K_w, K_a, K_s, K_d
from os import listdir
import random

is_working = True
game_state = 'start_screen'
is_initial_set_events_timers = True

BG_IMG = './assets/background.png'
PLAYER_IMG = './assets/player.png'
COIN_IMG = './assets/bonus.png'
ENEMY_IMG = './assets/enemy.png'
PLAYER_IMGS = './assets/goose'

BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)

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

# MAIN CONFIG
pygame.init()

FPS = pygame.time.Clock()

display_info = pygame.display.Info()
# screen = w, h = display_info.current_w, display_info.current_h
screen = w, h = 1440, 768
main_surface = pygame.display.set_mode(screen)

bg = pygame.transform.scale(pygame.image.load(BG_IMG).convert(), screen)
bgX = 0
bgX2 = bg.get_width()

font = pygame.font.SysFont('Verdana', 40)

# CREATE EVENTS
CREATE_ENEMY = pygame.USEREVENT + 0
CREATE_COIN = pygame.USEREVENT + 1
CHANGE_PLAYER_FRAME = pygame.USEREVENT + 2

def set_spawn_timers():
    print('set spawn timers')
    pygame.time.set_timer(CREATE_COIN, COIN_PERIOD)
    pygame.time.set_timer(CREATE_ENEMY, ENEMY_PERIOD)
    pygame.time.set_timer(CHANGE_PLAYER_FRAME, CHANGE_PLAYER_FRAME_PERIOD)

def create_player():
    player_frames = [pygame.image.load(PLAYER_IMGS + '/' + file).convert_alpha() for file in listdir(PLAYER_IMGS)]
    player = player_frames[player_frames_index]
    player_rect = player.get_rect()
    return {"surface": player, "rect": player_rect, "frames": player_frames}

def create_enemy():
    enemy = pygame.transform.scale(pygame.image.load(ENEMY_IMG).convert_alpha(), ENEMY_SIZE)
    enemy_rect = pygame.Rect(w + enemy.get_width(), random.randint(0, h), *enemy.get_size())
    enemy_speed = random.randint(ENEMY_SPEED_RANGE[0], ENEMY_SPEED_RANGE[1])
    return {"surface": enemy, "rect": enemy_rect, "speed": enemy_speed}

def create_coin():
    coin = pygame.transform.scale(pygame.image.load(COIN_IMG).convert_alpha(), COIN_SIZE)
    coin_rect = pygame.Rect(random.randint(0, w), 0 - coin.get_height(), *coin.get_size())
    coin_speed = random.randint(COIN_SPEED_RANGE[0], COIN_SPEED_RANGE[1])
    return {"surface": coin, "rect": coin_rect, "speed": coin_speed}

def create_start_screen():
    title = font.render('Press Space to start game', True, BLACK_COLOR)
    main_surface.blit(title, (w/2 - title.get_width()/2, h/2 - title.get_height()/2))
    pygame.display.update()

def draw_game_over_screen():
    title = font.render('Game Over', True, BLACK_COLOR)
    points = font.render('Points ' + str(player_score), True, BLACK_COLOR)
    restart_quit_buttons = font.render('R - Restart | Q - Quit', True, BLACK_COLOR)
    main_surface.blit(title, (w/2 - title.get_width()/2, h/2 - title.get_height()/3))
    main_surface.blit(points, (w/2 - points.get_width()/2, h/1.9 + points.get_height()))
    main_surface.blit(restart_quit_buttons, (w/2 - restart_quit_buttons.get_width()/2, h/2 + restart_quit_buttons.get_height()/2))
    pygame.display.update()

def clear():
    enemies.clear()
    coins.clear()

while is_working:
    FPS.tick(60)
    pressed_key = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == QUIT:
            is_working = False

        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        
        if event.type == CREATE_COIN:
            coins.append(create_coin())
        
        if event.type == CHANGE_PLAYER_FRAME:
            player_frames_index += 1
            if player_frames_index == len(player['frames']):
                player_frames_index = 0
            player['surface'] = player['frames'][player_frames_index]


    main_surface.blit(bg, (bgX, 0))
    main_surface.blit(bg, (bgX2, 0))

    if game_state == 'start_screen':
        create_start_screen()
        # KEYS BINDING
        if pressed_key[K_SPACE] and game_state == 'start_screen':
            clear()
            player_score = 0
            player = create_player()
            game_state = 'game_start'


    elif game_state == 'game_start':
        if is_initial_set_events_timers:
            set_spawn_timers()
            is_initial_set_events_timers = False

        bgX -= BG_SPEED
        bgX2 -= BG_SPEED

        if bgX < -bg.get_width():
            bgX = bg.get_width()
        if bgX2 < -bg.get_width():
            bgX2 = bg.get_width()  

        main_surface.blit(player['surface'], player['rect'])

        rendered_text = font.render(SCORE_TEXT + str(player_score), True, BLACK_COLOR)

        main_surface.blit(rendered_text, (w - rendered_text.get_width(), 0))

        for enemy in enemies:
            main_surface.blit(enemy['surface'], enemy['rect'])
            enemy['rect'] = enemy['rect'].move(-enemy['speed'], 0)

            if enemy['rect'].right < 0:
                enemies.pop(enemies.index(enemy))

            if player['rect'].colliderect(enemy['rect']):
                game_state = 'game_over'

        for coin in coins:
            main_surface.blit(coin['surface'], coin['rect'])
            coin['rect'] = coin['rect'].move(0, coin['speed'])

            if coin['rect'].top > h:
                coins.pop(coins.index(coin))

            if player['rect'].colliderect(coin['rect']):
                coins.pop(coins.index(coin))
                player_score += 1

        # KEYs BINDING
        if pressed_key[K_DOWN] or pressed_key[K_s] and player['rect'].bottom <= h:
            player['rect'] = player['rect'].move(0, player_speed)

        if pressed_key[K_UP] or pressed_key[K_w] and player['rect'].top >= 0:
            player['rect'] = player['rect'].move(0, -player_speed)

        if pressed_key[K_RIGHT] or pressed_key[K_d] and player['rect'].right <= w:
            player['rect'] = player['rect'].move(player_speed, 0)

        if pressed_key[K_LEFT] or pressed_key[K_a] and player['rect'].left >= 0:
            player['rect'] = player['rect'].move(-player_speed, 0)

    elif game_state == 'game_over':
        draw_game_over_screen()
        if pressed_key[K_q]:
            is_working = False
        if pressed_key[K_r]:
            game_state = 'start_screen'
    pygame.display.flip()
