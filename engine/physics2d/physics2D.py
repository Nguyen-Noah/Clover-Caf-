import pymunk, math
from pymunk.vec2d import Vec2d

from engine.physics2d.components.box2d_collider import Box2DCollider
from engine.physics2d.components.circle_collider import CircleCollider
from engine.physics2d.components.rigidbody2d import RigidBody2D
from engine.primitives import vec2
from engine.utils.elements import Element


class Physics2D(Element):
    def __init__(self, is_playing=True):
        super().__init__()
        self.is_playing = is_playing
        self.gravity = vec2(0, -10)
        self.space = pymunk.Space()
        self.space.gravity = self.gravity
        self.physics_time = 0.0
        self.physics_timestep = 1 / self.e['Game'].fps

    def add(self, entity):
        rb = entity.get_component(RigidBody2D)
        if rb is not None and rb.raw_body is None:
            transform = entity.transform

            if rb.body_type == 'Dynamic':
                pymunk_body_type = pymunk.Body.DYNAMIC
            elif rb.body_type == 'Static':
                pymunk_body_type = pymunk.Body.STATIC
            elif rb.body_type == 'Kinematic':
                pymunk_body_type = pymunk.Body.KINEMATIC

            body = pymunk.Body(rb.mass, pymunk.moment_for_box(rb.mass, (50, 50)), pymunk_body_type)
            body.position = vec2(transform.position.x, transform.position.y)
            body.angle = math.radians(transform.rotation)

            body.velocity_func = lambda b, g, d, dt: self._apply_damping(b, g, rb.linear_damping, rb.angular_damping, dt)

            collider_shape = None
            if entity.get_component(CircleCollider):
                circle_collider = entity.get_component(CircleCollider)
                collider_shape = pymunk.Circle(body, circle_collider.radius)
                collider_shape.offset = Vec2d(circle_collider.offset.x, circle_collider.offset.y)
            if entity.get_component(Box2DCollider):
                box_collider = entity.get_component(Box2DCollider)
                size = (box_collider.half_size.x * 2, box_collider.half_size.y * 2)
                offset = Vec2d(box_collider.offset.x, box_collider.offset.y)
                collider_shape = pymunk.Poly.create_box(body, size)
                collider_shape.offset = offset

            self.space.add(body, collider_shape)
            entity.raw_body = rb

    def _apply_damping(self, body, gravity, linear_damping, angular_damping, dt):
        pymunk.Body.update_velocity(body, gravity, linear_damping, dt)
        body.angular_velocity *= (1 - angular_damping * dt)

    def update(self, dt):
        self.physics_time += dt
        if self.physics_time >= self.physics_timestep:
            self.physics_time -= self.physics_timestep
            self.space.step(self.physics_timestep)
