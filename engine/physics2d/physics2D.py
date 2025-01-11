import pymunk, math
from pymunk.vec2d import Vec2d

from engine.physics2d.components.box2d_collider import Box2DCollider
from engine.physics2d.components.circle_collider import CircleCollider
from engine.physics2d.components.rigidbody2d import RigidBody2D
from engine.utils.elements import Element

class Physics2D(Element):
    def __init__(self, is_playing=True):
        super().__init__()
        self.is_playing = is_playing
        self.gravity = Vec2d(0, -10)
        self.space = pymunk.Space()
        self.space.gravity = self.gravity
        self.physics_time = 0.0
        self.physics_timestep = 1 / self.e['Game'].fps

    def add(self, entity):
        rb = entity.get_component(RigidBody2D)
        if rb is not None and rb.raw_body is None:
            transform = entity.transform

            pymunk_body_type = rb.body_type.value

            body = pymunk.Body(rb.mass, pymunk.moment_for_box(rb.mass, (50, 50)), pymunk_body_type)
            body.position = Vec2d(transform.position.x, transform.position.y)
            body.angle = math.radians(transform.rotation)

            collider_shape = None
            if entity.get_component(CircleCollider):
                circle_collider = entity.get_component(CircleCollider)
                collider_shape = pymunk.Circle(body, circle_collider.radius)
            if entity.get_component(Box2DCollider):
                box_collider = entity.get_component(Box2DCollider)
                size = (box_collider.half_size.x * 2, box_collider.half_size.y * 2)
                offset = Vec2d(box_collider.offset.x, box_collider.offset.y)
                collider_shape = pymunk.Poly.create_box(body, size)
                collider_shape.offset = offset

            collider_shape.mass = rb.mass
            collider_shape.friction = rb.friction
            collider_shape.elasticity = rb.elasticity

            self.space.add(body, collider_shape)
            rb.raw_body = body

    def destroy_entity(self, entity):
        rb = entity.get_component(RigidBody2D)
        if rb is not None:
            if rb.raw_body is not None:
                self.space.remove(rb.raw_body)

    def update(self, dt):
        self.physics_time += dt
        if self.physics_time >= 0:
            self.physics_time -= self.physics_timestep
            self.space.step(self.physics_timestep)