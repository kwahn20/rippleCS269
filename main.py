import pygame
import sounds
import M
from pygame.locals import *

class Player:
    def __init__(self):
        self.x = 44
        self.y = 44
        self.rect = pygame.Rect(self.x,self.y, 44, 44)
        self.speed = 1

        # fields for temporary implementation of step sound
        self.which_step = 1
        self.sound_interval = 1

    def play_steps(self):
        if self.sound_interval % 12 == 0:
            if self.which_step % 2 == 1:
                sounds.step_1_set_1.play()
                print('played step 1')
                self.which_step += 1
            else:
                sounds.step_2_set_1.play()
                print('played step 2')
                self.which_step += 1
        self.sound_interval += 1

    def moveRight(self):
        self.x = self.x + self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

    def moveLeft(self):
        self.x = self.x - self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

    def moveUp(self):
        self.y = self.y - self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

    def moveDown(self):
        self.y = self.y + self.speed
        self.play_steps()
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

# for now this is almost the same as the Player class
# keeping them seperate for now just since they might end up being very different
class Guard:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(self.x,self.y, 44, 44)
        self.speed = 1

    def moveRight(self):
        self.x = self.x + self.speed
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

    def moveLeft(self):
        self.x = self.x - self.speed
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

    def moveUp(self):
        self.y = self.y - self.speed
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

    def moveDown(self):
        self.y = self.y + self.speed
        self.rect = pygame.Rect(self.x,self.y, 44, 44)

class Maze:
    def __init__(self):
        self.M = 10
        self.N = 13
        self.maze = [ 1,1,1,1,1,1,1,1,1,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,0,0,0,0,0,2,0,1,
                     1,0,0,1,1,1,1,0,0,1,
                     1,0,0,1,0,0,0,0,0,1,
                     1,0,0,1,0,0,0,0,0,1,
                     1,0,0,1,0,0,1,1,1,1,
                     1,0,0,1,0,0,0,0,0,1,
                     1,0,0,1,0,0,0,0,0,1,
                     1,0,0,1,1,1,1,0,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,0,0,0,0,0,0,0,0,1,
                     1,1,1,1,1,1,1,1,1,1,]

        self.walls = []
        self.guards = []
        bx = 0
        by = 0
        for i in range(0, self.M*self.N):
            if self.maze[ bx + (by*self.M) ] == 1:
                self.walls.append(pygame.Rect(bx*44, by*44, 44, 44))
            if self.maze[ bx + (by*self.M) ] == 2:
                self.guards.append(pygame.Rect(bx*44, by*44, 44, 44))
            bx = bx + 1
            if bx > self.M-1:
               bx = 0
               by = by + 1


    def draw(self,screen,background):
       for i in range(0, len(self.walls)):
           pygame.draw.rect(background, (0, 128, 255), self.walls[i])
       for i in range(0, len(self.guards)):
           pygame.draw.rect(background, (255, 128, 0), self.guards[i])

       screen.blit(background,(0, 0))

class App:
    windowWidth = 800
    windowHeight = 600
    player = 0

    def collision(self, player, walls):
        for i in range(0, len(walls)):
            if player.colliderect(walls[i]):
                return True
        return False

    def __init__(self):
        pygame.init()
        pygame.mixer.init() # this is for sounds
        self._running = True
        self.player = Player()
        self.maze = Maze()

    def on_init(self):
        self.window = (800,600)
        self.screen = pygame.display.set_mode(self.window)

        self.fog_of_war = pygame.Surface(self.window)
        self.background = pygame.Surface(self.window)
        self.screen.blit(self.background,(0,0))

        pygame.display.flip()

        self._running = True

    def on_event(self, event):
        if event.type == QUIT:
            self._running = False

    def on_loop(self):
        pass

    def on_render(self):
        self.background.fill((0,0,0))
        pygame.draw.rect(self.background,(255,0,255),self.player.rect)
        self.maze.draw(self.screen, self.background)

        self.fog_of_war.fill((0,0,0))
        pygame.draw.circle(self.fog_of_war,(60,60,60),(self.player.x+22,self.player.y+22),100,0)
        for i in range(0, len(self.maze.guards)):
            pygame.draw.circle(self.fog_of_war,(60,60,60),(self.maze.guards[i].x+22,self.maze.guards[i].y+22),100,0)

        self.fog_of_war.set_colorkey((60,60,60))
        self.screen.blit(self.fog_of_war,(0,0))

        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        # quit the music while the main game is going
        pygame.mixer.music.stop()

        while( self._running ):
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            if (keys[K_RIGHT]):
                self.player.moveRight()
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveLeft()

            if (keys[K_LEFT]):
                self.player.moveLeft()
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveRight()

            if (keys[K_UP]):
                self.player.moveUp()
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveDown()

            if (keys[K_DOWN]):
                self.player.moveDown()
                if self.collision(self.player.rect, self.maze.walls):
                    self.player.moveUp()

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