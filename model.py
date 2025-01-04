from __future__ import annotations
from dataclasses import dataclass
from typing import List, TYPE_CHECKING
from events import Event

if TYPE_CHECKING:
    from grid import Grid
    from model_view import Viewer
    from rulesets import Ruleset
    from events import EventDispatch

class Model:
    fps: int
    running: bool = True

    def __init__(self, _event_dispatch: EventDispatch, _fps: int):
        self.event_dispatch = _event_dispatch
        self.fps = _fps

        # add event listeners for controller here!
        # self.event_dispatch.add_listener


    def step(self) -> None:
        """
        takes a step in the game loop
        grid -> calculates next generation
        viewer -> tells viewer to render
        """
        self.event_dispatch.dispatch(Event("calculate_next_generation", None))

        # model tells grid to update
        # grid emits event for viewer to update

        # self.grid_model.calculate_next_generation()
        # self.viewer.update()

    def toggle_cell(self, x: int, y: int) -> None:
        """
        updates grid's cell to toggle on or off
        """
        # THIS CAN BE EMIITED BY THE CONTROLLER NOW !
        pass
        # self.event_dispatch.dispatch(Event("toggle_cell", {"y": y, "x": x}))



        # self.grid_model.cells[y][x].toggle()

    def set_grid_size(self, grid_width: int, grid_height: int) -> None:
        """
        update's grid size property.
        this should wipe all cells and create new cells
        new cells will need new width,height based on grid/screen size
        """
        # THIS CAN BE EMMITED DIRECTLY FROM 
        pass
        # overwrite old grid_model
        self.grid_model = Grid(
            ruleset=self.grid_model.ruleset,
            width=grid_width,
            height=grid_height,
        )
        # update viewer accordingly
        self.viewer.resize_viewer()

    def set_ruleset(self, ruleset: Ruleset) -> None:
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

    def set_viewer(self, _viewer: Viewer) -> None:
        self.viewer = _viewer
        self.viewer.set_model(self)