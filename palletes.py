from abc import ABC, abstractmethod
import pygame

class ColorPallete(ABC):

    @classmethod
    @abstractmethod
    def get_color(state: int) -> pygame.Color:
        """
        returns color based on cell's current state
        """
        pass

class ClassicPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(0, 0, 0)
            case 1:
                return pygame.Color(255, 255, 255)
            case _:
                return pygame.Color(0, 0, 0)

class TransPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(188, 229, 226)
            case 1:
                return pygame.Color(215, 188, 229)
            case _:
                return pygame.Color(0, 0, 0)

class MatrixPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(0, 0, 0)
            case 1:
                return pygame.Color(0, 255, 0)
            case _:
                return pygame.Color(0, 0, 0)

class RetroPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(0, 0, 0)
            case 1:
                return pygame.Color(255, 0, 0)
            case _:
                return pygame.Color(0, 0, 0)

class GameBoyPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(0, 0, 0)
            case 1:
                return pygame.Color(155, 188, 15)
            case _:
                return pygame.Color(0, 0, 0)

class PastelPinkYellowPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(255, 182, 193)
            case 1:
                return pygame.Color(255, 255, 153)
            case _:
                return pygame.Color(0, 0, 0)

class PastelBlueYellowPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(173, 216, 230)
            case 1:
                return pygame.Color(255, 255, 102)
            case _:
                return pygame.Color(0, 0, 0)

class BlackRedPallete(ColorPallete):
    def get_color(state: int) -> pygame.Color:
        match state:
            case 0:
                return pygame.Color(0, 0, 0)
            case 1:
                return pygame.Color(255, 0, 0)
            case _:
                return pygame.Color(0, 0, 0)
