from engine.components.component import Component
from engine.components.non_pickable import NonPickable
from engine.components.sprite_renderer import SpriteRenderer
from engine.components.sprite import Sprite
from engine.components.transform import Transform
from engine.misc.prefabs import Prefabs
from engine.primitives import vec2, vec4


# FIX COLOR SETTING, CURRENTLY CAUSING FPS ISSUES
# GIZMOS DONT WORK WHEN CAMERA IS CHANGED
class Gizmo(Component):
    def __init__(self, arrow_sprite: Sprite):
        super().__init__()
        self.y_active = False
        self.x_active = False
        self.x_axis_color = vec4(1, 0.3, 0.3, 0.5)
        self.x_axis_color_hover = vec4(1, 0, 0, 1)
        self.y_axis_color = vec4(0.3, 1, 0.3, 0.5)
        self.y_axis_color_hover = vec4(0, 1, 0, 1)

        self.x_axis_entity = Prefabs.generate_sprite_object(self.e, arrow_sprite, 16, 48)
        self.y_axis_entity = Prefabs.generate_sprite_object(self.e, arrow_sprite, 16, 48)
        self.x_axis_sprite: SpriteRenderer = self.x_axis_entity.get_component(SpriteRenderer)
        self.y_axis_sprite: SpriteRenderer = self.y_axis_entity.get_component(SpriteRenderer)

        self.x_axis_entity.add_component(NonPickable())
        self.y_axis_entity.add_component(NonPickable())

        self.x_axis_offset = vec2(56, -2)
        self.y_axis_offset = vec2(12, 56)

        self.e['Game'].current_scene.add_entity_to_scene(self.x_axis_entity)
        self.e['Game'].current_scene.add_entity_to_scene(self.y_axis_entity)

        self.gizmo_width = 16
        self.gizmo_height = 48

        self.active_entity = None
        self.using = False
        self.snap = False

    def _set_active(self):
        self.x_axis_sprite.color = self.x_axis_color
        self.y_axis_sprite.color = self.y_axis_color

    def _set_inactive(self):
        self.active_entity = None
        self.x_axis_sprite.color = vec4(0, 0, 0, 0)
        self.y_axis_sprite.color = vec4(0, 0, 0, 0)

    def start(self):
        self.x_axis_entity.transform.rotation = 90
        self.y_axis_entity.transform.rotation = 180
        self.x_axis_entity.transform.z_index = 100
        self.y_axis_entity.transform.z_index = 100
        self.x_axis_entity.set_no_serialize()
        self.y_axis_entity.set_no_serialize()

    def check_x_hover_state(self):
        mouse_pos = vec2(self.e['Mouse'].get_ortho_x(), self.e['Mouse'].get_ortho_y())
        if (self.x_axis_entity.transform.position.x >= mouse_pos.x >= self.x_axis_entity.transform.position.x - self.gizmo_height and
            self.x_axis_entity.transform.position.y <= mouse_pos.y <= self.x_axis_entity.transform.position.y + self.gizmo_width):
            #self.x_axis_sprite.set_color(self.x_axis_color_hover)
            return True

        #self.x_axis_sprite.set_color(self.x_axis_color)
        return False

    def check_y_hover_state(self):
        mouse_pos = vec2(self.e['Mouse'].get_ortho_x(), self.e['Mouse'].get_ortho_y())
        if (self.y_axis_entity.transform.position.x >= mouse_pos.x >= self.y_axis_entity.transform.position.x - self.gizmo_width and
            self.y_axis_entity.transform.position.y >= mouse_pos.y >= self.y_axis_entity.transform.position.y - self.gizmo_height):
            #self.y_axis_sprite.set_color(self.y_axis_color_hover)
            return True

        #self.y_axis_sprite.set_color(self.y_axis_color)
        return False

    def set_using(self):
        self.using = True

    def set_not_using(self):
        self.using = False
        self._set_inactive()

    def enable_snap(self):
        self.snap = True

    def disable_snap(self):
        self.snap = False

    def editor_update(self, dt):
        if not self.using:
            return

        if self.e['Input'].holding('shift'):
            self.snap = True
        else:
            self.snap = False

        self.active_entity = self.e['ImGui'].properties_window.active_entity
        if self.active_entity:
            self._set_active()
        else:
            self._set_inactive()
            return

        x_is_hot = self.check_x_hover_state()
        y_is_hot = self.check_y_hover_state()

        if (x_is_hot or self.x_active) and self.e['Mouse'].is_dragging() and self.e['Input'].holding('left_click'):
            self.x_active = True
            self.y_active = False
        elif (y_is_hot or self.y_active) and self.e['Mouse'].is_dragging() and self.e['Input'].holding('left_click'):
            self.x_active = False
            self.y_active = True

        if self.e['Input'].released('left_click'):
            self.x_active = False
            self.y_active = False

        if self.active_entity is not None:
            self.x_axis_entity.transform.position = self.active_entity.transform.position
            self.y_axis_entity.transform.position = self.active_entity.transform.position

            self.x_axis_entity.transform.position += self.x_axis_offset
            self.y_axis_entity.transform.position += self.y_axis_offset

    def update(self, dt):
        if self.using:
            self._set_inactive()