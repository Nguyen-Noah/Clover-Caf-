from dataclasses import dataclass
from multiprocessing.reduction import duplicate

from engine.components.component_deserializer import register_component
from engine.physics2d.enums import BodyType


class Component:
    ID_COUNTER = 0      # global to component

    def __init__(self):
        self.entity = None  
        self.uid = -1       # unique to object

    def init(max_id):
        Component.ID_COUNTER = max_id

    def start(self):
        pass

    # can be used for things like: weapons breaking sound, hit sounds, etc.
    def destroy(self):
        pass

    def generate_id(self):
        if self.uid == -1:
            self.uid = Component.ID_COUNTER
            Component.ID_COUNTER += 1

    def serialize(self):
        return self.__dict__

@dataclass
@register_component
class RigidBody2DComponent(Component):
    body_type: BodyType = BodyType.DYNAMIC
    mass: float = 1.0
    friction: float = 0.5
    elasticity: float = 0.5
    raw_body = None

    def __post_init__(self):
        super().__init__()
