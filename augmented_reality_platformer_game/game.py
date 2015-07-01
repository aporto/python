"""
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/

From:
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py

Explanation video: http://youtu.be/BCxWJgN4Nnc

Part of a series:
http://programarcadegames.com/python_examples/f.php?file=move_with_walls_example.py
http://programarcadegames.com/python_examples/f.php?file=maze_runner.py
http://programarcadegames.com/python_examples/f.php?file=platform_jumper.py
http://programarcadegames.com/python_examples/f.php?file=platform_scroller.py
http://programarcadegames.com/python_examples/f.php?file=platform_moving.py
http://programarcadegames.com/python_examples/sprite_sheets/
"""

import pygame
import cv2
import numpy as np;
import time
from sprite_sheet import SpriteSheet


cap = cv2.VideoCapture(0)

# Global constants

# Colors
BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
BLUE     = (   0,   0, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)

# Screen dimensions
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600

levelBlocks = [[210, 70, 500, 500]]
""",
                 [210, 70, 200, 400],
                 [210, 70, 600, 300],
                 ]
"""
projectionLimits = [ [10,10], [630,20], [600,470], [20,430]]

class Player(pygame.sprite.Sprite):
    """ This class represents the bar at the bottom that the player
        controls. """

    # -- Methods
    def __init__(self):
        """ Constructor function """

        # Call the parent's constructor
        super(Player, self).__init__()

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        width = 40
        height = 80 #60

        sprite_sheet = SpriteSheet("walk_red2.png")
        #sprite_sheet = SpriteSheet("p1_walk.png")
        # Load all the right facing images into a list
        self.image = sprite_sheet.get_image(0, 0, 40, 80)

        self.walking_frames_r = []
        self.walking_frames_l = []
        for i in range(10):
            image = sprite_sheet.get_image(i * 40, 0, 40, 80)
            self.walking_frames_r.append(image)
            image = sprite_sheet.get_image(i * 40, 80, 40, 80)
            self.walking_frames_l.append(image)

        self.imageFrame = 0
        self.image = self.walking_frames_r[self.imageFrame]

        #self.image = pygame.Surface([width, height])
        self.rect = self.image.get_rect()
        #self.image.fill(RED)

        # Set a referance to the image rect.
        self.rect = self.image.get_rect()

        # Set speed vector of player
        self.change_x = 0
        self.change_y = 0
        self.goLeft = False

        # List of sprites we can bump against
        self.level = None
        self.onAir = False


    def update(self):
        """ Move the player. """
        # Gravity
        self.calc_grav()

        # Move left/right
        self.rect.x += self.change_x
        if (self.change_x > 0):
            self.imageFrame = self.imageFrame + 0.2
            if self.imageFrame > 9:
                self.imageFrame = 1
        else:
            if (self.change_x < 0):
                self.imageFrame = self.imageFrame - 0.2
                if self.imageFrame < 1:
                    self.imageFrame = 9
            else:
                if (self.change_x > 0):
                    self.imageFrame = 0
        if self.change_x == 0:
            if self.goLeft:
                self.image = self.walking_frames_l[0]
            else:
                self.image = self.walking_frames_r[0]
        else:
            if (self.change_x > 0):
                self.image = self.walking_frames_r[int(self.imageFrame)]
            else:
                self.image = self.walking_frames_l[10-int(self.imageFrame)]

        #print self.change_y
        if self.onAir:
            if self.goLeft:
                self.image = self.walking_frames_l[3]
            else:
                self.image = self.walking_frames_r[3]

        # See if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:
            # If we are moving right,
            # set our right side to the left side of the item we hit
            if self.change_x > 0:
                self.rect.right = block.rect.left
            elif self.change_x < 0:
                # Otherwise if we are moving left, do the opposite.
                self.rect.left = block.rect.right

        # Move up/down
        self.rect.y += self.change_y

        # Check and see if we hit anything
        block_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        for block in block_hit_list:

           # Reset our position based on the top/bottom of the object.
            if self.change_y > 0:
                self.rect.bottom = block.rect.top
            elif self.change_y < 0:
                self.rect.top = block.rect.bottom

            # Stop our vertical movement
            self.change_y = 0
            self.onAir = False

    def calc_grav(self):
        """ Calculate effect of gravity. """
        if self.change_y == 0:
            self.change_y = 1
        else:
            self.change_y += .35
        if abs(self.change_y) > 1:
            self.onAir = True
        else:
            self.onAir = False

        # See if we are on the ground.
        if self.rect.y >= SCREEN_HEIGHT - self.rect.height and self.change_y >= 0:
            self.change_y = 0
            self.rect.y = SCREEN_HEIGHT - self.rect.height

    def jump(self):
        """ Called when user hits 'jump' button. """

        # move down a bit and see if there is a platform below us.
        # Move down 2 pixels because it doesn't work well if we only move down 1
        # when working with a platform moving down.
        self.rect.y += 2
        platform_hit_list = pygame.sprite.spritecollide(self, self.level.platform_list, False)
        self.rect.y -= 2

        # If it is ok to jump, set our speed upwards
        if len(platform_hit_list) > 0 or self.rect.bottom >= SCREEN_HEIGHT:
            self.change_y = -9
        self.onAir = True

    # Player-controlled movement:
    def go_left(self):
        """ Called when the user hits the left arrow. """
        self.change_x = -3
        self.goLeft = True;

    def go_right(self):
        """ Called when the user hits the right arrow. """
        self.change_x = 3
        self.goLeft = False;

    def stop(self):
        """ Called when the user lets off the keyboard. """
        self.change_x = 0

