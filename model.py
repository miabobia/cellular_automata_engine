from dataclasses import dataclass
from typing import List
import model_view
import rulesets
import config

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
    config_handler: config.ConfigHandler
    global_config: config.GlobalConfig
    
    def set_cell_neighbors(self):
        for i, row in enumerate(self.cells):
            for j, cell in enumerate(row):
                cell.neighbors = []
                for nx, ny in self.ruleset.get_neighbor_pattern():
                    neighbor_x = (j + nx) % self.width
                    neighbor_y = (i + ny) % self.height

                    cell.neighbors.append(self.cells[neighbor_y][neighbor_x])

    def add_observer(self, _observer) -> None:
        self.observer = _observer

    def notify_observer(self) -> None:
        self.observer.update()

    def set_ruleset(self, _ruleset: rulesets.Ruleset):
        self.ruleset = _ruleset

    def check_config_handler(self):
        if not self.config_handler.event_flag: return
        
        # retrieve event and trigger event being toggled off
        action, payload = self.config_handler.get_event()


        match action:
            case "pallete_update":
                self.observer.set_pallete(self.read_global_config("pallete"))

            
            case _:
                print('default case!')


        # if event_type == "config_update":
        #     # update
        #     if event_payload == ""
        # elif event_type == "model_update":
        #     pass

    def read_global_config(self, key: str):

        return self.global_config.data.get(key)


        

    
    def calculate_next_generation(self):
        self.ruleset.next_generation(self.cells)

        # swap current state with next state
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                self.cells[i][j].state = self.cells[i][j].next_state


