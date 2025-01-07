from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING
from grid import Grid

if TYPE_CHECKING:
    from model_view import Viewer
    from rulesets import Ruleset

class Model:
    running: bool = True
    generation: int = 0

    def __init__(self, _viewer: Viewer, _fps: int, _ruleset: Ruleset, _total_generations=-1, _width=50, _height=50):
        self.fps = _fps
        self.viewer = _viewer
        self.grid_model = Grid(_ruleset, _width, _height)
        self.viewer.resize_viewer(_width, _height)
        self.total_generations = _total_generations

    def step(self) -> bool:
        """
        takes a step in the game loop
        grid -> calculates next generation
        viewer -> tells viewer to render
        """
        # model tells grid and viewer to update
        # returns true if there are more simulations to run
        if self.generation == self.total_generations:
            self.viewer.cleanup()
            return False
        if not self.running:
            return True
        self.generation += 1
        self.grid_model.calculate_next_generation()
        self.viewer.update(self.grid_model)
        return True

    def toggle_cell(self, x: int, y: int):
        """
        updates grid's cell to toggle on or off
        """
        self.grid_model.cells[y][x].toggle()

    def increment_grid_size(self, n: int):
        """
        takes grid of size n x n and transforms it to n + (-1/1) x n + (-1/1)
        """
        new_grid_size = self.grid_model.width + n
        if new_grid_size <= 0: return

        self.set_grid_size(new_grid_size, new_grid_size)

    def reset_grid(self):
        # overwrite old grid_model
        self.grid_model = Grid(
            _ruleset=self.grid_model.ruleset,
            _width=self.grid_model.width,
            _height=self.grid_model.height
        )   

    def set_grid_size(self, grid_width: int, grid_height: int):
        """
        update's grid size property.
        this should wipe all cells and create new cells
        new cells will need new width,height based on grid/screen size
        """
        # overwrite old grid_model
        self.grid_model = Grid(
            _ruleset=self.grid_model.ruleset,
            _width=grid_width,
            _height=grid_height,
        )
        # update viewer accordingly
        self.viewer.resize_viewer(grid_width, grid_height)

    def set_ruleset(self, ruleset: Ruleset):
        """
        give grid a new ruleset for calculating next gen
        """
        self.grid_model.set_ruleset(ruleset)

    def set_fps(self):
        """
        setter for fps. changes how often step is called
        """
        # unsure of how to implement this as it's outside of scope of model due to main game loop being ran by pygame
        pass

    def toggle_pause_resume(self):
        """
        sets game state to paused or running
        """
        self.running = not self.running

    def set_viewer(self, _viewer: Viewer):
        self.viewer = _viewer
        self.viewer.set_model(self)