import math
from typing import Tuple
from dataclasses import dataclass

def aspect_ratio(w: int, h: int) -> Tuple[int, int]:
    return w // math.gcd(w, h), h // math.gcd(w, h)

@dataclass(frozen=True)
class Screen:
    WIDTH: int = 1080#13501920#
    HEIGHT: int = 720#9001080#
    RESOLUTION: tuple = (WIDTH, HEIGHT)
    ASPECT_RATIO: tuple = aspect_ratio(WIDTH, HEIGHT)
    SCALE_RATIO: int = 3
    TITLE: str = "Farming Game Idk the Name Yet"
    FPS: int = 240