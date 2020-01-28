from pygame.locals import *
import pygame
import M
import math
import sounds
import astar
import Story

class Player:
    def __init__(self, x, y, speed, tileSize):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.speed = speed
        self.beingChased = False

        # self.images = [pygame.image.load("images/unknownBack.png"), pygame.image.load("images/unknownFront.png"), pygame.image.load("images/unknownLeft.png"), pygame.image.load("images/unknownRight.png")]
        # self.image_rects = [[pygame.Rect(19, 19, 37, 38), pygame.Rect(19, 19, 37, 38)], [pygame.Rect(19, 19, 37, 38), pygame.Rect(19, 19, 37, 38)], [pygame.Rect(14, 13, 35, 38), pygame.Rect(81, 13, 32, 38)], [pygame.Rect(14, 13, 32, 38), pygame.Rect(78, 13, 35, 38)]]
        # self.image_idx = 0
        # self.animation_idx = 0
        # self.frame_count = 0

        # fields for temporary implementation of step sound
        self.which_step = 1
        self.sound_interval = 1

        # self.image = pygame.image.load("Sounds/player.png")

    def play_steps(self):
        if self.sound_interval % 12 == 0:
            if self.which_step % 2 == 1:
                # sounds.step_1_set_1.play()
                # print('played step 1')
                self.which_step += 1
            else:
                # sounds.step_2_set_1.play()
                # print('played step 2')
                self.which_step += 1
        self.sound_interval += 1

    def moveRight(self, tileSize):
        self.x = self.x + self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)

    def moveLeft(self, tileSize):
        self.x = self.x - self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)

    def moveUp(self, tileSize):
        self.y = self.y - self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)

    def moveDown(self, tileSize):
        self.y = self.y + self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)

    def toggleChase(self):
        self.beingChased = not self.beingChased
        if not self.beingChased:
            self.speed /= 1.5
        else:
            self.speed *= 1.5

# for now this is almost the same as the Player class
# keeping them seperate for now just since they might end up being very different
class Guard:
    def __init__(self, x, y, speed, col, row):
        self.x = x
        self.y = y
        self.speed = speed
        self.movedFrom = None
        self.prevTile = [col, row]
        self.previousMove = None
        self.curMove = None

        self.images = [pygame.image.load("images/guardBack.png"), pygame.image.load("images/guardFront.png"), pygame.image.load("images/guardLeft.png"), pygame.image.load("images/guardRight.png")]
        self.image_rects = [[pygame.Rect(19, 19, 37, 38), pygame.Rect(19, 19, 37, 38)], [pygame.Rect(19, 19, 37, 38), pygame.Rect(19, 19, 37, 38)], [pygame.Rect(14, 13, 35, 38), pygame.Rect(81, 13, 32, 38)], [pygame.Rect(14, 13, 32, 38), pygame.Rect(78, 13, 35, 38)]]
        self.image_idx = 0
        self.animation_idx = 0
        self.frame_count = 0
        self.chasePlayer = False

    def moveRight(self):
        self.x = self.x + self.speed
        self.previousMove = self.moveRight
        self.image_idx = 3

    def moveLeft(self):
        self.x = self.x - self.speed
        self.previousMove = self.moveLeft
        self.image_idx = 2

    def moveUp(self):
        self.y = self.y - self.speed
        self.previousMove = self.moveUp
        self.image_idx = 0

    def moveDown(self):
        self.y = self.y + self.speed
        self.previousMove = self.moveDown
        self.image_idx = 1

    def moveBack(self):
        self.previousMove()

    def toggleChase(self):
        self.chasePlayer = not self.chasePlayer
        if not self.chasePlayer:
            self.speed /= 1.5
        else:
            self.speed *= 1.5

    def updatePosition(self, t_x, t_y):
        # self.prevPos = [self.x, self.y]
        # print(t_x, t_y, self.x, self.y)

        if self.x < t_x - self.speed:
            # print("Moved Right")
            self.moveRight()
            if self.x > t_x - self.speed:
                self.x = t_x
                return True
            return False
        elif self.x > t_x + self.speed:
            # print("Moved Left")
            self.moveLeft()
            if self.x < t_x + self.speed:
                self.x = t_x
                return True
            return False

        if self.y < t_y - self.speed:
            # print("Moved Down")
            self.moveDown()
            if self.y > t_y - self.speed:
                self.y = t_y
                return True
            return False
        elif self.y > t_y + self.speed:
            # print("Moved Up")
            self.moveUp()
            if self.y < t_y + self.speed:
                self.y = t_y
                return True
            return False
        else:
            self.y = t_y

