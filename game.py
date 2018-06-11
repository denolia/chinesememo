import os
from enum import Enum
from typing import List

import pygame
from pygame import freetype
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP
from pygame.rect import Rect

SCREENRECT = Rect(0, 0, 1000, 1000)
PANE_HEIGHT = 10
PANE_WIDTH = 10
CARD_SIZE = 64


class CardState(Enum):
    SHOWN = 1
    HIDDEN = 2
    REMOVED = 3


colors = {
    "grey_light": pygame.Color(200, 200, 200),
    "grey_dark": pygame.Color(100, 100, 100),
    "green": pygame.Color(50, 255, 63),
    "red": pygame.Color(220, 30, 30),
    "blue": pygame.Color(50, 75, 245)
}


def drawCard(font, screen, x, y, state: CardState):
    if state == CardState.HIDDEN:
        color = colors["grey_dark"]
    elif state == CardState.SHOWN:
        color = colors["red"]
    else:
        return
    font.render_to(screen, (CARD_SIZE * x, CARD_SIZE * y), "猫", color,
                   size=CARD_SIZE, style=freetype.STYLE_NORMAL)


def update(font, screen, cards_state: List[List[CardState]]):
    for y in range(PANE_WIDTH):
        for x in range(PANE_HEIGHT):
            drawCard(font, screen, x, y, cards_state[x][y])


def main():
    winstyle = 0  # | pygame.FULLSCREEN
    current_dir = os.path.dirname(os.path.abspath(__file__))
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, 32)

    card_state = [[CardState.HIDDEN for i in range(PANE_WIDTH)] for j in range(PANE_HEIGHT)]

    font = freetype.Font(os.path.join(current_dir, "fonts", "kaiti.ttf"))

    while True:
        screen.fill(pygame.Color(200, 200, 200))

        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONUP:
                pos = event.pos
                x = int(pos[0] / 64)
                y = int(pos[1] / 64)

                if x >= PANE_WIDTH or y >= PANE_HEIGHT:
                    continue

                state = card_state[x][y]
                if state == CardState.HIDDEN:
                    card_state[x][y] = CardState.SHOWN
                elif state == CardState.SHOWN:
                    card_state[x][y] = CardState.HIDDEN

        update(font, screen, card_state)
        pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
