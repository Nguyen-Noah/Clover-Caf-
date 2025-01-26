from .component import Component
from ..primitives.vec3 import vec3
from ..primitives.vec4 import vec4

# what is this for? delete if not needed

class RigidBody(Component):
    def __init__(self):
        super().__init__()
        self.collider_type = 0
        self.friction = 0.8
        self.velocity = vec3(0, 0.5, 0)
        self.temp = vec4(0, 0, 0, 0)
        print('sdfljh')

    def serialize(self):
        data = super().serialize()
        data.update({
            "collider_type": self.collider_type,
            "friction": self.friction,
            "velocity": self.velocity.serialize(),
            "temp": self.temp.serialize()
        })
        return data

    @classmethod
    def deserialize(cls, data):
        instance = cls()

        instance.collider_type = data.get("collider_type", 0)
        instance.friction = data.get("friction", 0.8)
        velocity_data = data.get("velocity", {})
        instance.velocity = vec3.deserialize(velocity_data)
        temp_data = data.get("temp", {})
        instance.temp = vec4.deserialize(temp_data)
        
        return instance