import palletes

class DisplayConfig:
    pallete_set = [
        palletes.ClassicPallete, palletes.TransPallete,
        palletes.MatrixPallete, palletes.RetroPallete,
        palletes.GameBoyPallete, palletes.PastelPinkYellowPallete,
        palletes.PastelBlueYellowPallete, palletes.BlackRedPallete
    ]

    data = {
        "grid_size": (50, 50),
        "pallete_index": 0,
        "pallete": palletes.ClassicPallete,
        "screen_size": (500, 500)
    }

    def update_pallete_index(self, inc: int):
        """
        increment or decrement pallete_index based on inc
        adjust current pallete according to new pallete_index
        """
        self.data["pallete_index"] += inc
        if self.data["pallete_index"] > len(self.pallete_set) - 1:
            self.data["pallete_index"] = 0
        elif self.data["pallete_index"] < 0:
            self.data["pallete_index"] = len(self.pallete_set) - 1
        self.change_pallete()

    def change_pallete(self):
        self.data["pallete"] = self.pallete_set[self.data["pallete_index"]]
        pass