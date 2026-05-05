import pygame
import math


class Bubble:
    def __init__(self, x, y, radius, color):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.speed = 300

        self.vx = 0
        self.vy = 0


    def get_position(self):
        return self.x,self.y

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt

    def draw(self, surface):
        x, y = self.get_position()

        pygame.draw.circle(
            surface,
            self.color,
            (int(x), int(y)),
            self.radius
        )