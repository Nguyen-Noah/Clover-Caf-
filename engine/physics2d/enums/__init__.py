from enum import Enum
import pymunk

class BodyType(Enum):
    STATIC = pymunk.Body.STATIC
    DYNAMIC = pymunk.Body.DYNAMIC
    KINEMATIC = pymunk.Body.KINEMATIC

    def serialize(self):
        return {
            'body_type': self.name
        }

    @classmethod
    def deserialize(cls, data):
        name = data.get('body_type')
        if name not in cls.__members__:
            raise ValueError(f'{name} is not a valid BodyType')
        return cls[name]