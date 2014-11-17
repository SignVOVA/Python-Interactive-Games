import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
     
# global variable
interval = 100

# upload image
watch_image = simplegui.load_image("https://dl.dropboxusercontent.com/u/280794727/BreakTheSentry/watch_image.jpg")

# messages
success_msg = msg_init = "Try to stop at .0 ms"
msg_missed = ["Not very lucky...", "Keep trying ;)", "Ouch!",\
              "Missed!","Nope...", "Maybe next time", "*@$#"]
msg_hit = ["Great success!!!", "Very nice!", "WaWaWeeWa!!!",\
           "It's a hit!", "Bravo!", "Bravissimo!!!", "I like!",\
           "High five!", "Lucky B)", "To good", "But.. how?"]

color = color_init = "LightBlue"

background_sound = simplegui.load_sound("https://dl.dropboxusercontent.com/u/280794727/BreakTheSentry/Jessie_Ware_Running_Disclosure_Remix.wav")
# set the volume and play
background_sound.set_volume(.2)
background_sound.play()

def format(t):
    '''
    Converts time MM SS mm.
    Works correctly upto 60 minutes
    '''
    global min_tens, min_ones, sec_tens, sec_ones, msec, mins, sec
    mins = t // 600 % 60
    sec = t // 10 % 60
    msec = t % 10

    min_tens = mins // 10 % 10
    min_ones = mins % 10

    sec_tens = sec // 10 % 10
    sec_ones = sec % 10
    return [[min_tens, min_ones], [sec_tens, sec_ones], msec]

def start():
    '''Start timer button''' 
    timer.start()


def stop():
    '''Stops the timer and calls update_score function'''
    if timer.is_running():
        timer.stop()
        update_score()

        
def reset():
    '''Stops the timer and sets time, hits and tries to 0.'''
    global time, hits, tries, success_msg, color
    color = color_init
    success_msg = msg_init
    timer.stop()
    time =  hits = tries = 0


def update_score():
    '''
    Updates the number of tries.
    Adds to hits if stopped on a whole second (1.0, 2.0, 3.0, etc.)
    '''
    global hits, tries, success_msg, color
    tries += 1
    msg = msg_missed
    color = "Salmon"
    if time % 10 == 0:
        hits += 1
        msg = msg_hit
        color = "LightGreen"
        
    # Pick random msg form msg_missed or msg_hit
    idx = random.randrange(len(msg))
    success_msg = msg[idx]
        


def hit_rate():
    '''Returns success rate, %'''
    if hits > 0:
        rate = hits * 100.0 / tries
    else:
       rate = 0
    return rate


def print_score():
    '''Return the score in format hits/tries'''
    return str(hits) + "/" + str(tries)


def timer():
    global time
    time += 1

