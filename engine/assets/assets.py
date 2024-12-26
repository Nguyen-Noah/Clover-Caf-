import pygame
from ..utils.elements import ElementSingleton
from ..utils.assets import load_img_dir, pg2tex
from .spritesheets import load_spritesheets

class Assets(ElementSingleton):
    def __init__(self, spritesheet_path=None, colorkey=(0, 0, 0)):
        super().__init__()
        self.spritesheet_path = spritesheet_path
        self.spritesheets = load_spritesheets(spritesheet_path)
        #self.autotile_config = self.parse_autotile_config(read_tjson(spritesheet_path))
        self.images = {}

    def load_folder(self, path, alpha=False, scale=1, colorkey=None):
        collection = path.split('/')[-1]
        self.images[collection] = load_img_dir(path, alpha=alpha, scale=scale, colorkey=colorkey)

    def create_texture_atlas(self, atlas_size=(256, 256)):
        """
        Combines textures from self.images (a nested dictionary) into a texture atlas.
        
        Args:
            atlas_size (tuple): Dimensions of the atlas (width, height).

        Returns:
            moderngl.Texture: The created texture atlas.
            dict: A dictionary of texture coordinates.
        """
        atlas = pygame.Surface(atlas_size, pygame.SRCALPHA)
        atlas.fill((0, 0, 0, 0))  # Transparent background
        coords = {}  # Dictionary to store texture coordinates
        
        # Packing parameters
        x_offset, y_offset = 0, 0
        row_height = 0

        # Process the self.images dictionary
        for category, textures in self.images.items():
            for name, texture in textures.items():
                if not isinstance(texture, pygame.Surface):
                    raise TypeError(f"Expected pygame.Surface, got {type(texture)} for {name}.")

                # Get the texture size
                texture_width, texture_height = texture.get_size()

                # Check if the texture fits in the current row
                if x_offset + texture_width > atlas_size[0]:
                    # Move to the next row
                    x_offset = 0
                    y_offset += row_height
                    row_height = 0

                # Ensure the texture fits in the atlas vertically
                if y_offset + texture_height > atlas_size[1]:
                    raise ValueError("Atlas size is too small to fit all textures.")

                # Blit the texture onto the atlas
                atlas.blit(texture, (x_offset, y_offset))

                # Create a unique key based on category and name
                key = f"{category}/{name}"

                # Store the UV coordinates
                coords[key] = {
                    "x": x_offset,
                    "y": y_offset,
                    "width": texture_width,
                    "height": texture_height,
                    "u_min": x_offset / atlas_size[0],
                    "v_min": y_offset / atlas_size[1],
                    "u_max": (x_offset + texture_width) / atlas_size[0],
                    "v_max": (y_offset + texture_height) / atlas_size[1],
                }

                # Update offsets
                x_offset += texture_width
                row_height = max(row_height, texture_height)

        return pg2tex(atlas, self.e['Renderer'].ctx), coords