class Platform(pygame.sprite.Sprite):
    """ Platform the user can jump on """

    def __init__(self, width, height):
        """ Platform constructor. Assumes constructed with user passing in
            an array of 5 numbers like what's defined at the top of this
            code. """
        super(Platform, self).__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(GREEN)

        self.rect = self.image.get_rect()

class Level(object):
    """ This is a generic super-class used to define a level.
        Create a child class for each level with level-specific
        info. """

    # Lists of sprites used in all levels. Add or remove
    # lists as needed for your game.
    platform_list = None
    enemy_list = None

    # Background image
    background = None

    def __init__(self, player):
        """ Constructor. Pass in a handle to player. Needed for when moving platforms
            collide with the player. """
        self.platform_list = pygame.sprite.Group()
        self.enemy_list = pygame.sprite.Group()
        self.player = player
        self.drawBlocks = False

    # Update everythign on this level
    def update(self):
        """ Update everything in this level."""
        self.platform_list.update()
        self.enemy_list.update()

    def draw(self, screen):
        """ Draw everything on this level. """

        # Draw the background
        screen.fill(WHITE)

        # Draw all the sprite lists that we have
        #if self.drawBlocks:
        self.platform_list.draw(screen)
        self.enemy_list.draw(screen)


# Create platforms for the level
class Level_01(Level):
    """ Definition for level 1. """

    def __init__(self, player):
        """ Create level 1. """

        # Call the parent constructor
        Level.__init__(self, player)

        # Array with width, height, x, and y of platform
        global levelBlocks

        # Go through the array above and add platforms
        for platform in levelBlocks:
            block = Platform(platform[0], platform[1])
            block.rect.x = platform[2]
            block.rect.y = platform[3]
            block.player = self.player
            self.platform_list.add(block)

def play():
    """ Main Program """
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    pygame.display.set_caption("Augmented Reality Platformer")

    # Create the player
    player = Player()

    # Create all the levels
    level_list = []
    level_list.append( Level_01(player) )

    # Set the current level
    current_level_no = 0
    current_level = level_list[current_level_no]

    active_sprite_list = pygame.sprite.Group()
    player.level = current_level

    player.rect.x = 340
    player.rect.y = SCREEN_HEIGHT - player.rect.height
    active_sprite_list.add(player)

    #Loop until the user clicks the close button.
    done = False

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()

    # -------- Main Program Loop -----------
    while not done:
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                done = True # Flag that we are done so we exit this loop

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player.go_left()
                if event.key == pygame.K_RIGHT:
                    player.go_right()
                if event.key == pygame.K_UP:
                    player.jump()

                if event.key == pygame.K_SPACE:
                    current_level.drawBlocks = not current_level.drawBlocks

                if event.key == pygame.K_RETURN: # atualiza
                    screen.fill(WHITE)
                    pygame.display.flip()
                    time.sleep(0.010)
                    detectBlocks()
                    level_list = []
                    level_list.append( Level_01(player) )
                    current_level = level_list[current_level_no]
                    player.level = current_level

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT and player.change_x < 0:
                    player.stop()
                if event.key == pygame.K_RIGHT and player.change_x > 0:
                    player.stop()

        # Update the player.
        active_sprite_list.update()

        # Update items in the level
        current_level.update()

        # If the player gets near the right side, shift the world left (-x)
        if player.rect.right > SCREEN_WIDTH:
            player.rect.right = SCREEN_WIDTH

        # If the player gets near the left side, shift the world right (+x)
        if player.rect.left < 0:
            player.rect.left = 0

        # ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
        current_level.draw(screen)
        active_sprite_list.draw(screen)

        # ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT

        # Limit to 60 frames per second
        clock.tick(60)

        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    # Be IDLE friendly. If you forget this line, the program will 'hang'
    # on exit.
    pygame.quit()

def loadImage():
    #capture = cv.CaptureFromCAM(0)
    #frame = cv.QueryFrame(capture)
    ret, img = cap.read()
    #img = cv2.imread("C:\\Users\\aporto\\Desktop\\whiteboard.jpg")
    return img

