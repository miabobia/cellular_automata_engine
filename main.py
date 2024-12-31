import pygame
import sys
import model_view
import model
from typing import Tuple
from random import randint
import rulesets
import palletes

# frames cleanup !
# name video

def init_automata(grid_size: Tuple[int], screen: pygame.surface, m_view, ruleset: rulesets.Ruleset, pallete: palletes.ColorPallete) -> Tuple[model.Grid, model_view.GridView]:
    # init cells
    cells = []
    grid_width, grid_height = grid_size
    for i in range(grid_height):
        cells.append([])
        for j in range(grid_width):
            cells[i].append(model.Cell(j, i, randint(0, 1)))

    grid = model.Grid(50, 50, cells)
    grid_view = m_view(grid, screen, pallete)
    grid.set_ruleset(ruleset)
    grid.set_cell_neighbors()

    return (grid, grid_view)

def update_pallete_index(p_index: int, increment: int) -> int:
    p_index += increment
    if p_index > len(pallete_set) - 1: p_index = 0
    return p_index
    
# ===board=dimensions===
screen_size = (2000, 2000)
grid_size = (500, 500)

# ===model=viewer===
model_viewer = model_view.ExportView

# ===ruleset===
ruleset = rulesets.HighLifeRuleset()

# ===pallete===
pallete_set = [
    palletes.ClassicPallete, palletes.TransPallete,
    palletes.MatrixPallete, palletes.RetroPallete,
    palletes.GameBoyPallete, palletes.PastelPinkYellowPallete,
    palletes.PastelBlueYellowPallete, palletes.BlackRedPallete
    ]
pallete_index = 0
pallete = pallete_set[pallete_index]

# ===simulation=timing===
timed_sim = True
timer_end = 500

# ===animation=timer===
pallete_swap_index = 0
pallete_swap_time = 45

# ===fps===
fps = 30
fps_counter = 0
fps_sum = 0

# ===rendering=flags===
render_screen = model_viewer not in [model_view.ExportView]

pygame.init()
screen = pygame.display.set_mode(screen_size)
grid, grid_view = init_automata(grid_size, screen, model_viewer, ruleset, pallete)
pygame.display.set_caption(str(grid.ruleset))
clock = pygame.time.Clock()

key_pressed = {"c": False, "s": False}

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c and not key_pressed["c"]:
                print("Key 'C' pressed!")
                key_pressed["c"] = True

            if event.key == pygame.K_s and not key_pressed["s"]:
                pallete_index = update_pallete_index(pallete_index, 1)
                grid_view.set_pallete(pallete_set[pallete_index])
                key_pressed["s"] = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_c:
                key_pressed["c"] = False

            if event.key == pygame.K_s:
                key_pressed["s"] = False

    grid.calculate_next_generation()
    grid.notify_observer()

    if render_screen: pygame.display.flip()

    clock.tick(fps)

    fps_counter += 1

    if pallete_swap_time:
        pallete_swap_index += 1
        if pallete_swap_time == pallete_swap_index:
            pallete_index = update_pallete_index(pallete_index, 1)
            grid_view.set_pallete(pallete_set[pallete_index])
            pallete_swap_index = 0

    if timed_sim and fps_counter == timer_end:
        break

if not render_screen: grid_view.compile_frames(fps)

pygame.quit()
sys.exit()
