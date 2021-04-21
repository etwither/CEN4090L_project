import pygame
import os
import math
import time
import random

FPS = 60
VEL = 2
CHARW = 64
CHARH = 64
# walkLeft = [pygame.image.load(os.path.join('Assets','trdown1.png')), pygame.image.load(os.path.join('Assets', 'trdown2.png')), pygame.image.load(os.path.join('Assets', 'trdown3.png')), pygame.image.load(os.path.join('Assets', 'trdown4.png'))]
# walkCount = 0

class Pokemon:
    def __init__(self, name, type, moves, attack, defense, health, img):
        self.name = name
        self.type = type
        self.moves = moves
        self.attack = attack
        self.defense = defense
        self.health = health
        self.img = img
        # self.direction = 3

class Player:
    def __init__(self, xpos, ypos):
        self.pos = [xpos, ypos]
        self.x = xpos
        self.y = ypos

    def movepos(self, x, y):
        self.pos[0] += x
        self.pos[1] += y

    def renderer(self, screen):
        pygame.draw.rect(screen, 0, (self.pos[0]*CHARW, self.pos[1]*CHARH, CHARW, CHARH), CHARW)

class Move:
    def __init__(self, name, power):
        self.name = name
        self.power = power

moveList = [Move('Fire Blast', 5), Move('Volcano', 10), Move('Flame On', 7),
                         Move('Leafblower', 5), Move('Leaf Blade', 10), Move('Grass Dance', 7),
                         Move('Water Fountain', 5), Move('Water Cannon', 10), Move('Wave', 7)]

pokemonlist = [Pokemon('Copper', 'Fire', [moveList[0], moveList[1], moveList[2]], 5, 5, 100, ""),
                            Pokemon('Diddydoo', 'Grass', [moveList[3], moveList[4], moveList[5]], 5, 5, 100, ""),
                            Pokemon('Aquaboy', 'Water', [moveList[6], moveList[7], moveList[8]], 5, 5, 100, "")]

class PokemonGame:

    def __init__(self):
        pygame.init()
        # self.colors = {"Screen", (90, 180, 255)}
        self.clock = pygame.time.Clock()
        self.height = 1280
        self.width = 720
        self.screen = pygame.display.set_mode((self.height, self.width))
        self.direction = 3
        self.img = "trainerfront.png"
        self.map = []
        self.pokemoncurrent = []
        pygame.display.set_caption("Pokemon Test")

    def click(self, x, y, w, h):
        mousePos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mousePos[0] > x and y + h > mousePos[1] > y:
            if click[0] == 1:
                return True
        return False

    # def water(self, x=0, y=0):
    #     for w in self.map:
    #         print()

    def movement(self, keypress, player, character):
        if keypress[pygame.K_a] and player.x - VEL > 0:
            # if self.map[math.floor(player.y/64)][math.floor(player.x/64)] != "W": # left
            player.x -= VEL
            # self.direction = 2
            self.img = "trainerleft.png"
            # player.updatepos(-1, 0)
            pygame.display.update()
        if keypress[pygame.K_d] and player.x + VEL < 1220:# right
            # if self.map[math.floor(player.y / 64)][math.floor(player.x / 64)] != "W":
            player.x += VEL
            # self.direction = 4
            # player.updatepos(1, 0)
            self.img = "trainerright.png"
            pygame.display.update()
        if keypress[pygame.K_w] and player.y - VEL > 0: # up
            # if self.map[math.floor(player.y / 64)][math.floor(player.x / 64)] != "W":
            player.y -= VEL
            # self.direction = 1
            # player.updatepos(0, -1)
            self.img = "trainerback.png"
            pygame.display.update()
        if keypress[pygame.K_s]:  # down
            # if self.map[math.floor(player.y / 64)][math.floor(player.x / 64)] != "W":
            player.y += VEL
            # self.direction = 3
            # player.updatepos(0, 1)
            self.img = "trainerfront.png"
            pygame.display.update()

        # print(math.floor(player.y / 64), " ", math.floor(player.x / 64), "\n")
        # print(self.map[math.floor(player.y/64)][math.floor(player.x/64)])


    def maploader(self, file):
        with open(file) as mapf:
            for l in mapf:
                tiles = []
                for i in range(0, len(l) - 1, 2):
                    tiles.append(l[i])
                self.map.append(tiles)

    def renderer(self):
        ypos = 0
        for line in self.map:
            xpos = 0
            for tile in line:
                image = map_tile_image[tile]
                rect = pygame.Rect(xpos * CHARW, ypos * CHARH, CHARW, CHARH)
                self.screen.blit(image, rect)
                xpos = xpos + 1
            ypos = ypos + 1

    def battlegenerator(self, player):
        if self.map[math.floor(player.y / 64)][math.floor(player.x / 64)] == "G":
            # print(pygame.KEYDOWN)
            if pygame.KEYDOWN and random.random() <= 0.005:
                run2 = True
                while run2:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run2 = False
                    self.screen.fill(0)
                    title = pygame.image.load(os.path.join('Assets', 'battletest.png'))
                    self.screen.blit(title, (0, 0))
                    pygame.display.update()

    def main(self):
        random.seed(time.time())
        run = True
        while run:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.screen.fill(0)
            title = pygame.image.load(os.path.join('Assets', 'title.png'))
            self.screen.blit(title, (0, 0))
            playButton = pygame.image.load(os.path.join('Assets',"playButton.png"))
            quitButton = pygame.image.load(os.path.join('Assets',"quitButton.png"))
            self.screen.blit(playButton, (300, 250))
            self.screen.blit(quitButton, (700, 250))
            pygame.display.update()
            if self.click(300, 250, 200, 80):
                player = Player(50, 50)
                run1 = True
                self.maploader("map1.txt")
                while run1:
                    # print("x: ", player.x, " y: ", player.y, "\n")
                    # print("xpos: ", player.pos[0], " ypos: ", player.pos[1], "\n")
                    self.renderer()
                    self.clock.tick(FPS)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run1, run = False, False
                    # test = pygame.image.load(os.path.join('Assets',"test.png"))
                    # character = pygame.image.load(os.path.join('Assets', self.img))
                    character = pygame.transform.scale(pygame.image.load(os.path.join('Assets', self.img)), (CHARW, CHARH))
                    # self.screen.blit(test, (0, 0))
                    self.screen.blit(character, (player.x, player.y))
                    keypress = pygame.key.get_pressed()
                    self.movement(keypress, player, character)
                    self.battlegenerator(player)
                    pygame.display.update()

            if self.click(700, 250, 200, 80):
                run = False

        pygame.quit()
        exit(0)


map_tile_image = {
    "G": pygame.transform.scale(pygame.image.load("Assets/grass.png"), (CHARW, CHARH)),
    "L": pygame.transform.scale(pygame.image.load("Assets/land.png"), (CHARW, CHARH)),
    "W": pygame.transform.scale(pygame.image.load("Assets/water.png"), (CHARW, CHARH))
}

if __name__ == '__main__':
    game = PokemonGame()
    game.main()
