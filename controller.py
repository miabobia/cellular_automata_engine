from __future__ import annotations
import pygame
from typing import TYPE_CHECKING, Tuple

if TYPE_CHECKING:
    from model import Model
    from model_view import Viewer
    from config import DisplayConfig

class Controller():
    def __init__(self, _model: Model, _viewer: Viewer, _config: DisplayConfig):
        self.key_pressed = {
            "d": False, "s": False,
            "z": False, "x": False,
            " ": False, "r": False
        }
        self.mouse_pressed = {
            "left": False,
            "right": False,
            "middle": False
        }
        self.model = _model
        self.viewer = _viewer
        self.config = _config
        self.mouse_mode = 0

    def read_input(self):
        for event in pygame.event.get():

            # key press event handling
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

                elif event.key == pygame.K_SPACE and not self.key_pressed[" "]:
                    self.key_pressed[" "] = True
                    self.model.toggle_pause_resume()

                elif event.key == pygame.K_r and not self.key_pressed["r"]:
                    self.key_pressed["r"] = True
                    self.model.reset_grid()
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.key_pressed["d"] = False

                if event.key == pygame.K_s:
                    self.key_pressed["s"] = False

                if event.key == pygame.K_z:
                    self.key_pressed["z"] = False

                if event.key == pygame.K_x:
                    self.key_pressed["x"] = False

                if event.key == pygame.K_SPACE:
                    self.key_pressed[" "] = False

                if event.key == pygame.K_r:
                    self.key_pressed["r"] = False
            
            # mouse press event handling
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                left, middle, right = pygame.mouse.get_pressed()

                cell_x, cell_y = self.mouse_to_grid_pos(pygame.mouse.get_pos())
                if self.model.grid_model.cells[cell_y][cell_x].state:
                    self.mouse_mode = 0
                else:
                    self.mouse_mode = 1
                if left and not self.mouse_pressed["left"]:
                    self.mouse_pressed["left"] = True

                if right and not self.mouse_pressed["right"]:
                    self.mouse_pressed["right"] = True

                if middle and not self.mouse_pressed["middle"]:
                    self.mouse_pressed["middle"] = True
            
            elif event.type == pygame.MOUSEBUTTONUP:
                self.mouse_pressed["left"], self.mouse_pressed["right"], self.mouse_pressed["middle"] = pygame.mouse.get_pressed()

            if self.mouse_pressed["left"]:
                cell_x, cell_y = self.mouse_to_grid_pos(pygame.mouse.get_pos())
                self.model.toggle_cell(cell_x, cell_y, self.mouse_mode)

    def mouse_to_grid_pos(self, mouse_pos: Tuple[int, int]) -> Tuple[int, int]:
        return (int(mouse_pos[0]//self.viewer.cell_width), int(mouse_pos[1]//self.viewer.cell_height))