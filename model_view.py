from typing import List
import model
import pygame as pg
import palletes
import PIL
from pathlib import Path
import cv2
import os
from datetime import datetime


class GridView:

    def __init__(self, _grid: model.Grid, _screen: pg.surface, _pallete: palletes.ColorPallete):
        self.grid = _grid
        self.grid.add_observer(self)

        # use screen to preprocess math for cell size
        self.screen = _screen
        self.screen_size = self.screen.get_size()
        self.cell_width = self.screen_size[0]/self.grid.width
        self.cell_height = self.screen_size[1]/self.grid.height

        self.pallete = _pallete

    def update(self) -> None:
        self.render(self.grid)

    def set_pallete(self, pallete: palletes.ColorPallete):
        self.pallete = pallete

    def render(self, grid: model.Grid) -> None:
        for i, row in enumerate(grid.cells):
            for j, cell in enumerate(row):
                # cell = grid.cells[i][j]
                c = [cell.state * 255] * 3
                c = self.pallete.get_color(cell.state)
                r = pg.Rect(j * self.cell_width, i * self.cell_height, self.cell_width, self.cell_height)
                pg.draw.rect(self.screen, c, r)

class ExportView:

    def __init__(self, _grid: model.Grid, _screen: pg.surface, _pallete: palletes.ColorPallete):
        self.grid = _grid
        self.grid.add_observer(self)

        # use screen to preprocess math for cell size
        self.screen = _screen
        self.screen_size = self.screen.get_size()
        self.cell_width = self.screen_size[0]/self.grid.width
        self.cell_height = self.screen_size[1]/self.grid.height
        self.pallete = _pallete

        Path(f'frames').mkdir(parents=True, exist_ok=True)
        self.image_counter = 0

    def update(self) -> None:
        self.render(self.grid)

    def set_pallete(self, pallete: palletes.ColorPallete):
        self.pallete = pallete

    def render(self, grid: model.Grid) -> None:
        for i, row in enumerate(grid.cells):
            for j, cell in enumerate(row):
                c = [cell.state * 255] * 3
                c = self.pallete.get_color(cell.state)
                r = pg.Rect(j * self.cell_width, i * self.cell_height, self.cell_width, self.cell_height)
                pg.draw.rect(self.screen, c, r)
        self.save_image()

    def save_image(self):
        print(f'saving image to frames/{self.image_counter}.JPEG')
        pg.image.save(self.screen, f'frames/{self.image_counter}.JPEG')
        self.image_counter += 1

    def compile_frames(self, fps: int):
        transformed_frames = [f'frames/{frame}' for frame in os.listdir('frames')]
        img = list(map(cv2.imread, [f for f in transformed_frames]))

        # ensure there are images
        if not img:
            print("No images found!")
            return
        
        height, width, _ = img[0].shape
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        Path(f'output').mkdir(parents=True, exist_ok=True)

        video = cv2.VideoWriter(f'output/video.mp4', fourcc, fps, (width, height))

        for frame in img:
            video.write(frame)
        
        cv2.destroyAllWindows()
        video.release()

        self.cleanup_frames('frames/')

    def cleanup_frames(self, output_dir: str):
        file_list = os.listdir(output_dir)
        file_count = len(file_list)
        for filename in file_list:
            file_path = os.path.join(output_dir, filename)		
            if os.path.isfile(file_path):
                os.remove(file_path)

        return file_count