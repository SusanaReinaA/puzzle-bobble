import pygame
import math


class Bubble:
    def __init__(self, row, col, radius, color):
        self.row = row
        self.col = col
        self.radius = radius
        self.color = color
        self.speed =300

        self.vx = 0
        self.vy = 0

    def find_group(self, bubble):
        """Trouve toutes les bulles connectées de la même couleur"""
        from collections import deque

        target_color = bubble.color
        bx, by = bubble.get_position()

        visited = []
        queue = deque([bubble])
        group = []

        while queue:
            current = queue.popleft()
            if current in visited:
                continue
            visited.append(current)
            group.append(current)

            # chercher les voisins de la même couleur
            cx, cy = current.get_position()
            for row in self.grid:
                for other in row:
                    if other in visited:
                        continue
                    ox, oy = other.get_position()
                    distance = math.sqrt((cx - ox) ** 2 + (cy - oy) ** 2)
                    # voisin = distance proche + même couleur
                    if distance < self.bubble_radius * 2.5 and other.color == target_color:
                        queue.append(other)

        return group

    def remove_group(self, group):
        """Supprime un groupe de bulles de la grille"""
        for row in self.grid:
            for bubble in group:
                if bubble in row:
                    row.remove(bubble)

    def get_position(self):
        x = self.col * self.radius * 2 + self.radius
        y = self.row * self.radius * 2 + self.radius
        return self.col, self.row

    def update(self, dt):
        self.col += self.vx * dt
        self.row += self.vy * dt

    def draw(self, surface):
        x, y = self.get_position()

        pygame.draw.circle(
            surface,
            self.color,
            (int(x), int(y)),
            self.radius
        )