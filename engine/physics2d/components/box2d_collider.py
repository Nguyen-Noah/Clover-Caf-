from engine.components.component import Component
from engine.primitives import vec2


class Box2DCollider(Component):
    def __init__(self):
        super().__init__()
        self.half_size = vec2(1, 1)
        self.origin = vec2()
        self.offset = vec2()