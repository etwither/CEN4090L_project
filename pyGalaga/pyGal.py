import pygame
pygame.init()

winW = 800
winH = 800
pygame.display.set_caption('pyGalaga')
win = pygame.display.set_mode((winW,winH))

##########################################################################################################
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
        
        #health
        self.health = 3
    
    #removes health when hit
    def hit(self):
        self.health -= 1
        
        
    #removes the player when health is 0
    def clear(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.vel = 0
        self.hitbox = (self.x, self.y, 0, 0)
        self.health = 0
        
    #creates the player
    def draw(self, Win):
        #draws the player
        if self.health > 0:
            pygame.draw.rect(win, (150, 150, 150), (self.x,self.y,self.width,self.height))
            pygame.draw.rect(win, (255, 0, 0), (self.x+2.5,self.y-5,self.width-5,5))
            pygame.draw.rect(win, (255, 0, 0), (self.x+5,self.y-10,self.width-10,5))
            pygame.draw.rect(win, (255, 0, 0), (self.x+7.5,self.y-15,self.width-15,5))
            pygame.draw.rect(win, (0, 0, 175), (self.x-(self.width-22.5),self.y+(self.height-20),(self.width-15)*3,5))
            pygame.draw.rect(win, (0, 0, 175), (self.x-22.5,self.y+5,self.width-25,25))
            pygame.draw.rect(win, (0, 0, 175), (self.x+(self.width+12.5),self.y+5,self.width-25,25))
        
            #creates the hitbox
            self.hitbox = (self.x-24, self.y-18, 83, 55)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

##########################################################################################################
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

##########################################################################################################
class enemy(object):
    def __init__(self,x,y,width,height,vel):
        #position
        self.x = x
        self.y = y
        self.xStart = x
        self.yStart = y
        
        #size
        self.width = width
        self.height = height
        self.wStart = width
        self.hStart = height
        
        #speed
        self.velHor = vel
        self.velVert = 5
        self.vhStart = 10
        self.vvStart = 5
        
        #hitbox
        self.hitbox = (self.x-27, self.y-17, 86, 72)
        
        #health
        self.health = 1
        
    def move(self):
        #moving to the left
        if self.velHor < 0:
            if self.x > self.velHor + 50:
                self.x += self.velHor
                
                if self.velVert < 0:
                    if self.y > self.yStart - 50:
                        self.y += self.velVert
                    else:
                        self.velVert = self.velVert * -1
                        self.y += self.velVert
                        
                else:
                    if self.y < self.yStart + 50:
                        self.y += self.velVert
                    else:
                        self.velVert = self.velVert * -1
                        self.y += self.velVert
            else:
                self.velHor = self.velHor * -1
                self.x += self.velHor  
                       
        #moving to the right
        else:
            if self.x < winW - 75:
                self.x += self.velHor
                
                if self.velVert < 0:
                    if self.y > self.yStart - 50:
                        self.y += self.velVert
                    else:
                        self.velVert = self.velVert * -1
                        self.y += self.velVert
                        
                else:
                    if self.y < self.yStart + 50:
                        self.y += self.velVert
                    else:
                        self.velVert = self.velVert * -1
                        self.y += self.velVert
            else:
                self.velHor = self.velHor * -1
                self.x += self.velHor
                
    #removes health when hit
    def hit(self):
        self.health -= 1
        
    #removes the player when health is 0       
    def clear(self):
        self.x = 0
        self.y = 0
        self.width = 0
        self.height = 0
        self.velHor = 0
        self.velVert = 0
        self.hitbox = (self.x, self.y, 0, 0)
        self.health = 0
        
    def draw(self,win):
        #draws out the enemy
        if self.health > 0:
            pygame.draw.rect(win, (0, 255, 0), (self.x,self.y,self.width,self.height))      #main body
            pygame.draw.rect(win, (0, 255, 0), (self.x+5,self.y-10,self.width-10,5))        #short bar above long bar
            pygame.draw.rect(win, (150, 0, 0), (self.x-25,self.y-5,self.width+50,5))        #long bar above body
            pygame.draw.rect(win, (150, 0, 0), (self.x-25,self.y-15,self.width-20,30))      #cannon attached to long bar
            pygame.draw.rect(win, (150, 0, 0), (self.x+45,self.y-15,self.width-20,30))      #cannon attached to long bar
            pygame.draw.rect(win, (0, 150, 0), (self.x-(self.width-22.5),self.y+(self.height-10),(self.width-15)*3,5))      #long bar in front
            pygame.draw.rect(win, (150, 0, 0), (self.x-22.5,self.y+30,self.width-25,25))    #cannon attached to long bar
            pygame.draw.rect(win, (150, 0, 0), (self.x+(self.width+12.5),self.y+30,self.width-25,25))    #cannon attached to long bar
        
            #hitbox
            self.hitbox = (self.x-27, self.y-17, 86, 72)
            #pygame.draw.rect(win, (255,0,0), self.hitbox,2)

##########################################################################################################
#start screen
def startGame():
    playerTemp = player(250,300,35,35)
    enemyTemp = enemy(540,290,35,35,10)
    start = True

    while start:
        clock.tick(27)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
            
        keys = pygame.key.get_pressed()         
        if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]:
            start = False
            
        win.fill((0,0,0)) 
        title = pygame.font.SysFont('Yackien', 100, True, italic=True).render('PyGalaga', 1, (255,0,0))
        instructions1 = pygame.font.SysFont('comicsans', 60, True).render('Press the shift to start', 1, (255,255,255))
        instructions2 = pygame.font.SysFont('comicsans', 60, True).render('Space to shoot', 1, (255,255,255))
        instructions3 = pygame.font.SysFont('comicsans', 60, True).render('Left and right arrows to move', 1, (255,255,255))
        win.blit(title, (250, 140))  
        win.blit(instructions1, (180, 400))    
        win.blit(instructions2, (240, 510))
        win.blit(instructions3, (110, 455)) 
        playerTemp.draw(win)  
        enemyTemp.draw(win)
        pygame.display.update()

