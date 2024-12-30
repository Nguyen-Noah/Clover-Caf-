from ..utils.elements import Element
from ..utils.assets import load_texture

class Texture(Element):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.load_texture(self.path)
        
    def load_texture(self, path):
        self.texture = load_texture(path, self.e['Game'].ctx)
        self.width = self.texture.width
        self.height = self.texture.height
        self.size = self.texture.size

    def serialize(self):
        return {
            "path": self.path,
            "width": self.width,
            "height": self.height
        }
    
    @classmethod
    def deserialize(cls, data):
        texture = cls(data['path'])
        return texture