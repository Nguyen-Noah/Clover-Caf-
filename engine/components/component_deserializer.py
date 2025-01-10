from .sprite_renderer import SpriteRenderer
from .rigidbody import RigidBody
from .transform import Transform
from engine.physics2d.components.rigidbody2d import RigidBody2D
from engine.physics2d.components.box2d_collider import Box2DCollider
from engine.physics2d.components.circle_collider import CircleCollider

component_registry = {
    "Transform": Transform,
    "SpriteRenderer": SpriteRenderer,
    "RigidBody2D": RigidBody2D,
    "Box2DCollider": Box2DCollider,
    "CircleCollider": CircleCollider
}

def deserialize_component(data):
    component_type = data['type']
    if component_type in component_registry:
        return component_registry[component_type].deserialize(data)
    else:
        raise ValueError(f'Unknown component type: {component_type}')