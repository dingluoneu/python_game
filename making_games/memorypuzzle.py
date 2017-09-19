import random, pygame, sys
from pygame.locals import *


FPS = 60
WINDOW_WIDTH = 640
WINDOW_HEIGHT = 480
REVEALSPEED = 8
BOXSIZE = 40
GAPSIZE = 10
BOARD_WIDTH = 10
BOARD_HEIGHT = 7

assert (BOARD_WIDTH * BOARD_HEIGHT) % 2 == 0, 'Board needs to have an even number of boxes for pairs of matches.'

X_MARGIN = int((WINDOW_WIDTH - (BOARD_WIDTH * (BOXSIZE + GAPSIZE))) / 2)
Y_MARGIN = int((WINDOW_HEIGHT - (BOARD_HEIGHT * (BOXSIZE + GAPSIZE))) / 2)

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 255,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (255, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)

BG_COLOR = NAVYBLUE
LIGHT_BG_COLOR = GRAY
BOX_COLOR = WHITE
HIGH_LIGHT_COLOR = BLUE

DONUT = 'donut'
SQUARE = 'square'
DIAMOND = 'diamond'
LINES = 'lines'
OVAL = 'oval'

ALL_COLORS = (RED, GREEN, BLUE, YELLOW, ORANGE, PURPLE, CYAN)
ALL_SHAPES = (DONUT, SQUARE, DIAMOND, LINES, OVAL)
assert len(ALL_COLORS) * len(ALL_SHAPES) * 2 >= BOARD_WIDTH * BOARD_HEIGHT, "Board is too big for the number of shapes/colors defined."


def main():
    global FPS_CLOCK, DISPLAY_SURF
    pygame.init()
    FPS_CLOCK = pygame.time.Clock()
    DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    mouse_x = 0
    mouse_y = 0
    pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

    main_board = get_randomized_board()
    revealed_boxes = generate_revealed_boxes_data(False)

    first_selection = None # Stores the (x, y) of the first box clicked

    DISPLAY_SURF.fill(BG_COLOR)
    start_game_animation(main_board)

    # Main game loop
    while True:
        mouse_clicked = False

        DISPLAY_SURF.fill(BG_COLOR) # drawing the window
        draw_board(main_board, revealed_boxes)

        # Even handling loop
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYUP and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEMOTION:
                mouse_x, mouse_y = event.pos
            elif event.type == MOUSEBUTTONUP:
                mouse_clicked = True

        boxx, boxy = get_box_at_pixel(mouse_x, mouse_y)
        if boxx is not None and boxy is not None:
            # The mouse is currently over a box
            if not revealed_boxes[boxx][boxy]:
                draw_high_light_box(boxx, boxy)
            if not revealed_boxes[boxx][boxy] and mouse_clicked:
                reveal_boxes_animation(main_board, [(boxx, boxy)])
                revealed_boxes[boxx][boxy] = True  # Set the box as "revealed"
                if first_selection is None:  # The current box was the first box clicked
                    first_selection = (boxx, boxy)
                else:
                    # The current box was the second box clicked
                    # Check if there is a match between the two icons.
                    icon1_shape, icon1_color = get_shape_and_color(main_board, first_selection[0], first_selection[1])
                    icon2_shape, icon2_color = get_shape_and_color(main_board, boxx, boxy)

                    if icon1_shape != icon2_shape or icon1_color != icon2_color:
                        # Icons don't match. Re-cover up both selections
                        pygame.time.wait(1000)
                        cover_boxes_animation(main_board, [(first_selection[0], first_selection[1]), (boxx, boxy)])
                        revealed_boxes[first_selection[0]][first_selection[1]] = False
                        revealed_boxes[boxx][boxy] = False
                    elif has_won(revealed_boxes):
                        game_won_animation(main_board)
                        pygame.time.wait(2000)

                        # Reset the board
                        main_board = get_randomized_board()
                        revealed_boxes = generate_revealed_boxes_data(False)

                        # Show the fully unrevealed board for a second.
                        draw_board(main_board, revealed_boxes)
                        pygame.display.update()
                        pygame.time.wait(1000)

                        # Replay the start game animation
                        start_game_animation(main_board)
                    first_selection = None
        # Redraw the screen and wait a clock tick
        pygame.display.update()
        FPS_CLOCK.tick(FPS)


def generate_revealed_boxes_data(val):
    revealed_boxes = []
    for i in range(BOARD_WIDTH):
        revealed_boxes.append([val] * BOARD_HEIGHT)
    return revealed_boxes


def get_randomized_board():
    icons = []
    for color in ALL_COLORS:
        for shape in ALL_SHAPES:
            icons.append((shape, color))

    random.shuffle(icons)
    num_icons_used = int(BOARD_WIDTH * BOARD_HEIGHT / 2)
    icons = icons[:num_icons_used] * 2
    random.shuffle(icons)

    # Create the board data structure, with randomly placed icons.
    board = []
    for x in range(BOARD_WIDTH):
        column = []
        for y in range(BOARD_HEIGHT):
            column.append(icons[0])
            del icons[0]
        board.append(column)
    return board