class Maze:
    def __init__(self, tileSize, maze):
        self.M = 16*3
        self.N = 16*3
        self.maze = maze
        self.maze = [list(i) for i in zip(*self.maze)]
        # [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        #             [1,0,0,0,0,0,0,0,2,0,0,0,0,0,0,1],
        #             [1,0,0,0,0,1,0,0,2,0,0,1,0,0,0,1],
        #             [1,0,1,1,1,1,0,0,2,0,0,1,0,0,0,1],
        #             [1,0,0,0,2,0,1,1,2,1,1,0,0,0,0,3],
        #             [1,0,1,1,2,1,0,0,2,0,0,0,0,0,0,1],
        #             [1,1,0,0,2,0,1,0,2,0,0,0,0,0,0,1],
        #             [1,0,0,0,2,1,0,0,2,1,1,1,0,0,0,1],
        #             [1,0,1,1,2,1,0,0,1,4,1,0,0,0,0,1],
        #             [1,0,1,5,2,1,0,0,1,0,0,1,0,0,0,1],
        #             [3,0,0,1,2,0,1,0,1,0,0,1,1,1,1,1],
        #             [1,1,1,0,2,0,1,0,0,0,0,0,2,1,1,1],
        #             [1,0,0,0,1,0,0,1,0,0,0,1,2,0,1,1],
        #             [1,0,0,1,5,1,1,1,0,0,0,1,2,0,1,1],
        #             [1,2,2,2,2,2,2,2,2,2,1,0,2,1,1,1],
        #             [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]
        self.tileSize = tileSize
        self.walls = []
        self.litWalls = []
        # self.guards = []
        for i in range(0, self.N):
            for j in range(0, self.M):
                if self.maze[i][j] == 1:
                    self.walls.append(pygame.Rect(i*self.tileSize, j*self.tileSize, self.tileSize, self.tileSize))

    def getTileCoords(self, x, y):
        return (int(y/self.tileSize), int(x/self.tileSize))

    def draw(self, background):
        for i in range(0, len(self.walls)):
            pygame.draw.rect(background, (0, 128, 255), self.walls[i])

