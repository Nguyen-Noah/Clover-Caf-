from engine.primitives.vec2 import vec2
from engine.components.sprite import Sprite

class Spritesheet:
    def __init__(self, texture, sprite_width, sprite_height, num_sprites, padding):

        self.texture = texture
        self.sprites = []

        outer_pad = padding
        internal_pad = 2 * padding

        if sprite_width % 2 == 1:
            internal_pad += 1

        current_x = outer_pad                                         # starting at top of image
        current_y = texture.height - sprite_height - outer_pad        # getting the bottom of the sprite
        for i in range(num_sprites):
            if current_x + sprite_width > (self.texture.width - outer_pad):
                current_x = outer_pad
                current_y -= (sprite_height + internal_pad)

                if current_y < 0:
                    break

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

            sprite = Sprite(self.texture, sprite_width, sprite_height, tex_coords=tex_coords)
            self.sprites.append(sprite)

            current_x += (sprite_width + internal_pad)

    def get_sprite(self, index):
        return self.sprites[index]
    
    def size(self):
        return len(self.sprites)
    
    @property
    def width(self):
        return self.texture.width
    
    @property
    def height(self):
        return self.texture.height