from engine.components.gizmo import Gizmo
from engine.components.sprite import Sprite

class ScaleGizmo(Gizmo):
    def __init__(self, scale_sprite: Sprite):
        super().__init__(scale_sprite)
        self.last_dy = 0
        self.last_dx = 0

    def update(self, dt):
        if self.e['Input'].holding('shift'):
            self.snap = True
        else:
            self.snap = False

        if self.last_dx == self.e['Mouse'].get_world_dx():
            dx = 0
        else:
            self.last_dx = self.e['Mouse'].get_world_dx()
            dx = self.last_dx

        if self.last_dy == self.e['Mouse'].get_world_dy():
            dy = 0
        else:
            self.last_dy = self.e['Mouse'].get_world_dy()
            dy = self.last_dy

        if self.active_entity is not None:
            if self.x_active and not self.y_active:
                self.active_entity.transform.scale.x += dx
            elif self.y_active and not self.x_active:
                self.active_entity.transform.scale.y += dy

        super().update(dt)