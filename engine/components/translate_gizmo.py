from engine.components.gizmo import Gizmo
from engine.components.sprite import Sprite
from engine.utils.game_math import round
from engine.utils.settings import Settings

# IMPLEMENT SNAPPING
class TranslateGizmo(Gizmo):
    def __init__(self, arrow_sprite: Sprite):
        super().__init__(arrow_sprite)
        self.last_dx = 0
        self.last_dy = 0

    def editor_update(self, dt):
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
                self.active_entity.transform.position.x += dx
                if self.snap:
                    self.active_entity.transform.position.x = round(self.e['Mouse'].get_world_x(), Settings.GRID_WIDTH) + (Settings.GRID_WIDTH / 2)
            elif self.y_active and not self.x_active:
                self.active_entity.transform.position.y += dy
                if self.snap:
                    self.active_entity.transform.position.y = round(self.e['Mouse'].get_world_y(), Settings.GRID_HEIGHT) + (Settings.GRID_HEIGHT / 2)

        super().editor_update(dt)