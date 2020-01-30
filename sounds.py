import pygame
pygame.mixer.init(buffer = 64)

button_press_2 = pygame.mixer.Sound('Sounds/home_screen_button_press_2.wav')

step_1_set_1 = pygame.mixer.Sound('step 1.wav')
step_2_set_1 = pygame.mixer.Sound('step 2.wav')

step_1_set_1.set_volume(0.2)
step_2_set_1.set_volume(0.2)
