# TODO:
#   store high scores
#   implement Rect collisions to replace current system

# Imports
import sys
import os
import random
import math
import json
import pygame_textinput
import pygame
from pygame import mixer

# Store the directory this file is running from
CWD = sys.path[0]

# Default scores data
scores_default = {"AAA": 555, "BBB": 444, "CCC": 333, "DDD": 222, "EEE": 111}

# Load scores if file exists, otherwise create file
try:
    with open(os.path.join(CWD, "scores.json"), "r") as scores_json:
        scores_dict = json.load(scores_json)
except:
    with open(os.path.join(CWD, "scores.json"), "w") as scores_json:
        json.dump(scores_default, scores_json)
        scores_dict = json.dumps(scores_default)

# input("\nPress Enter to continue...") # Pause the interface.

# Initialise pygame
pygame.init()

# Create TextInput-object
textinput = pygame_textinput.TextInput(
    font_family="",
    font_size=100,
    text_color=(98, 175, 57),
    cursor_color=(255, 255, 254),
    repeat_keys_initial_ms=400,
    repeat_keys_interval_ms=35,
    max_string_length=3,
)

# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Hide mouse cursor
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# Background
background = pygame.image.load(os.path.join(CWD, "images/hen_house2.png"))
background_blur = pygame.image.load(os.path.join(CWD, "images/hen_house_blur.png"))

# Music Settings
mixer.music.load(os.path.join(CWD, "audio/chicken_dance_song.wav"))
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Chicken Defender")
icon = pygame.image.load(os.path.join(CWD, "images/chick.png"))
pygame.display.set_icon(icon)

# Button images
button_reset_image = pygame.image.load(os.path.join(CWD, "images/button_reset.png"))
button_quit_image = pygame.image.load(os.path.join(CWD, "images/button_quit.png"))

# Player settings
PLAYER_START_Y = 515
player_image = pygame.image.load(os.path.join(CWD, "images/pewpew_small.png"))
player_danger = False
player_collision = False
player_x = 370
player_y = PLAYER_START_Y
player_x_change = 0

# Enemy settings
ENEMY_CHANGE_SPEED = 1
ENEMY_CHANGE_HEIGHT = 70
ENEMY_START_HEIGHT = 85
enemy_image = []
enemy_x = []
enemy_y = []
enemy_x_change = []
enemy_y_change = []
enemy_count = 6
enemy_heights = []
# Populate enemy arrays
for i in range(enemy_count):
    enemy_image.append(pygame.image.load(os.path.join(CWD, "images/chick.png")))
    enemy_x.append(random.randint(0, 735))
    enemy_y.append(ENEMY_START_HEIGHT)
    enemy_x_change.append(ENEMY_CHANGE_SPEED)
    enemy_y_change.append(ENEMY_CHANGE_HEIGHT)
    enemy_heights.append(enemy_y[i])

# Projectile shot settings
PROJECTILE_Y_CHANGE = 1.5
PROJECTILE_START_Y = 1000
projectile_image = pygame.image.load(os.path.join(CWD, "images/rhubarb64.png"))
projectile_x = player_x  # Set to not-zero so it doesn't catch the enemys at the bottom if not thrown
projectile_y = 480
projectile_state = "ready"  # ready = ready to throw; throw = moving on screen

# Text format
font = pygame.font.Font(os.path.join(CWD, "fonts/appopaint-Regular.otf"), 42)

# Score settings
SCORE_X = 10
SCORE_Y = -35
score_image = pygame.image.load(os.path.join(CWD, "images/score.png"))
score_value = 0

# Timer settings
TIMER_X = SCREEN_WIDTH - 170
TIMER_Y = SCORE_Y - 10

timer_image = pygame.image.load(os.path.join(CWD, "images/timer.png"))
timer_start = 0
timer_value = 0
timer_pause = 0

# Game Over Settings
game_over = False
over_value = "GAME OVER"
over_font = pygame.font.Font(os.path.join(CWD, "fonts/Feathergraphy2.ttf"), 90)
over_font_background = pygame.font.Font(os.path.join(CWD, "fonts/Feathergraphy2.ttf"), 92)
over_x = 150
over_y = 420  # heh

# Clear the current terminal window depending on OS.
def clear_terminal():
    os.system("cls" if os.name == "nt" else "clear")


def show_score(x, y):
    score = font.render(str(score_value).zfill(4), True, (0, 255, 0))
    screen.blit(score, (x + 23, y + 125))


def show_timer(x, y, value):
    global timer_start
    global timer_start

    if value > 59:
        minutes = int(value / 60)
        seconds = value - (minutes * 60)
    else:
        minutes = 0
        seconds = value

    timer = font.render(str(minutes).zfill(2) + ":" + str(seconds).zfill(2), True, (0, 255, 0))
    screen.blit(timer, (x + 15, y + 135))


def player(x, y):
    screen.blit(player_image, (x, y))


def enemy(x, y, i):
    screen.blit(enemy_image[i], (x, y))


