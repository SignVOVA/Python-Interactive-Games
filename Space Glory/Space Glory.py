# import libraries            vmaksymc
import SimpleGUICS2Pygame.simpleguics2pygame as simplegui
import random
import math


# define global variables
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False
game_over = False
new_shield_available = True
overheating = 0
high_score = 0
shield = True
shield_hp = 2
current_song = None
 
# ImageInfo class 
class ImageInfo:
 
    def __init__(self, center, size, radius=0, lifespan=None, animated=False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated
 
    def get_center(self):
        return self.center
 
    def get_size(self):
        return self.size
 
    def get_radius(self):
        return self.radius
 
    def get_lifespan(self):
        return self.lifespan
 
    def get_animated(self):
        return self.animated

class miniBoss:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.angle = angle
        # 1 thurst
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self, canvas):
        center = list(self.image_center)
        # if thurst
        canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
        
    def update(self):
        # update angle
        self.angle += self.angle_vel
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        
        # thurst    set_thrust    increment_angle_vel    decrement_angle_vel
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0],
                       self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0],
                       self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0,
                                 missile_image, missile_info, missile_sound))

#Ship class 
class Ship:

    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
 
    def draw(self, canvas):
        center = list(self.image_center)
        if self.thrust:
            center[0] = self.image_center[0] + self.image_size[0]
        canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
        if shield_hp == 1:
            center[0] = self.image_center[0] + self.image_size[0]
            canvas.draw_image(shields_lvl1_image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
        elif shield_hp >= 2:
            center[0] = self.image_center[0] + self.image_size[0]
            canvas.draw_image(shields_lvl2_image, center, self.image_size,
                          self.pos, self.image_size, self.angle)           
            
 
    def update(self):
        # update angle
        self.angle += self.angle_vel
 
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
 
        # update velocity
        if self.thrust:
            acc = angle_to_vector(self.angle)
            self.vel[0] += acc[0] * .1
            self.vel[1] += acc[1] * .1
 
        self.vel[0] *= .99
        self.vel[1] *= .99
 
    def set_thrust(self, on):
        self.thrust = on
        if on:
            ship_thrust_sound.rewind()
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.pause()
 
    def increment_angle_vel(self):
        self.angle_vel += .05
 
    def decrement_angle_vel(self):
        self.angle_vel -= .05
 
    def shoot(self):
        global missile_group
        forward = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + self.radius * forward[0],
                       self.pos[1] + self.radius * forward[1]]
        missile_vel = [self.vel[0] + 6 * forward[0],
                       self.vel[1] + 6 * forward[1]]
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0,
                                 missile_image, missile_info, missile_sound))
 
 
# Sprite class 
class Sprite:
 
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound=None):
        self.pos = [pos[0], pos[1]]
        self.vel = [vel[0], vel[1]]
        self.init_vel = [vel[0], vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
 
    def draw(self, canvas):
        center = list(self.image_center)
        if self.animated:
            center[0] = self.image_center[0] + (self.image_size[0] * self.age)
        canvas.draw_image(self.image, center, self.image_size,
                          self.pos, self.image_size, self.angle)
 
    def update(self):
        # update angle
        self.angle += self.angle_vel
 
        # update position
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
 
        self.age += 1
        return self.age > self.lifespan
 
    def collide(self, other_object):
        return dist(self.pos, other_object.pos) <= self.radius + other_object.radius

 
# art assets created by Kim Lathrop, may be freely re-used in
# non-commercial projects, please credit Kim
 
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
# debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png,
# debris_blend.png        3D effects
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")
 
# nebula images - nebula_brown.png, nebula_blue.png    background
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/spice%20background.jpg")


blood_effect_info = ImageInfo([400, 300], [800, 600])
blood_effect_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/emergency.png")

# splash image    click to start image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/space%20glory.png")

# ship image    ship
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/spaceship_sprite.png")

shields_lvl1_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/shields.png")

shields_lvl2_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/shields_lvl2.png")

# enemy boss image
boss_info = ImageInfo([90, 90], [180, 180], 35)
boss_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/boss.png")

ship_life_info = ImageInfo([22.5, 22.5], [45, 45])
ship_life_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/spaceship_life.png")

shield_life_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/rsz_crystal_heart_shield_by_swedishroyalguard.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5, 5], [10, 10], 3, 100)
missile_image = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/rsz_laser.png")

