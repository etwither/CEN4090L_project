import pygame
import os
pygame.font.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0,0,0)
WHITE = (250, 250, 250)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)


FPS = 60
V_VEL = 3
VEL = 5


SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'land.jpg')), (WIDTH, HEIGHT))


INDIANA_WIDTH, INDIANA_HEIGHT = 55, 40
INDIANA_IMAGE = pygame.image.load(os.path.join('Assets', 'lego.jpeg'))
INDIANA = pygame.transform.rotate(pygame.transform.scale(INDIANA_IMAGE, (50,40)), 360)
VILLAIN_IMAGE = pygame.image.load(os.path.join('Assets', 'trooper.jpg'))
VILLAIN1 = pygame.transform.rotate(pygame.transform.scale(VILLAIN_IMAGE, (50, 40)), 360)
VILLAIN2 = pygame.transform.rotate(pygame.transform.scale(VILLAIN_IMAGE, (50, 40)), 360)
VILLAIN3 = pygame.transform.rotate(pygame.transform.scale(VILLAIN_IMAGE, (50, 40)), 360)
VILLAIN4 = pygame.transform.rotate(pygame.transform.scale(VILLAIN_IMAGE, (50, 40)), 360)

def handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_w]:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s]:
        yellow.y += VEL
    if keys_pressed[pygame.K_a]:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d]:
        yellow.x += VEL
    if keys_pressed[pygame.K_p]:
        pause_menu(keys_pressed)


def enemy_movement(yellow, v1, V_VEL, yellow_health):
    if v1.x > yellow.x:
        v1.x -= V_VEL
    if v1.x < yellow.x:
        v1.x += V_VEL
    if v1.y > yellow.y:
        v1.y -= V_VEL
    if v1.y < yellow.y:
        v1.y += yellow.y

#def handle_collisions(yellow, v1, yellow_health):
   # if yellow.colliderect(v1):
     #  yellow_health -= 1 

def pause_menu(keys_pressed):
    pause = True
    while pause:
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys_pressed[pygame.K_q]:
                pygame.quit()
            if keys_pressed[pygame.K_e]:
                pause = False
        WIN.fill(WHITE)
        largeText = pygame.font.SysFont('comicsans', 40)
        textP = largeText.render("Pause, press e to resume, q to quit", 1, BLACK)
        WIN.blit(textP, (150, 250))
        pygame.display.update()


def draw_window(yellow, v1, v2, v3, v4, yellow_health):
    WIN.blit(SPACE, (0,0))
    #WIN.fill(BLACK)
    WIN.blit(INDIANA, (yellow.x, yellow.y))
    WIN.blit(VILLAIN1, (v1.x, v1.y))
    WIN.blit(VILLAIN2, (v2.x, v2.y))
    WIN.blit(VILLAIN3, (v3.x, v3.y))
    WIN.blit(VILLAIN4, (v4.x, v4.y))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10) )
    pause_text = HEALTH_FONT.render("Press 'p' to pause", 1, WHITE)
    WIN.blit(pause_text, (150, 365))
    pygame.display.update()

def main():
    yellow = pygame.Rect(100, 300, INDIANA_WIDTH, INDIANA_HEIGHT)
    v1 = pygame.Rect(700, 30, INDIANA_WIDTH, INDIANA_HEIGHT)
    v2 = pygame.Rect(700, 130, INDIANA_WIDTH, INDIANA_HEIGHT)
    v3 = pygame.Rect(700, 230, INDIANA_WIDTH, INDIANA_HEIGHT)
    v4 = pygame.Rect(700, 330, INDIANA_WIDTH, INDIANA_HEIGHT)

    yellow_health = 5
    
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow) 
        enemy_movement(yellow, v1, V_VEL, yellow_health)
        enemy_movement(yellow, v2, V_VEL, yellow_health)
        enemy_movement(yellow, v3, V_VEL, yellow_health)
        enemy_movement(yellow, v4, V_VEL, yellow_health)  
       # handle_collisions(yellow, v1, yellow_health)
           
        draw_window(yellow, v1, v2, v3, v4, yellow_health)
    main()

if __name__ == "__main__":
    main()        