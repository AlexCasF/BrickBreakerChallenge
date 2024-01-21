import pygame
from pygame import mixer
from ball import Ball
from level import Level
from button import Button
from paddle import Paddle

pygame.init()
mixer.init()

# Load sound effects
tick = mixer.Sound('select.wav')
pong = mixer.Sound('pong.wav')
bang = mixer.Sound('bang.wav')
meep = mixer.Sound('over.wav')
ciao = mixer.Sound('quit.wav')
win = mixer.Sound('win.wav')

def play_sound(sound):
    sound.play()


scr_width = 800
scr_height = 600

screen = pygame.display.set_mode((scr_width, scr_height))
pygame.display.set_caption("Brick Breaker")


def show_difficulty_selection(screen):
    # Buttons:
    turtle_button = Button(screen, (80, 240, 80), (0, 0, 0), (100, 200), (100, 50), "Slow", 20)
    rabbit_button = Button(screen, (80, 240, 80), (0, 0, 0), (250, 200), (100, 50), "Medium", 20)
    rocket_button = Button(screen, (80, 240, 80), (0, 0, 0), (400, 200), (100, 50), "Fast", 20)
    demo_button = Button(screen, (80, 240, 80), (0, 0, 0), (550, 200), (100, 50), "DEMO", 20)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONUP:
                if turtle_button.isOverMouse():
                    play_sound(tick)
                    return 2  # Slow speed
                elif rabbit_button.isOverMouse():
                    play_sound(tick)
                    return 8  # Middle speed (default)
                elif rocket_button.isOverMouse():
                    play_sound(tick)
                    return 16  # Fast speed
                elif demo_button.isOverMouse():
                    play_sound(tick)
                    return 17

        screen.fill((200, 200, 200))
        turtle_button.show()
        rabbit_button.show()
        rocket_button.show()
        demo_button.show()
        pygame.display.update()


def brick_collision(level: Level, ball: Ball):
    for brick_position in list(level.bricks_with_colors.keys()):
        x, y = brick_position
        if (x < ball.ballX < (x + level.length) and
                y < ball.ballY < (y + level.width)):
            # Invert the y direction
            ball.y_vel = -ball.y_vel
            center = x + level.length/2
            if x < ball.ballX < center:
                ratio = (center - ball.ballX)/(level.length/2)
                ball.x_vel += -ball.max_x_vel * ratio
            elif center < ball.ballX < (x + level.length):
                ratio = (ball.ballX - center)/(level.length/2)
                ball.x_vel += ball.max_x_vel * ratio
            level.remove(brick_position)
            play_sound(bang)
            break  # Break after removing the brick to avoid modifying the list during iteration


def show_gameover():
    global scr_height
    global scr_width
    text = pygame.font.Font("freesansbold.ttf", int(scr_height*0.1))
    gameover = text.render("GAME OVER", True, (255, 23, 20))
    screen.blit(gameover, (int(scr_width*0.25), int(scr_height*0.4)))


def show_you_win():
    global scr_height
    global scr_width
    text = pygame.font.Font("freesansbold.ttf", int(scr_height*0.1))
    gameover = text.render("YOU WIN", True, (0, 255, 0))
    screen.blit(gameover, (int(scr_width*0.25), int(scr_height*0.4)))


clock = pygame.time.Clock()
background_color = (200, 200, 200)

def check_win(level):
    return len(level.bricks_with_colors) == 0

while True:
    # Show difficulty selection
    ball_speed = show_difficulty_selection(screen)

    # Initialize game objects with chosen ball speed
    paddle = Paddle(screen)
    ball = Ball(paddle, screen, ball_speed)
    level = Level(screen, background_color)
    over = False
    clicked_replay = False

    # paddle movement switches
    key_left = False
    key_right = False

    while True:

        clock.tick(30)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    key_left = True
                if event.key == pygame.K_RIGHT:
                    key_right = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    paddle.stop()
                    key_left = False
                if event.key == pygame.K_RIGHT:
                    paddle.stop()
                    key_right = False

        # GAME LOGIC
        if ball_speed == 17:
            # logic to automatically move the paddle
            if ball.ballX < paddle.paddleX + 40:
                paddle.auto_left()
            elif ball.ballX > paddle.paddleX + 80:
                paddle.auto_right()
        else:
            # paddle movement switches
            if key_left == True:
                paddle.move_left()
            if key_right == True:
                paddle.move_right()

        # ball machanics
        ball.update()

        ball_bottom = ball.ballY + ball.ball_radius
        ball_within_paddle = paddle.paddleX < ball.ballX < (
            paddle.paddleX + paddle.length)

        if paddle.paddleY + 10 > ball_bottom > paddle.paddleY and ball_within_paddle:
            play_sound(pong)
            ball.collision_change()
        # brick collision
        brick_collision(level, ball)

        # paddle boundries
        paddle.boundries()
        if ball.ballY > scr_height:
            show_gameover()
            play_sound(meep)
            over = True
            # REPLAY BUTTON
            b_replay = Button(screen, (80, 45, 200), (200, 250, 255),
                          (210, 350), (150, 60), "REPLAY", 30)
            # QUIT BUTTON
            b_quit = Button(screen, (255, 0, 0), (255, 255, 255),
                            (400, 350), (150, 60), "QUIT", 30)

            while True:
                b_replay.show()
                b_quit.show()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if b_replay.isOverMouse() and event.type == pygame.MOUSEBUTTONUP:
                        play_sound(tick)
                        clicked_replay = True
                    elif b_quit.isOverMouse() and event.type == pygame.MOUSEBUTTONUP:
                        play_sound(ciao)
                        pygame.time.delay(1000)
                        pygame.quit()
                        exit()

                    # Update button appearance based on mouse hover
                    if b_replay.isOverMouse():
                        b_replay.changeColor((80, 240, 80), (14, 37, 100))
                    else:
                        b_replay.changeColor((80, 45, 200), (200, 250, 255))

                    if b_quit.isOverMouse():
                        b_quit.changeColor((255, 100, 100), (255, 255, 255))
                    else:
                        b_quit.changeColor((255, 0, 0), (255, 255, 255))

                if clicked_replay:
                    break

                pygame.display.update()

        if check_win(level):
            show_you_win()
            play_sound(win)
            over = True
            # REPLAY BUTTON
            b_replay = Button(screen, (80, 45, 200), (200, 250, 255),
                          (210, 350), (150, 60), "REPLAY", 30)
            # QUIT BUTTON
            b_quit = Button(screen, (255, 0, 0), (255, 255, 255),
                            (400, 350), (150, 60), "QUIT", 30)

            while True:
                b_replay.show()
                b_quit.show()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                    if b_replay.isOverMouse() and event.type == pygame.MOUSEBUTTONUP:
                        play_sound(tick)
                        clicked_replay = True
                    elif b_quit.isOverMouse() and event.type == pygame.MOUSEBUTTONUP:
                        play_sound(ciao)
                        pygame.time.delay(1000)
                        pygame.quit()
                        exit()

                    # Update button appearance based on mouse hover
                    if b_replay.isOverMouse():
                        b_replay.changeColor((80, 240, 80), (14, 37, 100))
                    else:
                        b_replay.changeColor((80, 45, 200), (200, 250, 255))

                    if b_quit.isOverMouse():
                        b_quit.changeColor((255, 100, 100), (255, 255, 255))
                    else:
                        b_quit.changeColor((255, 0, 0), (255, 255, 255))

                if clicked_replay:
                    break

                pygame.display.update()

        screen.fill(background_color)
        paddle.show()
        level.show()

        ball.show()
        if over == True:
            break

        pygame.display.update()