class App:
    def collision(self, player, walls):
        for i in range(0, len(walls)):
            if player.colliderect(walls[i]):
                return True
        return False

    def pingAudioLines(self, x, y, color, chase=False):
        t_x, t_y = self.maze.getTileCoords(y, x)

        for dir in self.unitcircle:
            count = 0
            wallCount = 0
            while count < 8:
                count += 1
                try:
                    if self.maze.maze[int(t_x + (dir.x*count))][int(t_y + (dir.y*count))] == 1:
                        self.maze.litWalls.append([int(t_x + (dir.x*count)), int(t_y + (dir.y*count)), color, x, y, chase])
                        wallCount += 1
                        if wallCount == 5:
                            break
                except:
                    break

    def searchForPlayer(self, x, y, p_x, p_y):
        t_x, t_y = self.maze.getTileCoords(y, x)
        p_t_x, p_t_y = self.maze.getTileCoords(p_y, p_x)

        max_tiles = 7
        if self.player.beingChased:
            max_tiles = 14

        for dir in self.unitcircle:
            count = 0
            while count < max_tiles:
                count += 1
                try:
                    if int(t_x + (dir.x*count)) == p_t_x and int(t_y + (dir.y*count)) == p_t_y:
                        return True
                except:
                    break
        return False

    def __init__(self):
        self.GameState = Story.GameState()
        # self.maze1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        #              [1, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 1],
        #              [1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 7],
        #              [1, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1],
        #              [1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1],
        #              [1, 1, 1, 0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 1, 1],
        #              [1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 2, 1],
        #              [1, 0, 0, 1, 1, 2, 2, 2, 2, 2, 2, 1, 0, 1, 2, 1],
        #              [1, 0, 0, 0, 0, 2, 1, 1, 1, 1, 2, 0, 1, 0, 2, 1],
        #              [1, 0, 0, 1, 0, 2, 2, 6, 2, 2, 2, 0, 0, 1, 2, 1],
        #              [1, 0, 0, 0, 1, 1, 1, 5, 1, 0, 0, 0, 1, 0, 2, 1],
        #              [1, 2, 2, 2, 2, 0, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1],
        #              [1, 2, 0, 0, 2, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 3],
        #              [1, 2, 1, 1, 2, 1, 1, 1, 0, 0, 1, 1, 1, 1, 0, 1],
        #              [1, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 4, 1, 1, 1],
        #              [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        self.maze1 = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 9, 9, 9, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 9, 9, 7, 9],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 9],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 9, 7, 9],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 0, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 9, 0, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 9, 0, 9, 1, 1, 1, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 9, 1, 1, 1, 9, 0, 9, 1, 1, 1, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 9, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 2, 9, 1, 1, 1, 9, 9, 9, 1, 1, 1, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 2, 9, 9, 9, 9, 1, 1, 1, 9, 9, 9, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 2, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 6, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 0, 0, 0, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 2, 0, 0, 0, 9, 1, 1, 1, 9, 9, 9, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 2, 0, 0, 0, 9, 9, 9, 9, 1, 1, 1, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 2, 2, 2, 2, 2, 2, 6, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 1, 1, 1, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 5, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 9, 9, 9, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 5, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 0, 0, 0, 2, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 5, 9, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 9, 9, 9, 9, 9, 9, 1, 1, 1],
                     [1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 9, 0, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 9, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 9],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 9, 9, 9, 9],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 9, 9, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 9, 1, 1, 1],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 0, 0, 0, 0, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 9, 9, 9, 1, 1, 1],
                     [1, 1, 1, 9, 2, 0, 0, 0, 0, 0, 0, 0, 0, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 0, 0, 0, 0, 9, 9, 9, 9, 9, 9, 9, 9, 4, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 9, 2, 2, 2, 6, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 9, 9, 9, 9, 2, 9, 9, 2, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 4, 9, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                     [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]


        self._running = True
        self.windowWidth = 1000
        self.windowHeight = 563
        # self.windowWidth = 1920
        # self.windowHeight = 1080
        tileSize = 60/3
        self.maze = Maze(tileSize, self.maze1)
        self.unitcircle = []

        for i in range(-100, 120, 20):
            for j in range(-100, 120, 20):
                if i != 0 and j != 0:
                    self.unitcircle.append(pygame.Vector2(i/100.0, j/100.0))

        self.guards = []
        for row in range(0, len(self.maze.maze)):
            for col in range(0, len(self.maze.maze[row])):
                if self.maze.maze[row][col] == 6:
                    self.maze.maze[row][col] = 2
                    self.guards.append(Guard(tileSize*row + tileSize/4, tileSize*col + tileSize/4, 1, col, row))
                if self.maze.maze[row][col] == 3:
                    self.player = Player(tileSize*row, tileSize*col, 2, 3*tileSize/2)

    def on_init(self):
        pygame.init()
        pygame.mixer.init() # this is for sounds

        self.window = (self.windowWidth,self.windowHeight)
        self.screen = pygame.display.set_mode(self.window)

        self.fog_of_war = pygame.Surface((2000, 2000), pygame.SRCALPHA)
        self.background = pygame.Surface((2000, 2000))
        self.screen.blit(self.background,(0,0))

        pygame.display.flip()

        self._running = True

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self.screen.fill((0,0,0))
        self.background.fill((0,0,0))
        self.fog_of_war.fill((0,0,0))

        pygame.draw.rect(self.background,(0,200,0),self.player.rect)
        pygame.draw.rect(self.fog_of_war,(0,0,0,0),self.player.rect)

        self.maze.draw(self.background)

        for i in range(0, len(self.guards)):
            if self.guards[i].frame_count == 50:
                self.guards[i].animation_idx ^= 1
                self.guards[i].frame_count = 0
            self.guards[i].frame_count += 1
            # print(self.guards[i].frame_count)
            # pygame.draw.rect(self.background, (255, 128, 0), self.guards[i])
            idx = self.guards[i].image_idx
            width = self.guards[i].image_rects[idx][self.guards[i].animation_idx].w
            height = self.guards[i].image_rects[idx][self.guards[i].animation_idx].h
            self.background.blit(self.guards[i].images[idx], (self.guards[i].x-(width/2), self.guards[i].y-(height/2)), self.guards[i].image_rects[idx][self.guards[i].animation_idx])
            self.fog_of_war.blit(self.guards[i].images[idx], (self.guards[i].x-(width/2), self.guards[i].y-(height/2)), self.guards[i].image_rects[idx][self.guards[i].animation_idx])

        # pygame.draw.circle(self.fog_of_war,(0,0,0,0),(self.player.x+22,self.player.y+22),100,0)
        # for i in range(0, len(self.guards)):
        #     # print(self.guards[i].x, self.guards[i].y)
        #     pygame.draw.rect(self.fog_of_war,(0,0,0,0), self.guards[i].rect)

        # print("player:", self.player.x, self.player.y)

        for i in range(len(self.maze.litWalls)):
            x = self.maze.litWalls[i][0]
            y = self.maze.litWalls[i][1]

            if self.maze.maze[x][y] == 1:
                p_x, p_y = self.maze.getTileCoords(self.maze.litWalls[i][4]+22, self.maze.litWalls[i][3]+22)

                max_distance = 5.0
                if self.maze.litWalls[i][5]:
                    max_distance = 7.0

                alpha = 255 - (255 * (max_distance - math.sqrt((p_x-x)**2 + (p_y-y)**2))/3.0)
                alpha = 255 if alpha > 255 else alpha
                alpha = 0 if alpha < 0 else alpha
                if alpha < 225:
                    pygame.draw.rect(self.fog_of_war, (0, 0, 0, alpha), pygame.Rect(x*self.maze.tileSize, y*self.maze.tileSize, self.maze.tileSize, self.maze.tileSize))
                    pygame.draw.rect(self.background, self.maze.litWalls[i][2], pygame.Rect(x*self.maze.tileSize, y*self.maze.tileSize, self.maze.tileSize, self.maze.tileSize))

        # self.fog_of_war.set_colorkey((60,60,60))
        self.background.blit(self.fog_of_war,(0,0))

        # self.screen.blit(pygame.transform.scale(self.background, (self.background.get_width()*2, self.background.get_height()*2)), (-self.player.x + self.window[0]/2, -self.player.y + self.window[1]/2))
        self.screen.blit(self.background, (-self.player.x + self.window[0]/2, -self.player.y + self.window[1]/2))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        for row in range(0, len(self.maze.maze)):
            for col in range(0, len(self.maze.maze[row])):
                if self.maze.maze[row][col] == 6:
                    self.maze.maze[row][col] = 2
                    self.guards.append(Guard(50*row + 50/4, 50*col + 50/4, 1, col, row))
                if self.maze.maze[row][col] == 3:
                    self.player = Player(20*row, 20*col, 10, 30)
                    print(self.player.y)
                    print(self.maze.getTileCoords(self.player.x, self.player.y))

        if self.on_init() == False:
            self._running = False

        pygame.mixer.music.stop()

        self.newChase = False

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            self.maze.litWalls = []

            self.pingAudioLines(self.player.x, self.player.y, (0,0,255), self.player.beingChased)


            for guard in self.guards:
                t_x, t_y = self.maze.getTileCoords(guard.y, guard.x)
                x = t_x * self.maze.tileSize
                y = t_y * self.maze.tileSize

                # print(t_x, t_y, guard.prevTile, self.maze.maze[t_x-1][t_y], self.maze.maze[t_x+1][t_y], self.maze.maze[t_x][t_y-1], self.maze.maze[t_x][t_y+1])

                moved = False
                # print(self.maze.getTileCoords(guard.y, guard.x), guard.x, guard.y)
                # print(self.maze.getTileCoords(self.player.y, self.player.x), self.player.x, self.player.y)

                if not guard.chasePlayer:
                    try:
                        if self.maze.maze[t_x-1][t_y] == 2 and (guard.prevTile[0] != t_x-1 or guard.prevTile[1] != t_y):
                            guard.moveLeft()

                            if self.maze.getTileCoords(guard.y, guard.x)[0] == t_x-1:
                                # guard.x = (t_x-1)*self.maze.tileSize
                                guard.prevTile = [t_x, t_y]
                            moved = True
                    except:
                        pass

                    try:
                        if self.maze.maze[t_x+1][t_y] == 2 and (guard.prevTile[0] != t_x+1 or guard.prevTile[1] != t_y) and not moved:
                            guard.moveRight()
                            if self.maze.getTileCoords(guard.y, guard.x)[0] == t_x+1:
                                # guard.x = (t_x+1)*self.maze.tileSize
                                guard.prevTile = [t_x, t_y]
                            moved = True
                    except:
                        pass

                    try:
                        if self.maze.maze[t_x][t_y-1] == 2 and (guard.prevTile[0] != t_x or guard.prevTile[1] != t_y-1) and not moved:
                            # guard.moveUp()
                            # print(self.maze.getTileCoords(guard.y, guard.x)[1], t_y-1)
                            if self.maze.getTileCoords(guard.y, guard.x)[1] == t_y-1:
                                guard.y = (t_y-1)*self.maze.tileSize
                                guard.prevTile = [t_x, t_y]
                            else:
                                guard.moveUp()
                            moved = True
                    except:
                        pass

                    try:
                        if self.maze.maze[t_x][t_y+1] == 2 and (guard.prevTile[0] != t_x or guard.prevTile[1] != t_y+1) and not moved:
                            guard.moveDown()
                            if self.maze.getTileCoords(guard.y, guard.x)[1] == t_y+1:
                                # guard.y = (t_y+1)*self.maze.tileSize
                                guard.prevTile = [t_x, t_y]
                            moved = True
                    except:
                        pass

                    if not moved:
                        guard.moveBack()

                self.pingAudioLines(guard.x, guard.y, (255,0,0))
                foundPlayer = self.searchForPlayer(guard.x, guard.y, self.player.x, self.player.y)

                if foundPlayer or guard.chasePlayer:
                    p_t_x, p_t_y = self.maze.getTileCoords(self.player.y, self.player.x)
                    path = astar.astar(self.maze.maze, self.maze.getTileCoords(guard.y, guard.x), self.maze.getTileCoords(self.player.y, self.player.x))
                    if not path:
                        continue

                    if not guard.chasePlayer:
                        guard.toggleChase()
                        self.newChase = True

                    if len(path) > 0:
                        if path[0][0] == t_x and path[0][1] == t_y:
                            del path[0]

                    if len(path) > 0:
                        if path[0][0] < t_x and self.maze.maze[t_x-1][t_y] != 1:
                            guard.moveLeft()
                        elif path[0][0] > t_x and self.maze.maze[t_x+1][t_y] != 1:
                            guard.moveRight()
                        elif path[0][1] < t_y and self.maze.maze[t_x][t_y-1] != 1:
                            guard.moveUp()
                        elif path[0][1] > t_y and self.maze.maze[t_x][t_y+1] != 1:
                            guard.moveDown()

            if (keys[K_RIGHT]):
                self.player.moveRight(3*self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveLeft(3*self.maze.tileSize/2)
                elif self.newChase and not self.player.beingChased:
                    self.newChase = False
                    self.player.toggleChase()

            if (keys[K_LEFT]):
                self.player.moveLeft(3*self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveRight(3*self.maze.tileSize/2)
                elif self.newChase and not self.player.beingChased:
                    self.newChase = False
                    self.player.toggleChase()

            if (keys[K_UP]):
                self.player.moveUp(3*self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveDown(3*self.maze.tileSize/2)
                elif self.newChase and not self.player.beingChased:
                    self.newChase = False
                    self.player.toggleChase()

            if (keys[K_DOWN]):
                self.player.moveDown(3*self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveUp(3*self.maze.tileSize/2)
                elif self.newChase and not self.player.beingChased:
                    self.newChase = False
                    self.player.toggleChase()

            coords = self.maze.getTileCoords(self.player.y, self.player.x)
            print(coords)
            # print(len(self.maze.maze))
            # print(len(self.maze.maze[0]))
            #
            # if self.maze.maze[coords[0]][coords[1]] == 7:
            #     self.currentStage = self.GameState.nextLevel()
            #     self.newMaze = self.currentStage.maze
            #     self.maze = Maze(60/3, self.newMaze)
            #     self.on_execute()
            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()

    M.startscreen_wait()
    theApp.on_execute()

'''
average_frame = 1000 / FPS
while True:
    # ...
    average_frame *= 0.9
    average_frame += 0.1 * CLOCK.tick(FPS)
    print(1000 / average_frame)
'''
# bat sonar to ping forward in front of you in a flashlight manner
# other manners of moving, sprinting (move faster, bigger ring), etc.
# detection of hiding spots, etc.
# powerups in relation to story, not necessarily to help escape the maze
