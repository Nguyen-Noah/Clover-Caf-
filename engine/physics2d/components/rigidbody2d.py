import math

import pymunk

from engine.components.component import Component
from engine.physics2d.enums import BodyType
from engine.primitives import vec2

class RigidBody2D(Component):
    def __init__(self, body_type=pymunk.Body.STATIC, mass=1.0, friction=0.5, elasticity=0.5):
        super().__init__()
        self.body_type = body_type
        self.mass = mass
        self.friction = friction
        self.elasticity = elasticity

        self.raw_body = None

    def update(self, dt):
        if self.raw_body is not None:
            self.entity.transform.position = vec2(self.raw_body.position.x, self.raw_body.position.y)
            self.entity.transform.rotation = math.degrees(self.raw_body.angle)
        
    def serialize(self):
        data = super().serialize()
        data.update({
            "body_type": self.body_type,
            "mass": self.mass,
            "friction": self.friction,
            "elasticity": self.elasticity
        })
        return data

    @classmethod
    def deserialize(cls, data):
        return cls(
            body_type=data.get('body_type', pymunk.Body.DYNAMIC),
            mass=data.get('mass', 1.0),
            friction=data.get('friction', 0.5),
            elasticity=data.get('elasticity', 0.5)
        )