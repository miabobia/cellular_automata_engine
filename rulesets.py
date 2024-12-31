from abc import ABC, abstractmethod
from typing import List, Tuple
import model

class Ruleset(ABC):
    
    @abstractmethod
    def next_generation(self, grid):
        """
        Computes the next generation of cells based on the current grid state
        using the rules defined by this Ruleset.
        """
        pass

    @abstractmethod
    def get_neighbor_pattern(self) -> List[Tuple]:
        """
        returns a list of tuples which define each Cell's neighbor's relative to its position
        """
        pass

class Conway(Ruleset):

    def next_generation(self, grid):
        for i, row in enumerate(grid):
            for j, col in enumerate(row):
                cell = grid[i][j]
                state = cell.state
                live_neighbors = self.count_live_neighbors(cell)

                if state == 1:
                    if live_neighbors < 2 or live_neighbors > 3:
                        cell.next_state = 0
                    else:
                        cell.next_state = 1
                else:
                    if live_neighbors == 3 or live_neighbors == 6:
                        cell.next_state = 1

    def get_neighbor_pattern(self):
        return [
            (-1, -1), (-1, 0), (-1, 1),  # Top row
            (0, -1),           (0, 1),     # Middle row
            (1, -1), (1, 0), (1, 1)       # Bottom row
        ]

    def count_live_neighbors(self, cell: "Cell") -> int:
        live_count = 0
        for cell in cell.neighbors:
            if cell.state: live_count += 1
        return live_count
    
    def __repr__(self) -> str:
        return "Conway's Game of Life"
  
class HighLifeRuleset(Ruleset):
# https://conwaylife.com/wiki/OCA:HighLife
    def get_neighbor_pattern(self):
        return [
            (-1, -1), (-1, 0), (-1, 1),
            (0, -1),           (0, 1),
            (1, -1), (1, 0), (1, 1)
        ]
    
    def next_generation(self, grid):
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                cell = grid[y][x]
                live_neighbors = self.count_live_neighbors(cell)
                if cell.state:
                    if live_neighbors == 2 or live_neighbors == 3:
                        cell.next_state = 1
                    else:
                        cell.next_state = 0
                else:
                    if live_neighbors == 3 or live_neighbors == 6:
                        cell.next_state = 1
    
    def count_live_neighbors(self, cell: "Cell") -> int:
        live_count = 0
        for cell in cell.neighbors:
            if cell.state: live_count += 1
        return live_count
    
    def __repr__(self) -> str:
        return "HighLife Ruleset"

class DayNightRuleset(Ruleset):
# https://conwaylife.com/wiki/OCA:Day_%26_Night
# cells survive from one generation to the next if they have 3, 4, 6, 7, or 8 neighbours, and are born if they have 3, 6, 7, or 8 neighbours
    def get_neighbor_pattern(self):
        return [
            (-1, -1), (-1, 0), (-1, 1),  # Top row
            (0, -1),           (0, 1),     # Middle row
            (1, -1), (1, 0), (1, 1)       # Bottom row
        ]
    
    def next_generation(self, grid):
        survive_condition = set([3, 4, 6, 7, 8])
        born_condition = set([3, 6, 7, 8])
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                cell = grid[y][x]
                live_neighbors = self.count_live_neighbors(cell)
                if cell.state:
                    if live_neighbors not in survive_condition:
                        cell.next_state = 0
                else: 
                    if live_neighbors in born_condition:
                        cell.next_state = 1
    
    def count_live_neighbors(self, cell: "Cell") -> int:
        live_count = 0
        for cell in cell.neighbors:
            if cell.state: live_count += 1
        return live_count

    def __repr__(self) -> str:
        return "Day & Night Ruleset"

class WickstretcherParasites(Ruleset):
    # https://conwaylife.com/wiki/OCA:Wickstretcher_And_The_Parasites
    def get_neighbor_pattern(self):
        return [
            (-1, -1), (-1, 0), (-1, 1),  # Top row
            (0, -1),           (0, 1),     # Middle row
            (1, -1), (1, 0), (1, 1)       # Bottom row
        ]
    
    def next_generation(self, grid):
        survive_condition = set([0, 1, 2, 3, 4, 5])
        born_condition = set([0, 1, 3, 5, 6])
        for y in range(len(grid)):
            for x in range(len(grid[0])):
                cell = grid[y][x]
                live_neighbors = self.count_live_neighbors(cell)
                if cell.state:
                    if live_neighbors not in survive_condition:
                        cell.next_state = 0
                else: 
                    if live_neighbors in born_condition:
                        cell.next_state = 1

    def count_live_neighbors(self, cell: "Cell") -> int:
        live_count = 0
        for cell in cell.neighbors:
            if cell.state: live_count += 1
        return live_count

    def __repr__(self) -> str:
        return "Wickstretcher And The Parasites Ruleset"
