import pygame
from controller import Controller
from model import Model
from config import DisplayConfig
import rulesets
from model_view import Viewer, GridView, ExportView
import sys

pygame.init()

screen_size = (1500, 1500)
screen = pygame.display.set_mode(screen_size)

config = DisplayConfig(_viewer_type=ExportView)
viewer = config.viewer_type(screen, config)
game_model = Model(viewer, 60, rulesets.DayNightRuleset(), 50, 50)
game_controller = Controller(game_model, viewer, config)

timed_simulation = False
frame = 0

# viewer is exporting to video has to be a limited amount of simulations
# and timed_simulation wasn't set manually by user
timed_simulation = not timed_simulation and config.viewer_type == ExportView
# if viewer is exporting to video then we don't render simulations to pygame window
render_simulation = config.viewer_type != ExportView

clock = pygame.time.Clock()
running = True
while running:    
    game_controller.read_input()
    game_model.step()

    if render_simulation:
        screen.fill((255, 0, 0))
        pygame.display.flip()

    clock.tick(60)

    if timed_simulation:
        frame += 1
        if frame == config.total_frames:
            break
viewer.compile_frames(15)
viewer.cleanup_frames("frames")

pygame.quit()
sys.exit()