def split_into_groups(group_size, the_list):
    result = []
    for i in range(0, len(the_list), group_size):
        result.append(the_list[i : i + group_size])
    return result


def left_top_coords_of_box(boxx, boxy):
    # Covert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + X_MARGIN
    top = boxy * (BOXSIZE + GAPSIZE) + Y_MARGIN
    return left, top


def get_box_at_pixel(x, y):
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            box_rect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if box_rect.collidepoint(x, y):
                return boxx, boxy
    return None, None


def draw_icon(shape, color, boxx, boxy):
    quarter = int(BOXSIZE * 0.25)
    half = int(BOXSIZE * 0.5)

    left, top = left_top_coords_of_box(boxx, boxy) # get pixel coords from board coords
    # Draw the shapes:
    if shape == DONUT:
        pygame.draw.circle(DISPLAY_SURF, color, (left + half, top + half), half - 5)
        pygame.draw.circle(DISPLAY_SURF, BG_COLOR, (left + half, top + half), quarter - 5)
    elif shape == SQUARE:
        pygame.draw.rect(DISPLAY_SURF, color, (left + quarter, top + quarter, BOXSIZE - half, BOXSIZE - half))
    elif shape == DIAMOND:
        pygame.draw.polygon(DISPLAY_SURF, color, ((left + half, top), (left + BOXSIZE - 1, top + half), (left + half, top + BOXSIZE - 1), (left, top + half)))
    elif shape == LINES:
        for i in range(0, BOXSIZE, 4):
            pygame.draw.line(DISPLAY_SURF, color, (left, top + i), (left + i, top))
            pygame.draw.line(DISPLAY_SURF, color, (left + i, top + BOXSIZE - 1), (left + BOXSIZE - 1, top + i))
    elif shape == OVAL:
        pygame.draw.ellipse(DISPLAY_SURF, color, (left, top + quarter, BOXSIZE, half))


def get_shape_and_color(board, boxx, boxy):
    return board[boxx][boxy][0], board[boxx][boxy][1]


def draw_box_covers(board, boxes, coverage):
    """
    Draws boxes being covered/revealed.
    :param board:
    :param boxes: list of two-item lists, which have the x & y spot of the box
    :param coverage:
    :return:
    """
    for box in boxes:
        left, top = left_top_coords_of_box(box[0], box[1])
        pygame.draw.rect(DISPLAY_SURF, BG_COLOR, (left, top, BOXSIZE, BOXSIZE))
        shape, color = get_shape_and_color(board, box[0], box[1])
        draw_icon(shape, color, box[0], box[1])
        if coverage > 0:
            pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, coverage, BOXSIZE))
    pygame.display.update()
    FPS_CLOCK.tick(FPS)


def reveal_boxes_animation(board, boxes_to_reveal):
    for coverage in range(BOXSIZE, (-REVEALSPEED) - 1, -REVEALSPEED):
        draw_box_covers(board, boxes_to_reveal, coverage)


def cover_boxes_animation(board, boxes_to_cover):
    for coverage in range(0, BOXSIZE + REVEALSPEED, REVEALSPEED):
        draw_box_covers(board, boxes_to_cover, coverage)


def draw_board(board, revealed):
    # Draw all of the boxes in their covered or revealed state
    for boxx in range(BOARD_WIDTH):
        for boxy in range(BOARD_HEIGHT):
            left, top = left_top_coords_of_box(boxx, boxy)
            if not revealed[boxx][boxy]:
                # Draw a covered box
                pygame.draw.rect(DISPLAY_SURF, BOX_COLOR, (left, top, BOXSIZE, BOXSIZE))
            else:
                # Draw the (revealed) icon
                shape, color = get_shape_and_color(board, boxx, boxy)
                draw_icon(shape, color, boxx, boxy)


def draw_high_light_box(boxx, boxy):
    left, top = left_top_coords_of_box(boxx, boxy)
    pygame.draw.rect(DISPLAY_SURF, HIGH_LIGHT_COLOR, (left - 5, left - 5, BOXSIZE + 10, BOXSIZE + 1), 4)


def start_game_animation(board):
    # Randomly reveal the boxes 8 at a time
    covered_boxes = generate_revealed_boxes_data(False)
    boxes = []
    for x in range(BOARD_WIDTH):
        for y in range(BOARD_HEIGHT):
            boxes.append((x, y))
    random.shuffle(boxes)
    box_groups = split_into_groups(8, boxes)


def game_won_animation(board):
    # Flash the background color when the player has won
    covered_boxes = generate_revealed_boxes_data(True)
    color1 = LIGHT_BG_COLOR
    color2 = BG_COLOR

    for i in range(13):
        color1, color2 = color2, color1 # Swap colors
        DISPLAY_SURF.fill(color1)
        draw_board(board, covered_boxes)
        pygame.display.update()
        pygame.time.wait(300)


def has_won(revealed_boxes):
    # Return True if all the boxes have been revealed, otherwise False
    for i in revealed_boxes:
        if False in i:
            return False
    return True


if __name__ == '__main__':
    main()