def throw_projectile(x, y):
    global projectile_state
    projectile_state = "throw"
    screen.blit(projectile_image, (x, y))


# THIS NEEDS TO BE REPLACED WITH RECT COLLISIONS
def isCollision(enemy_x, enemy_y, collider_x, collider_y, what):

    distance = math.sqrt(math.pow(enemy_x - collider_x, 2) + math.pow(enemy_y - collider_y, 2))

    if what == "projectile" and distance < 40:
        return True
    elif what == "player" and distance < 48:
        return True
    else:
        return False


def score_table():
    pass


def game_over():
    # Grab global variables so they can be reset within function
    global projectile_state
    global projectile_x
    global projectile_y
    global timer_value
    global scores_dict

    # Stop the music
    mixer.music.stop()

    # Show mouse cursor
    pygame.mouse.set_visible(True)

    over_text_background = over_font.render(over_value, True, (105, 54, 0))
    over_text = over_font.render(over_value, True, (255, 204, 0))

    OUTLINE = [
        (3, 0),
        (3, 3),
        (0, 3),
        (-3, 3),
        (0, -3),
        (-3, -3),
        (-3, 0),
    ]  # Coordinates to blit 3px outline behind text
    while True:
        screen.blit(background, (0, 0))
        for i in OUTLINE:
            screen.blit(over_text_background, (over_x + i[0], over_y + i[1]))

        screen.blit(over_text, (over_x, over_y))
        screen.blit(score_image, (SCORE_X, SCORE_Y))
        screen.blit(timer_image, (TIMER_X, TIMER_Y))

        show_score(SCORE_X, SCORE_Y)
        show_timer(TIMER_X, TIMER_Y, timer_value)

        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_menu()

        if game_run:
            return

        # Feed it with events every frame
        textinput.update(events)
        # Blit its surface onto the screen
        pygame.draw.rect(screen, (0, 0, 0), (325, 5, 150, 100))
        screen.blit(textinput.get_surface(), (330, 20))

        pygame.display.update()


def reset():
    # Grab global variables so they can be reset within function
    global score_value
    global projectile_state
    global projectile_x
    global projectile_y
    global timer_pause
    global timer_start
    global game_run

    score_value = 0
    for j in range(enemy_count):
        enemy_y[j] = ENEMY_START_HEIGHT
    mixer.music.stop()
    mixer.music.play(-1)
    pygame.mouse.set_visible(False)
    projectile_state = "ready"
    projectile_x = player_x
    projectile_y = PLAYER_START_Y
    timer_start = pygame.time.get_ticks()
    timer_pause = 0
    game_run = True


def game_menu():
    # Grab global variables so they can be reset within function
    global score_value
    global projectile_state
    global projectile_x
    global projectile_y
    global timer_pause
    global timer_start
    global game_run

    pause_start = pygame.time.get_ticks()

    # Button position
    BUTTON_RESET_X = 125
    BUTTON_QUIT_X = 425
    BUTTON_BOTH_Y = 250
    BUTTON_BOTH_WIDTH = 250
    BUTTON_BOTH_HEIGHT = 80

    # Stop the music
    mixer.music.pause()

    # Show mouse cursor
    pygame.mouse.set_visible(True)

    while True:
        # Draw blurred background and buttons
        screen.blit(background_blur, (0, 0))
        screen.blit(button_reset_image, (BUTTON_RESET_X, BUTTON_BOTH_Y))
        screen.blit(button_quit_image, (BUTTON_QUIT_X, BUTTON_BOTH_Y))

        mouse = pygame.mouse.get_pos()

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                quit_game()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mouse.set_visible(False)
                    mixer.music.unpause()
                    timer_pause += pygame.time.get_ticks() - pause_start
                    return
                if event.key == pygame.K_SPACE:
                    if (
                        BUTTON_RESET_X <= mouse[0] <= BUTTON_RESET_X + BUTTON_BOTH_WIDTH
                        and BUTTON_BOTH_Y <= mouse[1] <= BUTTON_BOTH_Y + BUTTON_BOTH_HEIGHT
                    ):
                        reset()
                        return

            if event.type == pygame.MOUSEBUTTONDOWN:
                if (
                    BUTTON_RESET_X <= mouse[0] <= BUTTON_RESET_X + BUTTON_BOTH_WIDTH
                    and BUTTON_BOTH_Y <= mouse[1] <= BUTTON_BOTH_Y + BUTTON_BOTH_HEIGHT
                ):
                    reset()
                    return

                if (
                    BUTTON_QUIT_X <= mouse[0] <= BUTTON_QUIT_X + BUTTON_BOTH_WIDTH
                    and BUTTON_BOTH_Y <= mouse[1] <= BUTTON_BOTH_Y + BUTTON_BOTH_HEIGHT
                ):
                    quit_game()

        pygame.display.update()


def quit_game():
    print()
    pygame.quit()
    sys.exit()


