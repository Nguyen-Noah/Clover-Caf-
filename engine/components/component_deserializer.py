from .sprite_renderer import SpriteRenderer

component_registry = {
    "SpriteRenderer": SpriteRenderer
}

def deserialize_component(data):
    component_type = data['type']
    if component_type in component_registry:
        return component_registry[component_type].deserialize(data)
    else:
        raise ValueError(f'Unknown component type: {component_type}')