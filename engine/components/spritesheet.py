from ..primitives.vec2 import vec2
from .sprite import Sprite

class Spritesheet:
    def __init__(self, texture, sprite_width, sprite_height, num_sprites, padding):
        self.texture = texture

        self.sprites = []

        current_x = 0                                       # starting at top of image
        current_y = texture.height - sprite_height          # getting the bottom of the sprite
        for i in range(num_sprites):
            top_y = (current_y + sprite_height) / texture.height
            right_x = (current_x + sprite_width) / texture.width
            left_x = current_x / texture.width
            bottom_y = current_y / texture.height

            tex_coords = [
                vec2(right_x,   top_y),
                vec2(right_x,   bottom_y),
                vec2(left_x,    bottom_y),
                vec2(left_x,    top_y),
            ]

            sprite = Sprite(self.texture, tex_coords=tex_coords)
            self.sprites.append(sprite)

            current_x += sprite_width + padding
            if (current_x >= self.texture.width):
                current_x = 0
                current_y -= sprite_height + padding

    def get_sprite(self, index):
        return self.sprites[index]