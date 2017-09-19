import pygame
import queue

# Create colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Parameters related to grid
ROW = 20
COL = 20
MARGIN = 5
CELL_WIDTH = 20
CELL_HEIGHT = 20
WIDTH = MARGIN * (COL + 1) + CELL_WIDTH * COL
HEIGHT = MARGIN * (ROW + 1) + CELL_HEIGHT * ROW


def create_grid_array(row, col, all_zero=True):
    """
    Create a 2D arrays which represent the grid, initialize with 0
    :param row: row
    :param col: col
    :return: a 2D arrays with row x col
    """
    arrs = []
    for i in range(0, row):
        r = []
        for j in range(0, col):
            if all_zero:
                r.append(0)
            else:
                r.append(j)
        arrs.append(r)
    return arrs


def print_2d_array(arr):
    for i in range(len(arr)):
        for j in range(len(arr[0])):
            print(str(arr[i][j]) + " ", end="")
        print("")


def bfs(matrix, start_x, start_y):
    row = len(matrix)
    col = len(matrix[0])

    x_dir = [0, 0, 1, -1]
    y_dir = [1, -1, 0, 0]

    q = queue.Queue()
    q.put([start_x, start_y])

    while not q.empty():
        cell = q.get()
        matrix[cell[0]][cell[1]] = 1

        for i in range(4):
            x = cell[0] + x_dir[i]
            y = cell[1] + y_dir[i]

            if x in range(0, row) and y in range(0, col) and matrix[x][y] != 1:
                matrix[x][y] = 2
                q.put([x, y])


# Initialize PyGame
pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
grid = create_grid_array(ROW, COL)


done = False

while not None:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill(BLACK)

    for i in range(ROW):
        for j in range(COL):
            color = WHITE
            if grid[i][j] == 1:
                color = RED

            pygame.draw.rect(screen, color, [
                (MARGIN + CELL_WIDTH) * j + MARGIN,
                (MARGIN + CELL_HEIGHT) * i + MARGIN,
                CELL_WIDTH,
                CELL_HEIGHT
            ])

    bfs(grid, 0, 0)

    clock.tick(60)
    pygame.display.flip()


pygame.quit()
quit()

