import pygame
import os

# Define some colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

pygame.init()

# Create an 800x600 sized screen
screen = pygame.display.set_mode([800, 600])

clock = pygame.time.Clock()

# Before the loop, load the sounds:
click_sound = pygame.mixer.Sound("./sound/laser5.ogg")

# Set positions of graphics
background_position = [0, 0]

# Load and set up graphics
background_image = pygame.image.load("./images/saturn_family1.jpg").convert()
player_image = pygame.image.load("./images/player.png").convert()
player_image.set_colorkey(BLACK)

done = False

while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_sound.play()

    # Copy image to screen:
    screen.blit(background_image, background_position)

    # Get the current mouse position.
    player_position = pygame.mouse.get_pos()
    x = player_position[0]
    y = player_position[1]

    # Copy image to screen:
    screen.blit(player_image, [x, y])
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
quit()
