import pygame
import random
import math
from collections import deque
from BackEnd.Game.Bubble import Bubble
from FrontEnd.ui.Styles import BUBBLE_COLORS, BUBBLE_SIZE


class Grid:

    def __init__(self, screen_width, allowed_colors):
        self.rows = 8
        self.cols = 10
        self.bubble_radius = BUBBLE_SIZE
        self.screen_width = screen_width
        self.allowed_colors = allowed_colors
        self.wall_left = 0
        self.wall_right = screen_width
        self.grid = self._generate_grid()

    def _generate_grid(self):
        grid = []
        colors = self.allowed_colors
        grid_width = self.cols * self.bubble_radius * 2
        start_x = (self.screen_width - grid_width) // 2

        for row in range(self.rows):
            row_list = []

            offset = 0
            if row % 2 != 0:
                offset = self.bubble_radius

            cols_in_row = self.cols if row % 2 == 0 else self.cols - 1

            for col in range(cols_in_row):
                x = start_x + col * self.bubble_radius * 2 + self.bubble_radius + offset
                y = row * self.bubble_radius * 1.732 + self.bubble_radius

                color = random.choice(colors)
                bubble = Bubble(x, y, self.bubble_radius, color)
                row_list.append(bubble)

            grid.append(row_list)

        return grid

    def attach_bubble(self, bubble):

        bx, by = bubble.get_position()
        r = self.bubble_radius

        best_pos = None
        min_dist = float("inf")

        for row in self.grid:
            for other in row:
                ox, oy = other.get_position()

                candidates = [
                    (ox + 2 * r, oy),
                    (ox - 2 * r, oy),
                    (ox + r, oy + r * 1.732),
                    (ox - r, oy + r * 1.732),
                    (ox + r, oy - r * 1.732),
                    (ox - r, oy - r * 1.732),
                ]

                for nx, ny in candidates:
                    dist = math.sqrt((bx - nx) ** 2 + (by - ny) ** 2)

                    if dist < min_dist:
                        min_dist = dist
                        best_pos = (nx, ny)

        if min_dist > r * 2:
            return None

        new_x, new_y = best_pos

        new_x = max(self.wall_left + r, new_x)
        new_x = min(self.wall_right - r, new_x)

        new_bubble = Bubble(new_x, new_y, bubble.radius, bubble.color)

        inserted = False

        for row in self.grid:
            if len(row) > 0:
                _, ry = row[0].get_position()
                if abs(ry - new_y) < r:
                    row.append(new_bubble)
                    inserted = True
                    break

        if not inserted:
            self.grid.append([new_bubble])

        if best_pos is None:
            return None

        return new_bubble

    def find_group(self, bubble):
        target_color = bubble.color
        visited = []
        queue = deque([bubble])
        group = []

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.append(current)
            group.append(current)

            cx, cy = current.get_position()
            for row in self.grid:
                for other in row:
                    if other in visited:
                        continue
                    ox, oy = other.get_position()
                    distance = math.sqrt((cx - ox)**2 + (cy - oy)**2)
                    if distance < self.bubble_radius * 2.05 and other.color == target_color:
                        queue.append(other)

        return group

    def remove_group(self, group):
        for bubble in group:
            bubble.radius += 5

        pygame.time.delay(50)

        for row in self.grid:
            for bubble in group:
                if bubble in row:
                    row.remove(bubble)

        self.grid =[row for row in self.grid if len(row) > 0]

    def draw(self, surface):
        for row in self.grid:
            for bubble in row:
                x, y = bubble.get_position()
                pygame.draw.circle(surface, bubble.color, (int(x), int(y)), self.bubble_radius)

    def is_game_over(self, limit_y):
        for row in self.grid:
            for bubble in row:
                x, y = bubble.get_position()

                if y + bubble.radius >= limit_y:
                    return True

        return False

    def remove_floating(self):
        from collections import deque

        visited = []
        queue = deque()

        # ajouter toutes les bulles du haut

        if len(self.grid) == 0 or len(self.grid[0]) == 0:
            return

        for bubble in self.grid[0]:
            queue.append(bubble)

        # BFS (bulles connectées au plafond)
        while queue:
            current = queue.popleft()
            if current in visited:
                continue

            visited.append(current)

            cx, cy = current.get_position()

            for row in self.grid:
                for other in row:
                    if other in visited:
                        continue

                    ox, oy = other.get_position()
                    dist = math.sqrt((cx - ox) ** 2 + (cy - oy) ** 2)

                    if dist < self.bubble_radius * 2.05:
                        queue.append(other)

        # supprimer les bulles non connectées
        for row in self.grid:
            for bubble in row[:]:
                if bubble not in visited:
                    row.remove(bubble)

    def get_remaining_colors(self):
        colors = set()

        for row in self.grid:
            for bubble in row:
                colors.add(bubble.color)

        return list(colors)

    def is_empty(self):
        for row in self.grid:
            if len(row) > 0:
                return False
        return True

    def drop_grid(self):
        r = self.bubble_radius

        for row in self.grid:
            for bubble in row:
                bubble.y += r * 1.732

    def set_colors(self, colors):
        for row in self.grid:
            for bubble in row:
                bubble.color = random.choice(colors)