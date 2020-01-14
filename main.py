import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pygame.display.flip()
