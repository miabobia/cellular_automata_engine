from __future__ import annotations
from typing import Tuple, TYPE_CHECKING
import pygame as pg
from pathlib import Path
import cv2
import os
from PIL import Image, ImageDraw

if TYPE_CHECKING:
    from model import Model
    from config import DisplayConfig
    from grid import Grid


class Viewer:
    
    cell_width: int = 0
    cell_height: int = 0

    def __init__(self, _screen_size: Tuple[int, int], _display_config: DisplayConfig):
        self.screen_size = _screen_size
        self.display_config = _display_config
        self.pallete = self.display_config.data["pallete"]
        self.interactable = False
        # self.resize_viewer()

    def set_model(self, _model: Model):
        """
        sets model for Viewer. This is the source
        of truth for the viewer's information about
        the grid model
        """
        self.model = _model
        self.resize_viewer()

    def resize_viewer(self, grid_width: int, grid_height: int):
        """
        whenever changes are made to the grid size
        the viewer needs to update its cell sizes 
        """
        self.cell_width = self.screen_size[0]/grid_width
        self.cell_height = self.screen_size[1]/grid_height

    def update(self, model_grid: Grid):
        self.render(model_grid)

    def update_pallete(self):
        """
        controller will send signal to display config to
        update the pallete. display config will send signal to
        viewer to read new pallete from display config 
        """
        self.pallete = self.display_config.data["pallete"]

    def get_alpha(self, cell):
        return max(255 - 255*cell.lifetime//cell.age_limit, 0)


    def cleanup(self):
        """
        some implementations of Viewer will need to cleanup on exit
        eg: ExportView will need to delete frames it generated
        """
        pass
        
class PyGameView(Viewer):

    def __init__(self, _screen_size: Tuple[int, int], _display_config: DisplayConfig):
        super().__init__(_screen_size, _display_config)

        pg.init()
        self.base_screen = pg.display.set_mode(self.screen_size)
        self.render_screen = pg.Surface(self.screen_size, pg.SRCALPHA)
        self.interactable = True

    def show_screen(self):
        self.base_screen.blit(self.render_screen, (0, 0))
        pg.display.flip()

    def cleanup(self):
        pg.quit()
        return super().cleanup()

class GridView(PyGameView):

    def render(self, model_grid: Grid):
        
        self.base_screen.fill(self.pallete.get_color(0))
        for i, row in enumerate(model_grid.cells):  
            for j, cell in enumerate(row):
                c = self.pallete.get_color(cell.state, self.get_alpha(cell))
                r = pg.Rect(j * self.cell_width, i * self.cell_height, self.cell_width, self.cell_height)
                pg.draw.rect(self.render_screen, c, r)

        self.show_screen()

class ExportView(Viewer):

    def __init__(self, _screen_size: Tuple[int, int], _display_config: DisplayConfig):
        super().__init__(_screen_size, _display_config)
        Path(f'frames').mkdir(parents=True, exist_ok=True)
        self.image_counter = 0

    def render(self, model_grid: Grid):
        # Create fresh image for this frame
        self.image = Image.new('RGB', self.screen_size, color=self.pallete.get_color(0))
        self.draw = ImageDraw.Draw(self.image, 'RGBA')
        
        for i, row in enumerate(model_grid.cells):
            for j, cell in enumerate(row):
                color = self.pallete.get_color(cell.state, self.get_alpha(cell))
                # if i in [0, 1] and j in [0, 1]: print(color)
                # Calculate rectangle coordinates
                x0 = j * self.cell_width
                y0 = i * self.cell_height
                x1 = x0 + self.cell_width
                y1 = y0 + self.cell_height
                # Draw rectangle
                self.draw.rectangle([x0, y0, x1, y1], fill=color, outline=None, width=0)
        
        self.save_image()

    def save_image(self):
        # Ensure frames directory exists
        import os
        os.makedirs('frames', exist_ok=True)
        
        filename = f'frames/{self.image_counter:04d}.png'
        print(f'saving image to {filename}')
        self.image.save(filename, 'PNG', quality=95)
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
    
    def cleanup(self):
        self.compile_frames(15)
        self.cleanup_frames("frames")
        return super().cleanup()