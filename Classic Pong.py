import pygame, sys
from pygame.locals import *

pygame.init()
#speed of the game in frames
FPS = 70
fpsClock = pygame.time.Clock()
#screen dimensions, starting coordinates, center line coordinates
SCREEN_W = 1200
SCREEN_H = 800
SCREEN = pygame.display.set_mode((SCREEN_W, SCREEN_H))
background = pygame.Surface(SCREEN.get_size())
background.fill((0,0,0))
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
init_x = SCREEN_W - 1125
init_y = SCREEN_H - 500
ai_x = SCREEN_W - 75
center_top = [SCREEN_W/2, 0]
center_bottom = [SCREEN_W/2, SCREEN_H]

class Arena():
    def __init__(self):
        self.center_line = pygame.draw.line(SCREEN, BLUE, center_top, center_bottom, 5)       
    
class Paddle():
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('paddle.png')
        self.blit_bg = pygame.image.load('paddle_blit_bg.png')
        self.rect = self.image.get_rect()
        self.blit_coords = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)
        self.x = x
        self.y = y
        self.dy = 0
        self.state = "still"
        self.init_player_pos = (self.x, self.y)
        SCREEN.blit(self.image, self.init_player_pos)
   
    def draw(self):
	#re-draw paddle in new position
        SCREEN.blit(self.image, [self.x, self.y])  
	
    def erase(self):
	#erase the paddle using background
        SCREEN.blit(background, [self.x, self.y], self.blit_coords) 
	
    def moveUp(self):
        self.dy = -10
        #add the change in movement to top of paddle
        self.y += self.dy
        #test if paddle hits top of screen
        if self.y <= 0:
            self.dy = 0
            self.y = 0
         
    def moveDown(self):
        self.dy = 10      
        #add change in movement to top of paddle
        self.y += self.dy        
	#test if paddle hits bottom of screen
        if (self.y + self.rect.height >= SCREEN_H):
            self.dy = 0        
            self.y = SCREEN_H - self.rect.height
	    
    def update(self):
        self.rect.topleft = [self.x, self.y]

class Ball():
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('ball.png')
	#get rectangular coordinates of the ball, as well as width and height
        self.rect = self.image.get_rect()
        self.blit_coords = pygame.Rect(self.rect.left, self.rect.top, self.rect.width, self.rect.height)
        self.x = SCREEN_W - 800
        self.y = SCREEN_H - 450
        self.speed_up = 0.0
        self.dx = -4
        self.dy = 4
	#initial position of ball
        SCREEN.blit(self.image, [self.x, self.y])

    def draw(self):
	#re-draw the ball at new point
        SCREEN.blit(self.image, [self.x, self.y])        

    def erase(self):
	#erase the ball from old point
        SCREEN.blit(background, [self.x, self.y], self.blit_coords)
	
    def move(self):
        #move ball x and y coordinates
        self.x += self.dx
        self.y += self.dy
        self.rect.topleft = [self.x, self.y]

    def collision(self, paddle1, paddle2):
        if paddle1.rect.colliderect(self.rect) or paddle2.rect.colliderect(self.rect):
            paddle1.draw()
            paddle2.draw()
            self.dx = -1 * self.dx
            #self.dy = -1 * self.dy
        if (self.y + self.rect.height >= SCREEN_H or self.y <= 0):
            self.dy = -1 * self.dy 
        self.x += self.dx + self.speed_up	 
        self.y += self.dy + self.speed_up
	

class Ai(Paddle):
    def moveUp(self):
        self.dy = -6.5
        self.y += self.dy
        #re-draw the paddle in new position
        SCREEN.blit(self.image, [self.x, self.y]) 
        #test if paddle hits top of screen
        if self.y <= 0:
            self.dy = 0
            self.y = 0
    def moveDown(self):
        self.dy = 6.7      
        #add change in movement to top of paddle
        self.y += self.dy         
	#test if paddle hits bottom of screen
        if (self.y + self.rect.height >= SCREEN_H):
            self.dy = 0        
            self.y = SCREEN_H - self.rect.height
	    
    def update(self):
        self.rect.topright = [self.x, self.y]

#create instances of ball and both paddles     
ball = Ball()
player = Paddle(init_x, init_y)
ai = Ai(ai_x, init_y)
  
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit() 

    arena = Arena()
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        player.erase()
        player.moveUp()
        player.draw()
    elif keys[pygame.K_DOWN]:
        player.erase()
        player.moveDown()
        player.draw()
    if ball.x < 600:
        ai.dy = 0
    elif ball.rect.centery < ai.rect.centery:
        ai.erase()
        ai.moveUp()
        ai.draw()
    elif ball.rect.centery > ai.rect.centery:
        ai.erase()
        ai.moveDown()
        ai.draw()
    if ball.x >= SCREEN_W:
        ball.erase()
        ball.x = SCREEN_W - 800
        ball.y = SCREEN_H - 450      
    elif ball.x <= 0:
        ball.erase()
        ball.x = SCREEN_W - 400
        ball.y = SCREEN_H - 450
    elif ball.x >= 0 and ball.x <= SCREEN_W:
        player.update()
        ai.update()	
        ball.erase()
        ball.collision(player, ai)
        ball.move()
        ball.draw()

        


    
    pygame.display.update()   
    fpsClock.tick(FPS)