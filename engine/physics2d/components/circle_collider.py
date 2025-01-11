from engine.physics2d.components.collider import Collider

class CircleCollider(Collider):
    def __init__(self, radius=1):
        super().__init__()
        self.radius = radius

    def debug_draw(self):
        self.e['DebugDraw'].add_circle(self.entity.transform.position, self.radius)

    def editor_update(self, dt):
            if self.debug:
                self.debug_draw()

    def update(self, dt):
        if self.debug:
            self.debug_draw()

    def serialize(self):
        data = super().serialize()
        data.update({
            "radius": self.radius
        })
        return data
    
    @classmethod
    def deserialize(cls, data):
        return cls(
            radius=data.get('radius', 1)
        )