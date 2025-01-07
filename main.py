import pygame
from controller import Controller
from model import Model
from config import DisplayConfig
import rulesets
from model_view import Viewer, GridView, ExportView
import sys

screen_size = (1500, 1500)

config = DisplayConfig(_viewer_type=GridView)
viewer = config.viewer_type(screen_size, config)
game_model = Model(_viewer=viewer, _fps=60, _ruleset=rulesets.DayNightRuleset(), _total_generations=-1,_width=50, _height=50)
game_controller = Controller(game_model, viewer, config)

clock = pygame.time.Clock()
running = True
while running:    
    game_controller.read_input()
    if not game_model.step(): running = False

    clock.tick(60)
sys.exit()