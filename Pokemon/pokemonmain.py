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
    def __init__(self, name, type, moves, attack, defense, health, img, chp = 100):
        self.name = name
        self.type = type
        self.moves = moves
        self.attack = attack
        self.defense = defense
        self.maxhp = health
        self.img = img
        self.currenthp = chp
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
    def __init__(self, name, power, img, ac = 1.0):
        self.name = name
        self.power = power
        self.img = img
        self.ac = ac

moveList = [Move('Fire Blast', 1, "fireblast.png"), Move('Volcano', 2, "volcano.png", 0.7), Move('Flame On', 1.5, "flameon.png", 0.85),
            Move('Leafblower', 1,"leafblower.png"), Move('Leaf Blade', 2, "leafblade.png", 0.7), Move('Grass Dance', 1.5, "grassdance.png", 0.85),
            Move('Water Fountain', 1, "waterfountain.png"), Move('Water Cannon', 2, "watercannon.png", 0.7), Move('Wave', 1.5, "wave.png", 0.85),
            Move('Steel Strike', 1, "steelstrike.png"), Move('Steel Wing', 2, "steelwing.png", 0.7), Move('Spikes', 1.5, "spikes.png", 0.85),
            Move('Rough Tough', 1, "roughtough.png"), Move('Smash Castle', 2, "smashcastle.png", 0.7), Move('Blast', 1.5, "blast.png", 0.85),
            Move('Spook', 1, "spook.png"), Move('Calamity', 2, "calamity.png", 0.7), Move('Shadow Force', 1.5, "shadowforce.png", 0.85),
            Move('Spark', 1, ""), Move('Electric Fury', 2, "", 0.6), Move('Boom Blast', 1.5, "", 0.8)]

