import pygame as pg
from constants import *
import random
from pygame.math import Vector2 as vec
import time

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
        #pg.draw.circle(self.game.screen, pg.Color("yellow"), (int(self.pixel_pos[0]), int(self.pixel_pos[1])), self.game.tile_width//2 - 2)
        """pg.draw.circle(self.game.screen, pg.Color('yellow'), 
            (int(self.pixel_pos[0] - 0.5) , int(self.pixel_pos[1] - 0.3)), self.game.tile_width//2) """
        #self.game.screen.blit(self.pacman_img, (int(self.pixel_pos[0]), int(self.pixel_pos[1])))
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
        for wall in self.game.walls:
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



################################## GHOST CLASS #################################################




class Ghost():
    def __init__(self, game, ghostPos, identity):
        self.layout_map = [[0 for x in range(28)] for x in range(30)]
        self.game = game
        self.grid_pos = ghostPos
        self.start_pos = [ghostPos.x, ghostPos.y]
        self.pixel_pos = self.getPixelPos()
        self.direction = vec(0, 0)
        self.identity = identity
        self.target = None
        self.g1_image = pg.image.load("red_ghost.png").convert_alpha()

        self.g2_image = pg.image.load("green_ghost.png").convert_alpha()

        self.g3_image = pg.image.load("blue_ghost.png").convert_alpha()

        self.g4_image = pg.image.load("yellow_ghost.png").convert_alpha()


    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pixel_pos += self.direction
            if self.checkMove():
                self.move()

        # making sure grid position is being updated correctly
        self.grid_pos[0] = (self.pixel_pos[0] - SPACE + self.game.tile_width//2) // self.game.tile_width + 1
        self.grid_pos[1] = (self.pixel_pos[1] - SPACE + self.game.tile_height//2) // self.game.tile_height + 1

    def draw(self):
        if self.identity == 0: # red ghost
            self.g1_image = pg.transform.scale(self.g1_image, (self.game.tile_width, self.game.tile_height)).convert_alpha()
            self.g1_rect = self.g1_image.get_rect()
            self.g1_rect.centerx = int(self.pixel_pos[0])
            self.g1_rect.centery = int(self.pixel_pos[1])
            self.game.screen.blit(self.g1_image, self.g1_rect)
        else:
            pass
        if self.identity == 1: # green ghost
            self.g2_image = pg.transform.scale(self.g2_image, (self.game.tile_width, self.game.tile_height)).convert_alpha()
            self.g2_rect = self.g2_image.get_rect()
            self.g2_rect.centerx = int(self.pixel_pos[0])
            self.g2_rect.centery = int(self.pixel_pos[1])
            self.game.screen.blit(self.g2_image, self.g2_rect)
        else:
            pass
        if self.identity == 2: #blue ghost
            self.g3_image = pg.transform.scale(self.g3_image, (self.game.tile_width, self.game.tile_height)).convert_alpha()
            self.g3_rect = self.g3_image.get_rect()
            self.g3_rect.centerx = int(self.pixel_pos[0])
            self.g3_rect.centery = int(self.pixel_pos[1])
            self.game.screen.blit(self.g3_image, self.g3_rect)
        else:
            pass
        if self.identity == 3:
            self.g4_image = pg.transform.scale(self.g4_image, (self.game.tile_width, self.game.tile_height)).convert_alpha()
            self.g4_rect = self.g4_image.get_rect()
            self.g4_rect.centerx = int(self.pixel_pos[0])
            self.g4_rect.centery = int(self.pixel_pos[1])
            self.game.screen.blit(self.g4_image, self.g4_rect)
        else:
            pass

    def getPixelPos(self):
        return vec((self.grid_pos.x * self.game.tile_width) + SPACE//2 + self.game.tile_width//2, (self.grid_pos.y * self.game.tile_height) + SPACE//2 + self.game.tile_height//2)

    def checkMove(self):
        if self.direction == vec(0,0):
            return True

        if int(self.pixel_pos.x + SPACE//2) % self.game.tile_width == 0: # making it so we're only moving between cells and not in between lines
            if self.direction == vec(1, 0) or self.direction == vec(-1, 0): #want to be moving on X-axis to check x direction
                return True

        if int(self.pixel_pos.y + SPACE//2) % self.game.tile_height == 0:
            if self.direction == (0, 1) or self.direction == vec(0, -1):
                return True
        
        return False

    def move(self):
        if self.identity == 0: #random movement red ghost
            self.direction = self.get_randPos()
        else:
            pass
        if self.identity in [1]: # green
            self.direction = self.get_Path(self.target)
        else:
            pass
        if self.identity in [2]: # red
            self.direction = self.get_Path(self.target)
        else:
            pass
        if self.identity in [3]: # orange (shy one)
            self.direction = self.get_Path(self.target)
        else:
            pass

    def get_randPos(self):
        while True:
            num = random.randint(-2, 1)
            if num == -2:
                x, y = 1, 0
            elif num == -1:
                x, y = 0, 1
            elif num == 0:
                x, y = -1, 0
            else:
                x, y = 0, -1

            # we use this to check that if the position it generates is in a wall, then obv the ghost can't move there
            newDir = vec(self.grid_pos.x + x, self.grid_pos.y + y)
            if newDir not in self.game.walls:
                break

        return vec(x, y)

    def get_Path(self, target):
        new_gridpos = self.get_nextPath(target)
        x = new_gridpos[0] - self.grid_pos[0]
        y = new_gridpos[1] - self.grid_pos[1]
        return vec(x, y)

    def get_nextPath(self, target):
        path = self.get_shortestPath([int(self.grid_pos.x), int(self.grid_pos.y)], [int(target[0]), int(target[1])])
        return path[1]

    def get_shortestPath(self, start, target):
        #layout_map = [[0 for x in range(28)] for x in range(30)] # loop through the map
        for wall in self.game.walls:
            if wall.x < 28 and wall.y < 30: 
                self.layout_map[int(wall.y)][int(wall.x)] = '=' # append walls to the map so we dont count those in the future
        queue = [start]
        path = []
        visited = []
        start_time = time.time()
        while queue:
            end_time = time.time() 
            time_taken = end_time - start_time
            curr_Cell = queue[0]
            queue.remove(queue[0])
            visited.append(curr_Cell) # keep track of the cells we have visited so we dont keep going back to it
            #end_time = time.time()
            if curr_Cell == target:
                break # so if we're at our destination, we park
            else:
                neighbor_Cells = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbor in neighbor_Cells:
                    if neighbor[0] + curr_Cell[0] >= 0 and neighbor[0] + curr_Cell[0] < len(self.layout_map[0]): # making sure we're not off the grid
                        if neighbor[1] + curr_Cell[1] >= 0 and neighbor[1] + curr_Cell[1] < len(self.layout_map):
                            new_gridpos = [neighbor[0] + curr_Cell[0], neighbor[1] + curr_Cell[1]]
                            if new_gridpos not in visited:
                                if self.layout_map[new_gridpos[1]][new_gridpos[0]] != '=': # if its not a wall
                                    queue.append(new_gridpos)
                                    path.append({"curr_Cell": curr_Cell, "new_gridpos": new_gridpos})
        shortest_path = [target]
        while target != start:
            for spot in path:
                if spot["new_gridpos"] == target:
                    target = spot["curr_Cell"]
                    shortest_path.insert(0, spot["curr_Cell"])

        #time_taken = end_time - start_time
        print("====================> PERFORMANCE =========> " + str(time_taken))
        return shortest_path

    
    def set_target(self): # green and blue ghost
        if self.identity == 1 or self.identity == 2:
            return self.game.pacman.grid_pos
        else:
            if self.game.pacman.grid_pos[0] > COLS // 2 and self.game.pacman.grid_pos[1] > ROWS // 2:
                return vec(1, 1)
            if self.game.pacman.grid_pos[0] > COLS // 2 and self.game.pacman.grid_pos[1] < ROWS // 2:
                return vec(1,  ROWS - 2)
            if self.game.pacman.grid_pos[0] < COLS // 2 and self.game.pacman.grid_pos[1] > ROWS // 2:
                return vec(COLS - 2, 1)
            else:
                return vec(COLS - 2, ROWS - 2)





   
    
    