asteroid_info = ImageInfo([45, 45], [90, 90], 40)

asteroid_image_0 = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/asteroid.png")

asteroid_image_1 = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/asteroid1.png")

asteroid_image_2 = simplegui.load_image(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/asteroid2.png")
asteroid_image_live = asteroid_image_0

# animated explosion - explosion_orange.png, explosion_blue.png,
# explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image(
    "http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
 
# soundtracks and sound effects
current_song = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/The_Prodigy_First_Warning.wav")

missile_sound = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/alian_laser.wav")
missile_sound.set_volume(.2)

laser_overheat_sound = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/laser_gun_overheat.wav")
laser_overheat_sound.set_volume(0.3)

shield_damage_sound = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/shield_damage.wav")

boss_defected_sound = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/alarm_boss_detected.wav")

explosion_sound = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/explosion.wav")
explosion_sound.set_volume(0.2)

ship_thrust_sound = simplegui.load_sound(
    "https://dl.dropboxusercontent.com/u/280794727/spaceglory/sounds/thrust.wav")
ship_thrust_sound.set_volume(0.2)

def generate_number():
    global asteroid_image_live
    number = random.randrange(0,3)
    if number == 0:
        asteroid_image_live = asteroid_image_0
    elif number == 1:
        asteroid_image_live = asteroid_image_1
    else:
        asteroid_image_live = asteroid_image_2
     
# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]
 
 
def dist(p, q):
    return math.sqrt((p[0] - q[0]) ** 2 + (p[1] - q[1]) ** 2)
 
 
def process_sprite_group(group, canvas):
    for each in set(group):
        each.draw(canvas)
        if each.update():
            group.remove(each)
 
 
def group_collide(group, other_object):
    global explosion_group
    collided = False
    for each in set(group):
        if each.collide(other_object):
            group.remove(each)
            collided = True
            explosion_group.add(Sprite(each.pos, [0, 0], 0, 0, explosion_image,
                                       explosion_info, explosion_sound))
    return collided
 
 
def group_group_collide(group, other_group, isBoss):
    counter = 0
    for each in set(group):
        collision = group_collide(other_group, each)
        if collision and not isBoss:
            group.remove(each)
            counter += 1
        elif collision and isBoss:    # add some life for Boss. modify or add group_collide. TODO: REFACTOR
            group.remove(each)
            counter += 1         
    return counter 

# key handlers to control ship 
def keyup(key):    
    if key == simplegui.KEY_MAP['left']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(False)
 
 
# mouseclick handlers that reset UI and conditions whether splash image is
# drawn
def click(pos):
    global started, lives, score, shield_hp
    center = [WIDTH / 2, HEIGHT / 2]
    size = splash_info.get_size()
    inwidth = (center[0] - size[0] / 2) < pos[0] < (center[0] + size[0] / 2)
    inheight = (center[1] - size[1] / 2) < pos[1] < (center[1] + size[1] / 2)
    if (not started) and inwidth and inheight:
        started = True
        lives = 3
        score = 0
        shield_hp = 2
        
        current_song.rewind()
        current_song.play()
 
 
def draw(canvas):
    global time, started, score, lives, rock_group, my_ships, boss_group, high_score, game_over, shield_hp, shield
 
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(),
                      nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                      [WIDTH, HEIGHT])
    
    if overheating >= 9: # TODO: ADD A TIMER FOR FLASHING EFFECT
        canvas.draw_image(blood_effect_image, # 800x600
                          blood_effect_info.get_center(), blood_effect_info.get_size(),
                          [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    #===========================================================================
    #canvas.draw_image(debris_image, [center[0] - wtime, center[1]],
    #                  [size[0] - 2 * wtime, size[1]],
    #                  [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2],
    #                  [WIDTH - 2.5 * wtime, HEIGHT])
    #canvas.draw_image(debris_image, [size[0] - wtime, center[1]],
    #                  [2 * wtime, size[1]], [1.25 * wtime, HEIGHT / 2],
    #                  [2.5 * wtime, HEIGHT])

    for rock in rock_group:
        for i in range(2):
            rock.vel[i] = rock.init_vel[i] + (rock.init_vel[i] * score * 0.02)
 
    # draw ship and sprites
    my_ship.draw(canvas)
    my_ship.update()
    process_sprite_group(rock_group, canvas)
    process_sprite_group(missile_group, canvas)
    process_sprite_group(explosion_group, canvas)
    process_sprite_group(boss_group, canvas)
 
    # process collisions
    if group_collide(rock_group, my_ship):
        if shield_hp > 0:
            shield_damage_sound.rewind()
            shield_damage_sound.play()
            shield_hp -= 1
        elif shield_hp == 0:
            shield = False
            lives -= 1
            explosion_sound.rewind()
            explosion_sound.play()            
    score += group_group_collide(missile_group, rock_group, False) * 10
 
    # destroy asteroid when boss colide with them  REFACTOR
    if group_collide(boss_group, my_ship):
        if shield_hp > 0:
            shield_damage_sound.rewind()
            shield_damage_sound.play()
            shield_hp -= 1
        elif shield_hp == 0:
            shield = False
            lives -= 1
            explosion_sound.rewind()
            explosion_sound.play()   
    if group_group_collide(missile_group, boss_group, True):
        score += group_group_collide(missile_group, boss_group, True) * 50
        if lives < 10 and new_shield_available and shield_hp < 3:
            shield_hp += 1
            shield_cool_down_timer.start()
 
    # check game over
    if lives == 0:
        rock_group = set()
        boss_group = set()        
        started = False
        game_over = True # NEW: if no lives game is over, later High Score can be displayed
        if score > high_score:  # NEW: High Score Added only if its higher than score
            high_score = score
 
    # draw UI
    canvas.draw_text("Lives", [50, 50], 22, "White", "sans-serif")
    canvas.draw_text("Score", [680, 50], 22, "White", "sans-serif")
    
    #    canvas.draw_image(image, center_source, width_height_source, center_dest, width_height_dest)
    distance = 0 
    for i in range(lives):
        canvas.draw_image(ship_life_image, 
                          [22.5, 22.5], [45, 45],
                          [50 + distance, 80], [45, 45])
        distance += 25
        
    shield_distance = 0
    if shield_hp > 0:
        for i in range(shield_hp):
            canvas.draw_image(shield_life_image, 
                          [22.5, 22.5], [45, 45],
                          [50 + shield_distance, (HEIGHT - 40)], [45, 45])
            shield_distance += 35
            
        
    #canvas.draw_text(str(lives), [50, 80], 22, "White", "sans-serif")
    canvas.draw_text(str(score), [680, 80], 22, "White", "sans-serif")
    
    # overhearing - TODO: REFACTOR
    heat_lenght = 10
    heat_space = 0
    for i in range(overheating):
        #canvas.draw_line((WIDTH / 2 + heat_distance, 50), 
        #                 (WIDTH / 2 + (heat_distance - 10), 50), 12, 'Red')
        canvas.draw_line((WIDTH, HEIGHT - heat_space), (WIDTH, HEIGHT - heat_lenght), 24, 'Red')
        heat_lenght += HEIGHT / 10
        heat_space += HEIGHT / 10
                
    # Overheating idicator for testing only
    #canvas.draw_text(str(overheating), [WIDTH / 2, 50], 22, "White", "sans-serif")
 
    # draw splash screen if not started
    if not started:
        canvas.draw_image(splash_image, splash_info.get_center(),
                          splash_info.get_size(), [WIDTH / 2, HEIGHT / 2],
                          splash_info.get_size())
        current_song.pause()
    # spawn a mini-boss
    boss_spawner()
    
    if game_over:   # NEW: Draw a score if Game is Over
        canvas.draw_text("Best", [WIDTH - 50, 50], 17, "Black", "sans-serif")
        canvas.draw_text(str(high_score), [WIDTH - 50, 80], 17, "Black", "sans-serif")
        
 
 
# timer handler that spawns a rock

def rock_spawner():
    global rock_group, started
    if len(rock_group) > 12 or not started:
        return
    rock_vel = [random.random() * .6 - .3, random.random() * .6 - .3]
    rock_avel = random.random() * .2 - .1
    rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    # ensure rock_pos is at least 100px away of my_ship
    while dist(rock_pos, my_ship.pos) < 100:
        rock_pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    # add rock to the group
    #generate_number()
    rock_group.add(Sprite(rock_pos, rock_vel, 0, rock_avel,
                          asteroid_image_live, asteroid_info))
    
def boss_spawner():
    global boss_group
    if len(boss_group) > 1 or not started:
        return
    # if score > 1000 add boss
    boss_vel = [0, 0.2]
    boss_avel = random.random() * .2 - .1
    boss_pos = [WIDTH / 2, -HEIGHT]
    
    # boss every 100 poins TODO: REFACTOR
    if score % 100 == 0 and score != 0:
        boss_defected_sound.rewind()
        boss_defected_sound.play()
        boss_group.add(Sprite(boss_pos, boss_vel, 0, 0,
                              boss_image, boss_info))
    
    
cooling_countdown = 5
def keydown(key):
    global overheating
    if key == simplegui.KEY_MAP['left']:
        my_ship.decrement_angle_vel()
    elif key == simplegui.KEY_MAP['right']:
        my_ship.increment_angle_vel()
    elif key == simplegui.KEY_MAP['up']:
        my_ship.set_thrust(True)
    elif key == simplegui.KEY_MAP['space']:
        if overheating >= 0 and overheating <= 11 and not overheat_timer.is_running():
            my_ship.shoot()
            if overheating == 11:
                cooling_timer.stop()
                laser_overheat_sound.rewind()
                laser_overheat_sound.play()
                cooling_down_in.start()
                overheat_timer.start()
            else:
                overheating += 1
                
# timer handler that spawn overheat effect
def cool_down():
    global overheating, cooling_countdown
    if overheating > 0 and overheating <= 11:
        overheating -= 1
        
def engine_burned():
    global overheating
    cooling_timer.start()
    overheating = 5
    overheat_timer.stop()
    
def repair_engine():
    global cooling_countdown
    if cooling_countdown > 0:
        cooling_countdown -= 1
    elif cooling_countdown == 0:
        cooling_countdown = 5
        cooling_down_in.stop()
 
def recharge_shield():
    global new_shield_available
    new_shield_available = True
    shield_cool_down_timer.stop()
    
 
# initialize stuff
frame = simplegui.create_frame("Space Glory", WIDTH, HEIGHT)
 
# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
rock_group = set()
boss_group = set()
missile_group = set()
explosion_group = set()
 
 
# register handlers
frame.set_keyup_handler(keyup)
frame.set_keydown_handler(keydown)
frame.set_mouseclick_handler(click)
frame.set_draw_handler(draw)


timer = simplegui.create_timer(1000.0, rock_spawner)
cooling_timer = simplegui.create_timer(500.0, cool_down)
overheat_timer = simplegui.create_timer(3000.0, engine_burned)
cooling_down_in = simplegui.create_timer(1000.0, repair_engine) 
shield_cool_down_timer = simplegui.create_timer(10000.0, recharge_shield)

cooling_timer.start()
# get things rolling
timer.start()
frame.start()