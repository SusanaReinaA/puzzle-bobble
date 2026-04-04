import pygame
import random
import math
from collections import deque
from Bubble import Bubble
from FrontEnd.ui.Styles import BUBBLE_COLORS, BUBBLE_SIZE


class Grid:
    def __init__(self, screen_width):
        self.rows = 8
        self.cols = 10
        self.bubble_radius = BUBBLE_SIZE
        self.screen_width = screen_width
        self.grid = self._generate_grid()

    def _generate_grid(self):
        grid = []
        colors = list(BUBBLE_COLORS.values())

        for row in range(self.rows):
            row_list = []
            cols_in_row = self.cols if row % 2 == 0 else self.cols - 1
            row_width = cols_in_row * self.bubble_radius * 2
            start_x = (self.screen_width - row_width) // 2
            offset_x = self.bubble_radius if row % 2 != 0 else 0

            for col in range(cols_in_row):
                x = start_x + col * self.bubble_radius * 2 + self.bubble_radius + offset_x
                y = row * self.bubble_radius * 2 + self.bubble_radius
                color = random.choice(colors)
                bubble = Bubble(y, x, self.bubble_radius, color)
                row_list.append(bubble)

            grid.append(row_list)
        return grid

    def attach_bubble(self, bubble):
        bx, by = bubble.get_position()
        row_index = round((by - self.bubble_radius) / (self.bubble_radius * 2))
        row_index = max(0, min(row_index, self.rows - 1))
        new_bubble = Bubble(by, bx, bubble.radius, bubble.color)
        self.grid[row_index].append(new_bubble)
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
                    if distance < self.bubble_radius * 2.2 and other.color == target_color:
                        queue.append(other)

        return group

    def remove_group(self, group):
        for row in self.grid:
            for bubble in group:
                if bubble in row:
                    row.remove(bubble)

    def draw(self, surface):
        for row in self.grid:
            for bubble in row:
                x, y = bubble.get_position()
                pygame.draw.circle(surface, bubble.color, (int(x), int(y)), self.bubble_radius)
    def is_game_over(self, limit_y):
        for row in self.grid:
            for bubble in row:
                _, y = bubble.get_position()
                if y > limit_y:
                    return True
            return False