def draw_num(canvas, num, x, y, k=1, color="LightGray"):
    # x and y are the top left hand coordinates of the number
    lights = [False, False, False, False, False, False, False]
    
    # There are a total of 6 'lights' or shapes that can be
    #    'on' (drawn) or 'off' (not drawn). This if-elif 
    # segment decides which ones should be 'on' (True) 
    #        based on the number given to the function.
    if num == 0:
        lights = [True, True, True, False, True, True, True]
    elif num == 1:
        lights = [False, False, True, False, False, False, True]
    elif num == 2:
        lights = [False, True, True, True, True, True, False]
    elif num == 3:
        lights = [False, True, True, True, False, True, True]
    elif num == 4:
        lights = [True, False, True, True, False, False, True]
    elif num == 5:
        lights = [True, True, False, True, False, True, True]
    elif num == 6:
        lights = [True, True, False, True, True, True, True]
    elif num == 7:
        lights = [False, True, True, False, False, False, True]
    elif num == 8:
        lights = [True, True, True, True, True, True, True]
    elif num == 9:
        lights = [True, True, True, True, False, True, True]
    
    # This segment draws only the lights that are 'on' (True)
    #    from the above array.
    # k - is coeficiente for sizing
    if lights[0]:
        canvas.draw_polygon([(x, y + k*1.5), (x + k*3.5, y + k*5),(x + k*3.5, y + k*12),\
                             (x, y + k*15.5)], 2, color)
    if lights[1]:
        canvas.draw_polygon([(x + k*2.5, y), (x + k*6, y + k*3.5), (x + k*13, y + k*3.5),\
                             (x + k*16.5, y)], 2, color)
    if lights[2]:
        canvas.draw_polygon([(x + k*18.5, y + k*1.5), (x + k*15, y + k*5), (x + k*15, y + k*12),\
                             (x + k*18.5, y + k*15.5)], 2, color)
    if lights[3]:
        canvas.draw_polygon([(x + k*2.5, y + k*17.5), (x + k*6, y + k*20), (x + k*13, y + k*20),\
                             (x + k*16.5, y + k*17.5), (x + k*13, y + k*15), (x + k*6, y + k*15)], 2, color)
    if lights[4]:
        canvas.draw_polygon([(x, y + k*19.5), (x + k*3.5, y + k*23), (x + k*3.5, y + k*30),\
                             (x, y + k*33.5)], 2, color)
    if lights[5]:
        canvas.draw_polygon([(x + k*2.5, y + k*35), (x + k*6, y + k*31.5), (x + k*13, y + k*31.5),\
                             (x + k*16.5, y + k*35)], 2, color)
    if lights[6]:
        canvas.draw_polygon([(x + k*18.5, y + k*19.5), (x + k*15, y + k*23), (x + k*15, y + k*30),\
                             (x + k*18.5, y + k*33.5)], 2, color)

      
def draw(canvas):  
    # Draws an image
    canvas.draw_image(watch_image, (600/2, 600/2), (600, 600), (600/2, 600/2), (600, 600))
    
    # Score x/y
    canvas.draw_text(print_score(), (340, 287), 40, "LightBlue")      
    # Success message
    canvas.draw_text(success_msg, (235,385), 18, color)

    # Minutes: tens and ones
    draw_num(canvas, format(time)[0][0], 210, 305, 1.5)
    draw_num(canvas, format(time)[0][1], 245, 305, 1.5)
    # Seconds: tens and ones
    draw_num(canvas, format(time)[1][0], 295, 305, 1.5)
    draw_num(canvas, format(time)[1][1], 330, 305, 1.5)
    # Milliseconds
    draw_num(canvas, format(time)[2], 380, 322)
    # Separators
    if sec_ones % 2 == 0:
        canvas.draw_text(":", (275, 350), 70, "LightGray")
    canvas.draw_text(".", (358, 355), 70, "LightGray")
    
    # Hit rate    
    canvas.draw_text("Hit rate: ", (215, 240), 25, "LightGreen")
    canvas.draw_text("%", (335, 242), 25, "LightGreen")
    
    if hit_rate() < 100:
        if hit_rate() >= 10:
            draw_num(canvas, int(hit_rate()) // 10 , 300, 224, 0.5, "LightGreen")
        draw_num(canvas, int(hit_rate()) % 10, 315, 224, 0.5, "LightGreen")
    else:
        draw_num(canvas, int(hit_rate()) // 10 , 300, 224, 0.5, "LightGreen")
        
    if background_sound.play():
        background_sound.rewind()
        background_sound.play()
    else:
        pass
        

# mouseclick handlers that starts the timer and stops if it is running
def click(pos):
    if timer.is_running():
        timer.stop()
        update_score()
    else:
        timer.start()  

# key handlerds
def keyup(key):
    pass
     
def keydown(key):
    if key == simplegui.KEY_MAP['space']:
        if timer.is_running():
            timer.stop()
            update_score()
        else:
            timer.start() 

# craete a frame      
frame = simplegui.create_frame('Break the Sentry', 600, 600)
frame.set_canvas_background("black")
frame.set_draw_handler(draw)

# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click) 

timer = simplegui.create_timer(interval, timer)

frame.add_button("Start", start, 100)
frame.add_button("Stop", stop, 100)
frame.add_button("Reset", reset, 100)

reset()

# start the frame
frame.start()