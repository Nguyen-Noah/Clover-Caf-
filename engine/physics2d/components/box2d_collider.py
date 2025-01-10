from engine.physics2d.components.collider import Collider
from engine.primitives import vec2, vec3

class Box2DCollider(Collider):
    def __init__(self, half_size=None, origin=None, offset=None):
        super().__init__(offset)
        self.half_size = half_size if half_size is not None else vec2(1, 1)
        self.origin = origin if origin is not None else vec2()

        self.debug = True

    def debug_draw(self):
        center = self.entity.transform.position + self.offset
        dimensions = self.half_size * 2
        rotation = self.entity.transform.rotation

        # Call your debug drawing function
        self.e['DebugDraw'].add_box_2d(center, dimensions, rotation)

    def editor_update(self, dt):
            if self.debug:
                self.debug_draw()

    def update(self, dt):
        if self.debug:
            self.debug_draw()

    def serialize(self):
        data = super().serialize()
        data.update({
            "half_size": self.half_size.serialize(),
            "origin": self.origin.serialize(),
            "offset": self.offset.serialize()
        })
        return data
    
    @classmethod
    def deserialize(cls, data):
        return cls(
            half_size=vec2.deserialize(data['half_size']),
            origin=vec2.deserialize(data['origin']),
            offset=vec2.deserialize(data['offset'])
        )