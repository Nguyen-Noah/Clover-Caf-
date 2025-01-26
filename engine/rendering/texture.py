import moderngl
from ..utils.elements import Element
from ..utils.assets import load_texture

class Texture(Element):
    def __init__(self, path="Generated", width=None, height=None, colorkey=(255, 255, 255), blend_filter=(moderngl.LINEAR, moderngl.LINEAR)):
        super().__init__()
        self.path = path
        self.width = None
        self.height = None
        self.size = None

        if path != "Generated":
            self.load_texture(self.path, colorkey=colorkey)
        if width is not None and height is not None:
            self.texture = self.e['Game'].ctx.texture((width, height), 3)
            self.texture.repeat_x = True
            self.texture.repeat_y = True
            self.texture.filter = blend_filter

        self.colorkey=colorkey

    def release(self):
        self.texture.release()

    def load_texture(self, path, colorkey=(255, 255, 255)):
        self.texture = load_texture(path, self.e['Game'].ctx, colorkey=colorkey)
        self.width = self.texture.width
        self.height = self.texture.height
        self.size = self.texture.size

    def get_id(self):
        return self.texture.glo

    def serialize(self):
        return {
            "path": self.path,
            "width": self.width,
            "height": self.height,
            "colorkey": self.colorkey
        }
    
    @classmethod
    def deserialize(cls, data):
        return cls(path=data.get('path'), colorkey=data.get('colorkey', (255, 255, 255)))

    def __eq__(self, other):
        if not isinstance(other, Texture):
            return False
        return (self.path == other.path and
                self.width == other.width and
                self.height == other.height)

    def __hash__(self):
        # Allow instances to be used in sets or as dict keys
        return hash((self.path, self.width, self.height))