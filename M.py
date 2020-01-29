import pygame
import sys
import sounds
import time
from pygame.locals import *

START_SCREEN = 'images/titlescreen.png'
HIGHSCORES = 'images/HighScores.png'
CREDITS = 'images/Credits.png'
GAMEOVER = 'images/GameOver.png'

# a class for background images such as the start screen, or any other images
# that we want in the background (like a background for the game or whatnot)
class Background(pygame.sprite.Sprite):
    def __init__(self, file):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(file)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = [0,0]

def show_image(screen, background_img):
    screen.fill((0,0,0))
    screen.blit(background_img.image, background_img.rect)
    pygame.display.flip()

# make a 'trigger' function for a button located in the given x and y range
def make_button_click_trigger(x_range, y_range):
    def f(events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP:
                x, y = pygame.mouse.get_pos()
                if x in range(*x_range) and y in range(*y_range):
                    sounds.button_press_2.play()
                    return True
        return False
    return f

def startscreen_wait():
    new_game_clicked    = make_button_click_trigger(x_range = (190, 312), y_range = (380, 430))
    high_scores_clicked = make_button_click_trigger(x_range = (442, 570), y_range = (380, 430))
    credits_clicked     = make_button_click_trigger(x_range = (685, 812), y_range = (380, 430))

    # load the music for the start screen and play on loop
    pygame.mixer.music.stop()
    pygame.mixer.music.load('track1.wav')
    pygame.mixer.music.set_volume(0.95)
    pygame.mixer.music.play(-1)
    show_image(screen, startscreen_background)

    while True:

        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: sys.exit()
        if new_game_clicked(events): return()
        if high_scores_clicked(events): highscores_wait()
        if credits_clicked(events): credits_wait()

def highscores_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, highscores_image)
    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: sys.exit()
        if back_clicked(events):
            show_image(screen, startscreen_background)
            return()

def credits_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, credits_background)
    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: sys.exit()
        if back_clicked(events):
            show_image(screen, startscreen_background)
            return()

def gameover_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, gameover_background)
    while True:
        events = pygame.event.get()
        keys = pygame.key.get_pressed()
        if keys[K_ESCAPE]: sys.exit()
        if back_clicked(events):
            startscreen_wait()

screen = pygame.display.set_mode(size = (1000, 563))

startscreen_background = Background(START_SCREEN)
highscores_image = Background(HIGHSCORES)
credits_background = Background(CREDITS)
gameover_background = Background(GAMEOVER)

if(__name__ == '__main__'):
    pass
