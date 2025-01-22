from engine.utils.elements import Element
from engine.animations.frame import Frame
from engine.components.sprite import Sprite


class AnimationState(Element):
    def __init__(self, title=None):
        super().__init__()
        self.title = title
        self.animation_frames = []
        self.default_sprite = Sprite(self.e['Assets'].get_texture('placeholder.png'), 16, 16)
        self.time = 0.0
        self.current_sprite = 0
        self.loop = True

    def add_frame(self, sprite, frame_time):
        self.animation_frames.append(Frame(sprite, frame_time))

    def get_current_sprite(self):
        if self.current_sprite < len(self.animation_frames):
            return self.animation_frames[self.current_sprite].sprite

    def update(self, dt):
        if self.current_sprite < len(self.animation_frames):
            self.time -= dt
            if self.time <= 0:
                if self.current_sprite != len(self.animation_frames) - 1 or self.loop:
                    self.current_sprite = (self.current_sprite + 1) % len(self.animation_frames)
                self.time = self.animation_frames[self.current_sprite].frame_time

    def serialize(self):
        data = {
            "title": self.title,
            "time": self.time,
            "default_sprite": self.default_sprite.serialize() if self.default_sprite is not None else None,
            "loop": self.loop

        }

        frames_data = []
        for frame in self.animation_frames:
            frames_data.append(frame.serialize())

        data["animation_frames"] = frames_data

        return data

    @classmethod
    def deserialize(cls, data):
        state = cls()

        state.title = data.get('title')
        state.loop = data.get('loop', False)

        state.default_sprite = Sprite.deserialize(data.get('default_sprite'))

        frames_data = data.get('animation_frames', [])
        for frame in frames_data:
            state.animation_frames.append(Frame.deserialize(frame))

        return state