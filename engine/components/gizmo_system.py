from engine.components.component import Component
from engine.components.scale_gizmo import ScaleGizmo
from engine.components.spritesheet import Spritesheet
from engine.components.translate_gizmo import TranslateGizmo

class GizmoSystem(Component):
    def __init__(self, gizmo_sprites):
        super().__init__()
        self.gizmos: Spritesheet = gizmo_sprites
        self.using_gizmo = 0

    def start(self):
        self.entity.add_component(TranslateGizmo(self.gizmos.get_sprite(1)))
        self.entity.add_component(ScaleGizmo(self.gizmos.get_sprite(2)))

    def update(self, dt):
        if self.using_gizmo == 0:
            self.entity.get_component(TranslateGizmo).set_using()
            self.entity.get_component(ScaleGizmo).set_not_using()
        elif self.using_gizmo == 1:
            self.entity.get_component(TranslateGizmo).set_not_using()
            self.entity.get_component(ScaleGizmo).set_using()

        if self.e['Input'].pressed('e'):
            self.using_gizmo = 0

        if self.e['Input'].pressed('r'):
            self.using_gizmo = 1