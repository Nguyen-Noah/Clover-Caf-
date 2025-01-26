from engine.components.component import Component
from engine.components.scale_gizmo import ScaleGizmo
from engine.editor.game_view_window import GameViewWindow
from engine.rendering.spritesheet import Spritesheet
from engine.components.translate_gizmo import TranslateGizmo

class GizmoSystem(Component):
    def __init__(self, gizmo_sprites):
        super().__init__()
        self.new_components = None
        self.gizmos: Spritesheet = gizmo_sprites
        self.using_gizmo = 0

    def start(self):
        self.new_components = {
            TranslateGizmo: TranslateGizmo(self.gizmos.get_sprite(1)),
            ScaleGizmo: ScaleGizmo(self.gizmos.get_sprite(2))
        }

    def editor_update(self, dt):
        if self.using_gizmo == 0:
            self.entity.get_component(TranslateGizmo).set_using()
            self.entity.get_component(ScaleGizmo).set_not_using()
        elif self.using_gizmo == 1:
            self.entity.get_component(TranslateGizmo).set_not_using()
            self.entity.get_component(ScaleGizmo).set_using()

        if GameViewWindow.is_focused or GameViewWindow.is_hovered:
            if self.e['Input'].pressed('e'):
                self.using_gizmo = 0

            if self.e['Input'].pressed('r'):
                self.using_gizmo = 1