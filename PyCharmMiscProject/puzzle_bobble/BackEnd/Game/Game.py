import pygame
import random
import math
from BackEnd.Game.Grid import Grid
from BackEnd.Game.Bubble import Bubble
from BackEnd.Game.Physics import Physics
from BackEnd.Game.Highscore import Highscore
from FrontEnd.ui.Styles import BUBBLE_COLORS, BG_COLOR

from BackEnd.Game.GameState import GameState


class Game:
    def __init__(self):
        self._init_pygame()
        self._init_display()
        self.physics = Physics()
        self.ceiling_offset = 0
        self.timer = 0
        self.game_over = False
        self.highscore = Highscore()
        self.auto_play = False
        self.level_time = 0
        self.score = 0
        self.level = 1
        self.level_times = []
        self.level_start_time = 0
        self.show_level_time = False
        self.show_timer = 0
        self.paused = False
        self.state = GameState.PLAYING
        self.victory = False
        self.show_score = False
        self.score_timer = 0
        self.game_over_line = self.virtual_height - 60
        self._init_game()


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
        pygame.display.set_caption("Puzzle Bobble")

        self.virtual_width = 800
        self.virtual_height = 600

        self.surface = pygame.Surface(
            (self.virtual_width, self.virtual_height)
        )

    def _init_game(self):

        all_colors = list(BUBBLE_COLORS.values())

        if self.level == 1:
            self.allowed_colors = all_colors[:3]
        elif self.level == 2:
            self.allowed_colors = all_colors[:4]
        else:
            self.allowed_colors = all_colors[:5]

        #  on cree une  grille avec des couleurs autorisées
        self.grid = Grid(self.virtual_width, self.allowed_colors)

        # reset plafond + timer
        self.ceiling_offset = 0
        self.timer = 0
        self.level_timer = 0

        # murs
        r = self.grid.bubble_radius
        cols = self.grid.cols

        grid_width = cols * r * 2
        start_x = (self.virtual_width - grid_width) // 2

        self.physics.wall_left = start_x
        self.physics.wall_right = start_x + grid_width
        self.grid.wall_left = self.physics.wall_left
        self.grid.wall_right = self.physics.wall_right

        center_x = start_x + grid_width // 2

        self.Bubble = Bubble(
            center_x,
            self.virtual_height - 40,
            20,
            random.choice(self.allowed_colors)
        )

        self.next_bubble = Bubble(
            center_x + 60,
            self.virtual_height - 40,
            15,
            random.choice(self.allowed_colors)
        )

    def get_required_group(self):
        return 3


    def get_timer_limit(self):
        if self.level == 1:
            return 30
        elif self.level == 2:
            return 20
        else:
            return 10

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000
            dt = min(dt, 0.05)
            self.handle_event()

            if not self.game_over and not self.paused:
                self.update(dt)

            self.draw()

        pygame.quit()

    def handle_event(self):
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    self.highscore.save(self.score)
                    self.running = False


                elif event.key == pygame.K_r:
                    self.level = 1
                    self.score = 0
                    self.game_over = False
                    self.level_times = []
                    self._init_game()


                elif event.key == pygame.K_a:
                    self.auto_play = not self.auto_play


                elif event.key == pygame.K_p:

                    self.paused = not self.paused


            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over and not self.paused and self.Bubble.vx == 0:
                        mx, my = pygame.mouse.get_pos()
                        mx = mx * self.virtual_width / self.screen.get_width()
                        my = my * self.virtual_height / self.screen.get_height()

                        self.physics.shoot(self.Bubble, mx, my)

    def update(self, dt):

        if self.paused:
            return

        if self.show_level_time:
            self.show_timer -= dt
            if self.show_timer <= 0:
                self.show_level_time = False

        self.level_timer += dt
        self.timer += dt

        # plafond

        if self.timer >= self.get_timer_limit():
            self.timer = 0

            step = self.grid.bubble_radius * 1.732

            # verification avant la descente
            for row in self.grid.grid:
                for bubble in row:
                    _, y = bubble.get_position()

                    if y + step >= self.game_over_line:
                        self.highscore.save(self.score)
                        self.game_over = True
                        return

            # descente
            self.ceiling_offset += step
            self.grid.drop_grid()
            return

        # mouvement

        self.Bubble.update(dt)

        for row in self.grid.grid:
            for bubble in row:
                _, y = bubble.get_position()
                if y + bubble.radius >= self.game_over_line:
                    self.highscore.save(self.score)
                    self.game_over = True
                    return

        if self.auto_play:
            if self.Bubble.vx == 0 and self.Bubble.vy == 0:
                self.auto_shoot()

        self.physics.handle_wall_collision(self.Bubble, self.virtual_width)


        # collision
        last_bubble = None

        if self.Bubble.y - self.Bubble.radius <= self.ceiling_offset:

            self.Bubble.y = self.ceiling_offset + self.Bubble.radius
            self.Bubble.vx = 0
            self.Bubble.vy = 0

            r = self.grid.bubble_radius

            new_x = max(self.physics.wall_left + r, self.Bubble.x)
            new_x = min(self.physics.wall_right - r, new_x)

            new_bubble = Bubble(
                new_x,
                self.ceiling_offset + r,
                self.Bubble.radius,
                self.Bubble.color
            )

            self.grid.grid[0].append(new_bubble)
            last_bubble = new_bubble

        elif self.physics.handle_bubble_collision(self.Bubble, self.grid):

            self.Bubble.vx = 0
            self.Bubble.vy = 0

            last_bubble = self.grid.attach_bubble(self.Bubble)

            if last_bubble is None:
                return

        else:
            return

        # groupe

        group = self.grid.find_group(last_bubble)

        if len(group) >= 3:
            self.grid.remove_group(group)
            self.score += len(group) * 10
            self.grid.remove_floating()


        for row in self.grid.grid:
            for bubble in row:
                _, y = bubble.get_position()

                if y >= self.game_over_line:
                    self.highscore.save(self.score)
                    self.game_over = True
                    return

        # victoire

        if self.grid.is_empty():

            self.level_times.append(self.level_timer)

            bonus = max(200, int(2000 / (1 + self.level_timer)))
            self.score += bonus

            self.show_level_time = True
            self.show_timer = 3

            self.level += 1

            if self.level > 3:
                self.highscore.save(self.score)
                self.victory = True
                self.game_over = True
                return

            self._init_game()
            return

        # nouvele bulle

        self.spawn_new_bubble()

    def spawn_new_bubble(self):
        r = self.grid.bubble_radius
        cols = self.grid.cols

        grid_width = cols * r * 2
        start_x = (self.virtual_width - grid_width) // 2
        center_x = start_x + grid_width // 2

        # nouvelle bulle
        self.Bubble = Bubble(
            center_x,
            self.virtual_height - 40,
            20,
            self.next_bubble.color
        )

        available_colors = [
            c for c in self.allowed_colors
            if c in self.grid.get_remaining_colors()
        ]

        if len(available_colors) == 0:
            available_colors = self.available_colors

        # appliquer une difficulté par niveau
        level_colors = self.get_level_colors()

        # garder seulement les couleurs autorisées

        all_colors = list(BUBBLE_COLORS.values())

        if self.level == 1:
            allowed = all_colors[:3]
        elif self.level == 2:
            allowed = all_colors[:4]
        else:
            allowed = all_colors[:5]

        remaining = self.grid.get_remaining_colors()

        # garder seulement les couleurs présentes et autorisées
        filtered = [c for c in remaining if c in allowed]

        if len(filtered) == 0:
            filtered = allowed

        color = random.choice(filtered)

        # bulle suivant
        self.next_bubble = Bubble(
            center_x + 60,
            self.virtual_height - 40,
            15,
            color
        )

    def draw_aim(self, surface):
        mx, my = pygame.mouse.get_pos()
        mx = mx * self.virtual_width / self.screen.get_width()
        my = my * self.virtual_height / self.screen.get_height()

        bx, by = self.Bubble.get_position()

        dx = mx - bx
        dy = my - by

        if dy > -0.2:
            return

        dist = math.sqrt(dx**2 + dy**2)

        if dist == 0:
            return

        dx /= dist
        dy /= dist

        for i in range(1, 10):
            px = int(bx + dx * i * 20)
            py = int(by + dy * i * 20)
            pygame.draw.circle(surface, (255, 255, 255), (px, py), 3)

    def draw_game_over(self):
        font = pygame.font.SysFont(None, 80)
        font2 = pygame.font.SysFont(None, 50)

        score_text = font2.render(f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(score_text, (self.virtual_width // 2 - score_text.get_width() // 2, 300))

        best = max(self.score, self.highscore.get())
        best_text = font2.render(f"Best: {best}", True, (255, 255, 255))
        self.surface.blit(best_text, (self.virtual_width // 2 - best_text.get_width() // 2, 360))

        restart = font2.render("Appuie sur R pour recommencer", True, (255, 255, 0))
        self.surface.blit(restart, (self.virtual_width // 2 - restart.get_width() // 2, 420))

        y = 460
        for i, t in enumerate(self.level_times):
            txt = font2.render(f"Niveau {i + 1}: {round(t, 1)} s", True, (255, 255, 255))
            self.surface.blit(txt, (self.virtual_width // 2 - txt.get_width() // 2, y))
            y += 40

        if self.victory:
            text = font.render("YOU WON!", True, (0, 255, 0))
        else:
            text = font.render("GAME OVER!", True, (255, 0, 0))

        self.surface.blit(text, (self.virtual_width // 2 - text.get_width() // 2, 120))

    def draw_ui(self, surface):
        font = pygame.font.SysFont(None, 40)

        surface.blit(font.render(f"Score: {self.score}", True, (255, 255, 255)), (10, 10))

        level_text = font.render(f"Level: {self.level}", True, (255, 255, 255))
        surface.blit(level_text, (self.virtual_width - level_text.get_width() - 10, 10))


    def get_level_colors(self):
        all_colors = list(BUBBLE_COLORS.values())

        if self.level == 1:
            return all_colors[:3]
        elif self.level == 2:
            return all_colors[:4]
        else:
            return all_colors[:5]

    def draw(self):

        self.surface.fill(BG_COLOR)

        # grille
        self.grid.draw(self.surface)

        pygame.draw.line(
            self.surface,
            (255, 0, 0),
            (self.physics.wall_left, self.game_over_line),
            (self.physics.wall_right, self.game_over_line),
            2
        )

        # plafond
        r = self.grid.bubble_radius
        cols = self.grid.cols

        grid_width = cols * r * 2
        start_x = (self.virtual_width - grid_width) // 2

        pygame.draw.rect(
            self.surface,
            (180, 180, 180),
            (start_x, self.ceiling_offset, grid_width, 6)
        )

        # murs
        pygame.draw.rect(self.surface, (200, 200, 200),
                         (start_x - r, 0, r, self.virtual_height))

        pygame.draw.rect(self.surface, (200, 200, 200),
                         (start_x + grid_width - r + 20, 0, r, self.virtual_height))

        # jeu
        if self.game_over:
            self.draw_game_over()
        else:
            if self.Bubble.vx == 0 and self.Bubble.vy == 0 and not self.paused:
                self.draw_aim(self.surface)

            self.Bubble.draw(self.surface)
            self.next_bubble.draw(self.surface)

            if self.show_level_time and self.show_timer > 0 and len(self.level_times) > 0:
                font = pygame.font.SysFont(None, 60)

                txt = font.render(
                    f"Temps: {round(self.level_times[-1], 1)} s",
                    True,
                    (255, 255, 255)
                )

                x = self.virtual_width // 2 - txt.get_width() // 2
                y = self.virtual_height // 2 - 40

                self.surface.blit(txt, (x, y))

            if self.paused:
                font = pygame.font.SysFont(None, 80)
                txt = font.render("PAUSED", True, (255, 255, 0))

                x = self.virtual_width // 2 - txt.get_width() // 2
                y = self.virtual_height // 2

                self.surface.blit(txt, (x, y))



            self.draw_ui(self.surface)


        # affichage de l'écran
        scaled = pygame.transform.scale(
            self.surface,
            (self.screen.get_width(), self.screen.get_height())
        )
        self.screen.blit(scaled, (0, 0))

        pygame.display.flip()

    def auto_shoot(self):
        best_angle = None
        best_score = -9999

        for angle in range(-75, -15, 3):
            rad = math.radians(angle)

            vx = math.cos(rad) * 300
            vy = math.sin(rad) * 300

            x, y = self.Bubble.get_position()

            for _ in range(120):  # simulation plus longue
                x += vx * 0.03
                y += vy * 0.03

                #  rebond mur
                if x <= self.physics.wall_left or x >= self.physics.wall_right:
                    vx *= -1

                #  collision plafond
                if y <= self.ceiling_offset:
                    score = self.evaluate_position(x, y)
                    break

                #  collision bulles
                for row in self.grid.grid:
                    for b in row:
                        bx, by = b.get_position()
                        dist = math.sqrt((x - bx) ** 2 + (y - by) ** 2)

                        if dist < self.grid.bubble_radius * 2.2:
                            score = self.evaluate_position(x, y)
                            break
                    else:
                        continue
                    break
                else:
                    continue

                break

            if score > best_score:
                best_score = score
                best_angle = rad

        if best_angle:
            self.Bubble.vx = math.cos(best_angle) * 300
            self.Bubble.vy = math.sin(best_angle) * 300

    def evaluate_position(self, x, y):
        score = 0

        for row in self.grid.grid:
            for bubble in row:
                bx, by = bubble.get_position()

                dist = math.sqrt((x - bx) ** 2 + (y - by) ** 2)

                if dist < self.grid.bubble_radius * 2.2:

                    # même couleur
                    if bubble.color == self.Bubble.color:
                        score += 50

                    # proche
                    score += max(0, 100 - dist)

                    # plus haut
                    score += (600 - by) * 0.1

        return score


