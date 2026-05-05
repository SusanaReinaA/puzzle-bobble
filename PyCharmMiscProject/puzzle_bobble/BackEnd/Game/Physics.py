import math

class Physics:
    def __init__(self, speed=300):
        self.speed = speed
        self.wall_left = 0
        self.wall_right = 800

    def shoot(self, bubble, target_x, target_y):
        bx, by = bubble.get_position()

        dx = target_x - bx
        dy = target_y - by

        if dy > -10:
            dy = -10

        angle = math.atan2(dy, dx)

        bubble.vx = self.speed * math.cos(angle)
        bubble.vy = self.speed * math.sin(angle)

    def handle_wall_collision(self, bubble, screen_width):
        x, y = bubble.get_position()

        if x - bubble.radius <= self.wall_left:
            bubble.x = self.wall_left + bubble.radius+1
            bubble.vx *= -1

        if x + bubble.radius >= self.wall_right:
            bubble.x = self.wall_right - bubble.radius-1
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

                if distance <= bubble.radius * 2 - 2:
                    return True

        return False