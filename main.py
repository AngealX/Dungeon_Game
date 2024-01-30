# Here we will be creating the dungeon game with the use of "pygame"
# first thing we need to do is import pygame in order to use it
# REMINDER: We have to always run on this file, sense it is the main file

import pygame
from character import Character # we import the character file this way becase we are using "class" in the character file
from weapon import Weapon # same applies for this file
import constants # this is where all the variables that will not change will be stored here in the constant file

# after we have imported the game, we will need to also initialize it by using the following command:
pygame.init()


# Next, we want to create a game window (where the actual game will be displayed)
# In order to do so, we will use the code below to make our window:
screen = pygame.display.set_mode((constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT))

# Now we can change the name of the screen by doing the following below:
pygame.display.set_caption("Dungeon Crawler") 

# Here we will create a clock, the reason being is so that we can prevent the figure from 
# just shooting off screen. So, the clock will help slow down the frame rate (so, we are essentially 
# "capping" the frame rate to maintain the frame rate):
clock = pygame.time.Clock()

# Here are the variables to define/execute the players movement:
moving_left = False # these are just triggers, they dont necessarily move the player around themselves
moving_right = False
moving_up = False
moving_down = False


# Here is the helper function to scale image(which helps to speed things up, especially for things that need to occur repeatedly):
# This function also helps clean up the code some too

def scale_img(image, scale): # will pass in all the info for the players image
    # first making the width and height of the image:
    w = image.get_width()
    h = image.get_height()
    return pygame.transform.scale(image, (w * scale, h * scale)) # returning the scaled version for the image




#===================================== Loading weapon image/functioning =============================================================================================================

# first, we create/import the bow image
bow_image = scale_img(pygame.image.load("assets/images/weapons/bow.png").convert_alpha(), constants.WEAPON_SCALE) # wrapping in our "helper" function "scale_img" (which is above)

# Next, we will import/make the arrows for the bow:
arrow_image = scale_img(pygame.image.load("assets/images/weapons/arrow.png").convert_alpha(), constants.WEAPON_SCALE) 



#===================================== Allowing movement and iteration for the characters ===============================================================================


# Loading all the characters we will be using by making pretty much a triple nested list:
mob_animations = []
mob_types = ["elf", "imp", "skeleton", "goblin", "muddy", "tiny_zombie", "big_demon"] # these names coarilate with the actual photos for the characters

# starting at this point (until the end of the for loops) is where we are able to have
# each character move while in idle and iterate through each of the characters
# which we accomplish by triggering the self action trigger:
animation_types = ["idle", "run"]

# adding a for loop to iterate through the mod_types list:
for mob in mob_types:
# Creating the animation to load in the other images needed (automatically):
    animation_list = []
    for animation in animation_types:
    # reset temporary list of images
        temp_list = []
    
        for i in range(4):
            # With each iteration of the loop, it will load the images "0.png", "1.png", etc
            img = pygame.image.load(f"assets/images/characters/{mob}/{animation}/{i}.png").convert_alpha() # in "convert_alpha()" the convert part converts the image to match the format of the game window. While ".aplha()" just makes sure the image stays tranparent
            img = scale_img(img, constants.SCALE)
            temp_list.append(img)    
        animation_list.append(temp_list) # storing the image from temp list (making nested list)
        # need to create another store list to contain the animation for idle and run images
        
    mob_animations.append(animation_list)
    
# creating the chracter (REMINDER: We are using the "constructor" from the character file, in order maake our character):
player = Character(100, 100, mob_animations, 0)

# Creating the players weapon:
bow = Weapon(bow_image, arrow_image)

# this will create the sprite group (for now, for the arrows):
arrow_group = pygame.sprite.Group()

# ============================================================ MAIN CODE / LOOP ==========================================================================

