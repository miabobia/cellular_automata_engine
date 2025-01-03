import palletes
import model_view
from typing import Tuple


class GlobalConfig:

    pallete_set = [
        palletes.ClassicPallete, palletes.TransPallete,
        palletes.MatrixPallete, palletes.RetroPallete,
        palletes.GameBoyPallete, palletes.PastelPinkYellowPallete,
        palletes.PastelBlueYellowPallete, palletes.BlackRedPallete
    ]

    data = {
        "grid_size": (50, 50),
        "pallete_index": 0,
        "pallete": palletes.ClassicPallete
    }

class ConfigHandler:
    event_flag: bool = False
    event: Tuple[str, list] = ()
    config: GlobalConfig = GlobalConfig()

    def set_event(self, action: str, payload: dict):
        # functools partial
        # function handles that live in a default dict
        self.event_flag = True
        # event_type: str
        # event_payload: dict
        self.event = (action, payload)        
        match action:
            case "pallete_increment":
                pallete_index = self.config.data["pallete_index"] + payload["increment_val"]
                if pallete_index > len(self.config.pallete_set) - 1:
                    pallete_index = 0
                elif pallete_index < 0:
                    pallete_index = len(self.config.pallete_set) - 1

                self.config.data["pallete_index"] = pallete_index
                self.config.data["pallete"] = self.config.pallete_set[self.config.data["pallete_index"]]
                event_type = "pallete_update"
                event_payload = []
            
            case _:
                print('default case!')

        self.event = (event_type, event_payload)
    
    def get_event(self) -> Tuple[str, list]:
        # consume event
        self.event_flag = False
        return self.event

class DisplayConfig:
    pallete_set = [
        palletes.ClassicPallete, palletes.TransPallete,
        palletes.MatrixPallete, palletes.RetroPallete,
        palletes.GameBoyPallete, palletes.PastelPinkYellowPallete,
        palletes.PastelBlueYellowPallete, palletes.BlackRedPallete
    ]

    data = {
        "pallete_index": 0,
        "pallete": palletes.ClassicPallete
    }

    def set_viewer(self, _viewer: model_view.Viewer) -> None:
        self.viewer = _viewer

    def update_pallete_index(self, n: int) -> None:
        # update pallete index and current pallete 
        self.data["pallete_index"] += n
        if self.data["pallete_index"] >= len(self.pallete_set):
            self.data["pallete_index"] = 0
        elif self.data["pallete_index"] < 0:
            self.data["pallete_index"] = len(self.pallete_set) - 1
        
        self.data["pallete"] = self.pallete_set[self.data["pallete_index"]]

        # let viewer know there was update
        self.viewer.update_pallete()