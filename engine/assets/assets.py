from ..components.spritesheet import Spritesheet
from ..utils.elements import ElementSingleton
from ..rendering.texture import Texture
from ..rendering.shader import Shader

SHADER_PATH = 'engine/rendering/shaders'

class Assets(ElementSingleton):
    def __init__(self, spritesheet_path=None, colorkey=(0, 0, 0)):
        super().__init__()
        self.spritesheet_path = spritesheet_path
        self.shaders = {}
        self.spritesheets = {}
        self.textures = {}

    def get_shader(self, vert, frag):
        name = frag.split('.')[0]
        if name not in self.shaders:
            self.shaders[name] = Shader(f'{SHADER_PATH}/{vert}', f'{SHADER_PATH}/{frag}')
        return self.shaders[name]

    def get_texture(self, resource_name):
        name = resource_name.split('.')[0]
        if name in self.textures:
            return self.textures[name]
        tex = Texture(f'{self.spritesheet_path}/{resource_name}', colorkey=(255, 255, 255))
        #tex = pg2tex(load_img(f'{self.spritesheet_path}/{resource_name}', alpha=True, colorkey=(255, 255, 255)), self.e['Game'].ctx)
        self.textures[name] = tex
        return tex

    def add_spritesheet(self, resource_name, spritesheet: Spritesheet):
        name = resource_name.split('.')[0]
        if name not in self.spritesheets:
            self.spritesheets[name] = spritesheet

    def get_spritesheet(self, resource_name):
        name = resource_name.split('.')[0]
        if name not in self.spritesheets:
            return None
        return self.spritesheets[name]