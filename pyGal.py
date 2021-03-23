import pygame
pygame.init()

winW = 800
winH = 800
pygame.display.set_caption('pyGalaga')
win = pygame.display.set_mode((winW,winH))

#player
class player(object):
    def __init__(self,x,y,width,height):
        #position
        self.x = x
        self.y = y
        
        #size
        self.width = width
        self.height = height
        
        #speed
        self.vel = 10
        
        #hitbox
        self.hitbox = (self.x-24, self.y-18, 83, 55)
        
    #creates the player
    def draw(self, Win):
        #draws the player
        pygame.draw.rect(win, (150, 150, 150), (self.x,self.y,self.width,self.height))
        pygame.draw.rect(win, (255, 0, 0), (self.x+2.5,self.y-5,self.width-5,5))
        pygame.draw.rect(win, (255, 0, 0), (self.x+5,self.y-10,self.width-10,5))
        pygame.draw.rect(win, (255, 0, 0), (self.x+7.5,self.y-15,self.width-15,5))
        pygame.draw.rect(win, (0, 0, 175), (self.x-(self.width-22.5),self.y+(self.height-20),(self.width-15)*3,5))
        pygame.draw.rect(win, (0, 0, 175), (self.x-22.5,self.y+5,self.width-25,25))
        pygame.draw.rect(win, (0, 0, 175), (self.x+(self.width+12.5),self.y+5,self.width-25,25))
        
        #creates the hitbox
        self.hitbox = (self.x-24, self.y-18, 83, 55)
        pygame.draw.rect(win, (255,0,0), self.hitbox,2)
        
#class for the enemy and player lasers        
class laser(object):
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.width = 5
        self.height = 10
        self.vel = 15
    
    def draw(self,win):
        pygame.draw.rect(win, (255, 0, 0), (self.x,self.y,self.width,self.height))

class enemy(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 15
        
    def draw(self,win):
        #draws out the enemy
        pygame.draw.rect(win, (0, 255, 0), (self.x,self.y,self.width,self.height))
        pygame.draw.rect(win, (255, 0, 0), (self.x-25,self.y-5,self.width+50,5))
        pygame.draw.rect(win, (150, 0, 0), (self.x-25,self.y-15,self.width-20,30))
        pygame.draw.rect(win, (150, 0, 0), (self.x+45,self.y-15,self.width-20,30))
        pygame.draw.rect(win, (0, 255, 0), (self.x+5,self.y-10,self.width-10,5))
        pygame.draw.rect(win, (0, 150, 0), (self.x-(self.width-22.5),self.y+(self.height-10),(self.width-15)*3,5))
        pygame.draw.rect(win, (150, 0, 0), (self.x-22.5,self.y+30,self.width-25,25))
        pygame.draw.rect(win, (150, 0, 0), (self.x+(self.width+12.5),self.y+30,self.width-25,25))
        self.hitbox = (self.x-24, self.y-14, 83, 68)
    
#updates the player and the enemies        
def redraw():
    win.fill((0,0,0))
    player1.draw(win)
    enemy1.draw(win)
    for x in pLaser:
        x.draw(win)
    pygame.display.update()



run = True
intro = True
clock = pygame.time.Clock()

#laser mechanics
pLaser = []
shoot = 0

#player/enemies
player1 = player(250,600,35,35)
enemy1 = enemy(250,250,35,35)




#main loop for game
while run:
    clock.tick(27)
	
    #exits if the x button is hit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
            
    if shoot > 0:
        shoot += 1
    if shoot > 7:
        shoot = 0        
    
    #move the player laser and if it leaves the screen delete it
    for lazer in pLaser:
        if lazer.y < winH and lazer.y > 0:
            lazer.y -= lazer.vel
        else:
            pLaser.pop(pLaser.index(lazer))
            
    #gets the key pressed for movment
    keys = pygame.key.get_pressed()
    
    #move left
    if keys[pygame.K_LEFT] and player1.x-20 > player1.vel:
        if keys[pygame.K_DOWN] and player1.y < winH - player1.height - player1.vel:
            player1.y += player1.vel
            player1.x -= player1.vel
        elif keys[pygame.K_UP] and player1.y > 600:
            player1.y -= player1.vel
            player1.x -= player1.vel
        else:
            player1.x -= player1.vel
    
    #move right    
    elif keys[pygame.K_RIGHT] and player1.x < winW - player1.width - player1.vel - 20:
        if keys[pygame.K_DOWN] and player1.y < winH - player1.height - player1.vel:
            player1.y += player1.vel
            player1.x += player1.vel
        elif keys[pygame.K_UP] and player1.y > 600:
            player1.y -= player1.vel
            player1.x += player1.vel
        else:
            player1.x += player1.vel
    
    #move down    
    elif keys[pygame.K_DOWN] and player1.y < winH - player1.height - player1.vel:
        player1.y += player1.vel
    
    #move up
    elif keys[pygame.K_UP] and player1.y > 600:
        player1.y -= player1.vel
        
    #shoot laser
    elif keys[pygame.K_SPACE] and shoot == 0:
        if len(pLaser) < 2:
            pLaser.append(laser(player1.x+17.5,player1.y-10)) 
        shoot = 1
    
    redraw()
    
#quit game
pygame.display.quit()
