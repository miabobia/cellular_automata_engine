from dataclasses import dataclass
from typing import List
import model_view
import rulesets
import config
import palletes

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


    def read_global_config(self, key: str):

        return self.global_config.data.get(key)

    def calculate_next_generation(self):
        self.ruleset.next_generation(self.cells)

        # swap current state with next state
        for i, row in enumerate(self.cells):
            for j, col in enumerate(row):
                self.cells[i][j].state = self.cells[i][j].next_state

class DisplayConfig:

    pallete_set = [
        palletes.ClassicPallete, palletes.TransPallete,
        palletes.MatrixPallete, palletes.RetroPallete,
        palletes.GameBoyPallete, palletes.PastelPinkYellowPallete,
        palletes.PastelBlueYellowPallete, palletes.BlackRedPallete
    ]

    data = {
        "pallete_index": 0,
        "pallete": palletes.ClassicPallete
    }

class Model:

    grid: Grid
    viewer: "Viewer"
    fps: int

    def step(self):
        """
        takes a step in the game loop
        grid -> calculates next generation
        viewer -> tells viewer to render
        """
        pass

    def toggle_cell(self):
        """
        updates grid's cell to toggle on or off
        """
        pass

    def set_grid_size(self):
        """
        update's grid size property.
        this should wipe all cells and create new cells
        new cells will need new width,height based on grid/screen size
        """
        pass

    def set_ruleset(self):
        """
        give grid a new ruleset for calculating next gen
        """
        pass

    def set_fps(self):
        """
        setter for fps. changes how often step is called
        """
        pass

    def toggle_pause_resume(self):
        """
        sets game state to paused or running
        """
        pass

    def emit_view_update(self):
        """
        tells viewer to render
        """
        pass