pokemonlist = [Pokemon('Copper', 'Fire', [moveList[0], moveList[1], moveList[2]], 5, 5, 100, "copper.png"),
                Pokemon('Serpentino', 'Grass', [moveList[3], moveList[4], moveList[5]], 5, 5, 100, "diddydoo.png"),
                Pokemon('Aquafinna', 'Water', [moveList[6], moveList[7], moveList[8]], 5, 5, 100, "aquafinna.png"),
                Pokemon('Plat5000', 'Steel', [moveList[9], moveList[10], moveList[11]], 5, 5, 100, "plat5000.png"),
                Pokemon('Rockie', 'Rock', [moveList[12], moveList[13], moveList[14]], 5, 5, 100, "rockie.png"),
                Pokemon('Tsoh G.', 'Ghost', [moveList[15], moveList[16], moveList[17]], 5, 5, 100, "tsohg.png"),
               Pokemon('Gigabirdie', 'Electric', [moveList[18], moveList[19], moveList[20]], 10, 5, 200, "gigabirdie.png", 200)]

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
        self.potioncount = 5
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

    def iseffective(self, player, cpu): #ADD NEW TYPES
        if player.type == 'Fire' and (cpu.type == 'Grass' or cpu.type == 'Steel'):
            print("0")
            return True
        if player.type == 'Grass' and (cpu.type == 'Water' or cpu.type == 'Rock'):
            print("1")
            return True
        if player.type == 'Water' and (cpu.type == 'Fire' or cpu.type == 'Rock'):
            print("2")
            return True
        if player.type == 'Steel' and (cpu.type == 'Grass' or cpu.type == 'Rock'):
            print("3")
            return True
        if player.type == 'Rock' and cpu.type == 'Fire':
            print("4")
            return True
        if player.type == 'Ghost' and cpu.type == 'Ghost':
            print("5")
            return True
        if player.type == 'Electric' and cpu.type == 'Water':
            print("6")
            return True
        return False

    def isweak(self, player, cpu): #ADD NEW TYPES
        if player.type == 'Grass' and (cpu.type == 'Fire' or cpu.type == 'Grass' or cpu.type == 'Steel'):
            return True
        if player.type == 'Water' and (cpu.type == 'Grass' or cpu.type == 'Water'):
            return True
        if player.type == 'Fire' and (cpu.type == 'Water' or cpu.type == 'Fire' or cpu.type == 'Rock'):
            return True
        if player.type == 'Steel' and (cpu.type == 'Fire' or cpu.type == 'Water' or cpu.type == 'Electric' or cpu.type == 'Steel'):
            return True
        if player.type == 'Rock' and cpu.type == 'Steel':
            return True
        if player.type == 'Ghost' and cpu.type == 'Ghost':
            return True
        if player.type == 'Electric' and (cpu.type == 'Electric' or cpu.type == 'Grass'):
            return True
        return False

    def fainted(self, pokemon):
        if (pokemon.currenthp <= 0):
            return True
        else:
            return False

    def textrender(self, result, font, x = 600, y = 400):
        result = font.render(result, True, (255, 255, 255))
        self.screen.blit(result, (x, y))
        pygame.display.update()

    def battlebackground(self):
        self.screen.fill(0)
        title = pygame.image.load(os.path.join('Assets', 'battletest1.png'))
        self.screen.blit(title, (0, 0))

    def chances(self, cpu):
        if cpu.currenthp == 100:
            return 0
        elif cpu.currenthp >= 75:
            return 0.25
        elif cpu.currenthp >= 50:
            return 0.5
        elif cpu.currenthp >= 25:
            return 0.75
        else:
            return 0.9

    def cputurn(self, playerp, cpup, font, cpumult):
        cmove = cpup.moves[random.randint(0, 2)]
        self.battlebackground()
        result = cpup.name + ' used ' + cmove.name + ' on ' + playerp.name + '!'
        self.textrender(result, font)
        time.sleep(1)

        if self.accuracycheck(cmove):
            self.battlebackground()
            result = cpup.name + ' did ' + str(
                cmove.power * cpup.attack * cpumult) + ' damage on ' + playerp.name + '!'
            self.textrender(result, font)
            time.sleep(1)
            playerp.currenthp -= (cmove.power * cpup.attack * cpumult)
        else:
            self.battlebackground()
            result = cpup.name + ' missed!'
            self.textrender(result, font)
            time.sleep(1)

    def cpufaint(self, cpup, font, ecsound):
        self.battlebackground()
        result = cpup.name + ' has fainted!'
        self.textrender(result, font)
        time.sleep(3)
        ecsound.stop()

    def playerfaint(self, playerp, font, ecsound):
        self.battlebackground()
        result = playerp.name + ' has fainted!'
        self.textrender(result, font)
        pygame.time.delay(3000)
        self.pokemoncurrent.pop(0)
        if len(self.pokemoncurrent) == 0:
            self.clock.tick(FPS)
            self.screen.fill(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    quit()
            font = pygame.font.Font(None, 75)
            result = "GAME OVER!"
            self.textrender(result, font)
            ecsound.stop()
            pygame.time.delay(3000)
            quit()

    def accuracycheck(self, move):
        if random.random() < move.ac:
            return True
        else:
            return False


    def battlegenerator(self, player):
        if self.map[math.floor(player.y / 64)][math.floor(player.x / 64)] == "G":
            if pygame.KEYDOWN and random.random() <= 0.005 or len(self.pokemoncurrent) >= 6:
                run2 = True
                final = False
                if len(self.pokemoncurrent) >= 6:
                    final = True
                    self.screen.fill(0)
                    font = pygame.font.Font(None, 50)
                    result = "You have collected six pokemon. Now you must face the final boss!"
                    result = font.render(result, True, (255, 255, 255))
                    self.screen.blit(result, (50, 360))
                    pygame.display.update()
                    for a in self.pokemoncurrent:
                        a.currenthp = 100
                    time.sleep(3)
                ecsound = pygame.mixer.Sound('Assets/PokemonBattle.mp3')
                ecsound.set_volume(0.02)
                ecsound.play()
                fade = pygame.Surface((self.height, self.width))
                fade.fill((0,0,0))
                playerp = self.pokemoncurrent[0]
                playerp.currenthp = 2 #TESTING PURPOSES
                # self.pokemoncurrent.insert(1, copy.deepcopy(pokemonlist[random.randint(0, 2)])) #TESTING ONLY
                if final != True:
                    cpup = copy.deepcopy(pokemonlist[random.randint(0, 5)])
                else:
                    cpup = pokemonlist[6]
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
                    catch = pygame.image.load(os.path.join('Assets', "catch.png"))
                    self.screen.blit(catch, (1100, 580))
                    potion = pygame.image.load(os.path.join('Assets', "potions.png"))
                    if self.potioncount > 0:
                        self.screen.blit(potion, (1100, 640))

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
                    print(cpup.currenthp)

                    if self.iseffective(playerp, cpup):
                        # print("\nplayer super effective")
                        # print(playerp.type)
                        # print(cpup.type)
                        multiplier = 2.0
                    elif self.isweak(playerp, cpup):
                        # print("\nplayer weak effective")
                        # print(playerp.type)
                        # print(cpup.type)
                        multiplier = 0.5
                    else:
                        multiplier = 1.0

                    if self.iseffective(cpup, playerp):
                        cpumult = 2.0
                    elif self.isweak(cpup, playerp):
                        cpumult = 0.5
                    else:
                        cpumult = 1.0

                    if self.click(1100, 400, 100, 50): #attack 1
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = playerp.name + ' used ' + playerp.moves[0].name + ' on ' + cpup.name + '!'
                        self.textrender(result, font)
                        time.sleep(1)
                        if self.accuracycheck(playerp.moves[0]):
                            self.battlebackground()
                            result = playerp.name + ' did ' + str(playerp.moves[0].power * playerp.attack * multiplier) + ' damage on ' + cpup.name + '!'
                            self.textrender(result, font)
                            time.sleep(1)
                            cpup.currenthp -= (playerp.moves[0].power * playerp.attack * multiplier)
                        else:
                            self.battlebackground()
                            result = playerp.name + ' missed!'
                            self.textrender(result, font)
                            time.sleep(1)
                        if self.fainted(cpup):
                            self.cpufaint(cpup, font, ecsound)
                            run2 = False
                        else:
                            self.cputurn(playerp, cpup, font, cpumult)
                        if self.fainted(playerp):
                            run3, run2, run1 = False, False, False
                            self.playerfaint(playerp, font, ecsound)
                            playerp = self.pokemoncurrent[0]

                    if self.click(1100, 460, 100, 50): #attack 2
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = playerp.name + ' used ' + playerp.moves[1].name + ' on ' + cpup.name + '!'
                        self.textrender(result, font)
                        time.sleep(1)
                        if self.accuracycheck(playerp.moves[1]):
                            self.battlebackground()
                            result = playerp.name + ' did ' + str(
                                playerp.moves[1].power * playerp.attack * multiplier) + ' damage on ' + cpup.name + '!'
                            self.textrender(result, font)
                            time.sleep(1)
                            cpup.currenthp -= (playerp.moves[1].power * playerp.attack * multiplier)
                        else:
                            self.battlebackground()
                            result = playerp.name + ' missed!'
                            self.textrender(result, font)
                            time.sleep(1)
                        if self.fainted(cpup):
                            self.cpufaint(cpup, font, ecsound)
                            run2 = False
                        else:
                            self.cputurn(playerp, cpup, font, cpumult)
                        if self.fainted(playerp):
                            run3, run2, run1 = False, False, False
                            self.playerfaint(playerp, font, ecsound)
                            playerp = self.pokemoncurrent[0]

                    if self.click(1100, 520, 100, 50): #attack 3
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = playerp.name + ' used ' + playerp.moves[2].name + ' on ' + cpup.name + '!'
                        self.textrender(result, font)
                        time.sleep(1)
                        if self.accuracycheck(playerp.moves[2]):
                            self.battlebackground()
                            result = playerp.name + ' did ' + str(
                                playerp.moves[2].power * playerp.attack * multiplier) + ' damage on ' + cpup.name + '!'
                            self.textrender(result, font)
                            time.sleep(1)
                            cpup.currenthp -= (playerp.moves[2].power * playerp.attack * multiplier)
                        else:
                            self.battlebackground()
                            result = playerp.name + ' missed!'
                            self.textrender(result, font)
                            time.sleep(1)
                        if self.fainted(cpup):
                            self.cpufaint(cpup, font, ecsound)
                            run2 = False
                        else:
                            self.cputurn(playerp, cpup, font, cpumult)
                        if self.fainted(playerp):
                            run3, run2, run1 = False, False, False
                            self.playerfaint(playerp, font, ecsound)
                            playerp = self.pokemoncurrent[0]

                    if self.click(1100, 580, 100, 50): #Catching
                        self.battlebackground()
                        font = pygame.font.Font(None, 24)
                        result = 'You threw a pokeball!'
                        self.textrender(result, font)
                        time.sleep(3)
                        chance = self.chances(cpup)
                        if random.random() < chance:
                            self.battlebackground()
                            result = 'You caught ' + cpup.name + '!'
                            self.textrender(result, font)
                            self.pokemoncurrent.append(cpup)
                            time.sleep(3)
                            run2 = False
                            ecsound.stop()
                        else:
                            self.battlebackground()
                            result = 'You almost had it!'
                            self.textrender(result, font)
                            time.sleep(1)
                            self.cputurn(playerp, cpup, font, cpumult)
                        if self.fainted(playerp):
                            run3, run2, run1 = False, False, False
                            self.playerfaint(playerp, font, ecsound)
                            playerp = self.pokemoncurrent[0]

                    if self.potioncount > 0: #Healing
                        if self.click(1100, 640, 100, 50):
                            self.battlebackground()
                            font = pygame.font.Font(None, 24)
                            self.potioncount -= 1
                            result = 'You used a potion on ' + playerp.name + '! You have ' + str(self.potioncount) + ' left!'
                            playerp.currenthp = playerp.maxhp
                            self.textrender(result, font)
                            time.sleep(1)
                            self.cputurn(playerp, cpup, font, cpumult)
                        if self.fainted(playerp):
                            run3, run2, run1 = False, False, False
                            self.playerfaint(playerp, font, ecsound)
                            playerp = self.pokemoncurrent[0]

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
                run3 = True
                run1 = True
                while run3:
                    self.clock.tick(FPS)
                    self.screen.fill(0)
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run1, run, run3 = False, False, False
                    firep = pygame.image.load(os.path.join('Assets',"copper.png"))
                    waterp = pygame.image.load(os.path.join('Assets',"aquafinna.png"))
                    grassp = pygame.image.load(os.path.join('Assets',"diddydoo.png"))
                    firep = pygame.transform.scale(firep, (250, 250))
                    waterp = pygame.transform.scale(waterp, (250, 250))
                    grassp = pygame.transform.scale(grassp, (250, 250))
                    self.screen.blit(firep, (200, 400))
                    self.screen.blit(waterp, (500, 400))
                    self.screen.blit(grassp, (800, 400))
                    font = pygame.font.Font(None, 24)
                    p1 = font.render('Copper (Fire)', True, (255, 255, 255))
                    self.screen.blit(p1, (250, 390))
                    p2 = font.render('Aquafinna (Water)', True, (255, 255, 255))
                    self.screen.blit(p2, (550, 390))
                    p3 = font.render('Diddydoo (Grass)', True, (255, 255, 255))
                    self.screen.blit(p3, (850, 390))
                    font1 = pygame.font.Font(None, 75)
                    self.textrender('Choose your starter Pokemon!', font1, 250, 200)
                    if self.click(200, 400, 250, 250):
                        self.pokemoncurrent.insert(0, copy.deepcopy(pokemonlist[0]))
                        run3 = False
                        print("ADDED")
                    if self.click(500, 400, 250, 250):
                        self.pokemoncurrent.insert(0, copy.deepcopy(pokemonlist[2]))
                        run3 = False
                    if self.click(800, 400, 250, 250):
                        self.pokemoncurrent.insert(0, copy.deepcopy(pokemonlist[1]))
                        run3 = False

                player = Player(50, 50)
                self.maploader("map1.txt")
                print("Passed MAP")
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
