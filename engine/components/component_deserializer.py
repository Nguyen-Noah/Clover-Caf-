from .sprite_renderer import SpriteRenderer
from .rigidbody import RigidBody

component_registry = {
    "SpriteRenderer": SpriteRenderer,
    'RigidBody': RigidBody
}

def deserialize_component(data):
    print(data)
    component_type = data['type']
    if component_type in component_registry:
        return component_registry[component_type].deserialize(data)
    else:
        raise ValueError(f'Unknown component type: {component_type}')