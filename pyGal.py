import pygame
pygame.init()

winW = 800
winH = 800
pygame.display.set_caption('pyGalaga')
win = pygame.display.set_mode((winW,winH))

run = True

#main loop for game
while run:
	
    #exits if the x button is hit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
            
#quit game
pygame.display.quit()
