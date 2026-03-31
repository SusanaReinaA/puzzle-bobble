import pygame
from puzzle_bobble.FrontEnd.ui.Styles import BUBBLE_COLORS

class Bubble:
    def __init__(self, row, col, radius, color):
        self.row = row
        self.col = col
        self.radius = radius
        self.color = color   # ✅ usar el color recibido

    def get_position(self):
        x = self.col * self.radius * 2 + self.radius   # ✅ col → x
        y = self.row * self.radius * 2 + self.radius   # ✅ row → y
        return (x, y)

    def draw(self, surface):
        x, y = self.get_position()
        pygame.draw.circle(surface, self.color, (int(x), int(y)), self.radius)