import pygame, sys, random
from pygame.transform import *

#this size of the game window - you can change the width if you must, but then the skyline won't fit nicely
width, height = 1000,800
black = (255, 255, 255)

#this class creates a player object that is controlled by the arrow keys
class Player:
    def __init__(self, parentsurface, startX, startY, imageAddress):
        self.surface = parentsurface
        self.image  = pygame.image.load(imageAddress)
        self.hitBox = self.image.get_rect()

        self.hitBox.x = startX
        self.hitBox.y = startY

        #change this to alter the move rate of the player (smaller == slower == harder game)
        self.speed  = 3

    def draw(self):
        self.surface.blit(self.image,self.hitBox)

    def update(self):
        is_blue = True
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                is_blue = not is_blue

        #get the currently pressed key
        pressed = pygame.key.get_pressed()

        #based on the key pressed, change position by speed
        if (pressed[pygame.K_UP]    or pressed[pygame.K_w]): self.hitBox.y -= self.speed
        if (pressed[pygame.K_DOWN]  or pressed[pygame.K_s]): self.hitBox.y += self.speed
        if (pressed[pygame.K_LEFT]  or pressed[pygame.K_a]): self.hitBox.x -= self.speed
        if (pressed[pygame.K_RIGHT] or pressed[pygame.K_d]): self.hitBox.x += self.speed


class Sprite:
    def __init__(self, parentsurface, startX, startY, fallSpeed, isHostile, imageAddress):
        self.surface = parentsurface
        self.image  = pygame.image.load(imageAddress)

        #non-hostile sprites don't collide with the player
        self.isHostile = isHostile

        #a sprite doesn't have to fall - take the skyline for example - 0 would stop it falling
        #and a negative fallspeed would cause things to rise
        self.fallSpeed = fallSpeed

        self.collission = False

        #the hitbox determines where this sprite is drawn, and is used for collission detection
        self.hitBox   = self.image.get_rect()
        self.hitBox.x = startX
        self.hitBox.y = startY


    def draw(self):
        if(self.surface == None):
            return

        self.surface.blit(self.image,self.hitBox)

    def update(self):
        global health
        if(self.surface == None):
            return

        #if a collission occured, clean up the object and leave the update
        if(self.collission):
            self.cleanAway()
            return

        #moves the sprites hitbox down the y axis by it's speed
        self.hitBox=self.hitBox.move([0,self.fallSpeed])

        #Check if the object has left the bottom of the surface and clean it up if it has
        if self.hitBox.top > height:
            health -= 1
            print(health)
            self.cleanAway()

    #sets all the resources of the class to None - a clear indicator to whomever
    #'owns' the object that it should be disposed of.
    def cleanAway(self):
        self.surface = None
        self.image  = None

        self.isHostile = None
        self.fallSpeed = None
        self.hitBox = None

#This class creates an image that moves horizontally accross the top of the surface
class TopEnemy:
    def __init__(self, parentsurface, startX, startY, sideSpeed, imageAddress):
        self.surface = parentsurface
        self.image  = pygame.image.load(imageAddress)

        self.sideSpeed = sideSpeed

        self.hitBox   = self.image.get_rect()
        self.hitBox.x = startX
        self.hitBox.y = startY


    def draw(self):
        if(self.surface == None):
            return

        self.surface.blit(self.image,self.hitBox)

    def update(self):
        if(self.surface == None):
            return

        #if the object reaches an edge, reverse its direction
        if (self.hitBox.left < 0 or self.hitBox.right > width):
            self.sideSpeed = -self.sideSpeed

        self.hitBox=self.hitBox.move([self.sideSpeed,0])


#a helper class for taking objects out of lists (useful for discarding off-surface sprites)
def removeNoneObjects(someList):
    i = 0
    while i < len(someList):
        if(someList[i].surface == None):
            someList.pop(i)

        else:
            i += 1

def score(count):
    font = pygame.font.Font('freesansbold.ttf', 20)
    text = font.render('Score: ' + str(count), True, black)
    surface.blit(text, [100, 0])

#########################################Initial declarations
pygame.init()
surface = pygame.display.set_mode((width, height))

done = False

clock = pygame.time.Clock()

#increase or decrease the fps to make the game faster or slower (and harder or easier)
fps = 60

player = Player(surface,300,300,'superman.png')

#set this to change the amount of bombs it takes to end the game
startHealth = 10
health = startHealth

skylineStartY = height-200
skyline = Sprite(surface, 0,skylineStartY,0,False,"skyline.jpg")

bombs = [Sprite(surface,50,30,2, True, "bomb.png")]
alien = TopEnemy(surface,0,10,6,"spaceship.jpeg")

current_score = 0

#########################################
#This is the main game loop
#print(bool(pygame.image.get_extended()))
while not done:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

    score(current_score)

    #if health has reached 0 - break out of the main game loop to show the gameover surface
    if(health == 0):
        break

    #change the skyline so that it corresponds to the current health
    jumpSize = float(skyline.hitBox.height)/startHealth
    skyline.hitBox.y = skylineStartY + (startHealth-health)*jumpSize
    skyline.update()



    #update the position of the alien along the top of the surface
    alien.update()

    #perform the basic update to bombs (i.e. make them move down by their speed)
    for sprite in bombs:
        sprite.update()

    #sprite.update() is where bombs might turn into None object when they leave the surface (so they must be removed)
    removeNoneObjects(bombs)


    #randomly generate a new falling object (averaging at one new one per second)
    if(random.randint(0,fps) == 0):
        #the position of the new bomb is based on the aliens position
        newX = alien.hitBox.centerx
        newY = alien.hitBox.centery + 20
        fallSpeed = (random.randint(3,10))/3.0
        bombs.append(Sprite(surface,newX,newY,fallSpeed, True, "bomb.png"))


    #perform the basic update of the user constrolled object
    player.update()
    #check if the players sprite has overlapped with a falling object:
    for sprite in bombs:
        #has there been a collision?
        if(sprite.hitBox.colliderect(player.hitBox)):
            sprite.collission = True
            current_score += 1

    #reset the surface to all white so that the old game image doesn't remain
    surface.fill((255, 255, 255))

    #draw all the various images
    alien.draw()
    skyline.draw()
    player.draw()

    for sprite in bombs:
        sprite.draw()

    #Draw the above changes to the double buffered pygame display
    pygame.display.update()

    clock.tick(fps)

#create a game over image
gameover = pygame.image.load("gameover.png")

#iterate for 60 frames
for i in range(60):
    #keep handling events or the game will seem to freeze
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    surface.fill((255, 255, 255))
    #draw everything in the last position they were in before the game ended (except the skyline because it exploded)
    alien.draw()
    player.draw()
    for sprite in bombs:
        sprite.draw()

    #draw the game over sprite over everything else
    surface.blit(gameover,(250,100))

    #wait for a 20fps time span
    clock.tick(20)
    pygame.display.flip()

pygame.quit()
sys.exit()