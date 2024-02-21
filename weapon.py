import pygame
import math
import constants
import random

# As the file name implies, this is the file for creating the weapon that the main character will be able 
# to have (it will be a bow for now)

# first we will create a class for the weapon:
class Weapon():
    # next we make our constructor:
    def __init__(self, image, arrow_image): # image argument is the image we will use for the weapon
        self.original_image = image # this will help us keep track of the weapon, especially since it will be rotating around the our character alot
        self.angle = 0
        self.image = pygame.transform.rotate(self.original_image, self.angle) # here we are rotating the original image by/with the new angle
                                                                              # Because as the game go on the angle will be changing, which will have us take our original image and rotate it by the angle, which will genrate a new image
       # this will allow us to call for the arrows essentially:
        self.arrow_image = arrow_image                                                                      
        self.rect = self.image.get_rect()
        self.fired = False # here is our trigger for the arrow
        self.last_shot = pygame.time.get_ticks() # this is used to somewhat limit the user, so they can not spam the arrows, but instead they will need to wait for a certain amount of time before shooting the next arrow

    def update(self, player):
        shot_cooldown = 100 # this is in miliseconds (this is a wait time until the next arrow can be shot), this is similiar to the character animation
        arrow = None # this is so we dont get an error when we are in the game and the code is trying to return something
        
        self.rect.center = player.rect.center # will help us position the rectangle (the bow)

        pos = pygame.mouse.get_pos()
        x_dist = pos[0] - self.rect.centerx
        y_dist = -(pos[1] - self.rect.centery) # its negative because pygame y-coordinates increase down screen
        self.angle = math.degrees(math.atan2(y_dist, x_dist)) # this will first give us the angle, based on the y and x distances.
                                                              # However, it will give us the numbers in radiant, but the "math.degrees" will convert radians into degrees  
        
        
        # next, we will add the arrows in this update function so when we shoot the arrows, the arrow will appear:
        # the bow will always be centered on the player, so we will create the following functions to update the bow:
        # LATER, we want to use the shift key instead of the mouse:
        if pygame.mouse.get_pressed()[0] and self.fired == False and (pygame.time.get_ticks() - self.last_shot) >= shot_cooldown: # this will allow us to chekc to see if the mouse was pressed. The '[0]' checks to see if the left mouse button has been pressed. We will need to use '[2]' to know is the right mouse button has been pressed
            arrow = Arrow(self.arrow_image, self.rect.centerx, self.rect.centery, self.angle)
            self.fired = True
            self.last_shot = pygame.time.get_ticks()
            
        # resetting the mouse click:
        if pygame.mouse.get_pressed()[0] == False:
            self.fired = False
            
        return arrow # this will return the arrow back into the game
            
            
            
    def draw(self, surface):
        self.image = pygame.transform.rotate(self.original_image, self.angle) # first we update the image
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
        

# Next, we will create an arrow class. We also want to use inheritance from pygames existing sprite class
# which means, we will not have the parenthesis empty:
class Arrow(pygame.sprite.Sprite):
    def __init__(self, image, x, y, angle):
        # adding the sprite class inheritance constructor:
        pygame.sprite.Sprite.__init__(self)
        
        # next, we will assign the variables/arguments that are being passed into the class:
        self.original_image = image # just like with the weapon class above, we want to keep the orignal image since we will be "rotating" our arrows 
        self.angle = angle
        self.image = pygame.transform.rotate(self.original_image, self.angle - 90) # here we are rotating the original image by/with the new angle
        self.rect = self.image.get_rect() 
        self.rect.center = (x, y) # this will position our image
        
        # now we are about to calculate the horizontal and vertical speeds based on the angles
        self.dx = math.cos(math.radians(self.angle)) * constants.ARROW_SPEED
        self.dy = -(math.sin(math.radians(self.angle)) * constants.ARROW_SPEED) # adding the negative to this because the pygame y-coordinates increases down the screen
        
        
    def update(self, monster_list): # this is for the arrow animation (for now)
        
        # resetting variables:
        damage = 0
        damage_pos = None
        
        # reposition based on the speed of the arrow:
        self.rect.x += self.dx
        self.rect.y += self.dy
        
        # next, we want to check and see if the arrow has went off screen (so we can delete the sprite):
        
        if self.rect.right < 0 or self.rect.left > constants.SCREEN_WIDTH or self.rect.bottom < 0 or self.rect.top > constants.SCREEN_HEIGHT:
            self.kill() # this is apart of the sprite class, we can just kill the sprite if any of the commands are true
            
            
        # Here we will check to see if the arrow of our players bow has made contact with the monster
        # Also, we will check to see if the enemy is still alive, if it is then the arrow will continue hitting
        # the enemy and not go through them. However (for now), if the enemy is dead then the arrow will go past them:
        for monster in monster_list:
            if monster.rect.colliderect(self.rect) and monster.alive:
                damage = 10 + random.randint(-5, 5) # the 10 is the base damage of the arrow, the "-5, 5" means we can make damage from 5 to 15
                monster.health -= damage # whatever random damage is taken by the enemy, they will have it subtracted from their health
                
                # so we can show/print the damage onto the screen, but for where the monster is:
                damage_pos = monster.rect
                
                # next, we will want to stop the arrow once it makes contact with the monster
                self.kill()
                break
            
        # returning the daamage so it can show on the screen:
        return damage, damage_pos
        
    # here we will make the draw fucntion for the arrow:
    def draw(self, surface): # sprites normally do not need a draw method because it already has its own, but we need to make it to
        surface.blit(self.image, ((self.rect.centerx - int(self.image.get_width()/2)), self.rect.centery - int(self.image.get_height()/2)))
