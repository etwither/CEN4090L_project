import pygame as pg
from constants import *
import random
from pygame.math import Vector2 as vec
import time
from ghost import *

#pacmanimg = pg.image.load("pacman.png")
#pcimgrect = pacmanimg.get_rect()

# part 17
class Pacman:
    def __init__(self, game, pos):
        self.game = game
        #self.grid_pos = pos # grid/tile/cell position
        self.grid_pos = pos
        self.pixel_pos = self.get_pixel_pos()
        self.direction = vec(1, 0)
        self.futureDirection = None
        self.checkDirection = True
        self.currScore = 0
        self.pacman_img = pg.image.load("pacman.png").convert_alpha()
        self.lives_img =  pg.image.load("pacman.png").convert_alpha()
        self.speed = 1.5
        self.lives = 3
        self.start_pos = [pos.x, pos.y]

    def update(self):
        if self.checkDirection:
            self.pixel_pos += self.direction * self.speed
        if self.checkMove():
            if self.futureDirection != None:
                self.direction = self.futureDirection
            self.checkDirection = self.canMove()

        # making sure grid position is being updated correctly
        self.grid_pos[0] = (self.pixel_pos[0] - SPACE + self.game.tile_width//2) // self.game.tile_width + 1
        self.grid_pos[1] = (self.pixel_pos[1] - SPACE + self.game.tile_height//2) // self.game.tile_height + 1

        if self.onPellet():
            self.eatPellet()

    def draw(self):
        self.pacman_img = pg.transform.scale(self.pacman_img, (self.game.tile_width , self.game.tile_height )).convert_alpha()
        self.rect = self.pacman_img.get_rect()
        self.rect.centerx = int(self.pixel_pos[0] - 0.5)
        self.rect.centery = int(self.pixel_pos[1] - 0.3)
        self.game.screen.blit(self.pacman_img, self.rect)

        for x in range(self.lives):
            self.lives_img = pg.transform.scale(self.lives_img, (self.game.tile_width , self.game.tile_height )).convert_alpha()
            self.game.screen.blit(self.lives_img, (25 + 25*x, SCREENHEIGHT - 20))

    def move(self, direction):
        #  IF IT CHANGES DIRECTION, CHANGE ROTATION OF PICTURES
        if direction.x == -1.0 and direction.y == 0.0: # going left
            self.pacman_img = pg.image.load("pacman_L.png")
        if direction.x == 1.0 and direction.y == 0.0: # going right
            self.pacman_img = pg.image.load("pacman.png")
        if direction.x == 0 and direction.y == 1.0: # going down
            self.pacman_img = pg.image.load("pacman_D.png")
        if direction.x == 0 and direction.y == -1.0: #moving on up
            self.pacman_img = pg.image.load("pacman_U.png")
        self.futureDirection = direction

    # move by pixels so we have smooth movement (not jumping around) and we're in each actual cell    
    def get_pixel_pos(self):
        return vec((self.grid_pos[0] * self.game.tile_width) + SPACE//2 + self.game.tile_width//2, (self.grid_pos[1]* self.game.tile_height) + SPACE//2 + self.game.tile_height//2)


    def canMove(self):
        for wall in self.game.walls or self.game.gateWalls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True


    def checkMove(self):
        if self.direction == vec(0,0):
            return True
        if int(self.pixel_pos.x + SPACE//2) % self.game.tile_width == 0: # making it so we're only moving between cells and not in between lines
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0): #want to be moving on X-axis to check x direction
                return True

        if int(self.pixel_pos.y + SPACE//2) % self.game.tile_height == 0:
            if self.direction == (0, 1) or self.direction == vec(0, -1):
                return True


    def onPellet(self):
        for pellet in self.game.pellets:
            if vec(self.grid_pos) == pellet:
                return True
        return False
    
    def eatPellet(self):
        self.game.pellets.remove(self.grid_pos)
        self.currScore += 10








   
    
    


