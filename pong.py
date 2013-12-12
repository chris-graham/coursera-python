# Implementation of classic arcade game Pong

import simplegui
import random


# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True

ball_pos = [0, 0]
ball_vel = [0, 0]
paddle1_pos = HEIGHT / 2
paddle1_vel = 0
paddle2_pos = HEIGHT / 2
paddle2_vel = 0
score1 = 0
score2 = 0


# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]

    if (direction == LEFT):
        ball_vel = [-random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]
    if (direction == RIGHT):
        ball_vel = [random.randrange(120, 240) / 60, -random.randrange(60, 180) / 60]


# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2

    score1 = 0
    score2 = 0

    if (random.randrange(0, 2) == 0):
        spawn_ball(LEFT)
    else:
        spawn_ball(RIGHT)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    # draw ball
    # check if ball is touching left table edge
    if (ball_pos[0] - BALL_RADIUS) <= PAD_WIDTH:
        # check for player 1 paddle strike
        if ball_pos[1] >= paddle1_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle1_pos + HALF_PAD_HEIGHT:
            # player 1 paddle strike - increase velocity and reflect ball on X-axis
            ball_vel[0] = ball_vel[0] * .1 + ball_vel[0]
            ball_vel[1] = ball_vel[1] * .1 + ball_vel[1]
            ball_vel[0] = -ball_vel[0]
        else:
            # player 1 gutter strike - increment player 2 score and re-spawn ball directed to player 2
            score2 += 1
            spawn_ball(RIGHT)
    # check if ball is touching right table edge
    elif (ball_pos[0] + BALL_RADIUS) >= (WIDTH - PAD_WIDTH):
        # check for player 2 paddle strike
        if ball_pos[1] >= paddle2_pos - HALF_PAD_HEIGHT and ball_pos[1] <= paddle2_pos + HALF_PAD_HEIGHT:
            # player 2 paddle strike - increase velocity and reflect ball on X-axis
            ball_vel[0] = ball_vel[0] * .1 + ball_vel[0]
            ball_vel[1] = ball_vel[1] * .1 + ball_vel[1]
            ball_vel[0] = -ball_vel[0]
        else:
            # player 2 gutter strike - increment player 1 score and re-spawn ball directed to player 1
            spawn_ball(LEFT)
            score1 += 1
    # check for top or bottom table edge strike
    elif (ball_pos[1] <= (0 + BALL_RADIUS)) or (ball_pos[1] >= (HEIGHT - BALL_RADIUS)):
        # reflect ball on the Y-axis
        ball_vel[1] = -ball_vel[1]

    c.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel >= HALF_PAD_HEIGHT) and (paddle1_pos + paddle1_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle1_pos += paddle1_vel
    if (paddle2_pos + paddle2_vel >= HALF_PAD_HEIGHT) and (paddle2_pos + paddle2_vel <= HEIGHT - HALF_PAD_HEIGHT):
        paddle2_pos += paddle2_vel

    # draw paddles
    c.draw_line((HALF_PAD_WIDTH, paddle1_pos - HALF_PAD_HEIGHT),
                (HALF_PAD_WIDTH, paddle1_pos + HALF_PAD_HEIGHT), PAD_WIDTH, 'White')
    c.draw_line((WIDTH - HALF_PAD_WIDTH, paddle2_pos - HALF_PAD_HEIGHT), 
                (WIDTH - HALF_PAD_WIDTH, paddle2_pos + HALF_PAD_HEIGHT), PAD_WIDTH, 'White')

    # draw scores
    c.draw_text(str(score1), [WIDTH * .25, HEIGHT * .25], 56, "White")
    c.draw_text(str(score2), [WIDTH * .75, HEIGHT * .25], 56, "White")

def keydown(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -8
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 8
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -8
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 8

def keyup(key):
    global paddle1_vel, paddle2_vel

    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = 0

def reset():
    new_game()


# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
reset_button = frame.add_button("Reset Game", reset, 200)


# start frame and new game
new_game()
frame.start()
