from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING
from random import randint
# import rulesets

if TYPE_CHECKING:
    from rulesets import Ruleset

@dataclass
class Cell:
    x: int
    y: int
    state: int
    next_state: int = 0

    def set_neighbors(self, _neighbors: List["Cell"]) -> None:
        self.neighbors = _neighbors

    def toggle(self) -> None:
        if self.state:
            self.state = 1
        else:
            self.state = 0

class Grid:
    def __init__(self, _ruleset: Ruleset, _width: int = 50, _height: int = 50) -> None:
        self.ruleset = _ruleset
        self.width = _width
        self.height = _height
        self.init_cells()

    def init_cells(self) -> None:
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
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                self.cells[i][j].state = self.cells[i][j].next_state