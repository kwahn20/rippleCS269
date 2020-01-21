from pygame.locals import *
import pygame
import M
import math
import sounds

class Player:
    def __init__(self, x, y, speed, tileSize):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.speed = speed

        # fields for temporary implementation of step sound
        self.which_step = 1
        self.sound_interval = 1

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

# for now this is almost the same as the Player class
# keeping them seperate for now just since they might end up being very different
class Guard:
    def __init__(self, x, y, speed, tileSize, col, row):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.speed = speed
        self.movedFrom = None
        self.prevTile = [col, row]
        self.previousMove = None

    def moveRight(self, tileSize):
        self.x = self.x + self.speed
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.previousMove = self.moveRight

    def moveLeft(self, tileSize):
        self.x = self.x - self.speed
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.previousMove = self.moveLeft

    def moveUp(self, tileSize):
        self.y = self.y - self.speed
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.previousMove = self.moveUp

    def moveDown(self, tileSize):
        self.y = self.y + self.speed
        self.rect = pygame.Rect(self.x,self.y, tileSize, tileSize)
        self.previousMove = self.moveDown

    def moveBack(self, tileSize):
        self.previousMove(tileSize)

    def updatePosition(self, t_x, t_y, tileSize):
        # self.prevPos = [self.x, self.y]
        # print(t_x, t_y, self.x, self.y)

        if self.x < t_x - self.speed:
            # print("Moved Right")
            self.moveRight(tileSize)
            if self.x > t_x - self.speed:
                self.x = t_x
                return True
            return False
        elif self.x > t_x + self.speed:
            # print("Moved Left")
            self.moveLeft(tileSize)
            if self.x < t_x + self.speed:
                self.x = t_x
                return True
            return False

        if self.y < t_y - self.speed:
            # print("Moved Down")
            self.moveDown(tileSize)
            if self.y > t_y - self.speed:
                self.y = t_y
                return True
            return False
        elif self.y > t_y + self.speed:
            # print("Moved Up")
            self.moveUp(tileSize)
            if self.y < t_y + self.speed:
                self.y = t_y
                return True
            return False
        else:
            self.y = t_y

