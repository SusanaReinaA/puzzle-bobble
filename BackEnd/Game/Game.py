
from puzzle_bobble.BackEnd.Grid import Grid
from puzzle_bobble.FrontEnd.ui.Styles import BUBBLE_COLORS
from puzzle_bobble.BackEnd.Level import Level


class Game:
    def __init__(self):
        self.grid = Grid(8, 6, 20)
        self.init_bubbles()   #

        self.levels=[
            Level(1, "images/level1.png"),
            Level(2, "images/level2.png"),
            Level(3, "images/level3.png")]

        self.current_level_index=0
        self.current_level=self.levels[self.current_level_index]

        self.init_bubbles()

    def init_bubbles(self):   #
        self.grid.add_bubble(0, 0,BUBBLE_COLORS["red"])
        self.grid.add_bubble(0, 1,BUBBLE_COLORS["red"])
        self.grid.add_bubble(0, 2,BUBBLE_COLORS["blue"])
        self.grid.add_bubble(1, 0, BUBBLE_COLORS["yellow"])
        self.grid.add_bubble(1, 1, BUBBLE_COLORS["purple"])
        self.grid.add_bubble(1, 2, BUBBLE_COLORS["green"])
        self.grid.add_bubble(2, 0, BUBBLE_COLORS["yellow"])
        self.grid.add_bubble(2, 1, BUBBLE_COLORS["purple"])

    def next_level(self):
        self.current_level_index+=1

        if self.current_level_index<len(self.levels):
            self.current_level=self.levels[self.current_level_index]

    def draw(self,surface):   #
        self.grid.draw(surface)
