import pygame
import sys
import sounds
import time
from pygame.locals import *

START_SCREEN = 'mainscreen.png'

# a class for background images such as the start screen, or any other images
# that we want in the background (like a background for the game or whatnot)
class Background(pygame.sprite.Sprite):
    def __init__(self, file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0,0]

# displays the start screen and starts the music
def show_start_screen(screen, background_img):
    # draw the start screen
    screen.fill((0,0,0))
    screen.blit(background_img.image, background_img.rect)
    pygame.display.flip()

    # load the music for the start screen and play on loop
    pygame.mixer.music.load('track1.wav')
    pygame.mixer.music.play(-1)

def show_highscores():
    print('highscores was clicked')

def show_controls():
    print('controls was clicked')

def show_tutorial():
    print('tutorial clicked')

def show_options():
    print('options clicked')

def show_credits():
    print('credits clicked')

def make_button_click_trigger(x_range, y_range):
    def f():
        leftclick, *rest = pygame.mouse.get_pressed()
        x, y = pygame.mouse.get_pos()
        if leftclick and x in range(*x_range) and y in range(*y_range):
            sounds.button_press_2.play()
            return True
        else:
            return False
    return f

# the ranges define where on the screen the button is
new_game_clicked    = make_button_click_trigger(x_range = (151, 254), y_range = (392, 441))
high_scores_clicked = make_button_click_trigger(x_range = (256, 360), y_range = (392, 441))
controls_clicked    = make_button_click_trigger(x_range = (361, 446), y_range = (392, 441))
tutorial_clicked    = make_button_click_trigger(x_range = (468, 574), y_range = (392, 441))
options_clicked     = make_button_click_trigger(x_range = (574, 678), y_range = (392, 441))
credits_clicked     = make_button_click_trigger(x_range = (681, 801), y_range = (392, 441))

def wait_for_continues(waitscreen_func, waitscreen_args, function_relationships):
    waitscreen_func(*waitscreen_args)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
        for trigger_func, t_args, continue_func, c_args in function_relationships:
            if trigger_func(*t_args): continue_func(*c_args)
        time.sleep(0.1)
        # for debugging:
        print(pygame.mouse.get_pos())

screen = pygame.display.set_mode(size = (1000, 563))
background = Background(START_SCREEN)

if(__name__ == '__main__'):
    pass