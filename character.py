import pygame
import constants
import math

# Here will be the code to create the character for the game. 
# which of course we will need to import later into the main folder

class Character():
    
    # first we will make our constructor (REMINDER: "def" starts functions):
    
    def __init__(self, x, y, health, mob_animations, char_type): # "self" is always the first argument
        self.char_type = char_type
        self.flip = False # this will act as a trigger, so when the character goes right, the character image will flip to face that direction
        self.animation_list = mob_animations[char_type] # the "char_type" helps us determine which set is going to be aplicable by using the "char_type". So, if the image is the elf, then we must make sure that we are taking the first set of image
        self.frame_index = 0 # this controls which frame of the animation we want to show
        self.action = 0 # when its 0 = idle, when its 1 = run
        self.update_time = pygame.time.get_ticks() # use this to measure how much time has passed since the last time the frame has been updated
        self.running = False
        self.health = health
        self.alive = True # this is so when a monster (and even the player) health reaches zero, they will die/disappear in the game
        
        # taking care of the image
        self.image = self.animation_list[self.action][self.frame_index]
        self.rect = pygame.Rect(0, 0, 40, 40) # first 0 is the x-coordinate, the second 0 is the y-coordinate, and the last 40's is width and height (respectfully)
        self.rect.center = (x, y)
      
    # Now, we will make a method that will allow the player to move
    # and REMINDER: always add the self part)  
    
    def move(self, dx, dy):
        self.running = False # player will always start off as idle
        if dx != 0 or dy != 0:
            self.running = True # as soon as ther is any movement, the character should begin running (and vice versa)
            
        # allowing the chracter to flip/turn in the direction it is heading:
        if dx < 0: # going based on reather the change in x is negative or positive
            self.flip = True
        if dx > 0:
            self.flip = False
            
            
        # we now have control over the x and y, but we also need the same amount of speed for 
        # the "diagonal" ccurance (this was creating a small problem because the figure would take
        # the figure and move across the screen faster compared t)
        if dx != 0 and dy != 0:
            dx = dx * (math.sqrt(2)/(2))
            dy = dy * (math.sqrt(2)/(2))

        self.rect.x += dx
        self.rect.y += dy


    def update(self):
        
        # check to see if the character has died:
        if self.health <= 0:
            self.health = 0
            self.alive = False
        
        # checks what action the player is performing
        if self.running == True:
            self.update_action(1) # use self to call the function since its in the same class. the 1 means the character is running 
        else: 
            self.update_action(0) # will idle
        animation_cooldown = 100 # will control the speed of the animation (the lower the number, the faster the animation)
        
        # updating the image:
        self.image = self.animation_list[self.action][self.frame_index] # will change throughout the update method.
        
        # checking to see if enough time has passed since the last update:
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks() # this resets the timer
        
        # check is the animaiton has finished
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
            

    def update_action(self, new_action):
        # check is the new action is different from the previous one:
        if new_action != self.action:
            self.action = new_action
        
            # update the animation settings:
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()
        
    # In order to print to the screen, we have to explicitly tell python to print to 
    # the screen (and then call in the main file in order to show):
    def draw(self, surface):
        flipped_img = pygame.transform.flip(self.image, self.flip, False)
        if self.char_type == 0: # This will help us add an "offset" for the player character (for the elf) only
            surface.blit(flipped_img, (self.rect.x, self.rect.y - constants.SCALE * constants.OFFSET)) # this will make the needed offset for the character
        else:
            surface.blit(flipped_img, self.rect) # the "self.rect" controls the position and the collisions and the movement
                                            # the "self.image" will just draw/place the image at the location (the sqaure is still there underneath everything)
                                            
        pygame.draw.rect(surface, constants.RED, self.rect, 1) # the number "1" ensures the box is 1 thick on its outlines, which makes the character/image now visible 
                                                               # (granted, we will need to increase the size of the image to make it more visible)