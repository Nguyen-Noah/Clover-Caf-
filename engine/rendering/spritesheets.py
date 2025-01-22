from typing import Dict

from engine.rendering.spritesheet import Spritesheet


class Spritesheets:
    def __init__(self, spritesheets: Dict[str, Spritesheet]):
        self.spritesheets = spritesheets

    def get_state_sprite(self, state, index):
        return self.spritesheets[state].get_sprite(index)