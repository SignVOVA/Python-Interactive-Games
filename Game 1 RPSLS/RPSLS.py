import random
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui

choices = [0,1,2,3,4]
click = [0,0]

FRAME_WIDTH = 1000
FRAME_HEIGHT = 400
UNIT_WIDTH = 200
UNIT_HEIGHT = 200
user_choice = "..."
computer_choice = "..."
final_winner = ""
win_colour_code = "..."
score_colour_code = "Black"
score = 0

BG_WIDTH, BG_HEIGHT = 1000, 400
BG_IMAGE = simplegui.load_image('https://dl.dropboxusercontent.com/u/280794727/rsz_paper_background.jpg')

ROCK_WIDTH, ROCK_HEIGHT = 400, 400
ROCK_IMAGE = simplegui.load_image('https://dl.dropboxusercontent.com/u/280794727/rsz_rock.png')

SPOCK_WIDTH, SPOCK_HEIGHT = 400, 400
SPOCK_IMAGE = simplegui.load_image('https://dl.dropboxusercontent.com/u/280794727/rsz_1spock.png')

PAPER_WIDTH, PAPER_HEIGHT = 200, 200
PAPER_IMAGE = simplegui.load_image('https://dl.dropboxusercontent.com/u/280794727/rsz_1paper.png')

LIZARD_WIDTH, LIZARD_HEIGHT = 400, 400
LIZARD_IMAGE = simplegui.load_image('https://dl.dropboxusercontent.com/u/280794727/rsz_lizard.png')

SCISSORS_WIDTH, SCISSORS_HEIGHT = 400, 400
SCISSORS_IMAGE = simplegui.load_image('https://dl.dropboxusercontent.com/u/280794727/rsz_scissors.png')


list = {0 : 'rock', 1 : 'Spock', 2 : 'paper', 3 : 'lizard', 4 : 'scissors' }

def win_colour_decider():
    global win_colour_code
    if final_winner == "Draw":
        win_colour_code = "Black"
    elif final_winner == "Computer wins!":
        win_colour_code = "Red"
    elif final_winner == "Player wins!":
        win_colour_code = "Green"

def score_colour_decired():
    global score_colour_code
    if score == 0:
        score_colour_code = "Black"
    elif score >= 1:
        score_colour_code = "Green"
    elif score <= -1:
        score_colour_code = "Red"

def compare_output(computer, user):
    global final_winner, score
    if computer == user:
        final_winner = "Draw"
    elif (computer - user) % 5 <= 2:
        final_winner = "Computer wins!"
        score -= 1
    else:
        final_winner = "Player wins!"
        score += 1

def number_to_name(number):
    if number == 0:
        number = 'rock'
    elif number == 1:
        number = 'Spock'
    elif number == 2:
        number = 'paper'
    elif number == 3:
        number = 'lizard'
    elif number == 4:
        number = 'scissors'
    return number

def click(pos):
    global user_choice, computer_choice
    count_i = 0
    for item in list:
        if pos[0] > count_i * 200 and pos[0] < (count_i + 1) * 200 and pos[1] < 200:
            user_choice = item
            computer_choice = random.randrange(5)
            compare_output(computer_choice, user_choice)
            win_colour_decider()
            score_colour_decired()
            return user_choice, computer_choice        	
        else:
            count_i = count_i + 1    


def draw_handler(canvas):
    next_item = 0
    count = 0
    canvas.draw_image(BG_IMAGE, 
                      [BG_WIDTH // 2, BG_HEIGHT // 2], [BG_WIDTH, BG_HEIGHT],
                      [FRAME_WIDTH // 2, FRAME_HEIGHT // 2], [FRAME_WIDTH, FRAME_HEIGHT])
    canvas.draw_image(ROCK_IMAGE,
                      [ROCK_WIDTH // 2, ROCK_HEIGHT // 2], [ROCK_WIDTH, ROCK_HEIGHT],
                       [UNIT_WIDTH // 2, UNIT_HEIGHT // 2], [UNIT_WIDTH, UNIT_WIDTH]) 
    canvas.draw_image(SPOCK_IMAGE,
                      [SPOCK_WIDTH // 2, SPOCK_HEIGHT // 2],[SPOCK_WIDTH, SPOCK_HEIGHT],
                      [UNIT_WIDTH + 100, UNIT_HEIGHT // 2],[UNIT_WIDTH, UNIT_WIDTH])
    canvas.draw_image(PAPER_IMAGE,
                      [PAPER_WIDTH // 2, PAPER_HEIGHT // 2],[PAPER_WIDTH, PAPER_HEIGHT],
                      [UNIT_WIDTH + 300, UNIT_HEIGHT // 2],[UNIT_WIDTH, UNIT_WIDTH])
    canvas.draw_image(LIZARD_IMAGE,
                      [LIZARD_WIDTH // 2, LIZARD_HEIGHT // 2],[LIZARD_WIDTH, LIZARD_HEIGHT],
                      [UNIT_WIDTH + 500, UNIT_HEIGHT // 2],[UNIT_WIDTH, UNIT_WIDTH])
    canvas.draw_image(SCISSORS_IMAGE,
                      [SCISSORS_WIDTH // 2, SCISSORS_HEIGHT // 2],[SCISSORS_WIDTH, SCISSORS_HEIGHT],
                      [UNIT_WIDTH + 700, UNIT_HEIGHT // 2],[UNIT_WIDTH, UNIT_WIDTH])
    
    canvas.draw_text("Your choice is: " + number_to_name(user_choice), (UNIT_WIDTH / 2, UNIT_HEIGHT + 100), 25, 'Green')
    canvas.draw_text(final_winner, (FRAME_WIDTH / 2, FRAME_HEIGHT / 2 + (UNIT_HEIGHT / 2)+ 10), 25, win_colour_code)
    canvas.draw_text("Computer choice is: " + number_to_name(computer_choice), (UNIT_WIDTH / 2, UNIT_HEIGHT + 150), 25, 'Red')
    canvas.draw_text("Score: " + str(score), (FRAME_WIDTH - UNIT_WIDTH, FRAME_HEIGHT - (UNIT_HEIGHT / 2) + 10), 25, score_colour_code)
    canvas.draw_text("designed by Zhazira Utetleyeva", (FRAME_WIDTH - FRAME_WIDTH/6, FRAME_HEIGHT - 5), 12, "Black")
    
frame = simplegui.create_frame('Rock paper scissors lizard Spock - Game', FRAME_WIDTH, FRAME_HEIGHT)
frame.set_canvas_background('Black')
frame.set_draw_handler(draw_handler)
frame.set_mouseclick_handler(click)
frame.start()
