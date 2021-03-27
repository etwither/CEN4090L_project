import pygame as pg
from constants import *
from pacman import *
import random
import time

pg.init()
# We can use this for positioning, velocity, speed etc
vec = pg.math.Vector2

"""
TODO:
    1. Finish up ghost functionality
        1. add ghost picutres
        2. follow tutorial to get AI working
    2. Write param thingy at the top of functions
    3. Adding music
    4. hiscore tracking
OPTIONAL:
    1. Animate moving of the mouth
"""
class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
        self.clock = pg.time.Clock()
        self.gameRunning = True
        self.state = 'intro'
        self.tile_width = LEVEL_WIDTH // COLS
        self.tile_height = LEVEL_HEIGHT // ROWS
        self.walls = []
        self.pellets = []
        self.ghosts = []
        self.ghost_start = []
        self.score = 0
        self.pacman_start = None
        self.load_level()
        self.load_ghosts()
        self.pacman = Pacman(self, vec(self.pacman_start))

    def start(self):
        while self.gameRunning:
            if self.state == 'intro':
                self.intro_events()
                self.intro_update()
                self.intro_draw()
            if self.state =='playing':
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            self.clock.tick(30)
        pg.quit()
        exit()

########################################## HELPER FUNCTION ##############################################

    # TO-DO
    # Add variable to make it able to go to next level and not hardcoded
    def load_level(self):
        self.background = pg.image.load('ex_maze2_2.png').convert_alpha()
        self.background = pg.transform.scale(self.background, (LEVEL_WIDTH, LEVEL_HEIGHT)).convert_alpha()
        with open('ex_maze2.txt', 'r') as file: # reading the walls file
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
                    elif char in ["1", "2", "3", "4"]:
                        #self.ghost_start.append(vec(x, y))
                        self.ghost_start.append([x, y])
    
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

        """ for wall in self.walls:
            pg.draw.rect(self.background, pg.Color('red'), (wall.x * self.tile_width, wall.y * self.tile_height, self.tile_width, self.tile_height)) """

        """ for pellet in self.pellets:
            pg.draw.circle(self.background, pg.Color('orange'), 
            (int(pellet.x * self.tile_width) + self.tile_width // 2 + SPACE//2, int(pellet.y * self.tile_height)) + self.tile_height // 2 + SPACE, 3) """


    # @PARAMS
    #
    #
    #
    def draw_text(self, text, screen, pos, size, color, fontname, wantCentered = False):
        font = pg.font.SysFont(fontname, size)
        message = font.render(text, False, color)
        msg_sz = message.get_size()

        if wantCentered:
            pos[0] = pos[0] - msg_sz[0] // 2 # this is to make our text centered on the screen
            pos[1] = pos[1] - msg_sz[1] // 2 # this is to make our text centered on the screen

        screen.blit(message, pos)

########################################## START SCREEN FUNCTIONS ##########################################

    def intro_events(self):
        for event in pg.event.get(): # holds a list of all the events that has happened since last checked/updated
            if event.type == pg.QUIT: # if we press the "X" close it or else we have to force close
                self.gameRunning = False
            if event.type == pg.KEYDOWN and event.key == pg.K_SPACE: # user presses space bar to start playing pacman
                self.state = 'playing'
            if event.type == pg.KEYDOWN and event.key == pg.K_TAB: # we'll have this to display options/help/about menu
                pass
            if event.type == pg.KEYDOWN and event.key == pg.K_h: # we'll have this to display hiscores
                pass

    def intro_update(self):
        pass

    def intro_draw(self):
        self.screen.fill(BLACK)
        self.draw_text('Push Space to start', self.screen, [SCREENWIDTH//2, SCREENHEIGHT//2], 28, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Push 'H' to view hiscores!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.8], 28, pg.Color("red"), pg.font.get_default_font(), True)
        self.draw_text("Push TAB for help!", self.screen, [SCREENWIDTH//2, SCREENHEIGHT//1.65], 28, pg.Color("red"), pg.font.get_default_font(), True)
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

    def playing_update(self):
        self.pacman.update()
        for ghost in self.ghosts:
            ghost.draw()
            ghost.update()

        for ghost in self.ghosts:
            if ghost.grid_pos == self.pacman.grid_pos:
                self.pacman.lives -= 1
                if self.pacman.lives == 0:
                    self.state == "over"
                else:

                    # if we hit a ghost, reset the pacman position to the "Start"
                    self.pacman.grid_pos = vec(self.pacman.start_pos)
                    self.pacman.pixel_pos = self.pacman.get_pixel_pos()
                    self.pacman.direction *= 0 # so when they reset, we dont glitch through walls

                    # when we reset pacman, we also want to reset ghost position too
                    for ghost in self.ghosts:
                        ghost.grid_pos = vec(ghost.start_pos)
                        ghost.pixel_pos = ghost.getPixelPos()
                        ghost.direction *= 0 



    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.background, (SPACE // 2, SPACE // 2)) # drawing maze picture to the screen
        #self.draw_grid()
        self.draw_pellets()
        self.draw_text("CURRENT SCORE: {}".format(self.pacman.currScore), self.screen, [30, 8], 22, pg.Color("white"), pg.font.get_default_font(), False)
        self.draw_text("HIGH SCORE: 0", self.screen, [SCREENWIDTH//2, 8], 22, pg.Color("white"), pg.font.get_default_font(), False)
        self.pacman.draw()
        for ghost in self.ghosts:
            ghost.draw()
        pg.display.update()
