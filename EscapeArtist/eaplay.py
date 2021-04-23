import pygame
import os
import random
import time
pygame.font.init()

WIDTH, HEIGHT = 800, 400
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
BLACK = (0,0,0)
WHITE = (250, 250, 250)
BLUE = (0, 0, 128)
LBLUE = (0, 255, 255)
GREEN = (0, 255, 127)
RED = (255, 0, 0)
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)


FPS = 60
HS_FILE = "highscore.txt"

#shooters with health, enemy movement



SPACE = pygame.transform.scale(pygame.image.load(os.path.join('eaAssets', 'land.jpg')), (WIDTH, HEIGHT))


INDIANA_WIDTH, INDIANA_HEIGHT = 55, 40
INDIANA_IMAGE = pygame.image.load(os.path.join('eaAssets', 'spaceship_yellow.png'))

VILLAIN_IMAGE = pygame.image.load(os.path.join('eaAssets', 'spaceship_red.png'))
VILLAIN1 = pygame.transform.rotate(pygame.transform.scale(VILLAIN_IMAGE, (40, 30)), 270)
VILLAIN2 = pygame.transform.rotate(pygame.transform.scale(VILLAIN_IMAGE, (40, 30)), 270)

STAR_IMAGE = pygame.image.load(os.path.join('eaAssets', 'DeathStar2.webp'))
STAR = pygame.transform.rotate(pygame.transform.scale(STAR_IMAGE, (80, 70)), 360)
INDIANA = pygame.transform.rotate(pygame.transform.scale(INDIANA_IMAGE, (50,40)), 90)

def handle_movement(keys_pressed, yellow, VEL):
    if keys_pressed[pygame.K_w] and yellow.y > 0:
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y < HEIGHT - 50:
        yellow.y += VEL
    if keys_pressed[pygame.K_a] and yellow.x > 0:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x < WIDTH - 50:
        yellow.x += VEL
    if keys_pressed[pygame.K_p]:
        pause_menu(keys_pressed, score)

def startMenu():
    menu = True
    while menu:
        
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys_pressed[pygame.K_e]:
                start()
            if keys_pressed[pygame.K_q] or event.type == pygame.QUIT:
                over = False
                pygame.quit()
            if keys_pressed[pygame.K_r]:
                controls()
        WIN.fill(BLUE)
        largeText = pygame.font.SysFont('comicsans', 80)
        smallText = pygame.font.SysFont('comicsans', 40)
        textP = largeText.render("Escape Artist", 1, RED)
        textS = smallText.render("Press 'e' to start, 'r' to see the controls", 1, GREEN)
        textE = smallText.render("press 'q' to quit ", 1, GREEN)
        WIN.blit(textP, (200, 30))
        WIN.blit(textS, (150, 150))
        WIN.blit(textE, (150, 200))
        pygame.display.update()

def controls():
    menu = True
    while menu:
        
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys_pressed[pygame.K_e]:
                startMenu()
            if keys_pressed[pygame.K_q] or event.type == pygame.QUIT:
                over = False
                pygame.quit()
        WIN.fill(BLUE)
        largeText = pygame.font.SysFont('comicsans', 40)
        textP = largeText.render("Controls:", 1, RED)
        textS = largeText.render("Press 'a' to move left, 'd' to move right", 1, GREEN)
        textE = largeText.render("Press 'w' to move up, 's' to move down ", 1, GREEN)
        textR = largeText.render("Get to the deathstar without getting hit", 1, LBLUE)
        textT = largeText.render("Press 'e' to go to homepage", 1, GREEN)
        WIN.blit(textP, (150, 30))
        WIN.blit(textS, (150, 90))
        WIN.blit(textE, (150, 150))
        WIN.blit(textR, (150, 240))
        WIN.blit(textT, (150, 300))
        pygame.display.update()


