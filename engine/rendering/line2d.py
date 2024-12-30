from ..primitives import vec2
from ..primitives import vec4

class Line2D:
    def __init__(self, fr, to, color, lifetime):
        self.fr = fr
        self.to = to
        self.color = color
        self.lifetime = lifetime

    def begin_frame(self):
        self.lifetime -= 1      # determined in frames
        return self.lifetime
    
    def get_from(self):
        return self.fr
    
    def get_to(self):
        return self.to