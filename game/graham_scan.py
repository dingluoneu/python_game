from math import *

def cross(v1, v2):
    ''' return the cross product of two vectors 
    '''
    return (v1[0] * v2[1]) - (v1[1] * v2[0])

def dot(v1, v2):
    ''' return the dot product of two vectors 
    '''
    return v1[0] * v2[0] + v1[1] * v2[1]

def angle_cmp(pivot):
    ''' receive a coord as the pivot and return a 
    function for comparing angles formed by another
    two coords around the pivot
    '''
    def _angle_cmp(c1, c2):
        v1 = c1[0] - pivot[0], c1[1] - pivot[1]
        v2 = c2[0] - pivot[0], c2[1] - pivot[1]
        cp = cross(v1, v2)
        if cp < 0:
            return 1
        elif cp == 0:
            return 0
        else:
            return -1
    return _angle_cmp

def turnning(c1, c2, c3):
    ''' detemine which way does c1 -> c2 -> c3 go
    '''
    v1 = c2[0] - c1[0], c2[1] - c1[1]
    v2 = c3[0] - c2[0], c3[1] - c2[1]
    cp = cross(v1, v2)
    if cp < 0:
        return 'RIGHT'
    elif cp == 0:
        return 'STRAIGHT'
    else:
        return 'LEFT'
    

def graham_scan(coords):
    ''' 
    Parameters:
        [(x, y)] - List of cartesian coordinates

    Return:
        [(x, y)] - List of vertex of the target convex hull
    '''
    num = len(coords)
    if num < 3:
        raise Exception('too few coords') 

    # sort the coords according to x
    coords.sort()

    # select the leftmost coord as the pivot
    pivot = coords[0] 
    coords = coords[1:]

    # for remaining coords, sort them by polar angle
    # in counterclockwise order around pivot
    coords.sort(angle_cmp(pivot)) 
    
    # push the first three coords in a stack
    stack = []
    stack.append(pivot)
    stack.append(coords[0])
    stack.append(coords[1])
    
    # for the rest of the coords, while the angle formed by 
    # the coord of the next-to-top of the stack, coord of 
    # top of stack and the next coord makes a nonleft turn, 
    # pop the stack
    # also, push the next coord into the stack at each loop
    for i in range(2, num - 1):
        while len(stack) >= 2 and \
              turnning(stack[-2], stack[-1], coords[i]) != 'LEFT':
            stack = stack[:-1]
        stack.append(coords[i])
    return stack


if __name__ == '__main__':
    try:
        import pygame
        from pygame.color import *
        from pygame.locals import *

        pygame.init()

        caption = 'Convex hull solver demo using Graham Scan'
        resolution = (600, 600)
        text = ['Click mouse to draw dots', 
                'Press <Space> to reset',
                'Press <Esc> to exit'] 

        screen = pygame.display.set_mode(resolution)
        pygame.display.set_caption(caption)
        clock = pygame.time.Clock()
        font = pygame.font.Font(None, 20)

        coords = []
        segments = []
        running = True

        while running:
            # events handling
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == MOUSEBUTTONDOWN:
                    coords.append(event.pos)
                    if len(coords) >= 3:
                        segments = graham_scan(coords)
                elif event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        segments = []
                        coords = []
                    elif event.key == K_ESCAPE:
                        running = False
            
            # fill screen
            screen.fill(Color('white'))
            
            # draw help text
            y = 5
            for line in text:
                img = font.render(line, 1, Color('black'))
                screen.blit(img, (5, y))
                y += 15
            
            # draw dots
            for coord in coords:
                pygame.draw.circle(screen, Color('blue'), coord,
                                   2, 0)

            # draw segments
            if len(coords) >= 3:
                pygame.draw.lines(screen, Color('grey'), True,
                                  segments, 2)

            # step
            pygame.display.update()
            clock.tick(50)

    except ImportError:
        print('Unable to import pygame')
