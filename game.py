import os

import pygame
from pygame import freetype
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE
from pygame.rect import Rect

SCREENRECT = Rect(0, 0, 1000, 1000)

colors = {
    "grey_light": pygame.Color(200, 200, 200),
    "grey_dark": pygame.Color(100, 100, 100),
    "green": pygame.Color(50, 255, 63),
    "red": pygame.Color(220, 30, 30),
    "blue": pygame.Color(50, 75, 245)
}


def drawCard(font, screen, x, y):
    font.render_to(screen, (64 * x, 64 * y), "猫", colors["grey_dark"], size=64, style=freetype.STYLE_NORMAL)


def update(font, screen):
    for y in range(10):
        for x in range(10):
            drawCard(font, screen, x, y)


def main():
    winstyle = 0  # | pygame.FULLSCREEN
    current_dir = os.path.dirname(os.path.abspath(__file__))
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, 32)
    screen.fill(pygame.Color(200, 200, 200))

    font = freetype.Font(os.path.join(current_dir, "fonts", "kaiti.ttf"))

    update(font, screen)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
