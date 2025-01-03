from dataclasses import dataclass
from typing import List
import model_view
import rulesets
import grid

# @dataclass
# class Cell:
#     x: int
#     y: int
#     state: int
#     next_state: int = 0

#     def set_neighbors(self, _neighbors: List["Cell"]) -> None:
#         self.neighbors = _neighbors

#     def toggle(self) -> None:
#         if self.state:
#             self.state = 1
#         else:
#             self.state = 0

# @dataclass
# class Grid:
#     width: int
#     height: int
#     cells: List[Cell]
#     config_handler: config.ConfigHandler
#     global_config: config.GlobalConfig
    
#     def set_cell_neighbors(self):
#         for i, row in enumerate(self.cells):
#             for j, cell in enumerate(row):
#                 cell.neighbors = []
#                 for nx, ny in self.ruleset.get_neighbor_pattern():
#                     neighbor_x = (j + nx) % self.width
#                     neighbor_y = (i + ny) % self.height

#                     cell.neighbors.append(self.cells[neighbor_y][neighbor_x])

#     def add_observer(self, _observer) -> None:
#         self.observer = _observer

#     def notify_observer(self) -> None:
#         self.observer.update()

#     def set_ruleset(self, _ruleset: rulesets.Ruleset):
#         self.ruleset = _ruleset

#     def check_config_handler(self):
#         if not self.config_handler.event_flag: return
        
#         # retrieve event and trigger event being toggled off
#         action, payload = self.config_handler.get_event()


#         match action:
#             case "pallete_update":
#                 self.observer.set_pallete(self.read_global_config("pallete"))

#             case _:
#                 print('default case!')


#     def read_global_config(self, key: str):

#         return self.global_config.data.get(key)

#     def calculate_next_generation(self):
#         self.ruleset.next_generation(self.cells)

#         # swap current state with next state
#         for i, row in enumerate(self.cells):
#             for j, col in enumerate(row):
#                 self.cells[i][j].state = self.cells[i][j].next_state

# class DisplayConfig:

#     pallete_set = [
#         palletes.ClassicPallete, palletes.TransPallete,
#         palletes.MatrixPallete, palletes.RetroPallete,
#         palletes.GameBoyPallete, palletes.PastelPinkYellowPallete,
#         palletes.PastelBlueYellowPallete, palletes.BlackRedPallete
#     ]

#     data = {
#         "pallete_index": 0,
#         "pallete": palletes.ClassicPallete
#     }

@dataclass
class Model:

    grid_model: grid.Grid
    fps: int
    running: bool = True
    viewer: model_view.Viewer = None

    def step(self) -> None:
        """
        takes a step in the game loop
        grid -> calculates next generation
        viewer -> tells viewer to render
        """
        self.grid_model.calculate_next_generation()
        self.viewer.update()

    def toggle_cell(self, x: int, y: int) -> None:
        """
        updates grid's cell to toggle on or off
        """
        self.grid_model.cells[y][x].toggle()

    def set_grid_size(self, grid_width: int, grid_height: int) -> None:
        """
        update's grid size property.
        this should wipe all cells and create new cells
        new cells will need new width,height based on grid/screen size
        """
        # overwrite old grid_model
        self.grid_model = grid.Grid(
            ruleset=self.grid_model.ruleset,
            width=grid_width,
            height=grid_height,
        )
        # update viewer accordingly
        self.viewer.resize_viewer()

    def set_ruleset(self, ruleset: rulesets.Ruleset) -> None:
        """
        give grid a new ruleset for calculating next gen
        """
        self.grid_model.set_ruleset(ruleset)

    def set_fps(self) -> None:
        """
        setter for fps. changes how often step is called
        """
        # unsure of how to implement this as it's outside of scope of model due to main game loop being ran by pygame
        pass

    def toggle_pause_resume(self) -> None:
        """
        sets game state to paused or running
        """
        self.running = not self.running

    def set_viewer(self, _viewer: model_view.Viewer) -> None:
        self.viewer = _viewer
        self.viewer.set_model(self)