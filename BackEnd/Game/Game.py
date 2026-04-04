from turtledemo.sorting_animate import show_text

import pygame
import random
import math
from Bubble import Bubble
from Physics import Physics
from Grid import Grid
from Highscore import Highscore
from FrontEnd.ui.Styles import BUBBLE_COLORS, BG_COLOR


class Game:
    def __init__(self):
        self._init_pygame()
        self._init_display()
        self._init_game()
        self.Physics = Physics()
        self.clock = pygame.time.Clock()
        self.score = 0
        self.level = 1
        self.game_over = False


    def _init_pygame(self):
        pygame.init()
        self.clock = pygame.time.Clock()
        self.running = True

    def _init_display(self):
        info = pygame.display.Info()
        self.screen = pygame.display.set_mode(
            (info.current_w, info.current_h),
            pygame.FULLSCREEN
        )
        pygame.display.set_caption("Puzzle Bubble")

        self.virtual_width = 800
        self.virtual_height = 600

        self.surface = pygame.Surface(
            (self.virtual_width, self.virtual_height)
        )

    def _init_game(self):
        self.grid = Grid(self.virtual_width)
        self.Bubble = Bubble(
            self.virtual_height - 20,
            self.virtual_width // 2,
            20,
            BUBBLE_COLORS["purple"]
        )
        self.next_bubble = Bubble(
            self.virtual_height - 20,
            self.virtual_width // 2 + 60,
            15,
            random.choice(list(BUBBLE_COLORS.values()))
        )

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            self.handle_event()
            if not self.game_over:
                self.update(dt)
            self.draw()
        pygame.quit()

    def handle_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if event.key == pygame.K_r:
                    self._init_game()
                    self.game_over = False
                    self.score = 0

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.game_over:
                    mx, my = pygame.mouse.get_pos()
                    mx = mx * self.virtual_width / self.screen.get_width()
                    my = my * self.virtual_height / self.screen.get_height()
                    self.Physics.shoot(self.Bubble,mx, my)




    def update(self, dt):
        self.Bubble.update(dt)
        self.Physics.handle_wall_collision(self.Bubble, self.virtual_width)
        self.Physics.handle_ceiling_collision(self.Bubble)

        if self.grid.is_game_over(self.virtual_height - 20):
            self.highscore.save(self.score)
            self.game_over = True
            return

        if self.Physics.handle_bubble_collision(self.Bubble, self.grid):
            self.Bubble.vx = 0
            self.Bubble.vy = 0

            last_bubble = self.grid.attach_bubble(self.Bubble)
            group = self.grid.find_group(last_bubble)

            if len(group) >= 3:
                self.grid.remove_group(group)
                self.score += len(group) * 10

            self.Bubble = self.next_bubble
            self.Bubble.row = self.virtual_height - 20
            self.Bubble.col = self.virtual_width // 2
            self.Bubble.radius = 20
            self.Bubble.vx = 0
            self.Bubble.vy = 0

            self.next_bubble = Bubble(
                self.virtual_height - 20,
                self.virtual_width // 2 + 60,
                15,
                random.choice(list(BUBBLE_COLORS.values()))
            )

    def draw_aim(self, surface):
        mx, my = pygame.mouse.get_pos()
        mx = mx * self.virtual_width / self.screen.get_width()
        my = my * self.virtual_height / self.screen.get_height()

        bx, by = self.Bubble.get_position()

        dx = mx - bx
        dy = my - by
        distance = math.sqrt(dx**2 + dy**2)

        if distance == 0:
            return

        dx /= distance
        dy /= distance

        for i in range(1, 10):
            px = int(bx + dx * i * 20)
            py = int(by + dy * i * 20)
            pygame.draw.circle(surface, (255, 255, 255), (px, py), 3)

    def draw_game_over(self):
        font = pygame.font.SysFont(None, 80)
        font2 = pygame.font.SysFont(None, 50)

        text = font.render("GAME OVER", True, (255, 0, 0))
        x = self.virtual_width // 2 - text.get_width() // 2
        y = self.virtual_height // 2 - text.get_height() // 2
        self.surface.blit(text, (x, y))

        score_text = font2.render(f"Score: {self.score}", True, (255, 255, 255))
        sx = self.virtual_width // 2 - score_text.get_width() // 2
        self.surface.blit(score_text, (sx, y + 80))

#higscore
        hs_text = font2.render(f"Best : {self.score}", True, (255, 255, 255))
        sx = self.virtual_width // 2 - hs_text.get_width() // 2
        self.surface.blit(hs_text, (sx, y + 80))


        restart_text = font2.render("Appuie sur R pour recommencer", True, (255, 255, 0))
        rx = self.virtual_width // 2 - restart_text.get_width() // 2
        self.surface.blit(restart_text, (rx, y + 140))

    def draw_ui(self, surface):
        font = pygame.font.SysFont(None, 40)

        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        surface.blit(score_text, (10, 10))

        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        surface.blit(level_text, (self.virtual_width - level_text.get_width() - 10, 10))
    def draw(self):
        self.surface.fill(BG_COLOR)
        self.grid.draw(self.surface)

        if self.game_over:
            self.draw_game_over()
        else:
            self.draw_aim(self.surface)
            self.Bubble.draw(self.surface)
            self.next_bubble.draw(self.surface)
            self.draw_ui(self.surface)

        scaled = pygame.transform.scale(
            self.surface,
            (self.screen.get_width(), self.screen.get_height())
        )
        self.screen.blit(scaled, (0, 0))
        pygame.display.flip()