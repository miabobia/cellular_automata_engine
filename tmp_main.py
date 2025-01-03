import pygame
import controller
import model
import config
import grid
import rulesets
import model_view

# make a display config
# make a grid
# make a model (grid, fps)
# make a controller (model, )
# make a viewer

pygame.init()

screen_size = (500, 500)
screen = pygame.display.set_mode(screen_size)

display_config = config.DisplayConfig()
grid_model = grid.Grid(rulesets.Conway())
game_model = model.Model(grid_model=grid_model, fps=60)
game_controller = controller.Controller(display_config, game_model)
game_viewer = model_view.Viewer(_screen=screen, _display_config=display_config)

display_config.set_viewer(game_viewer)
game_model.set_viewer(game_viewer)

# # config_handler = config.ConfigHandler()
# # grid, grid_view = init_automata(grid_size, screen, model_viewer, ruleset, pallete, config_handler)
# # player_controller = controller.Controller(config_handler)
# pygame.display.set_caption(str(grid.ruleset))
# clock = pygame.time.Clock()
# running = True
# while running:
#     player_controller.read_input()

#     grid.check_config_handler()
#     grid.calculate_next_generation()
#     grid.notify_observer()

#     if render_screen: pygame.display.flip()

#     clock.tick(fps)

#     fps_counter += 1

#     if pallete_swap_time:
#         pallete_swap_index += 1
#         if pallete_swap_time == pallete_swap_index:
#             pallete_index = update_pallete_index(pallete_index, 1)
#             grid_view.set_pallete(pallete_set[pallete_index])
#             pallete_swap_index = 0

#     if timed_sim and fps_counter == timer_end:
#         break

# if not render_screen: grid_view.compile_frames(fps)

# pygame.quit()
# sys.exit()