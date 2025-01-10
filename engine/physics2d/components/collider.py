from engine.primitives import vec2
from engine.components.component import Component

class Collider(Component):
    def __init__(self, offset=None):
        super().__init__()
        if offset is None:
            offset = vec2(0, 0)
        self.offset = offset
