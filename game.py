import os
from enum import Enum
from typing import List

import pygame
from pygame import freetype
from pygame.constants import QUIT, KEYDOWN, K_ESCAPE, MOUSEBUTTONUP
from pygame.rect import Rect

SCREENRECT = Rect(0, 0, 1000, 1000)
PANE_WIDTH = 7
PANE_HEIGHT = 6
CARD_SIZE = 100

main_dir = os.path.split(os.path.abspath(__file__))[0]


class CardState(Enum):
    SHOWN = 1
    HIDDEN = 2
    REMOVED = 3


colors = {
    "grey_light": pygame.Color(200, 200, 200),
    "grey_dark": pygame.Color(100, 100, 100),
    "green": pygame.Color(50, 255, 63),
    "red": pygame.Color(220, 30, 30),
    "blue": pygame.Color(50, 75, 245),
    "background": pygame.Color(200, 200, 200),
}


def load_image(file):
    "loads an image, prepares it for play"
    file = os.path.join(main_dir, 'data', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        raise SystemExit('Could not load image "%s" %s' % (file, pygame.get_error()))
    return surface


class Back(pygame.sprite.Sprite):
    card_back_image = load_image('card_back_square.jpg')
    card_back_image = pygame.transform.scale(card_back_image, (CARD_SIZE, CARD_SIZE))

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image = self.card_back_image
        self.rect = Rect(0, 0, CARD_SIZE, CARD_SIZE)


def drawCard(font, screen, x, y, state: CardState):
    if state == CardState.SHOWN:
        rect = Rect(CARD_SIZE * x, CARD_SIZE * y, CARD_SIZE, CARD_SIZE)
        screen.fill(colors["background"], rect=rect)
        font.render_to(screen, (CARD_SIZE * x, CARD_SIZE * y), "猫", colors["grey_dark"],
                       size=CARD_SIZE, style=freetype.STYLE_NORMAL)


def update(font, screen, cards_state: List[List[CardState]]):
    for y in range(PANE_HEIGHT):
        for x in range(PANE_WIDTH):
            drawCard(font, screen, x, y, cards_state[x][y])


def main():
    winstyle = 0  # | pygame.FULLSCREEN
    current_dir = os.path.dirname(os.path.abspath(__file__))
    screen = pygame.display.set_mode(SCREENRECT.size, winstyle, 32)

    card_state = [[CardState.HIDDEN for i in range(PANE_HEIGHT)] for j in range(PANE_WIDTH)]

    font = freetype.Font(os.path.join(current_dir, "fonts", "kaiti.ttf"))
    all = pygame.sprite.RenderUpdates()
    Back.containers = all

    card_backs = [[Back() for i in range(PANE_HEIGHT)] for j in range(PANE_WIDTH)]

    # update all the sprites
    all.update()
    _update_cards(all, card_state, font, screen)
    while True:

        for event in pygame.event.get():
            if event.type == QUIT or \
                    (event.type == KEYDOWN and event.key == K_ESCAPE):
                return
            if event.type == MOUSEBUTTONUP:
                pos = event.pos
                x = int(pos[0] / CARD_SIZE)
                y = int(pos[1] / CARD_SIZE)

                if x >= PANE_WIDTH or y >= PANE_HEIGHT:
                    continue

                state = card_state[x][y]
                if state == CardState.HIDDEN:
                    card_state[x][y] = CardState.SHOWN
                elif state == CardState.SHOWN:
                    card_state[x][y] = CardState.HIDDEN

                _update_cards(all, card_state, font, screen)


def _update_cards(all, card_state, font, screen):
    screen.fill(pygame.Color(200, 200, 200))
    dirty = all.draw(screen)
    pygame.display.update(dirty)
    update(font, screen, card_state)
    pygame.display.flip()


if __name__ == '__main__':
    pygame.init()
    main()
    pygame.quit()
