import pygame

# Create colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

clock = pygame.time.Clock()
size = (255, 255)

width = 20
height = 20
margin = 5

# Create a 2 dimensional array.
grid = []
for row in range(10):
    grid.append([])
    for column in range(10):
        grid[row].append(0)

grid[1][5] = 1

pygame.init()
screen = pygame.display.set_mode(size)

done = False

while not done:
    # event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # User clicks the mouse, get the position
            pos = pygame.mouse.get_pos()
            # Change the x/y screen coordinates to grid coordinates
            column = pos[0] // (width + margin)
            row = pos[1] // (height + margin)

            # Set that location to one
            grid[row][column] = 1
            print("Click ", pos, " Grid coordinates: ", row, column)

    screen.fill(BLACK)

    # Draw the grid
    for row in range(10):
        for col in range(10):
            color = WHITE
            if grid[row][col] == 1:
                color = GREEN

            pygame.draw.rect(screen, color, [
                (margin + width) * col + margin,
                (margin + height) * row + margin,
                width,
                height
            ])

    clock.tick(60)
    pygame.display.flip()


pygame.quit()
quit()



