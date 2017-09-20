import pygame, sys, random
from pygame.locals import *


# Create the constants
BOARD_WIDTH = 4
BOARD_HEIGHT = 4
TILE_SIZE = 80
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 30
BLANK = None

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BRIGHT_BLUE = (0, 50, 255)
DARK_TURQUOISE = (3, 54, 73)
GREEN = (0, 204, 0)

BG_COLOR = DARK_TURQUOISE
TILE_COLOR = GREEN
TEXT_COLOR = WHITE
BORDER_COLOR = BRIGHT_BLUE
BASIC_FONT_SIZE = 20

BUTTON_COLOR = WHITE
BUTTON_TEXT_COLOR = BLACK
MESSAGE_COLOR = WHITE

X_MARGIN = int((WINDOW_WIDTH - (TILE_SIZE * BOARD_WIDTH + (BOARD_WIDTH - 1))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (TILE_SIZE * BOARD_HEIGHT + (BOARD_HEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPS_CLOCK, DISPLAY_SURF, BASIC_FONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Slide Puzzle")
    BASIC_FONT = pygame.font.Font('freesansbold.ttf', BASIC_FONT_SIZE)

    # Store the option buttons and their retangles in OPTIONS
    RESET_SURF, RESET_RECT = make_text('Reset', TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 90)
    NEW_SURF, NEW_RECT = make_text('New Game', TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = make_text('Solve', TEXT_COLOR, TILE_COLOR, WINDOW_WIDTH - 120, WINDOW_HEIGHT - 30)

    main_board, solution_seq = generate_new_puzzle(80)
    SOLVED_BOARD = get_starting_board()

    all_moves = []

    while True:
        slide_to = None
        msg = ''
        if main_board == SOLVED_BOARD:
            msg = 'Solved!'

        draw_board(main_board, msg)

        check_for_quit()

        for event in pygame.event.get():
            if event.type == MOUSEBUTTONUP:
                spot_x, spot_y = get_spot_clicked(main_board, event.pos[0], event.pos[1])

                if (spot_x, spot_y) == (None, None):
                    # Check if the user clicked on an option button
                    if RESET_RECT.collidepoint(event.pos):
                        reset_animation(main_board, all_moves)
                        all_moves = []
                    elif NEW_RECT.collidepoint(event.pos):
                        main_board, solution_seq = generate_new_puzzle(80)
                        all_moves = []
                    elif SOLVE_RECT.collidepoint(event.pos):
                        reset_animation(main_board, solution_seq + all_moves)
                        all_moves = []
                    else:
                        # Check if the clicked tile was next to the blank spot
                        blankx, blanky = get_blank_position(main_board)
                        if spot_x == blankx + 1 and spot_y == blanky:
                            slide_to = LEFT
                        elif spot_x == blankx - 1 and spot_y == blanky:
                            slide_to = RIGHT
                        elif spot_x == blankx and spot_y == blanky + 1:
                            slide_to = UP
                        elif spot_x == blankx and spot_y == blanky - 1:
                            slide_to = DOWN
            elif event.type == KEYUP:
                # Check if the user pressed a key to slide a tile
                if event.key in (K_LEFT, K_a) and is_valid_move(main_board, LEFT):
                    slide_to = LEFT
                elif event.key in (K_RIGHT, K_d) and is_valid_move(main_board, RIGHT):
                    slide_to = RIGHT
                elif event.key in (K_UP, K_w) and is_valid_move(main_board, UP):
                    slide_to = UP
                elif event.key in (K_DOWN, K_s) and is_valid_move(main_board, DOWN):
                    slide_to = DOWN

        if slide_to:
            slide_animation(main_board, slide_to, 'Click tile or press arrow keys to slide.', 8)
            make_move(main_board, slide_to)
            all_moves.append(slide_to)
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def check_for_quit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()
    for event in pygame.event.get(KEYUP):
        if event.key == K_ESCAPE:
            terminate()
        pygame.event.post(event)  # Put the other KEYUP event objects back


def get_starting_board():
    """
    Return a board data structure with tiles in the solved state.
    For example, if BOARD_WIDTH and BOARD_HEIGHT are both 3, this function return:
    [[1, 4, 7], [2, 5, 8], [3, 6, None]]
    :return: 2D list
    """
    counter = 1
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(counter)
            counter += BOARD_WIDTH
        board.append(column)
        counter -= BOARD_WIDTH * (BOARD_HEIGHT - 1) + BOARD_WIDTH - 1

    board[BOARD_WIDTH - 1][BOARD_HEIGHT - 1] = None
    return board


def get_blank_position(board):
    # Return the x and y of board coordinates of the blank space
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            if board[x][y] is None:
                return x, y


def make_move(board, move):
    # This function does not check if the move is valid
    blankx, blanky = get_blank_position(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] = board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]


def is_valid_move(board, move):
    blankx, blanky = get_blank_position(board)
    return (move == UP and blanky != len(board[0]) - 1) or (move == DOWN and blanky != 0) or (move == LEFT and blankx != len(board) - 1) or (move == RIGHT and blankx != 0)


def get_random_move(board, last_move=None):
    # Start with a full list of all four moves
    valid_moves = [UP, DOWN, LEFT, RIGHT]

    # Remove moves from the list as they are disqualified
    if last_move == UP or not is_valid_move(board, DOWN):
        valid_moves.remove(DOWN)
    if last_move == DOWN or not is_valid_move(board, UP):
        valid_moves.remove(UP)
    if last_move == LEFT or not is_valid_move(board, RIGHT):
        valid_moves.remove(RIGHT)
    if last_move == RIGHT or not  is_valid_move(board, LEFT):
        valid_moves.remove(LEFT)

    # Return a random move from the list of remaining moves
    return random.choice(valid_moves)


def get_left_top_of_tile(tile_x, tile_y):
    left = X_MARGIN + (tile_x * TILE_SIZE) + (tile_x - 1)
    top = Y_MARGIN + (tile_y * TILE_SIZE) + (tile_y - 1)
    return left, top


def get_spot_clicked(board, x, y):
    # From the x & y pixel coordinates, get the x & y board coordinates
    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            left, top = get_left_top_of_tile(tile_x, tile_y)
            tile_rect = pygame.Rect(left, top, TILE_SIZE, TILE_SIZE)
            if tile_rect.collidepoint(x, y):
                return tile_x, tile_y
    return None, None


def draw_tile(tile_x, tile_y, number, adjx=0, adjy=0):
    # Draw a tile at board coordinates tile_x, tile_y, optionally a few pixels over
    left, top = get_left_top_of_tile(tile_x, tile_y)
    pygame.draw.rect(DISPLAY_SURF, TILE_COLOR, [left + adjx, top + adjy, TILE_SIZE, TILE_SIZE])
    text_surf = BASIC_FONT.render(str(number), True, TEXT_COLOR)
    text_rect = text_surf.get_rect()
    text_rect.center = left + int(TILE_SIZE / 2) + adjx, top + int(TILE_SIZE / 2) + adjy
    DISPLAY_SURF.blit(text_surf, text_rect)


def make_text(text, color, bg_color, top, left):
    # Create the surface and Rect objects for some text.
    text_surf = BASIC_FONT.render(text, True, color, bg_color)
    text_rect = text_surf.get_rect()
    text_rect.topleft = (top, left)
    return text_surf, text_rect


def draw_board(board, message):
    DISPLAY_SURF.fill(BG_COLOR)
    if message:
        text_surf, text_rect = make_text(message, MESSAGE_COLOR, BG_COLOR, 5, 5)
        DISPLAY_SURF.blit(text_surf, text_rect)

    for tile_x in range(len(board)):
        for tile_y in range(len(board[0])):
            if board[tile_x][tile_y]:
                draw_tile(tile_x, tile_y, board[tile_x][tile_y])

    left, top = get_left_top_of_tile(0, 0)
    width = BOARD_WIDTH * TILE_SIZE
    height = BOARD_HEIGHT * TILE_SIZE
    pygame.draw.rect(DISPLAY_SURF, BORDER_COLOR, [left - 5, top - 5, width + 11, height + 11], 4)

    DISPLAY_SURF.blit(RESET_SURF, RESET_RECT)
    DISPLAY_SURF.blit(NEW_SURF, NEW_RECT)
    DISPLAY_SURF.blit(SOLVE_SURF, SOLVE_RECT)


def slide_animation(board, direction, message, animation_speed):
    blankx, blanky = get_blank_position(board)

    if direction == UP:
        move_x = blankx
        move_y = blanky + 1
    elif direction == DOWN:
        move_x = blankx
        move_y = blanky - 1
    elif direction == LEFT:
        move_x = blankx + 1
        move_y = blanky
    elif direction == RIGHT:
        move_x = blankx - 1
        move_y = blanky

    # Prepare the base surface
    draw_board(board, message)
    base_surf = DISPLAY_SURF.copy()

    # Draw a blank space over the moving tile on the base_surf
    move_left, move_top = get_left_top_of_tile(move_x, move_y)
    pygame.draw.rect(base_surf, BG_COLOR, [move_left, move_top, TILE_SIZE, TILE_SIZE])

    for i in range(0, TILE_SIZE, animation_speed):
        check_for_quit()
        DISPLAY_SURF.blit(base_surf, (0, 0))
        if direction == UP:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, -i)
        if direction == DOWN:
            draw_tile(move_x, move_y, board[move_x][move_y], 0, i)
        if direction == LEFT:
            draw_tile(move_x, move_y, board[move_x][move_y], -i, 0)
        if direction == RIGHT:
            draw_tile(move_x, move_y, board[move_x][move_y], i, 0)

        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def generate_new_puzzle(num_slides):
    # From a starting configuration, make num_slides number of moves
    sequence = []
    board = get_starting_board()
    draw_board(board, '')
    pygame.display.update()
    pygame.time.wait(500)
    last_move = None

    for i in range(num_slides):
        move = get_random_move(board, last_move)
        slide_animation(board, move, 'Generating new puzzle...', int(TILE_SIZE / 3))
        make_move(board, move)
        sequence.append(move)
        last_move = move
    return board, sequence


def reset_animation(board, all_moves):
    rev_all_moves = all_moves[:]  # get a copy of the list
    rev_all_moves.reverse()

    opposite_move = None

    for move in rev_all_moves:
        if move == UP:
            opposite_move = DOWN
        elif move == DOWN:
            opposite_move = UP
        elif move == RIGHT:
            opposite_move = LEFT
        elif move == LEFT:
            opposite_move = RIGHT
        slide_animation(board, opposite_move, '', int(TILE_SIZE / 2))
        make_move(board, opposite_move)


if __name__ == '__main__':
    main()