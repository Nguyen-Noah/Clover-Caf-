from engine.rendering.spritesheet import Spritesheet
from engine.rendering.spritesheets import Spritesheets
from engine.utils.elements import ElementSingleton
from engine.utils.io import load_dir
from engine.rendering.texture import Texture
from engine.rendering.shader import Shader

SHADER_PATH = 'engine/rendering/shaders'    # get this from Game.init() instead

class Assets(ElementSingleton):
    def __init__(self, spritesheet_path=None):
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

    def get_texture(self, resource_name, colorkey=(255, 255, 255)):
        name = resource_name.split('.')[0]
        if name in self.textures:
            return self.textures[name]
        tex = Texture(f'{self.spritesheet_path}/{resource_name}', colorkey=colorkey)
        self.textures[name] = tex
        return tex

    def get_textures(self, directory_name, colorkey=(255, 255, 255)):
        textures = load_dir(f'{self.spritesheet_path}/{directory_name}')

        tex = {}
        for name in textures:
            new_tex = Texture(f'{textures[name]}', colorkey=colorkey)
            self.textures[name] = new_tex
            tex[name] = new_tex
        return tex

    def add_spritesheet(self, resource_name, sprite_width, sprite_height, num_sprites, padding, colorkey=(255, 255, 255)):
        name = resource_name.split('.')[0]
        spritesheet = Spritesheet(self.get_texture(resource_name, colorkey=colorkey), sprite_width, sprite_height, num_sprites, padding)
        if name not in self.spritesheets:
            self.spritesheets[name] = spritesheet

    def add_spritesheets(self, directory_name, sprite_width, sprite_height, num_sprites, padding, colorkey=(255, 255, 255)):
        textures = self.get_textures(directory_name, colorkey=colorkey)
        for tex in textures:
            spritesheet = Spritesheet(textures[tex], sprite_width, sprite_height, num_sprites, padding)
            if tex not in self.spritesheets:
                self.spritesheets[tex] = spritesheet

    def get_spritesheets(self, directory_name):
        spritesheets = {}
        for f in load_dir(f'{self.spritesheet_path}/{directory_name}'):
            if f not in self.spritesheets:
                return None
            spritesheets[f] = self.spritesheets[f]
        return Spritesheets(spritesheets)

    def get_spritesheet(self, resource_name):
        name = resource_name.split('.')[0]
        if name not in self.spritesheets:
            return None
        return self.spritesheets[name]