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

def wait_for_continue(fill_func, continue_func, fill_args, continue_args):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

        keys = pygame.key.get_pressed()
        if keys[K_SPACE]: continue_func(*continue_args)

        fill_func(*fill_args)

screen = pygame.display.set_mode(size = (1000, 563))
background = Background(START_SCREEN)

if(__name__ == '__main__'):
    screen = pygame.display.set_mode(size = (1000, 563))
    background = Background(START_SCREEN)

    # while True:
    #     for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 sys.exit()

    #     show_start_screen(screen, background)

    wait_for_continue(show_start_screen, None, [screen, background], None)