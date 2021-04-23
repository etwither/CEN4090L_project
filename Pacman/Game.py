import pygame as pg
from constants import *
from pacman import *
import random
import time
from ghost import *
from os import path

pg.init()
# We can use this for positioning, velocity, speed etc
vec = pg.math.Vector2

# to play without ghosts, go to line 222
class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pg.time.Clock()
        self.gameRunning = True
        self.state = 'intro'
        self.tile_width = LEVEL_WIDTH // COLS
        self.tile_height = LEVEL_HEIGHT // ROWS
        self.walls = []
        self.gateWalls = []
        self.pellets = []
        self.ghosts = []
        self.ghost_start = []
        self.score = 0
        self.pacman_start = None
        self.currLevel = 1
        self.load_level(self.currLevel)
        self.load_ghosts()
        self.pacman = Pacman(self, vec(self.pacman_start))
        self.hiscore = 0
        self.load_scores()

    def load_scores(self):
        # load in hiscores
        self.dir = path.dirname(__file__)
        try:
            with open(path.join(self.dir, "hiscores.txt"), 'r+') as f: # create hiscores file if it doesnt exist
                self.hiscore = int(f.read())
        except:
            with open(path.join(self.dir, "hiscores.txt"), 'w') as f: # create hiscores file if it doesnt exist
                self.hiscore = 0

    def start(self):
        while self.gameRunning:
            if self.state == 'intro':
                self.intro_events()
                self.intro_update()
                self.intro_draw()
            elif self.state =='playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == 'over':
                self.over_events()
                self.over_update()
                self.over_draw()
            elif self.state == 'help':
                self.help_events()
                self.help_update()
                self.help_draw()
            else:
                self.gameRunning = False
            self.clock.tick(30)
        pg.quit()
        exit()

