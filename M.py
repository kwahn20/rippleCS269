import pygame
import sys
import sounds
import time
from pygame.locals import *
import Story
import main
import pygame_textinput as TextInput

START_SCREEN = 'images/titlescreen.png'
HIGHSCORES = 'images/HighScores.png'
CREDITS = 'images/Credits.png'
GAMEOVER = 'images/GameOver.png'
HOWTO = 'images/HowTo-2.png'
username = ""
PAUSE = "images/GamePause.png"

# some janky code for a Timer object from michael coyne's incredible freshman year project
class Timer(object):
    '''keeps track of time and displays it on screen'''
    def __init__(self, initial_time):
        self._font = pygame.font.SysFont('trebuchet', 50)
        self._initial_time = initial_time
        self._current_time = 0
        self._display_time = 0
        self.display_text = ''
        self.image = self._font.render(self.display_text, True, (255,255,255)) # creates a new surface with text on it
        self.rect = self.image.get_rect()
        self.rect.left = 450
        self.rect.top = 20

    @property
    def current_time(self):
        return self._current_time
    @current_time.setter
    def current_time(self, new_time):
        self._current_time = new_time

    @property
    def initial_time(self):
        return self._initial_time
    @initial_time.setter
    def initial_time(self, new_time):
        self._initial_time = new_time

    @property
    def display_time(self):
        return self._display_time
    @display_time.setter
    def display_time(self, new_time):
        self._display_time = new_time

    def pause(self):
        self.pausedtime = self.display_time

    def resume(self):
        self.reset()
        self.displaytime += self.pausedtime

    def reset(self, new_initial_time):
        '''reset the timer'''
        self.initial_time = new_initial_time

    def update(self, ticks): # ticks is the return value from pygame.time.get_ticks()
        '''update the current time, and set the image to the correct time so it can be drawn on screen'''
        self.current_time = ticks
        self.display_time = self.current_time - self.initial_time # display_time is in milliseconds
        self.translate() # transforms display_time into readable display_text
        self.image = self._font.render(self.display_text, 0, (255,255,255)) #creates a surface object with desired text

    def translate(self):
        '''translate milisecond time to a readable stopwatch-esque time (ex: 2:30, which means 2 mins 30 seconds)'''
        time_in_seconds = self.display_time // 1000 # calculate the time in seconds
        time_in_minutes = str(time_in_seconds // 60) # the minutes to display on the clock
        leftover_seconds = str(time_in_seconds % 60) # the seconds to display on the clock
        if float(leftover_seconds) < 10: leftover_seconds = '0' + leftover_seconds # so the timer looks nice
        self.display_text = time_in_minutes + ' : ' + leftover_seconds # set the display text for the timer


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

def lookfor_exit(events):
    for event in events:
        if event.type == pygame.QUIT:
            sys.exit()

def esc_pressed(app):
    startscreen_wait()
    app.on_execute()

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
    credits_clicked     = make_button_click_trigger(x_range = (690, 813), y_range = (380, 430))
    howTo_clicked       = make_button_click_trigger(x_range = (573, 685), y_range = (380, 430))
    # load the music for the start screen and play on loop
    pygame.mixer.music.stop()
    pygame.mixer.music.load('track1.wav')
    pygame.mixer.music.set_volume(0.95)
    pygame.mixer.music.play(-1)
    show_image(screen, startscreen_background)

    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if new_game_clicked(events): return entername_wait()
        if high_scores_clicked(events): highscores_wait()
        if credits_clicked(events): credits_wait()
        if howTo_clicked(events): howTo_wait()

def entername_wait():
    continue_clicked = make_button_click_trigger(x_range = (332,639), y_range=(390,457))
    textInput = TextInput.TextInput()
    textInput.text_color = (255,255,255)
    hs_background = Background('images/NewHighScore.png')
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        screen.fill((0,0,0))
        screen.blit(hs_background.image, hs_background.rect)
        textInput.update(events)
        screen.blit(textInput.get_surface(), (529, 220))
        if continue_clicked(events):
            global username
            username = textInput.input_string
            return intro1_wait()
        pygame.display.flip()

def intro1_wait():
    continue_clicked = make_button_click_trigger(x_range=(0,1000), y_range=(0,563))
    show_image(screen, Background("images/whereami.png") )
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if continue_clicked(events):
            return intro2_wait()

def intro2_wait():
    continue_clicked = make_button_click_trigger(x_range=(0, 1000), y_range=(0, 563))
    show_image(screen, Background("images/storydoorscene.png"))
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if continue_clicked(events):
            return intro3_wait()

def intro3_wait():
    continue_clicked = make_button_click_trigger(x_range=(0, 1000), y_range=(0, 563))
    show_image(screen, Background("images/Escape.png"))
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if continue_clicked(events):
            return()

def outro1_wait():
    continue_clicked = make_button_click_trigger(x_range=(0, 1000), y_range=(0, 563))
    show_image(screen, Background("images/tunnelLight.png"))
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if continue_clicked(events):
            return outro2_wait()

def outro2_wait():
    continue_clicked = make_button_click_trigger(x_range=(0, 1000), y_range=(0, 563))
    show_image(screen, Background("images/endScene.png"))
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Sounds/win noise.wav')
    pygame.mixer.music.set_volume(0.95)
    pygame.mixer.music.play(-1)
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if continue_clicked(events):
            Story.GameState.currentStage = 0
            return credits_wait()

def highscores_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, highscores_image)
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if back_clicked(events):
            show_image(screen, startscreen_background)
            return()

def credits_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, credits_background)
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if back_clicked(events):
            show_image(screen, startscreen_background)
            return()

def howTo_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, howTo_background)
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if back_clicked(events):
            show_image(screen, startscreen_background)
            return()

def gameover_wait():
    back_clicked = make_button_click_trigger(x_range = (19, 128), y_range = (21, 83))
    show_image(screen, gameover_background)
    pygame.mixer.music.stop()
    pygame.mixer.music.load('Sounds/lose noise.wav')
    pygame.mixer.music.set_volume(0.95)
    pygame.mixer.music.play()
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if back_clicked(events):
            Story.GameState.currentStage = 0
            app = main.App()
            startscreen_wait()
            app.on_execute()


def pause_wait():
    continue_clicked = make_button_click_trigger(x_range = (95, 479), y_range = (390, 495))
    main_clicked = make_button_click_trigger(x_range = (540, 926), y_range = (390, 495))
    show_image(screen, pause_background)
    while True:
        events = pygame.event.get()
        lookfor_exit(events)
        if main_clicked(events):
            Story.GameState.currentStage = 0
            app = main.App()
            startscreen_wait()
            app.on_execute()
        if continue_clicked(events):
            return()


screen = pygame.display.set_mode(size = (1000, 563))

startscreen_background = Background(START_SCREEN)
highscores_image = Background(HIGHSCORES)
credits_background = Background(CREDITS)
gameover_background = Background(GAMEOVER)
howTo_background = Background(HOWTO)
pause_background = Background(PAUSE)


if(__name__ == '__main__'):
    pass
