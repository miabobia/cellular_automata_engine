from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING
from random import randint

if TYPE_CHECKING:
    from rulesets import Ruleset

@dataclass
class Cell:
    x: int
    y: int
    state: int
    next_state: int = 0
    lifetime: int = 0
    age_factor: int = 5
    age_limit: int = 1000

    def set_neighbors(self, _neighbors: List[Cell]):
        self.neighbors = _neighbors

    def toggle(self):
        if self.state:
            self.state = 0
        else:
            self.state = 1

class Grid:
    def __init__(self, _ruleset: Ruleset, _width: int, _height: int):
        self.ruleset = _ruleset
        self.width = _width
        self.height = _height
        self.init_cells()
        self.set_cell_neighbors()

    def init_cells(self):
        self.cells = []



        for i in range(self.height):
            self.cells.append([])
            for j in range(self.width):
                self.cells[i].append(Cell(j, i, randint(0, 1)))

    def set_cell_neighbors(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.neighbors = []
                for nx, ny in self.ruleset.get_neighbor_pattern():
                    neighbor_x = (j + nx) % self.width
                    neighbor_y = (i + ny) % self.height
                    cell.neighbors.append(self.cells[neighbor_y][neighbor_x])

    def calculate_next_generation(self):
        self.ruleset.next_generation(self.cells)
        # swap current state with next state
        for row in self.cells:
            for cell in row:
                if self.ruleset.use_lifetimes:
                    self.ruleset.lifetime_update(cell)

                cell.state = cell.next_state