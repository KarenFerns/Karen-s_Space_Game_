import pgzrun
import random

user_name = input ('please enter you user name: ')

# define screen__________________________________________________________
WIDTH = 1000 #width of the window
HEIGHT = 600 #height of the window
SCOREBOX_HEIGHT = 50 #height of scorebox

#count score_____________________________________________________________
score = 0 #start off with zero points

#sprite speeds____________________________________________________________
junk_speed = 5
sat_speed = 3
debris_speed = 5
laser_speed = -5 #moving LEFT, so negative x direction

BACKGROUND_IMG = 'background_gamespace' #background file name
PLAYER_IMG = 'made_spaceship' #sprite file name
JUNK_IMG = 'space_junk' #space junk file name
SATELLITE_IMG = 'satellite_adv' #change to your file name
DEBRIS_IMG = 'tesla_roadster'
LASER_IMG = 'laser_red'

# initialize sprites______________________________________________________
# sprite_name = Actor ('file_name', rect_pos = (x, y))
player = Actor (PLAYER_IMG)
player.midright = (WIDTH - 10, HEIGHT/2) #rect_position = (x, y)

#initialize junk sprites
junks = [] #list to keep track of junks
for i in range (5):
    junk = Actor (JUNK_IMG) #create a junk sprite
    x_pos = random.randint (-500, -50)
    y_pos = random.randint (SCOREBOX_HEIGHT, HEIGHT - junk.height)
    junk.pos = (x_pos, y_pos) # rect_position = (x, y)
    junks.append (junk)

#initialize satellite
satellite = Actor (SATELLITE_IMG)# create a junk sprite
x_sat = random.randint (-500, -50)
y_sat = random.randint (SCOREBOX_HEIGHT, HEIGHT - satellite.height)
satellite.topright = (x_sat, y_sat) #rect_position

#initialize debris
debris = Actor (DEBRIS_IMG)
x_deb = random.randint (-500, -50)
y_deb = random.randint (SCOREBOX_HEIGHT, HEIGHT - debris.height)
debris.topright = (x_deb, y_deb) #rect_position

#initialize lasers
lasers = [] #empty list

#background music
sounds.spacelife.play(-1)

#main game loop_________________________________________________________
def update (): #main update function
    if score >= 0:
        updatePlayer() # calling our player update function
        updateJunk()
        updateSatellite()
        updateDebris()
        updateLasers() #call update lasers function
    
def draw ():
    screen.clear ()
    screen.blit (BACKGROUND_IMG, (0, 0))
    player.draw () # draw player sprite on screen
    for junk in junks:
        junk.draw () #draw junk sprite on screen
    satellite.draw()
    debris.draw()
    for laser in lasers:
        laser.draw()
    #game over screen
    if score < 0:
        game_over = 'GAME OVER'
        screen.draw.text (game_over, center = (WIDTH/2, HEIGHT/2), fontsize = 70, color = 'red', owidth = 0.5, ocolor = 'white')
        sounds.spacelife.stop()

    #show text on screen
    show_score = "Score: " + str (score) #remember to convert score to a string
    screen.draw.text (show_score, topleft=(15,15), fontsize=35, color='navy blue')
    show_name = 'player: ' + user_name
    screen.draw.text (show_name, topleft=(300,15), fontsize=35, color='navy blue')

#update sprites_________________________________________________________
def updatePlayer():
    # check for keyboard inputs
    if keyboard.up == 1:
        player.y += -5 # moving up is negative y-direction
    elif keyboard.down == 1:
        player.y += 5 # moving down is positive y-direction
    # prevent player from moving off screen
    if player.top < SCOREBOX_HEIGHT:
        player.top = SCOREBOX_HEIGHT
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    #check for firing lasers
    if keyboard.space == 1:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

def updateJunk ():
    global score
    for junk in junks: #add for loop
        junk.x += junk_speed #same as junk.x = junk.x + 3

        collision = player.colliderect (junk) #declare collision variable
    
        if junk.left > WIDTH or collision == 1: #make junk reappear if move off screen
            x_pos = random.randint (-500, -50) #start off screen
            y_pos = random.randint (SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

        if collision == 1: #if collision occurs
            sounds.collect_pep.play() #sound effect
            score += 1 #this is the same score = score +1


def updateSatellite():
    global score
    satellite.x += sat_speed # or just put 3
    collision = player.colliderect (satellite)

    if satellite.left > WIDTH or collision == 1:
        x_sat = random.randint (-500, -50)
        y_sat = random.randint (SCOREBOX_HEIGHT, HEIGHT - satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision == 1:
        score += -5

def updateDebris():
    global score
    debris.x += debris_speed # or just put 3
    collision = player.colliderect (debris)

    if debris.left > WIDTH or collision == 1:
        x_deb = random.randint (-500, -50)
        y_deb = random.randint (SCOREBOX_HEIGHT, HEIGHT - debris.height)
        debris.topright = (x_deb, y_deb)

    if collision == 1:
        score += -5

def updateLasers():
    global score
    for laser in lasers:
        laser.x += laser_speed
        #remove laser if off screen
        if laser.right < 0:
            lasers.remove (laser)
        #detect collisions
        if satellite.colliderect (laser) == 1:
            lasers.remove(laser)
            x_sat = random.randint (-500, -50)
            y_sat = random.randint (SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score += -5
            sounds.explosion.play ()
        if debris.colliderect (laser) == 1:
            lasers.remove (laser)
            x_deb = random.randint (-500, -50)
            y_deb = random.randint (SCOREBOX_HEIGHT, HEIGHT - debris.height)
            debris.topright = (x_deb, y_deb)
            score += 10
            sounds.explosion.play()

# activating lasers (template code)__________________________________________
player.laserActive = 1 #add laserActive status to the player

def makeLaserActive(): #when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire02.play() #play sounds effect
        lasers.append(laser) # add laser to lasers list

pgzrun.go () # function that runs our game loop
