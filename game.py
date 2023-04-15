import pygame as py
import os
py.font.init()
py.mixer.init()

WIDTH, HEIGHT = 800, 900
WINDOW = py.display.set_mode((WIDTH, HEIGHT))
py.display.set_caption('BOT WARS')

GOLD = (255, 215, 0) # Background color. After changing background to an image, i set gold as the winner text color
CYAN = (0, 255, 255)
PALE_LAVENDER =  (230, 230, 250) # Used image for bullets so this color wasn't used... Ended up using it for player names
BEIGE = (245, 245, 220) # Used image for bullets so this color wasn't used
WHITE = (255, 255, 255)

BORDER = py.Rect(0, HEIGHT//2 - 5, WIDTH, 10)

BULLET_HIT_SOUND = py.mixer.Sound(os.path.join('Assets', 'launch.mp3'))
BULLET_LAUNCH_SOUND = py.mixer.Sound(os.path.join('Assets', 'Impact.mp3'))

HEALTH_FONT = py.font.SysFont('comic sans ms', 30)
WINNER_FONT = py.font.SysFont('comic sans ms', 75)
INFO_FONT = py.font.SysFont('comic sans ms', 20)
PLAYER_FONT = py.font.SysFont('comic sans ms', 15)

# How fast our game runs, frames per second => FPS
FPS = 60
# How fast the characters will move when user presses key
VELOCITY = 5
# Bullet speed
BULLET_VEL = 10
MAX_BULLETS = 3
FIGHTERS_WIDTH, FIGHTERS_HEIGHT = 100, 120

P1_HIT = py.USEREVENT + 1
P2_HIT = py.USEREVENT + 2

PLAYER_1_IMAGE = py.image.load(os.path.join('Assets', 'player1.png'))
PLAYER_1 = py.transform.scale(PLAYER_1_IMAGE, (FIGHTERS_WIDTH, FIGHTERS_HEIGHT))
PLAYER_2_IMAGE = py.image.load(os.path.join('Assets', 'player2.png'))
PLAYER_2 = py.transform.rotate(py.transform.scale(PLAYER_2_IMAGE, (FIGHTERS_WIDTH, FIGHTERS_HEIGHT)), 180)

SNOW_BULLET_IMAGE = py.image.load(os.path.join('Assets', 'snowflake.png'))
SNOW_BULLET = py.transform.scale(SNOW_BULLET_IMAGE, (27, 32))
FIRE_BULLET_IMAGE = py.image.load(os.path.join('Assets', 'fireball.png'))
FIRE_BULLET = py.transform.rotate(py.transform.scale(FIRE_BULLET_IMAGE, (27, 32)), -35)



BACKGROUND = py.transform.scale(py.image.load(os.path.join('Assets', 'background.jpg')), (WIDTH, HEIGHT))

# Draw function used to display all designing to window
# We call the function in the main function so the window gets updated each time with the designs
def draw_window(p1, p2, p1_bullets, p2_bullets, p1_health, p2_health):
    WINDOW.blit(BACKGROUND, (0, 0))
    py.draw.rect(WINDOW, CYAN, BORDER)

    p1_health_text = HEALTH_FONT.render('SURVIVAL: ' + str(p1_health), 1, WHITE)
    p2_health_text = HEALTH_FONT.render('SURVIVAL: ' + str(p2_health), 1, WHITE)
    WINDOW.blit(p1_health_text, (5, 5))
    WINDOW.blit(p2_health_text, (580, 855))

    # Display the "wasd" and "Arrow keys" text so users know how to play and move
    wasd_text = INFO_FONT.render('MOVE ~ WASD', 1, WHITE)
    arrow_keys_text = INFO_FONT.render('MOVE ~ ARROW KEYS', 1, WHITE)
    wasd_launch = INFO_FONT.render('SHOOT ~ R', 1, WHITE)
    arrow_keys_launch = INFO_FONT.render('SHOOT ~ L', 1, WHITE)
    WINDOW.blit(wasd_text, (WIDTH-wasd_text.get_width()-5, 5))
    WINDOW.blit(arrow_keys_text, (5, HEIGHT-arrow_keys_text.get_height()-5))
    WINDOW.blit(wasd_launch, (WIDTH-wasd_text.get_width()-5, wasd_text.get_height()+10))
    WINDOW.blit(arrow_keys_launch, (5, HEIGHT-arrow_keys_text.get_height()-arrow_keys_launch.get_height()-10))

    # Display names player 1 and player 2 so players know which side is which
    p1_name = PLAYER_FONT.render('PLAYER 1', 1, PALE_LAVENDER)
    p2_name = PLAYER_FONT.render('PLAYER 2', 1, PALE_LAVENDER)
    WINDOW.blit(p1_name, (p1.x + PLAYER_1.get_width()//2 - p1_name.get_width()//2, p1.y - p1_name.get_height() + 20))
    WINDOW.blit(p2_name, (p2.x + PLAYER_2.get_width()//2 - p2_name.get_width()//2, p2.y + PLAYER_2.get_height() - 20))

    WINDOW.blit(PLAYER_1, (p1.x, p1.y))
    WINDOW.blit(PLAYER_2, (p2.x, p2.y))

    for bullet in p2_bullets:
        WINDOW.blit(SNOW_BULLET, bullet)
    
    for bullet in p1_bullets:
        WINDOW.blit(FIRE_BULLET, bullet)

    py.display.update()

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, GOLD)
    text_rect = draw_text.get_rect(center=(WIDTH/2, HEIGHT/2))
    WINDOW.blit(draw_text, text_rect)
    py.display.update()
    py.time.delay(3000) # Game resets after 3 seconds. User can leave by exiting window



def player1_movement(keys_pressed, p1):
    if keys_pressed[py.K_a]:
        p1.x = max(p1.x - VELOCITY, -20)  # Move left, but not past the left side
    if keys_pressed[py.K_d]:
        p1.x = min(p1.x + VELOCITY, WIDTH - FIGHTERS_WIDTH + 20)  # Move right, but not past the right side
    if keys_pressed[py.K_w]:
        p1.y = max(p1.y - VELOCITY, -30)  # Move up, but not past the top
    if keys_pressed[py.K_s]:
        p1.y = min(p1.y + VELOCITY, HEIGHT/2 - FIGHTERS_HEIGHT + 15)  # Move down, but not past the border

def player2_movement(keys_pressed, p2):
    if keys_pressed[py.K_LEFT]:
        p2.x = max(p2.x - VELOCITY, -20)  # Move left, but not past the left side
    if keys_pressed[py.K_RIGHT]:
        p2.x = min(p2.x + VELOCITY, WIDTH - FIGHTERS_WIDTH + 20)  # Move right, but not past the right side
    if keys_pressed[py.K_UP]:
        p2.y = max(p2.y - VELOCITY, HEIGHT/2 - 15)  # Move up, but not past the border
    if keys_pressed[py.K_DOWN]:
        p2.y = min(p2.y + VELOCITY, HEIGHT - FIGHTERS_HEIGHT + 30)  # Move down, but not past the bottom

def handle_bullets(p1_bullets, p2_bullets, p1, p2):
    # Check if player 2 gets hit
    for bullet in p1_bullets:
        bullet.y += BULLET_VEL
        if p2.colliderect(py.Rect(bullet.x, bullet.y - 25, bullet.width, bullet.height - 5)):
            py.event.post(py.event.Event(P2_HIT))
            p1_bullets.remove(bullet)
        elif bullet.y > WIDTH + 100:
            p1_bullets.remove(bullet)
    # Check if player 1 gets hit
    for bullet in p2_bullets:
        bullet.y -= BULLET_VEL
        if p1.colliderect(py.Rect(bullet.x, bullet.y + 35, bullet.width, bullet.height - 5)):
            py.event.post(py.event.Event(P1_HIT))
            p2_bullets.remove(bullet)
        elif bullet.y < 0:
            p2_bullets.remove(bullet)


def main():
    p2 = py.Rect(550, 700, FIGHTERS_WIDTH, FIGHTERS_HEIGHT)
    p1 = py.Rect(150, 100, FIGHTERS_WIDTH, FIGHTERS_HEIGHT)
    
    p1_bullets = []
    p2_bullets = []

    p1_health = 15
    p2_health = 15

    clock = py.time.Clock()
    run = True
    while run:
        clock.tick(FPS) # Controls the speed of the while loop
        for event in py.event.get():
            if event.type == py.QUIT:
                run = False
                py.quit()

            if event.type == py.KEYDOWN:
                if event.key == py.K_r and len(p1_bullets) < MAX_BULLETS:
                    # Launch the bullet from middle of character 1
                    bullet = py.Rect(p1.x + FIGHTERS_WIDTH//2 - 12, p1.y + FIGHTERS_HEIGHT, 7, 15)
                    p1_bullets.append(bullet)
                    BULLET_LAUNCH_SOUND.play()
                if event.key == py.K_l and len(p2_bullets) < MAX_BULLETS:
                    # Launch the bullet from middle of character 2
                    bullet = py.Rect(p2.x + FIGHTERS_WIDTH//2 - 12, p2.y, 7, 15)
                    p2_bullets.append(bullet)
                    BULLET_LAUNCH_SOUND.play()

            if event.type == P1_HIT:
                p1_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == P2_HIT:
                p2_health -= 1
                BULLET_HIT_SOUND.play()

        if p1_health == 0:
            winner_message = 'PLAYER 2 HAS WON! '
            draw_winner(winner_message)
            break
            

        if p2_health == 0:
            winner_message = 'PLAYER 1 HAS WON!'
            draw_winner(winner_message)
            break
    
        keys_pressed = py.key.get_pressed()
        player1_movement(keys_pressed, p1)
        player2_movement(keys_pressed, p2)

        handle_bullets(p1_bullets, p2_bullets, p1, p2)

        draw_window(p1, p2, p1_bullets, p2_bullets, p1_health, p2_health)
    
    main()

if __name__ == "__main__":
    main()


"""Line 195 one causes an eroor in terminal but doesn't affect the game. It shows because code is calling main function until user exits window. 
   If you change that line with py.quit(), the error will be gone from terminal but the game will only run once."""