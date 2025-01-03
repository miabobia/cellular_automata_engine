# controller receives user input
# controller pushes payload to config handler
# config handler makes change in global config obj
# config handler sets event flag to true
# model subscribes to config handler
# model checks config handler event flag
# if eventflag model reads event and transforms model logic

import pygame
import config
import model
from typing import Tuple

class Controller():

    def __init__(self, _display_config: config.DisplayConfig, _model: model.Model):
        self.display_config = _display_config
        self.model = _model
        self.key_pressed = {"d": False, "s": False}

    def read_input(self):
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
            
                # `d` increments the pallete index
                if event.key == pygame.K_d and not self.key_pressed["d"]:
                    self.key_pressed["d"] = True
                    print('pushing increment event +1')
                    self.display_config.update_pallete_index(1)
                    # self.push_event("pallete_increment", {"increment_val": 1})

                # `s` decrements the pallete index
                elif event.key == pygame.K_s and not self.key_pressed["s"]:
                    self.display_config.update_pallete_index(-1)
                    # self.key_pressed["s"] = True
                    # self.push_event("pallete_increment", {"increment_val": -1})
            
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_d:
                    self.key_pressed["d"] = False

                if event.key == pygame.K_s:
                    self.key_pressed["s"] = False
    
    def push_event(self, action: str, payload: dict):
        self.config_handler.set_event(action, payload)

    
    
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