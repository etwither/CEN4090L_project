import pygame
import os
import math
import time
import random
import copy

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
        self.maxhp = health
        self.img = img
        self.currenthp = 100
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
    def __init__(self, name, power, img):
        self.name = name
        self.power = power
        self.img = img

moveList = [Move('Fire Blast', 1, "fireblast.png"), Move('Volcano', 2, "volcano.png"), Move('Flame On', 1.5, "flameon.png"),
                         Move('Leafblower', 1,"fireblast.png"), Move('Leaf Blade', 2, "fireblast.png"), Move('Grass Dance', 1.5, "fireblast.png"),
                         Move('Water Fountain', 1, "fireblast.png"), Move('Water Cannon', 2, "fireblast.png"), Move('Wave', 1.5, "fireblast.png")]

pokemonlist = [Pokemon('Copper', 'Fire', [moveList[0], moveList[1], moveList[2]], 5, 5, 100, "copper.png"),
                            Pokemon('Diddydoo', 'Grass', [moveList[3], moveList[4], moveList[5]], 5, 5, 100, "diddydoo.png"),
                            Pokemon('Aquafinna', 'Water', [moveList[6], moveList[7], moveList[8]], 5, 5, 100, "aquafinna.png")]

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
        self.battledpokemon = []
        pygame.display.set_caption("Pokemon Test")

    def click(self, x, y, w, h):
        mousePos = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        if x + w > mousePos[0] > x and y + h > mousePos[1] > y:
            if click[0] == 1:
                return True
        return False

    def movement(self, keypress, player, character):
        if keypress[pygame.K_a] and player.x - VEL > 0:
            player.x -= VEL
            self.img = "trainerleft.png"
            pygame.display.update()
        if keypress[pygame.K_d] and player.x + VEL < 1220:# right
            player.x += VEL
            self.img = "trainerright.png"
            pygame.display.update()
        if keypress[pygame.K_w] and player.y - VEL > 0: # up
            player.y -= VEL
            self.img = "trainerback.png"
            pygame.display.update()
        if keypress[pygame.K_s]:  # down
            player.y += VEL
            self.img = "trainerfront.png"
            pygame.display.update()

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

    def iseffective(self, player, cpu):
        if player.type == 'Fire' and cpu.type == 'Grass':
            return True
        if player.type == 'Grass' and cpu.type == 'Water':
            return True
        if player.type == 'Water' and cpu.type == 'Fire':
            return True
        return False

    def isweak(self, player, cpu):
        if player.type == 'Grass' and cpu.type == 'Fire':
            return True
        if player.type == 'Water' and cpu.type == 'Grass':
            return True
        if player.type == 'Fire' and cpu.type == 'Water':
            return True
        return False

    def fainted(self, pokemon):
        if (pokemon.currenthp <= 0):
            return True
        else:
            return False

    def textrender(self, result, font):
        result = font.render(result, True, (255, 255, 255))
        self.screen.blit(result, (600, 400))
        pygame.display.update()

    def battlebackground(self):
        self.screen.fill(0)
        title = pygame.image.load(os.path.join('Assets', 'battletest1.png'))
        self.screen.blit(title, (0, 0))

    def battlegenerator(self, player):
        if self.map[math.floor(player.y / 64)][math.floor(player.x / 64)] == "G":
            if pygame.KEYDOWN and random.random() <= 0.005: #check later to see if can fix
                run2 = True
                ecsound = pygame.mixer.Sound('Assets/PokemonBattle.mp3')
                ecsound.set_volume(0.02)
                ecsound.play()
                fade = pygame.Surface((self.height, self.width))
                fade.fill((0,0,0))
                playerp = copy.deepcopy(pokemonlist[0]) #self.pokemoncurrent[0]
                cpup = copy.deepcopy(pokemonlist[random.randint(0, 2)]) #make sure to change to 5 after all pokemon are in
                for a in range(0, 300):
                    fade.set_alpha(a)
                    self.screen.blit(fade,(0, 0))
                    pygame.display.update()
                    pygame.time.delay(3)
                while run2:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            ecsound.stop()
                            run2 = False
                    self.screen.fill(0)
                    title = pygame.image.load(os.path.join('Assets', 'battletest1.png'))
                    self.screen.blit(title, (0, 0))

                    #player and cpu names, move picture rendering
                    font = pygame.font.Font(None, 24)
                    str1 = font.render(playerp.name, True, (0, 0, 0))
                    str2 = font.render(cpup.name, True, (0, 0, 0))
                    self.screen.blit(str1, (50, 300))
                    self.screen.blit(str2, (1150, 50))

                    move1 = pygame.image.load(os.path.join('Assets', playerp.moves[0].img))
                    self.screen.blit(move1, (1100, 400))
                    move2 = pygame.image.load(os.path.join('Assets', playerp.moves[1].img))
                    self.screen.blit(move2, (1100, 460))
                    move3 = pygame.image.load(os.path.join('Assets', playerp.moves[2].img))
                    self.screen.blit(move3, (1100, 520))

                    #all other rendering for screen besides background
                    php = str(playerp.currenthp) + "/" + str(playerp.maxhp)
                    chp = str(cpup.currenthp) + "/" + str(cpup.maxhp)
                    playerHP = font.render(php, True, (0, 0, 0))
                    cpuHP = font.render(chp, True, (0, 0, 0))
                    self.screen.blit(playerHP, (50, 330))
                    self.screen.blit(cpuHP, (1150, 80))

                    pokemonplayerimg = pygame.image.load(os.path.join('Assets', playerp.img))
                    pokemoncpuimg = pygame.image.load(os.path.join('Assets', cpup.img))
                    pokemonplayerimg = pygame.transform.scale(pokemonplayerimg, (250, 250))
                    pokemoncpuimg = pygame.transform.scale(pokemoncpuimg, (250, 250))
                    self.screen.blit(pokemonplayerimg, (200, 400))
                    self.screen.blit(pokemoncpuimg, (900, 70))

                    if self.iseffective(playerp, cpup):
                        multiplier = 2.0
                    elif self.isweak(playerp, cpup):
                        multiplier = 0.5
                    else:
                        multiplier = 1.0

                    if self.click(1100, 400, 100, 50): #attack 1
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = playerp.name + ' used ' + playerp.moves[0].name + ' on ' + cpup.name + '!'
                        self.textrender(result, font)
                        time.sleep(1)
                        cpup.currenthp -= (playerp.moves[0].power * playerp.attack * multiplier)
                        if self.fainted(cpup):
                            self.battlebackground()
                            result = cpup.name + ' has fainted!'
                            self.textrender(result, font)
                            time.sleep(3)
                            run2 = False
                            ecsound.stop()
                        else:
                            cmove = cpup.moves[random.randint(0, 2)]
                            self.battlebackground()
                            result = cpup.name + ' used ' + cmove.name + ' on ' + playerp.name + '!'
                            self.textrender(result, font)
                            time.sleep(1)
                            playerp.currenthp -= (cmove.power * cpup.attack)
                        if self.fainted(playerp):
                            self.battlebackground()
                            result = playerp.name + ' has fainted!'
                            self.textrender(result, font)
                            time.sleep(3)

                    if self.click(1100, 460, 100, 50): #attack 2
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = playerp.name + ' used ' + playerp.moves[1].name + ' on ' + cpup.name + '!'
                        self.textrender(result, font)
                        time.sleep(1)
                        cpup.currenthp -= (playerp.moves[1].power * playerp.attack * multiplier)
                        if self.fainted(cpup):
                            self.battlebackground()
                            result = cpup.name + ' has fainted!'
                            self.textrender(result, font)
                            time.sleep(3)
                            run2 = False
                            ecsound.stop()
                        else:
                            cmove = cpup.moves[random.randint(0, 2)]
                            self.battlebackground()
                            result = cpup.name + ' used ' + cmove.name + ' on ' + playerp.name + '!'
                            self.textrender(result, font)
                            time.sleep(1)
                            playerp.currenthp -= (cmove.power * cpup.attack)
                        if self.fainted(playerp):
                            self.battlebackground()
                            result = playerp.name + ' has fainted!'
                            self.textrender(result, font)
                            time.sleep(3)

                    if self.click(1100, 520, 100, 50): #attack 3
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = playerp.name + ' used ' + playerp.moves[2].name + ' on ' + cpup.name + '!'
                        self.textrender(result, font)
                        time.sleep(1)
                        cpup.currenthp -= (playerp.moves[2].power * playerp.attack * multiplier)
                        if self.fainted(cpup):
                            self.battlebackground()
                            result = cpup.name + ' has fainted!'
                            self.textrender(result, font)
                            time.sleep(3)
                            run2 = False
                            ecsound.stop()
                        else:
                            cmove = cpup.moves[random.randint(0, 2)]
                            self.battlebackground()
                            result = cpup.name + ' used ' + cmove.name + ' on ' + playerp.name + '!'
                            self.textrender(result, font)
                            time.sleep(1)
                            playerp.currenthp -= (cmove.power * cpup.attack)
                        if self.fainted(playerp):
                            self.battlebackground()
                            result = playerp.name + ' has fainted!'
                            self.textrender(result, font)
                            time.sleep(3)


                    pygame.display.update()

            else:
                pygame.time.delay(2)

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
                    character = pygame.transform.scale(pygame.image.load(os.path.join('Assets', self.img)), (CHARW, CHARH))
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
