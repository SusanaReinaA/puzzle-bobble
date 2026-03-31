from puzzle_bobble.BackEnd.Bubble import Bubble


class Grid:
    def __init__(self, rows, cols, radius):
        self.rows = rows
        self.cols = cols
        self.radius = radius
        self.grid = [[None for _ in range(cols)] for _ in range(rows)]

    def add_bubble(self, row, col, color):  # ✅ ESTE MÉTODO FALTA
        bubble = Bubble(row, col, self.radius, color)
        self.grid[row][col] = bubble

    def draw(self, surface):
        for row in self.grid:
            for bubble in row:
                if bubble:
                    bubble.draw(surface)


