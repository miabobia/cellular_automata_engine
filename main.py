import pygame
from controller import Controller
from model import Model
from config import DisplayConfig
from rulesets import Conway, HighLifeRuleset, WickstretcherParasites, DayNightRuleset
from model_view import Viewer, GridView, ExportView
import sys

def main():
    screen_size = (1000, 1000)
    grid_size = (50, 50)
    total_generations = -1
    
    config = DisplayConfig(_viewer_type=GridView)
    viewer: Viewer = config.viewer_type(screen_size, config)
    game_model = Model(
        _viewer=viewer,
        _fps=60,
        _ruleset=Conway(_use_lifetimes=True),
        _total_generations=total_generations,
        _width=grid_size[0],
        _height=grid_size[1]
    )
    game_controller = Controller(game_model, viewer, config)

    clock = pygame.time.Clock()
    running = True
    while running:
        if viewer.interactable:
            game_controller.read_input()
        if not game_model.step():
            running = False
        clock.tick(game_model.fps)
    sys.exit()

if __name__ == "__main__":
    main()