class Maze:
    def __init__(self, tileSize):
        self.M = 16
        self.N = 16
        self.maze = [[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                    [1,1,0,0,0,0,0,0,0,1,0,1,0,0,0,1],
                    [1,0,0,0,0,0,1,0,0,0,0,0,0,0,0,3],
                    [1,0,0,1,1,1,0,1,1,0,0,1,0,0,0,1],
                    [1,0,0,0,0,0,0,0,0,1,0,0,1,0,0,1],
                    [1,1,1,0,0,1,1,0,0,1,0,0,0,1,1,1],
                    [1,0,0,0,0,1,0,1,0,0,1,1,0,0,2,1],
                    [1,0,0,1,1,2,2,2,2,6,2,1,0,1,2,1],
                    [1,0,0,0,0,2,1,1,1,1,2,0,1,0,2,1],
                    [1,0,0,1,0,2,2,2,2,2,2,0,0,1,6,1],
                    [1,0,0,0,1,1,1,5,1,0,0,0,1,0,2,1],
                    [1,2,2,2,2,0,1,1,1,0,0,0,0,1,1,1],
                    [1,2,0,0,2,0,0,0,1,1,0,0,0,0,0,3],
                    [1,2,0,0,2,1,1,1,0,0,1,1,1,1,0,1],
                    [1,2,2,6,2,0,0,0,0,0,0,0,4,1,1,1],
                    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]

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

        self.unitcircle = []
        self.tileSize = tileSize

        for i in range(-100, 125, 25):
            for j in range(-100, 125, 25):
                if i != 0 and j != 0:
                    self.unitcircle.append(pygame.Vector2(i/100.0, j/100.0))

        self.walls = []
        self.litWalls = []
        self.guards = []
        for i in range(0, self.N):
            for j in range(0, self.M):
                if self.maze[i][j] == 1:
                    self.walls.append(pygame.Rect(i*self.tileSize, j*self.tileSize, self.tileSize, self.tileSize))
                # if self.maze[i][j] == 2:
                #     self.guards.append(pygame.Rect(j*self.tileSize, i*self.tileSize, self.tileSize, self.tileSize))

    def getTileCoords(self, x, y):
        return (int(y/self.tileSize), int(x/self.tileSize))

    def pingAudioLines(self, x, y, color):
        t_x, t_y = self.getTileCoords(y, x)

        for dir in self.unitcircle:
            count = 0
            while count < 6:
            # while True:
                count += 1
                try:
                    if self.maze[int(t_x + (dir.x*count))][int(t_y + (dir.y*count))] == 1:
                        self.litWalls.append([int(t_x + (dir.x*count)), int(t_y + (dir.y*count)), color, x, y])
                        break
                except:
                    break

    def draw(self, background):
        for i in range(0, len(self.walls)):
            pygame.draw.rect(background, (0, 128, 255), self.walls[i])
        for i in range(0, len(self.guards)):
            pygame.draw.rect(background, (255, 128, 0), self.guards[i])

class App:
    def collision(self, player, walls):
        for i in range(0, len(walls)):
            if player.colliderect(walls[i]):
                return True
        return False

    def __init__(self):
        self._running = True
        self.windowWidth = 1000
        self.windowHeight = 563
        # self.windowWidth = 1920
        # self.windowHeight = 1080
        tileSize = 50
        self.player = Player(tileSize*2, tileSize*2, 2, tileSize/2)
        self.maze = Maze(tileSize)
        self.guards = []

        for row in range(0, len(self.maze.maze)):
            for col in range(0, len(self.maze.maze[row])):
                if self.maze.maze[row][col] == 6:
                    self.maze.maze[row][col] = 2
                    self.guards.append(Guard(tileSize*row + tileSize/4, tileSize*col + tileSize/4, 1, tileSize/2, col, row))

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

        # pygame.draw.circle(self.fog_of_war,(0,0,0,0),(self.player.x+22,self.player.y+22),100,0)
        for i in range(0, len(self.guards)):
            # print(self.guards[i].x, self.guards[i].y)
            pygame.draw.rect(self.background,(255,0,255),self.guards[i].rect)
            pygame.draw.rect(self.fog_of_war,(0,0,0,0), self.guards[i].rect)

        # print("player:", self.player.x, self.player.y)

        for i in range(len(self.maze.litWalls)):
            x = self.maze.litWalls[i][0]
            y = self.maze.litWalls[i][1]

            if self.maze.maze[x][y] == 1:
                p_x, p_y = self.maze.getTileCoords(self.maze.litWalls[i][4]+22, self.maze.litWalls[i][3]+22)
                alpha = 255 - (255 * (4.0 - math.sqrt((p_x-x)**2 + (p_y-y)**2))/3.0)
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
        if self.on_init() == False:
            self._running = False

        pygame.mixer.music.stop()

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()
            self.maze.litWalls = []

            self.maze.pingAudioLines(self.player.x, self.player.y, (0,0,255))

            for guard in self.guards:
                t_x, t_y = self.maze.getTileCoords(guard.y, guard.x)
                x = t_x * self.maze.tileSize
                y = t_y * self.maze.tileSize

                # print(t_x, t_y, guard.prevTile, self.maze.maze[t_x-1][t_y], self.maze.maze[t_x+1][t_y], self.maze.maze[t_x][t_y-1], self.maze.maze[t_x][t_y+1])

                moved = False

                try:
                    if self.maze.maze[t_x-1][t_y] == 2 and (guard.prevTile[0] != t_x-1 or guard.prevTile[1] != t_y):
                        guard.moveLeft(self.maze.tileSize/2)
                        # reachedTile = guard.updatePosition(x-self.maze.tileSize, y, self.maze.tileSize/2)
                        # if reachedTile:
                        # if guard.x - guard.speed < x:
                        #     guard.x = x
                        if self.maze.getTileCoords(guard.y, guard.x)[0] == t_x-1:
                            guard.prevTile = [t_x, t_y]
                        moved = True
                except:
                    pass

                try:
                    if self.maze.maze[t_x+1][t_y] == 2 and (guard.prevTile[0] != t_x+1 or guard.prevTile[1] != t_y) and not moved:
                        guard.moveRight(self.maze.tileSize/2)
                        # reachedTile = guard.updatePosition(x+self.maze.tileSize, y, self.maze.tileSize/2)
                        # if reachedTile:
                        if self.maze.getTileCoords(guard.y, guard.x)[0] == t_x+1:
                            guard.prevTile = [t_x, t_y]
                        moved = True
                except:
                    pass

                try:
                    if self.maze.maze[t_x][t_y-1] == 2 and (guard.prevTile[0] != t_x or guard.prevTile[1] != t_y-1) and not moved:
                        guard.moveUp(self.maze.tileSize/2)
                        # print(t_x, t_y)
                        # reachedTile = guard.updatePosition(x, y-self.maze.tileSize, self.maze.tileSize/2)
                        # if reachedTile:
                        if self.maze.getTileCoords(guard.y, guard.x)[1] == t_y-1:
                            guard.prevTile = [t_x, t_y]
                        moved = True
                except:
                    pass

                try:
                    if self.maze.maze[t_x][t_y+1] == 2 and (guard.prevTile[0] != t_x or guard.prevTile[1] != t_y+1) and not moved:
                        guard.moveDown(self.maze.tileSize/2)
                        # print("test")
                        # reachedTile = guard.updatePosition(x, y+self.maze.tileSize, self.maze.tileSize/2)
                        # if reachedTile:
                        if self.maze.getTileCoords(guard.y, guard.x)[1] == t_y+1:
                            guard.prevTile = [t_x, t_y]
                        moved = True
                        # guard.prevTile = [t_x, t_y+1]
                except:
                    pass

                if not moved:
                    guard.moveBack(self.maze.tileSize/2)

                self.maze.pingAudioLines(guard.x, guard.y, (255,0,0))

            if (keys[K_RIGHT]):
                self.player.moveRight(self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveLeft(self.maze.tileSize/2)

            if (keys[K_LEFT]):
                self.player.moveLeft(self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveRight(self.maze.tileSize/2)

            if (keys[K_UP]):
                self.player.moveUp(self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveDown(self.maze.tileSize/2)

            if (keys[K_DOWN]):
                self.player.moveDown(self.maze.tileSize/2)
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveUp(self.maze.tileSize/2)

            if (keys[K_ESCAPE]):
                self._running = False

            self.on_loop()
            self.on_render()
        self.on_cleanup()

if __name__ == "__main__" :
    theApp = App()

    M.wait_for_continues(
        waitscreen_func = M.show_start_screen,
        waitscreen_args = [M.screen, M.background],
        function_relationships = [
            (M.new_game_clicked, theApp.on_execute),
            (M.high_scores_clicked, M.show_highscores),
            (M.controls_clicked, M.show_controls),
            (M.tutorial_clicked, M.show_tutorial),
            (M.options_clicked, M.show_options),
            (M.credits_clicked, M.show_credits)
        ]
    )

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