########################################## HELPER FUNCTION ##############################################

    # TO-DO
    # Add variable to make it able to go to next level and not hardcoded
    def load_level(self, level):
        self.pellets = []
        #self.walls = []
        if level == 1:
            map_level = "maze1"
        elif level == 2:
            map_level = "maze2"
        else:
            map_level = "maze3"
        self.background = pg.image.load(map_level + ".png").convert_alpha()
        self.background = pg.transform.scale(self.background, (LEVEL_WIDTH, LEVEL_HEIGHT)).convert_alpha()
        
        with open(map_level + ".txt", 'r') as file: # reading the walls file .. 'ex_maze2.txt'
            for y, line in enumerate(file):
                for x, char in enumerate(line):
                    if char == '=':
                        self.walls.append(vec(x, y))
                    elif char == '.':
                        self.pellets.append(vec(x, y))
                    elif char == 'P':
                        #self.pacman_start = vec(x, y)
                        self.pacman_start = [x, y]
                    elif char == 'G':
                        pg.draw.rect(self.background, BLACK, (x * self.tile_width, y * self.tile_height, self.tile_width, self.tile_height))
                        self.gateWalls.append(vec(x, y))
                    elif char in ["1", "2", "3", "4"]:
                        #self.ghost_start.append(vec(x, y))
                        self.ghost_start.append([x, y])
        #print(str(self.walls) + "====" + str(self.walls) )
    
    def load_ghosts(self):
        for identity, ghost in enumerate(self.ghost_start):
            self.ghosts.append(Ghost(self, vec(ghost), identity))


    def draw_pellets(self):
        for pellet in self.pellets:
            pg.draw.circle(self.screen, pg.Color('orange'), 
            (int(pellet.x * self.tile_width) + self.tile_width // 2 + SPACE//2, int(pellet.y * self.tile_height) + self.tile_height // 2 + SPACE//2), 3)


    def draw_grid(self):
        for x in range(SCREENWIDTH//self.tile_width): # for x in range(SCREENWIDTH//(SCREENWIDTH//28)):
            pg.draw.line(self.background, pg.Color("grey"), (x * self.tile_width, 0), (x * self.tile_width, SCREENHEIGHT))

        for y in range(SCREENHEIGHT//self.tile_height):
            pg.draw.line(self.background, pg.Color("grey"), (0, y * self.tile_height), (SCREENWIDTH, y * self.tile_height))

    
    def draw_text(self, text, screen, pos, size, color, fontname, wantCentered = False):
        font = pg.font.SysFont(fontname, size)
        message = font.render(text, False, color)
        msg_sz = message.get_size()

        if wantCentered:
            pos[0] = pos[0] - msg_sz[0] // 2 # this is to make our text centered on the screen
            pos[1] = pos[1] - msg_sz[1] // 2 # this is to make our text centered on the screen

        screen.blit(message, pos)

    def resetPos(self):
        # if we hit a ghost, reset the pacman position to the "Start"
        self.pacman.grid_pos = vec(self.pacman.start_pos)
        self.pacman.pixel_pos = self.pacman.get_pixel_pos()
        self.pacman.direction *= 0 # so when they reset, we dont glitch through walls

        # when we reset pacman, we also want to reset ghost position too
        for ghost in self.ghosts:
            ghost.grid_pos = vec(ghost.start_pos)
            ghost.pixel_pos = ghost.getPixelPos()
            ghost.direction *= 0 

    def newGame(self, resettingLevel = False):
        if resettingLevel:
            self.walls.clear()
            self.load_level(self.currLevel)
            self.resetPos()
            #self.walls = []
        else:
            self.currLevel = 1
            self.pacman.lives = 3
            self.load_level(self.currLevel)
            self.resetPos()
            self.pacman.currScore = 0
            self.state = 'playing'


########################################## START SCREEN FUNCTIONS ##########################################

    def intro_events(self):
        for event in pg.event.get(): # holds a list of all the events that has happened since last checked/updated
            if event.type == pg.QUIT: # if we press the "X" close it or else we have to force close
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: # user presses space bar to start playing pacman
                self.state = 'playing'
            if event.type == pg.KEYDOWN and event.key == pg.K_TAB: # we'll have this to display options/help/about menu
                self.state = 'help'
            if event.type == pg.KEYDOWN and event.key == pg.K_h: # we'll have this to display hiscores
                pass

    def intro_update(self):
        pass

    def intro_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('MacPan by Kajoyrie Purcell', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//3], 32, pg.Color("blue"), pg.font.get_default_font(), True)
        self.draw_text('Push Space to start', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 28, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Push TAB for help!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.65], 28, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("HIGH SCORE: " + str(self.hiscore), self.screen, [30, 8], 22, pg.Color("white"), pg.font.get_default_font(), False)
        pg.display.update()


#################################### IN GAME FUNCTIONS ###############################################

    def playing_events(self):
        for event in pg.event.get(): # holds a list of all the events that has happened since last checked/updated
            if event.type == pg.QUIT: # if we press the "X" close it or else we have to force close
                self.gameRunning = False
            if event.type == pg.KEYDOWN: 
                if event.key == pg.K_LEFT:
                    self.pacman.move(vec(-1, 0))
                if event.key == pg.K_RIGHT:
                    self.pacman.move(vec(1, 0))
                if event.key == pg.K_UP:
                    self.pacman.move(vec(0, -1))
                if event.key == pg.K_DOWN:
                    self.pacman.move(vec(0, 1))
                #if event.key == pg.K_n:
                    #self.currLevel += self.currLevel
                    #self.newGame(True)

    def playing_update(self):
        self.pacman.update()

        if len(self.pellets) == 0: # so we've eaten all the pellets in the current level, we move on to next level
            if self.currLevel == 1:
                self.currLevel = 2
                self.newGame(True)
            elif self.currLevel == 2:
                self.currLevel = 3
                self.newGame(True)
            elif self.currLevel == 3:
                self.state = 'over'
                self.start()
            else:
                pass
        else:
            for ghost in self.ghosts:
                #pass
                # COMMENT OUT THE NEXT 2 LINES TO PLAY THE GAME WITHOUT GHOSTS
                ghost.draw()
                ghost.update()
            for ghost in self.ghosts:
                if ghost.grid_pos == self.pacman.grid_pos: # means we hit a ghost
                    self.pacman.lives -= 1
                    if self.pacman.lives <= 0:
                        self.state = "over"
                        self.start()
                    else:
                        self.resetPos()



    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (SPACE // 2, SPACE // 2)) # drawing maze picture to the screen
        #self.draw_grid()
        self.draw_pellets()
        self.draw_text("CURRENT SCORE: {}".format(self.pacman.currScore), self.screen, [30, 8], 22, pg.Color("white"), pg.font.get_default_font(), False)
        self.draw_text("HIGH SCORE: " + str(self.hiscore), self.screen, [SCREENWIDTH//2, 8], 22, pg.Color("white"), pg.font.get_default_font(), False)
        self.pacman.draw()
        for ghost in self.ghosts:
            ghost.draw()
        pg.display.update()


#################################### GAME OVER FUNCTIONS ###############################################


    def over_events(self):
        for event in pg.event.get(): # holds a list of all the events that has happened since last checked/updated
            if event.type == pg.QUIT: # if we press the "X" close it or else we have to force close  
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.newGame()
                #self.state = 'intro'
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def over_update(self):
        pass

    def over_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("Game is over!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//3], 32, pg.Color("white"), pg.font.get_default_font(), True)
        if self.pacman.currScore > self.hiscore:
            self.draw_text("You earned {} points this session, a new high score!".format(self.pacman.currScore), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 32, pg.Color("white"), pg.font.get_default_font(), True)
            self.hiscore = self.pacman.currScore
            with open(path.join(self.dir, "hiscores.txt"), 'w') as f:
                f.write(str(self.pacman.currScore))
        else:
            self.draw_text("You earned {} points this session!".format(self.pacman.currScore), self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 32, pg.Color("white"), pg.font.get_default_font(), True)
            self.draw_text("HIGH SCORE: " + str(self.hiscore), self.screen, [30, 8], 22, pg.Color("white"), pg.font.get_default_font(), False)

        self.draw_text("Press SPACE to play again Or ESCAPE to quit!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 32, pg.Color("white"), pg.font.get_default_font(), True)
        pg.display.update()


################################# (TAB) HELP SCREEN ##################################################

    def help_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE:
                self.state = 'intro'
                self.start()
            if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
                pg.quit()
                exit()

    def help_update(self):
        pass

    def help_draw(self):
        self.screen.fill(BLACK)
        self.draw_text("Use Up, Down, Left, and Right arrows keys to move!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//3], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Your Hiscore is displayed in the top LEFT hand corner!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2.5], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("To advance levels, you must eat all the pellets (yellow dots) in that map.", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("There are 4 ghosts in total, who may or may not try to eat you, so beware!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("If you lose all 3 lives, you will lose!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.6], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Beat all 3 levels to win the game!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.4], 24, pg.Color("white"), pg.font.get_default_font(), True)
        self.draw_text("Press SPACE to go back or Press ESCAPE to quit", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.2], 24, pg.Color("white"), pg.font.get_default_font(), True)
        pg.display.update()