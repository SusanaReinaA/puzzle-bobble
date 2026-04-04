import math

class Physics:
    def __init__(self, speed=300):
        self.speed = speed

    def shoot(self, bubble, target_x, target_y):
        bx, by = bubble.get_position()

        dx = target_x - bx
        dy = target_y - by

        angle = math.atan2(dy, dx)

        bubble.vx = self.speed * math.cos(angle)
        bubble.vy = self.speed * math.sin(angle)

    def handle_wall_collision(self, bubble, screen_width):
        x, y = bubble.get_position()

        # mur gauche
        if x - bubble.radius <= 0:
            bubble.vx *= -1

        # mur droit
        if x + bubble.radius >= screen_width:
            bubble.vx *= -1

    def handle_ceiling_collision(self, bubble):
        _, y = bubble.get_position()

        if y - bubble.radius <= 0:
            bubble.vx = 0
            bubble.vy = 0

    def handle_bubble_collision(self, bubble, grid):
        bx, by = bubble.get_position()

        for row in grid.grid:
            for grid_bubble in row:
                gx, gy = grid_bubble.get_position()

                dx = bx - gx
                dy = by - gy
                distance = math.sqrt(dx**2 + dy**2)

                if distance < bubble.radius * 2:
                    return True

        return False