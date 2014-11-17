# Implementation of classic arcade game Pong

import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import time

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 25
PAD_WIDTH = 20
PAD_HEIGHT = 120
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
fatality = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/Pong/fatality.png")
ball = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/Pong/ball.png")
paddle1 = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/Pong/p1.png")
paddle2 = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/Pong/p2.png")
background = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/Pong/bg.jpg")
ball_pos = [300, 200]
ball_rot = 0
paddle1_pos = [10, 200]
paddle2_pos = [590, 200]
vel = [0, 0]
paddle1_vel = 0
paddle2_vel = 0
in_play = "False"
direction = "left"
score1 = 0
score2 = 0
fatal_tick = 4

# sounds 
ceiling_hit = simplegui.load_sound('https://dl.dropboxusercontent.com/u/280794727/Pong/20.wav')
paddle1_sound = simplegui.load_sound('https://dl.dropboxusercontent.com/u/280794727/Pong/07.wav')
theme_song = simplegui.load_sound('https://dl.dropboxusercontent.com/u/280794727/Pong/fight_style.wav')

#paddle2_sound = simplegui.load_sound('http://www.basementarcade.com/arcade/sounds/tapper/08.wav')
#player_scores = simplegui.load_sound('http://www.basementarcade.com/arcade/sounds/tapper/12.wav')

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, vel, in_play # these are vectors stored as lists
    ball_pos = [300, 200]
    in_play = "True"
    vel[1] = - (float(random.randrange(120, 240))) /100
    if direction == "right":
        vel[0] = (float(random.randrange(60, 180))) / 100
    elif direction == "left":
        vel[0] = - (float(random.randrange(60, 180))) / 100

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are numbers
    global score1, score2  # these are ints
    score1 = 0
    score2 = 0
    spawn_ball(direction)
    timer.start()  
    if theme_song.play():
        theme_song.rewind()
        theme_song.play()
    else:
        pass
      

def draw(canvas):
    global fatal_tick, score1, score2, paddle1_pos, paddle2_pos, ball_pos, vel, ball_rot, paddle1_vel, paddle2_vel
    # draw the background
    canvas.draw_image(background, (300, 200), (600, 400), (300, 200), (600, 400))
        
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    if in_play == "True":
        canvas.draw_image(ball, (40, 40), (80, 80), ball_pos, (50, 50), ball_rot)

    if fatal_tick <= 3:
        canvas.draw_image(fatality, (200, 60), (400, 120), (300, 100), (400, 120))

    
    # Update ball position
    if fatal_tick <= 3:
        ball_pos[0] = 300
        ball_pos[1] = 200
    ball_pos[0] += vel[0]
    ball_pos[1] += vel[1]
    ball_rot += .025
    
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS:
        if (abs(ball_pos[1] - paddle1_pos[1])) < HALF_PAD_HEIGHT:
            vel[0] = - vel[0]
            vel[0] = 1.1 * vel[0]
            vel[1] = 1.1 * vel[1]
            paddle1_sound.play()
        else:
            score2 += 1
            fatal_tick = 0
            spawn_ball("left")
            #player_scores.play()
            
    if ball_pos[0] >= ((WIDTH - 1- PAD_WIDTH) - BALL_RADIUS):
        if (abs(ball_pos[1] - paddle2_pos[1])) < HALF_PAD_HEIGHT:
            vel[0] = - vel[0]
            vel[0] = 1.1 * vel[0]
            vel[1] = 1.1 * vel[1]
            paddle1_sound.play()
        else:
            score1 += 1
            fatal_tick = 0          
            spawn_ball("right")
            #player_scores.play()
    

            
    if ball_pos[1] <= BALL_RADIUS:
        vel[1] = - vel[1]
        ceiling_hit.play()
    if ball_pos[1] >= ((HEIGHT - 1) - BALL_RADIUS):
        vel[1] = - vel[1]
        ceiling_hit.play()
    
    # draw paddles
    canvas.draw_image(paddle1, (10, 60), (20, 120), paddle1_pos, (20, 120))
    canvas.draw_image(paddle2, (10, 60), (20, 120), paddle2_pos, (20, 120))
    
    # update paddle position
    paddle1_pos[1] += paddle1_vel
    paddle2_pos[1] += paddle2_vel
    
    
    if paddle1_pos[1] <= HALF_PAD_HEIGHT:
        paddle1_vel = 0
    if paddle1_pos[1] >= HEIGHT - HALF_PAD_HEIGHT:
        paddle1_vel = 0
    if paddle2_pos[1] <= HALF_PAD_HEIGHT:
        paddle2_vel = 0
    if paddle2_pos[1] >= HEIGHT - HALF_PAD_HEIGHT:
        paddle2_vel = 0
    
    # draw scores
    canvas.draw_text(str(score1)+ "          " + str(score2), (218, 40), 50, 'White')

        
def keydown(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= 2
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += 2
        
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= 2
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += 2
    if key == simplegui.KEY_MAP['space']:
        new_game()
        
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel = 0
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel = 0
        
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel = 0
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel = 0
    if key == simplegui.KEY_MAP['space']:
        pass
    
def reset_button():
    new_game()    
    
def timer_handler():
    global fatal_tick
    fatal_tick += 1

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
timer = simplegui.create_timer(300, timer_handler)

# register event handlers
button2 = frame.add_button('Reset', reset_button, 100)


# start frame
frame.start()