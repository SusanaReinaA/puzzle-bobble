
import pygame
import sys

from pygame.locals import BG_COLOR
from FrontEnd.ui.styles import BUBBLE_COLOR ,BG_COLOR


class Game:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.width = info.current_w
        self.height = info.current_h

        self.screen = pygame.display.set_mode(
            (self.width, self.height),
            pygame.FULLSCREEN
        )

        pygame.display.set_caption("Puzzle Bobble - L2")

        self.clock = pygame.time.Clock()
        self.running = True

        # colores
        self.bg_color = BG_COLOR

        # burbuja
        self.bubble = Bubble(
            self.width // 2,
            self.height // 2,
            20,
            BUBBLE_COLOR
        )

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(self.bg_color)

        self.bubble.draw(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

        pygame.quit()
        sys.exit()
