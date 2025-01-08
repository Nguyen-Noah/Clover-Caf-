from engine.components.component import Component


class CircleCollider(Component):
    def __init__(self):
        super().__init__()
        self.radius = 1