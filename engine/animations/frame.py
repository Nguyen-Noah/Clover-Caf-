from dataclasses import dataclass

from engine.components.sprite import Sprite


@dataclass
class Frame:
    def __init__(self, sprite=None, frame_time=0):
        self.sprite = sprite
        self.frame_time = frame_time

    def serialize(self):
        return {
            "sprite": self.sprite.serialize(),
            "frame_time": self.frame_time
        }

    @classmethod
    def deserialize(cls, data):
        return cls(sprite=Sprite.deserialize(data['sprite']), frame_time=data['frame_time'])