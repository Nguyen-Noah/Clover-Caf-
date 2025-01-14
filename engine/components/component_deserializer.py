def register_component(cls):
    component_registry[cls.__name__] = cls
    return cls

component_registry = {}

def deserialize_component(data):
    component_type = data['type']
    if component_type in component_registry:
        return component_registry[component_type].deserialize(data)
    else:
        raise ValueError(f'Unknown component type: {component_type}')