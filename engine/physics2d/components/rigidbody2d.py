import math

import pymunk

from engine.components.component import Component
from engine.physics2d.enums import BodyType
from engine.primitives import vec2


class RigidBody2D(Component):
    def __init__(self):
        super().__init__()
        self.velocity = vec2()
        self.angular_damping = 0.8
        self.linear_damping = 0.9
        self.mass = 0
        self.body_type = BodyType.DYNAMIC

        self.fixed_rotation = False
        self.continuous_colision = True
        self.raw_body = None

    def update(self, dt):
        if self.raw_body is not None:
            self.entity.transform.position = vec2(self.raw_body.position.x, self.raw_body.position.y)
            self.entity.transform.rotation = math.degrees(self.raw_body.angle)