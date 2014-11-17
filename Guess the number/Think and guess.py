# import libraries
import random
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import math


# initialize global variables
upper = 100
lower = 0
message_1 = ''
message_2 = ''
message_3 = ''
search_message = ''
game_state = 'intro'

# helper function to start and restart the game
def new_game():
    global num_of_guesses, lower, game_state
    lower = 0
    num_of_guesses = 1
    game_state = 'intro'
    message_helper()

# helper function to print messages 

def message_helper():
    global lower, upper, guess, num_of_guesses, search_message
    global message_1, message_2, message_3, game_state
    if game_state == 'intro':
        message_1 = "Enter a positive integer"
        message_2 = ''
        message_3 = ''
        search_message = ''
    elif game_state == 'start':
        message_1 = 'Think of a number between 0 and ' + str(num)
        message_2 = 'I can guess your number in '+ str(int(n_guesses))+ ' or less.'
        message_3 = 'Is your number: '+ str(guess)
        search_message = 'Search range is currently ' + str(lower) + ' to ' + str(upper)
    elif game_state == 'mid':
        message_1 =  'Is your number: '+ str(guess)  
        message_2 = 'Total guesses: ' + str(num_of_guesses)
        message_3 = ''
        search_message = 'Search range is currently ' + str(lower) + ' to ' + str(upper)
    else:
        message_1 =  'See, I told you!'
        message_2 = 'I did it in ' + str(num_of_guesses) + ' guesses!'
        message_3 = ''
        search_message = 'Wait for new game to begin'

    
    
# define event handlers for control panel
def start_game(num):
    global upper, guess, lower, message_1, message_2, message_3
    global search_message
    upper = int(num)
    guess = (upper + lower) // 2
    n_guesses = math.ceil(math.log(int(num), 2))
    message_1 = 'Think of a number between 0 and ' + str(num)
    message_2 = 'I can guess your number in '+ str(int(n_guesses))+ ' or less.'
    message_3 = 'Is your number: '+ str(guess)
    search_message = 'Search range is currently ' + str(lower) + ' to ' + str(upper)
    
def high():
    global lower, upper, guess, num_of_guesses, game_state
    game_state = 'mid'
    lower = guess
    guess = (upper + lower) // 2
    num_of_guesses += 1
    message_helper()
    
def low():
    global lower, upper, guess, num_of_guesses, game_state
    game_state = 'mid'
    upper = guess
    guess = (upper + lower) // 2
    num_of_guesses += 1
    message_helper()


def correct():
    global game_state, time
    game_state = 'end'
    message_helper()
    time = 3
    timer.start()
    print (time)
    if time == 0:
        timer.stop()
        new_game()

def draw(canvas):
    global message_1, message_2, message_3, search_message
    canvas.draw_text(message_1, (75,50), 20, 'white')
    canvas.draw_text(message_2, (75,75), 20, 'white')
    canvas.draw_text(message_3, (75,100), 20, 'white')
    canvas.draw_text(search_message, (25,190), 20, 'white')

def timer_handler():
    global time
    time -= 1
    if time == 0:
        timer.stop()
        new_game()

# start the new game
new_game()   

# create frame
f = simplegui.create_frame("Think and guess",500,200)

timer = simplegui.create_timer(1000, timer_handler)
# register event handlers for control elements
f.set_draw_handler(draw)
f.add_button("Higher", high, 100)
f.add_button("Lower", low, 100)
f.add_button("Correct", correct, 100)
f.add_input("Range", start_game, 100)



# call new_game and start frame

f.start()


