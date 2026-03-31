
from puzzle_bobble.BackEnd.Grid import Grid
from puzzle_bobble.FrontEnd.ui.Styles import BUBBLE_COLORS


class Game:
    def __init__(self):
        self.grid = Grid(8, 6, 20)
        self.init_bubbles()   #

    def init_bubbles(self):   #
        self.grid.add_bubble(0, 0,BUBBLE_COLORS["red"])
        self.grid.add_bubble(0, 1,BUBBLE_COLORS["red"])
        self.grid.add_bubble(0, 2,BUBBLE_COLORS["blue"])
        self.grid.add_bubble(1, 0, BUBBLE_COLORS["yellow"])
        self.grid.add_bubble(1, 1, BUBBLE_COLORS["purple"])
        self.grid.add_bubble(1, 2, BUBBLE_COLORS["green"])
        self.grid.add_bubble(2, 0, BUBBLE_COLORS["yellow"])
        self.grid.add_bubble(2, 1, BUBBLE_COLORS["purple"])

    def draw(self, surface):   #
        self.grid.draw(surface)