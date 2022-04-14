import os
import pygame
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 1200, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GaME")

GREEN_HIT = pygame.USEREVENT + 2
RED_HIT = pygame.USEREVENT + 1

# COLORS
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY = 128, 128, 128
RED = 255, 0, 0
GREEN = 0, 255, 0

# SOUNDS 
# optional can uncomment 
# BG_SOUND = pygame.mixer.Sound(
#     '/Users/sahilbhor/LIfe/Python/pygame/Space_io/Assets/background.mp3')

BG_SOUND = pygame.mixer.Sound(
    'FILE_PATH/Assets/bg2.mp3')
BG_SOUND.play(-1)

BULLET_HIT_SOUND = pygame.mixer.Sound(
    'FILE_PATH/Assets/laser_shot.wav')
BULLET_FIRE_SOUND = pygame.mixer.Sound(
    'FILE_PATH/Assets/boom.mp3')

BORDER = pygame.Rect((WIDTH//2) - 1.5, 0, 5, HEIGHT)  # Partition

# HEALTH
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 80)

# CONSTANTS
FPS = 60
VELOCITY = 5
BULLET_VELOCITY = 7
MAX_BULLET = 3

spaceship_width = 100
spaceship_height = 90

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('FILE_NAME', 'Assets', 'space.png')), (WIDTH, HEIGHT))

# Red spaceship
red_spaceship_image = pygame.image.load(
    os.path.join('FILE_NAME', 'Assets', 'red_spaceship.png'))
red_spaceship = pygame.transform.rotate(pygame.transform.scale(
    red_spaceship_image, (spaceship_width, spaceship_height)), -90)

# Green spaceship
green_spaceship_image = pygame.image.load(
    os.path.join('FILE_NAME', 'Assets', 'green_spaceship.png'))
green_spaceship = pygame.transform.rotate(pygame.transform.scale(
    green_spaceship_image, (spaceship_width, spaceship_height)), 90)


def draw_window(red, green, red_bullet, green_bullet, red_health, green_health):
    WIN.blit((SPACE), (0, 0))

    pygame.draw.rect(WIN, BLACK, BORDER)  # middle Border

    WIN.blit(red_spaceship, (red.x, red.y))
    WIN.blit(green_spaceship, (green.x, green.y))

    red_health_text = HEALTH_FONT.render(
        "Health : " + str(red_health), 1, WHITE)
    green_health_text = HEALTH_FONT.render(
        "Health : " + str(green_health), 1, WHITE)

    WIN.blit(red_health_text, (10, 10))
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width() - 10, 10))

    for bullet in red_bullet:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in green_bullet:
        pygame.draw.rect(WIN, GREEN, bullet)

    pygame.display.update()


def handle_red(key_pressed, red):
    if key_pressed[pygame.K_a] and red.x - VELOCITY > 0:  # left
        red.x -= VELOCITY
    elif key_pressed[pygame.K_d] and red.x + VELOCITY + red.width-10 < (WIDTH//2):
        red.x += VELOCITY
    elif key_pressed[pygame.K_w] and red.y - VELOCITY > 0:
        red.y -= VELOCITY
    elif key_pressed[pygame.K_s] and red.y + VELOCITY + red.height + 10 < HEIGHT:
        red.y += VELOCITY


def handle_green(key_pressed, green):
    if key_pressed[pygame.K_LEFT] and green.x - VELOCITY > WIDTH//2:
        green.x -= VELOCITY
    elif key_pressed[pygame.K_RIGHT] and green.x + VELOCITY + green.width-10 < WIDTH:
        green.x += VELOCITY
    elif key_pressed[pygame.K_UP] and green.y - VELOCITY > 0:
        green.y -= VELOCITY
    elif key_pressed[pygame.K_DOWN] and green.y + VELOCITY + green.height + 10 < HEIGHT:
        green.y += VELOCITY


def handle_bullets(red_bullets, green_bullets, red, green):
    for bullet in red_bullets:
        bullet.x += BULLET_VELOCITY
        if green.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GREEN_HIT))
            red_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            red_bullets.remove(bullet)

    for bullet in green_bullets:
        bullet.x -= BULLET_VELOCITY
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            green_bullets.remove(bullet)
        elif bullet.x < 0:
            green_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width() //
             2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)


def main():

    red = pygame.Rect(50, HEIGHT//2, spaceship_width, spaceship_height)
    green = pygame.Rect(WIDTH-150, HEIGHT//2,
                        spaceship_width, spaceship_height)

    red_bullet = []
    green_bullet = []

    red_health = 10
    green_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:

                if (event.key == pygame.K_LSHIFT and len(red_bullet) < MAX_BULLET):
                    bullet = pygame.Rect(
                        (red.x + red.width), red.y + red.height//2-2, 10, 5)
                    red_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(green_bullet) < MAX_BULLET:
                    bullet = pygame.Rect(
                        green.x, green.y + green.height//2-2, 10, 5)
                    green_bullet.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

            if event.type == GREEN_HIT:
                green_health -= 1
                BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
            winner_text = "GREEN WINS!"
        if green_health <= 0:
            winner_text = "RED WINS!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        print(red_bullet, green_bullet)
        key_pressed = pygame.key.get_pressed()
        handle_red(key_pressed, red)
        handle_green(key_pressed, green)

        handle_bullets(red_bullet, green_bullet, red, green)

        draw_window(red, green, red_bullet, green_bullet,
                    red_health, green_health)

    main()


if __name__ == '__main__':
    main()