# Game loop
game_run = True
timer_start = pygame.time.get_ticks()
while True:

    # Background images
    screen.blit(background, (0, 0))
    screen.blit(score_image, (SCORE_X, SCORE_Y))
    screen.blit(timer_image, (TIMER_X, TIMER_Y))

    # Get mouse position
    mouse = pygame.mouse.get_pos()

    timer_value = int((pygame.time.get_ticks() - timer_start - timer_pause) / 1000)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit_game()

        # Stick player icon to mouse X axis
        if event.type == pygame.MOUSEMOTION:
            player_x = mouse[0]

        # Mouse click throw
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed(num_buttons=3)[0]:
                if projectile_state == "ready":
                    projectile_sound = mixer.Sound(os.path.join(CWD, "audio/throw_sound.wav"))
                    projectile_sound.play()
                    projectile_x = player_x
                    projectile_y = PLAYER_START_Y
                    throw_projectile(round(projectile_x), round(projectile_y))

        # Keyboard controls
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_KP_ENTER:
                game_run = False
                game_over()
            if event.key == pygame.K_ESCAPE:
                game_menu()
            if event.key == pygame.K_LEFT:
                player_x_change = -1.5
                # print("left")
            if event.key == pygame.K_RIGHT:
                player_x_change = 1.5
                # print("right")
            if event.key == pygame.K_SPACE:
                if projectile_state == "ready":
                    projectile_sound = mixer.Sound(os.path.join(CWD, "audio/throw_sound.wav"))
                    projectile_sound.play()
                    projectile_x = player_x
                    projectile_y = PLAYER_START_Y
                    throw_projectile(round(projectile_x), round(projectile_y))

        # Stop movement if left or right key released
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player_x_change = 0

    # Player Movement: Checking player boundary, keeps on screen
    player_x += player_x_change
    if player_x <= 0:
        player_x = 0
    elif player_x >= 736:
        player_x = 736

    # Enemy Movement: Checking enemy boundary, keeps on screen, moves down
    for i in range(enemy_count):
        # Update queue of enemy heights
        enemy_heights.append(enemy_y[i])
        enemy_heights.pop(0)

        # If lowest enemy is below 300 then danger image else normal image
        # Needs danger flag so it ONLY draws to switch the image, not overwrite
        if max(enemy_heights) > 300 and not player_danger:
            player_image = pygame.image.load(os.path.join(CWD, "images/uhoh_small.png"))
            player_danger = True
        elif max(enemy_heights) < 300 and player_danger:
            player_image = pygame.image.load(os.path.join(CWD, "images/pewpew_small.png"))
            player_danger = False

        # Game Over
        player_collision = isCollision(enemy_x[i], max(enemy_heights), player_x, player_y, "player")

        if (enemy_y[i] > 504 and player_collision) or enemy_y[i] >= 2000:
            for j in range(enemy_count):
                enemy_y[j] = 2000
            game_run = False
            game_over()
            break

        # Move enemy
        enemy_x[i] += enemy_x_change[i]
        if enemy_x[i] <= 0:
            enemy_y[i] += enemy_y_change[i]
            enemy_x_change[i] = ENEMY_CHANGE_SPEED
        elif enemy_x[i] >= 736:
            enemy_y[i] += enemy_y_change[i]
            enemy_x_change[i] = -1 * ENEMY_CHANGE_SPEED

        # Collision check
        projectile_collision = isCollision(enemy_x[i], enemy_y[i], projectile_x, projectile_y, "projectile")
        if projectile_collision:
            enemy_sound = mixer.Sound(os.path.join(CWD, "audio/squawk.wav"))
            enemy_sound.play()
            projectile_y = PROJECTILE_START_Y
            projectile_state = "ready"
            score_value += 15

            enemy_x[i] = random.randint(0, 735)
            enemy_y[i] = ENEMY_START_HEIGHT

        enemy(round(enemy_x[i]), round(enemy_y[i]), i)

    # Projectile movement
    if projectile_state == "throw":
        throw_projectile(round(projectile_x), round(projectile_y))
        projectile_y -= PROJECTILE_Y_CHANGE
        if projectile_y < -32:
            score_value -= 5
            projectile_state = "ready"
            projectile_x = player_x
            projectile_y = PLAYER_START_Y

    # Draw the player
    player(round(player_x), round(player_y))

    # Draw the score and timer on screen
    show_score(SCORE_X, SCORE_Y)
    show_timer(TIMER_X, TIMER_Y, timer_value)

    # Update the displayed window, always required.
    pygame.display.update()

    # Output debugging info to terminal
    clear_terminal()
    print("player_x\tmouse[0]\tprojectile_x")
    print(str(player_x) + "\t\t" + str(mouse[0]) + "\t\t" + str(projectile_x))
    print("\ntimer_start\ttimer_value")
    print(str(timer_start) + "\t\t" + str(timer_value))
    print("\nmax_enemy_height\n" + str(max(enemy_heights)))


# Fully quit the game
quit_game()