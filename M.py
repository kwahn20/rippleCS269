import pygame
import sys
from pygame.locals import *

START_SCREEN = 'mainscreen.png'

class Background(pygame.sprite.Sprite):
    def __init__(self, file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0,0]

def show_start_screen(screen, background_img):
    screen.fill((0,0,0))
    screen.blit(background_img.image, background_img.rect)
    pygame.display.flip()
    pygame.mixer.music.load('track1.wav')
    pygame.mixer.music.play(-1)

def new_game_clicked():
    leftclick, *rest = pygame.mouse.get_pressed()
    x, y = pygame.mouse.get_pos()

    # 151,389 is top left (of new game button)
    # 254, 441 is bottom right (of new game buttom)
    if leftclick and x in range(151, 254) and y in range(389, 441):
        return True
    else:
        return False

def wait_for_continue(waitscreen_func, waitscreen_args,
    continue_func, continue_args,
    trigger_func, trigger_args):
    waitscreen_func(*waitscreen_args)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        if trigger_func(*trigger_args): continue_func(*continue_args)

screen = pygame.display.set_mode(size = (1000, 563))
background = Background(START_SCREEN)

if(__name__ == '__main__'):
    pass