##########################################################################################################   
#updates the player and the enemies        
def redraw():
    win.fill((0,0,0))
    scores = pygame.font.SysFont('comicsans', 30, True).render('Score: ' + str(score), 1, (255,255,255))
    win.blit(scores, (winW-440, winH-775))
    lives = pygame.font.SysFont('comicsans', 30, True).render('Lives:', 1, (255,255,255))
    win.blit(lives, (winW-90, winH-60))
    drawLives()
    player1.draw(win)
    enemy1.draw(win)
    enemy1.move()
    enemy2.draw(win)
    enemy2.move()
    enemy3.draw(win)
    enemy3.move()
    enemy4.draw(win)
    enemy4.move()
    for x in pLaser:
        x.draw(win)
    for x in eLaser:
        x.draw(win)
    pygame.display.update()

def clean():
    if player1.health < 1:
        player1.clear()
    if enemy1.health < 1:
        enemy1.clear()
    if enemy2.health < 1:
        enemy2.clear()
    if enemy3.health < 1:
        enemy3.clear()
    if enemy4.health < 1:
        enemy4.clear()
        
def drawLives():
    if player1.health > 0:
        win.blit(ship, (winW-30, winH-30))
    if player1.health > 1:
        win.blit(ship, (winW-60, winH-30))
    if player1.health > 2:
        win.blit(ship, (winW-90, winH-30))
##########################################################################################################
run = True
intro = True
clock = pygame.time.Clock()

#laser mechanics
pLaser = []
eLaser = []
shoot = 0
elaserCount = 0

#player/enemies
player1 = player(250,600,35,35)
enemy1 = enemy(250,250,35,35,15)
enemy2 = enemy(250,150,35,35,-5)
enemy3 = enemy(250,50,35,35,10)
enemy4 = enemy(250,350,35,35,-10)

#score
score = 0

#player lives
ship = pygame.image.load('ship.PNG')

##########################################################################################################
#main loop for game
startGame()

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
            
    #move the enemy laser and if it leaves the screen delete it
    for lazer in eLaser:
        if lazer.y > 0 and lazer.y < winH:
            lazer.y += lazer.vel
        else:
            eLaser.pop(eLaser.index(lazer))
            
    #enemys fire a laser every 40 loops
    if elaserCount == 40:
        if enemy1.health == 1:
            eLaser.append(laser(enemy1.x+17.5,enemy1.y-10))
        if enemy2.health == 1:
            eLaser.append(laser(enemy2.x+17.5,enemy2.y-10))
        if enemy3.health == 1:
            eLaser.append(laser(enemy3.x+17.5,enemy3.y-10))
        if enemy4.health == 1:
            eLaser.append(laser(enemy4.x+17.5,enemy4.y-10))
        elaserCount = 0
    elaserCount += 1
    
    #enemy laser hit the player
    for lazer in eLaser:
        if lazer.y + lazer.height > player1.hitbox[1] and lazer.y + lazer.height < player1.hitbox[1] + player1.hitbox[3]:
            if lazer.x < player1.hitbox[0] + player1.hitbox[2] and lazer.x > player1.hitbox[0]:
                player1.hit()
                eLaser.pop(eLaser.index(lazer))
    
    #player laser hit an enemy        
    for lazer in pLaser:
        if lazer.y < enemy1.hitbox[1] + enemy1.hitbox[3] and lazer.y > enemy1.hitbox[1]:
            if lazer.x < enemy1.hitbox[0] + enemy1.hitbox[2] and lazer.x > enemy1.hitbox[0]:
                enemy1.hit()
                score = score + 10
                pLaser.pop(pLaser.index(lazer))
        if lazer.y < enemy2.hitbox[1] + enemy2.hitbox[3] and lazer.y > enemy2.hitbox[1]:
            if lazer.x < enemy2.hitbox[0] + enemy2.hitbox[2] and lazer.x > enemy2.hitbox[0]:
                enemy2.hit()
                score = score + 10
                pLaser.pop(pLaser.index(lazer))
        if lazer.y < enemy3.hitbox[1] + enemy3.hitbox[3] and lazer.y > enemy3.hitbox[1]:
            if lazer.x < enemy3.hitbox[0] + enemy3.hitbox[2] and lazer.x > enemy3.hitbox[0]:
                enemy3.hit()
                score = score + 10
                pLaser.pop(pLaser.index(lazer))
        if lazer.y < enemy4.hitbox[1] + enemy4.hitbox[3] and lazer.y > enemy4.hitbox[1]:
            if lazer.x < enemy4.hitbox[0] + enemy4.hitbox[2] and lazer.x > enemy4.hitbox[0]:
                enemy4.hit()
                score = score + 10
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
        
    #removes the enemy or player if their health reaches 0
    clean()
    
    redraw()
    
#quit game
pygame.display.quit()