# Next we will use a game loop (by using a while loop in this case) so that the screen can stay up
# so this will be the main game loop
run = True
while run:
    
    
    # Here we will help control the frame rate:
    clock.tick(constants.FPS)

    screen.fill(constants.BG) # this will basically clear the background of the character for each time we move them:
    
    
    # Here, we will calculate the players movement:
    dx = 0
    dy = 0 # the d's in dy and dx, stands for "delta" which (in math, calculus to be exact)
            # means the change in the "x" (for dx) and the change in the "y" (for dy)
    
    if moving_right == True: # checking to see if the user chooses the right arrow button:
        dx = constants.SPEED # the "SPEED" (which just use to be the # 5) stands for 5 pixels (so its moving to the right by 5 pixels)
    
    if moving_left == True: 
        dx = -constants.SPEED

    if moving_up == True: # the reason this has a negative number is because in pygame, the top-left corner of the screen is (0, 0) which means when we move
                            # "up", we are actually using a negative integer (in normal cases, this would not be true)
        dy = -constants.SPEED
    
    if moving_down == True: # the opposite effect of regular plot charts
        dy = constants.SPEED
            
    # We have the code (below) to check for any errors as we test:
    # print(str(dx) + ", " + str(dy))
    
    # now we will take the function named "move" from the character
    # file and begin to have the player move (in this case, the rectangle at the moment):
    player.move(dx, dy)
    
    # updates the player:
    player.update() # from the update function in the character file
    
    # updating the character weapon (the bow):
    arrow = bow.update(player) # what ever is being returned (based on the update function in the weapons file) will be stored in this varible
    
    if arrow: #checking to see if something has been returned (meaning, the user has clicked the mouse or not)
        arrow_group.add(arrow) # with groups we use ".add()" instead of ".append()" (which is used for list)

    for arrow in arrow_group: # allows us to update through each of the arrows in the arrow group
        arrow.update()
        
        
    # arrow_group.draw(screen), would be used since we are using sprite, meaning we would not need to make a draw class, but since we needed to modify
    # the arrows, we needed the draw method instead
        
    # here we will draw the character:
    player.draw(screen)
    
    # here we will draw/make the weapon:
    bow.draw(screen)
    
    # iterating througj the arrow group:
    for arrow in arrow_group:
        arrow.draw(screen)
        
        
    # first, we want to be able to exit out of the screen by creating an event handler
    # which basically will check for a certain action/event to occur in order to stop
    # the while loop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # This command basically lets us use the "x" to exit the screen
            run = False # since this become false, the game will then stop
        
        # Here we will take keyboard input from the user 
        if event.type == pygame.KEYDOWN: # Looks for what key is being pressed
            if event.key == pygame.K_RIGHT: # the "_RIGHT" symbolizes the "-->" arrow key on the keyboard
                moving_right = True
            if event.key == pygame.K_LEFT: # the "_LEFT" symbolizes the "<--" arrow key on the keyboard
                moving_left = True
            if event.key == pygame.K_UP: # the "_UP" symbolizes the "^" arrow key on the keyboard (not the exponent carrot)
                moving_up = True
            if event.key == pygame.K_DOWN: # the "_DOWN" symbolizes the "v" arrow key on the keyboard
                moving_down = True
        
        # For when the key is released/no longer being pressed
        if event.type == pygame.KEYUP: # Looks for what key is being released/let go
            if event.key == pygame.K_RIGHT: # if the right button is no pressed, then the character will stop moving right
                moving_right = False
            if event.key == pygame.K_LEFT: # if the right button is no pressed, then the character will stop moving left
                moving_left = False
            if event.key == pygame.K_UP: # if the right button is no pressed, then the character will stop moving up
                moving_up = False
            if event.key == pygame.K_DOWN: # if the right button is no pressed, then the character will stop moving down
                moving_down = False
        
    
    # REFERRING TO THE IF-STATEMENTS ABOVE AND THE WHILE LOOP: In the conditional statement above (and within the while loop in general)
    # we had to change some things up, one being to slow down the frame speed for the figure by using the "clock" function. The reason why we 
    # have to do this (also explains this above) is so that we can prevent the figure from just moving extremely 
    # quick (and off the screen) when the movement buttons are pressed.
    # Also, we had to change things up with the conditional as well, because when we press down the movement key button (on the keyboard)
    # the command on stayed as "True", so we needed to make another set of condionals, that checks to see if the user let go of the key, 
    # if so, then the figure will stop moving (shown in the code above) by making the moving command into false 
    
    # In order to show the character (and other displays in general),
    # we will need to tell python to update the screen by using the 
    # command below:
    pygame.display.update()


pygame.quit() # this will close everything down