def start():
    star = pygame.Rect(random.randint(650, 750), random.randint(20, 350), INDIANA_WIDTH + 10, INDIANA_HEIGHT + 10)
    yellow = pygame.Rect(100, 300, INDIANA_WIDTH, INDIANA_HEIGHT)
    v1 = pygame.Rect(700, 30, INDIANA_WIDTH, INDIANA_HEIGHT)
    v2 = pygame.Rect(700, 150, INDIANA_WIDTH, INDIANA_HEIGHT)
    
    
    VEL = 5
    V_VEL = 2.0
    
    yellow_health = 3
    score = 0
    highscore = highScore()


    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        keys_pressed = pygame.key.get_pressed()
        handle_movement(keys_pressed, yellow, VEL) 
        enemy_movement(yellow, v1, V_VEL, yellow_health)
        enemy_movement(yellow, v2, V_VEL, yellow_health)
        collisions(yellow, v1, v2, score, keys_pressed, star, yellow_health, highscore)
        if col(yellow, star) == True:
            score += 1
            if (VEL - V_VEL) <= 2.0:
                VEL += 1  
            V_VEL += 0.2
            yellow = pygame.Rect(100, 300, INDIANA_WIDTH, INDIANA_HEIGHT)
            v1 = pygame.Rect(700, 30, INDIANA_WIDTH, INDIANA_HEIGHT)
            v2 = pygame.Rect(700, 130, INDIANA_WIDTH, INDIANA_HEIGHT)
            star = pygame.Rect(random.randint(630, 730), random.randint(40, 330), INDIANA_WIDTH + 20, INDIANA_HEIGHT + 40)
            handle_movement(keys_pressed, yellow, VEL) 
            enemy_movement(yellow, v1, V_VEL, yellow_health)
            enemy_movement(yellow, v2, V_VEL, yellow_health)


        draw_window(yellow, v1, v2, yellow_health, score, star)

def highScore():
    with open(os.path.join('eaAssets', HS_FILE), 'r+') as f:
        try:
            return int(f.read())
        except:
            return 0


def enemy_movement(yellow, v1, V_VEL, yellow_health):
    if v1.x > yellow.x and v1.x > 0:
        v1.x -= V_VEL
    if v1.x < yellow.x and v1.x < WIDTH - 50:
        v1.x += V_VEL
    if v1.y > yellow.y and v1.y > 0:
        v1.y -= V_VEL
    if v1.y < yellow.y and v1.y < HEIGHT - 50:
        v1.y += yellow.y

def collisions(yellow, v1, v2, score, keys_pressed, star, yellow_health, highscore):
    if yellow.colliderect(v1) or yellow.colliderect(v2):
        gameOver(score, keys_pressed, highscore)

def col(yellow, star):
    if yellow.colliderect(star):
        return True



def gameOver(score, keys_pressed, highscore):
    over = True
    while over:
        
        if score > highscore: 
            with open(os.path.join('eaAssets', HS_FILE), 'w') as f:
                f.write(str(score))  

        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys_pressed[pygame.K_e]:
               startMenu()
            if keys_pressed[pygame.K_q] or event.type == pygame.QUIT:
                over = False
                pygame.quit()

        WIN.fill(BLUE)
        largeText = pygame.font.SysFont('comicsans', 40)
        largerText = pygame.font.SysFont('comicsans', 80)
        textP = largerText.render("Game Over!", 1, RED)
        textR = largeText.render("High Score: " + str(highScore()), 1, LBLUE)
        textS = largeText.render("Your Score was: " + str(score), 1, LBLUE)
        textE = largeText.render("press 'e' to go to home screen and 'q' to quit ", 1, GREEN)
        WIN.blit(textP, (250, 100))
        WIN.blit(textS, (150, 210))
        WIN.blit(textE, (150, 300))
        WIN.blit(textR, (150, 30))
        pygame.display.update()
            


def pause_menu(keys_pressed, score):
    pause = True
    while pause:
        keys_pressed = pygame.key.get_pressed()
        for event in pygame.event.get():
            if keys_pressed[pygame.K_q] or event.type == pygame.QUIT:
                pygame.quit()
            if keys_pressed[pygame.K_e]:
                pause = False
        WIN.fill(BLUE)
        largeText = pygame.font.SysFont('comicsans', 40)
        largerText = pygame.font.SysFont('comicsans', 80)
        textP = largerText.render("Pause Menu", 1, RED)
        textR = largeText.render("Your score: " + str(score), 1, LBLUE)
        textS = largeText.render("press 'e' to resume, 'q' to quit", 1, GREEN)
        WIN.blit(textP, (200, 80))
        WIN.blit(textP, (150, 150))
        WIN.blit(textS, (150, 250))
        pygame.display.update()


def draw_window(yellow, v1, v2, yellow_health, score, star):
    WIN.blit(SPACE, (0,0))
    #WIN.fill(BLACK)
    WIN.blit(INDIANA, (yellow.x, yellow.y))
    WIN.blit(VILLAIN1, (v1.x, v1.y))
    WIN.blit(VILLAIN2, (v2.x, v2.y))
    WIN.blit(STAR, (star.x, star.y))
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)
    WIN.blit(yellow_health_text, (yellow_health_text.get_width() - 100, 10))
    score_text = HEALTH_FONT.render("Score: " + str(score), 1, LBLUE)
    WIN.blit(score_text, (WIDTH - score_text.get_width() - 10, 10) )
    pause_text = HEALTH_FONT.render("Press 'p' to pause", 1, GREEN)
    WIN.blit(pause_text, (150, 365))
    pygame.display.update()

def main():
    startMenu()
    main()

if __name__ == "__main__":
    main()        