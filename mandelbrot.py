import pygame
import math
from random import randint as rand
from random import shuffle

WIDTH = 512
HEIGHT = 512
MAX_PIXEL_SIZE = 8
DEFAULT_PIXEL_SIZE = 1
ITERATIONS = 100
LIMIT = 4
REDRAW_INTERVAL = 0.2
PIXEL_SIZE_CHANGE = True

DEFAULT_CENTER_A = center_a = -1
DEFAULT_CENTER_B = center_b = 0
DEFAULT_COMPLEX_DIST = complex_dist = 4

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

def mandel_value(x, y, pwidth, pheight):

    ratioX = x / pwidth
    ratioY = y / pheight

    a = a_0 = ratioX * complex_dist + (center_a - complex_dist/2)
    b = b_0 = ratioY * complex_dist + (center_b - complex_dist/2)

    for i in range(ITERATIONS):
        new_a = a**2 - b**2 + a_0
        new_b = 2 * a * b + b_0

        a = new_a
        b = new_b

        z_mag = math.sqrt(a**2 + b**2)

        if z_mag > LIMIT:
            return i

    return -1

if PIXEL_SIZE_CHANGE:
    pixel_size = MAX_PIXEL_SIZE
else:
    pixel_size = DEFAULT_PIXEL_SIZE
while running:
    break_flag = False

    pwidth = int(WIDTH // pixel_size)
    pheight = int(HEIGHT // pixel_size)

    all_x = list(range(pwidth))
    all_y = list(range(pheight))

    shuffle(all_y)
    coords = [(x, y) for y in all_y for x in all_x]
    shuffle(coords)

    counter = 0
    
    for x, y in coords:
        # Check if user has quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                # Escape pressed
                if event.key == 27:
                    quit()

                # A number key is pressed
                if event.key > 48 and event.key < 58:
                    ITERATIONS = (event.key - 48) * 100

                # E key is pressed
                if event.key == 101:
                    complex_dist *= 4

                # R key is pressed
                if event.key == 114:
                    center_a = DEFAULT_CENTER_A
                    center_b = DEFAULT_CENTER_B
                    complex_dist = DEFAULT_COMPLEX_DIST

                break_flag = True
                if PIXEL_SIZE_CHANGE:
                    pixel_size = MAX_PIXEL_SIZE
                else:
                    screen.fill("#000000")
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                counter = 0
                ratioX = event.pos[0] / WIDTH
                ratioY = event.pos[1] / HEIGHT

                center_a = ratioX * complex_dist + (center_a - complex_dist/2)
                center_b = ratioY * complex_dist + (center_b - complex_dist/2)
                complex_dist /= 4

                if PIXEL_SIZE_CHANGE:
                    pixel_size = MAX_PIXEL_SIZE
                    break_flag = True
                    break
                else:
                    screen.fill("#000000")
        if break_flag:
            break

        counter += 1

        value = mandel_value(x, y, pwidth, pheight)
        r = g = b = 0

        if value == -1:
            color = "#000000"
        else:
            colour_ratio = value / ITERATIONS
            if colour_ratio < 0.5:
                r = 255
                g = 255 * colour_ratio
                b = 0
            else:
                r = 255 * (1 - colour_ratio)
                g = 255
                b = 0
            color = '#{:02x}{:02x}{:02x}'.format(int(r), int(g), int(b))

        pygame.draw.rect(screen, color, pygame.Rect(x*pixel_size, y*pixel_size, pixel_size, pixel_size))

        if counter >= pheight:
            counter = 0

            pygame.display.flip()
            # clock.tick(60)

    if break_flag:
        continue

    if pixel_size > 1 and PIXEL_SIZE_CHANGE:
        pixel_size /= 2