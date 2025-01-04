# controller receives user input
# controller pushes payload to config handler
# config handler makes change in global config obj
# config handler sets event flag to true
# model subscribes to config handler
# model checks config handler event flag
# if eventflag model reads event and transforms model logic

from __future__ import annotations
import pygame
from typing import TYPE_CHECKING
from events import Event

if TYPE_CHECKING:
    from model import Model
    from model_view import Viewer
    from config import DisplayConfig

class Controller():

    def __init__(self, _model: Model, _viewer: Viewer, _config: DisplayConfig):
        self.key_pressed = {"d": False, "s": False, "z": False, "x": False}
        self.model = _model
        self.viewer = _viewer
        self.config = _config

    def read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
            
                # `d` increments the pallete index
                if event.key == pygame.K_d and not self.key_pressed["d"]:
                    self.key_pressed["d"] = True
                    self.config.update_pallete_index(1)
                    self.viewer.update_pallete()

                # `s` decrements the pallete index
                elif event.key == pygame.K_s and not self.key_pressed["s"]:
                    self.key_pressed["s"] = True
                    self.config.update_pallete_index(-1)
                    self.viewer.update_pallete()

                # `z` decrements the grid size            
                elif event.key == pygame.K_z and not self.key_pressed["z"]:
                    self.key_pressed["z"] = True
                    self.model.increment_grid_size(1)

                # `x` increments the grid size
                elif event.key == pygame.K_x and not self.key_pressed["x"]:
                    self.key_pressed["x"] = True
                    self.model.increment_grid_size(-1)
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.key_pressed["d"] = False

                if event.key == pygame.K_s:
                    self.key_pressed["s"] = False

                if event.key == pygame.K_z:
                    self.key_pressed["z"] = False

                if event.key == pygame.K_x:
                    self.key_pressed["x"] = False
    
"""
===PAYLOADS===
- toggle the state of a cell
- toggle run state of game (pause/unpause)
- change framerate
- pallete change
- grid size
- go to iteration (n)
- randomize board



what does a payload look like?
{
    function_name -> str,
    parameters -> dict
}
"""