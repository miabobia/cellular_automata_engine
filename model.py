from dataclasses import dataclass
from typing import List
import model_view
import rulesets

@dataclass
class Cell:
    x: int
    y: int
    state: int
    next_state: int = 0

    def set_neighbors(self, _neighbors: List["Cell"]) -> None:
        self.neighbors = _neighbors

@dataclass
class Grid:
    width: int
    height: int
    cells: List[Cell]
    
    def set_cell_neighbors(self):
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                col.neighbors = []
                for nx, ny in self.ruleset.get_neighbor_pattern():
                    neighbor_x = (j + nx) % self.width
                    neighbor_y = (i + ny) % self.height

                    col.neighbors.append(self.cells[neighbor_y][neighbor_x])

    def add_observer(self, _observer) -> None:
        self.observer = _observer

    def notify_observer(self) -> None:
        self.observer.update()

    def set_ruleset(self, _ruleset: rulesets.Ruleset):
        self.ruleset = _ruleset
    
    def calculate_next_generation(self):
        self.ruleset.next_generation(self.cells)

        # swap current state with next state
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                self.cells[i][j].state = self.cells[i][j].next_state


