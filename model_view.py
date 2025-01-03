from typing import List
import model
import pygame as pg
import palletes
from pathlib import Path
import cv2
import os
import config

class Viewer:
    
    cell_width: int = 0
    cell_height: int = 0

    def __init__(self, _screen: pg.surface, _display_config: config.DisplayConfig):
        # use screen to preprocess math for cell size
        self.screen = _screen
        self.screen_size = self.screen.get_size()
        self.display_config = _display_config
        self.pallete = self.display_config.data["pallete"]

    def set_model(self, _model: model.Model) -> None:
        """
        sets model for Viewer. This is the source
        of truth for the viewer's information about
        the grid model
        """
        self.model = _model
        self.resize_viewer()

    def resize_viewer(self) -> None:
        """
        whenever changes are made to the grid size
        the viewer needs to update its cell sizes 
        """
        self.cell_width = self.screen_size[0]/self.model.grid_model.width
        self.cell_height = self.screen_size[1]/self.model.grid_model.height

    def update(self) -> None:
        self.render()

    def update_pallete(self) -> None:
        """
        controller will send signal to display config to
        update the pallete. display config will send signal to
        viewer to read new pallete from display config 
        """
        self.pallete = self.display_config.data["pallete"]
        

class GridView(Viewer):

    def __init__(self, _screen: pg.surface, _display_config: config.DisplayConfig):
        super().__init__(_screen, _display_config)

    def render(self) -> None:
        for i, row in enumerate(self.model.grid_model.cells):
            for j, cell in enumerate(row):
                c = self.pallete.get_color(cell.state)
                r = pg.Rect(j * self.cell_width, i * self.cell_height, self.cell_width, self.cell_height)
                pg.draw.rect(self.screen, c, r)

class ExportView(Viewer):

    def __init__(self, _screen: pg.surface, _display_config: config.DisplayConfig):
        super().__init__(_screen, _display_config)
        Path(f'frames').mkdir(parents=True, exist_ok=True)
        self.image_counter = 0

    def set_pallete(self, pallete: palletes.ColorPallete):
        self.pallete = pallete

    def render(self) -> None:
        for i, row in enumerate(self.model.grid_model.cells):
            for j, cell in enumerate(row):
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