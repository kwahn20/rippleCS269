import pygame

pygame.init()
screen = pygame.display.set_mode((1920, 1080))
done = False
x_pos = 30
y_pos = 30

while not done:
    screen.fill((0, 0, 0))
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_UP]: y_pos -= 3
    if pressed[pygame.K_DOWN]: y_pos += 3
    if pressed[pygame.K_LEFT]: x_pos -= 3
    if pressed[pygame.K_RIGHT]: x_pos += 3

    pygame.draw.rect(screen, (0, 128, 255), pygame.Rect(x_pos, y_pos, 60, 60))

    pygame.display.flip()
