from dataclasses import dataclass

@dataclass(frozen=True)
class Screen:
    WIDTH: int = 1080
    HEIGHT: int = 720
    RESOLUTION: tuple = (WIDTH, HEIGHT)
    SCALE_RATIO: int = 3
    TITLE: str = "Farming Game Idk the Name Yet"
    FPS: int = 240