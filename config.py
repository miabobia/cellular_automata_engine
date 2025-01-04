import palletes

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

    def update_pallete_index(self, n: int) -> None:
        # update pallete index and current pallete 
        self.data["pallete_index"] += n
        if self.data["pallete_index"] >= len(self.pallete_set):
            self.data["pallete_index"] = 0
        elif self.data["pallete_index"] < 0:
            self.data["pallete_index"] = len(self.pallete_set) - 1
        
        self.data["pallete"] = self.pallete_set[self.data["pallete_index"]]