from ..utils.elements import ElementSingleton
from ..utils.assets import load_img_dir, create_texture_array
from .spritesheets import load_spritesheets

class Assets(ElementSingleton):
    def __init__(self, spritesheet_path=None, colorkey=(0, 0, 0)):
        super().__init__()
        self.spritesheet_path = spritesheet_path
        self.spritesheets = load_spritesheets(spritesheet_path)
        #self.autotile_config = self.parse_autotile_config(read_tjson(spritesheet_path))
        self.images = {}
        self.tex_arrays = {}

    def load_folder(self, path, alpha=False, scale=1, colorkey=None):
        collection = path.split('/')[-1]
        self.images[collection] = load_img_dir(path, self.e['Renderer'].ctx, alpha=alpha, scale=scale, colorkey=colorkey)

        texture_array, mapping = create_texture_array(self.e['Renderer'].ctx, self.images[collection])
        self.tex_arrays[collection] = {
            'texture_array': texture_array,
            'mapping': mapping
        }