def detectBlocks():
    img = loadImage()
    #, cv2.IMREAD_GRAYSCALE)
    time1 = time.time();
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret,thresh = cv2.threshold(imgray, 100,255,0)
    cv2.imshow("Camera", imgray)
    cv2.imshow("thresh", thresh)

    #image, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    global levelBlocks
    levelBlocks[:] = []

    #global projectionLimits
    #srcPts = np.float32([[0,0], [639,0], [639, 479], [0,479]]).reshape(-1,1,2)
    #dstPts = np.float32(projectionLimits).reshape(-1,1,2)
    #M, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC,5.0)
    global homo
    for contour in contours:
        x,y,w,h = cv2.boundingRect(contour)
        if w < 620 and w > 60:
            if h < 400 and h > 5:
                #cv2.rectangle(im,(x,y),(x+w,y+h),(0,255,0),2)
                pts = np.float32([ [x,y],[x+w, y],[x+w, y+h],[x, y+h] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts, homo)
                dst = np.int32(dst)
                x1 = dst[0][0][0]
                y1 = dst[0][0][1]
                w1 = dst[2][0][0] - x1
                h1 = dst[2][0][1] - y1

                #x1 = x1 * SCREEN_WIDTH / 640
                #y1 = y1 * SCREEN_HEIGHT / 480
                #w1 = w1 * SCREEN_WIDTH / 640
                #h1 = h1 * SCREEN_HEIGHT / 480

                #levelBlocks.append ([w1*SCREEN_WIDTH/640, h1*SCREEN_HEIGHT/480, x1*SCREEN_WIDTH/640, y1*SCREEN_HEIGHT/480])
                levelBlocks.append ([w1, h1, x1, y1])
    #cv2.drawContours(im, contours, -1, (0,255,0), 3)
    print (time.time() - time1) * 1000

    if len(levelBlocks) == 0:
        levelBlocks.append([210, 70, 500, 500])

    #cv2.imshow("thresould", thresh)
    #cv2.imshow("img", im)
    #cv2.waitKey(0)

def calibrate():
    pygame.init()

    # Set the height and width of the screen
    size = [SCREEN_WIDTH, SCREEN_HEIGHT]
    screen = pygame.display.set_mode(size)

    done = False
    end = False
    clock = pygame.time.Clock()
    global levelBlocks
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                end = True

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RETURN:
                    done = True
        clock.tick(30)
        screen.fill(WHITE)
        pygame.display.flip()
        detectBlocks()
    pygame.quit()


    return not end

def cvMouseEvent(event,x,y,flags,param):
    import cv2
    global mouseX,mouseY
    global projectionLimits

    if x < 320:
        if y < 240:
            idx = 0
        else:
            idx = 3
    else:
        if y < 240:
            idx = 1
        else:
            idx = 2

    if event == 0:
        return
    if event == 1: #cv2.EVENT_LBUTTONDBLCLK:
        projectionLimits[idx][0] = x
        projectionLimits[idx][1] = y
        #cv2.circle(img,(x,y),100,(255,0,0),-1)
        #mouseX,mouseY = x,y

def calculateProjectionCoordinates():
    import cv2
    import numpy as np;

    cv2.namedWindow('camera')
    cv2.setMouseCallback('camera',cvMouseEvent)

    global projectionLimits
    #projectionLimits = [ [0,0], [799,0], [799,599], [0,599]]

    while(1):
        img = loadImage()
        cv2.line(img, (projectionLimits[0][0], projectionLimits[0][1]), (projectionLimits[1][0], projectionLimits[1][1]), (0,0,255), 2)
        cv2.line(img, (projectionLimits[1][0], projectionLimits[1][1]), (projectionLimits[2][0], projectionLimits[2][1]), (0,0,255), 2)
        cv2.line(img, (projectionLimits[2][0], projectionLimits[2][1]), (projectionLimits[3][0], projectionLimits[3][1]), (0,0,255), 2)
        cv2.line(img, (projectionLimits[3][0], projectionLimits[3][1]), (projectionLimits[0][0], projectionLimits[0][1]), (0,0,255), 2)
        cv2.imshow('camera',img)
        k = cv2.waitKey(20) & 0xFF
        if k == 13:
            break
        elif k == ord('a'):
            print mouseX,mouseY

    cv2.destroyAllWindows()

    srcPts = np.float32(projectionLimits).reshape(-1,1,2)
    dstPts = np.float32([[0,0], [SCREEN_WIDTH,0], [SCREEN_WIDTH, SCREEN_HEIGHT], [0,SCREEN_HEIGHT]]).reshape(-1,1,2)
    global homo
    homo, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC,5.0)

if __name__ == "__main__":
    srcPts = np.float32(projectionLimits).reshape(-1,1,2)
    dstPts = np.float32([[0,0], [SCREEN_WIDTH,0], [SCREEN_WIDTH, SCREEN_HEIGHT], [0,SCREEN_HEIGHT]]).reshape(-1,1,2)
    global homo
    homo, mask = cv2.findHomography(srcPts, dstPts, cv2.RANSAC,5.0)

    calculateProjectionCoordinates()
    #if (calibrate()):


    play()
