import math
from .component import Component
from ..primitives import vec2

class EditorCamera(Component):
    def __init__(self, editor_camera):
        super().__init__()
        self.editor_camera = editor_camera
        self.drag_debounce = 0.032
        self.drag_sensitivity = 30
        self.click_origin = vec2()
        self.scroll_sensitivity = 0.01
        self.reset = False
        self.lerp_time = 0

        self.listener = 'middle_click'

    def update(self, dt):
        if self.e['Input'].pressed(self.listener) and self.drag_debounce > 0:
            self.click_origin = self.e['Mouse'].get_world()
            self.drag_debounce -= dt
            return
        elif self.e['Input'].holding(self.listener) and self.e['Mouse'].moved:
            mouse_pos = self.e['Mouse'].get_world()
            delta = mouse_pos - self.click_origin
            self.editor_camera.position -= delta * dt * self.drag_sensitivity
            self.click_origin = self.click_origin * (1 - dt) + mouse_pos * dt

        if self.drag_debounce <= 0 and not self.e['Input'].holding(self.listener):
            self.drag_debounce = 0.032

        if self.e['Mouse'].get_scroll_y() != 0 and self.e['Mouse'].in_viewport_boundary():
            add_value = abs(self.e['Mouse'].get_scroll_y() * self.scroll_sensitivity) ** (
                        1 / self.editor_camera.zoom)
            add_value *= -math.copysign(1.0, self.e['Mouse'].get_scroll_y())
            self.editor_camera.zoom += add_value

        # re-center
        if self.e['Input'].pressed('recenter'):
            self.reset = True

        if self.reset:
            self.editor_camera.position.x += (0.0 - self.editor_camera.position.x) * self.lerp_time
            self.editor_camera.position.y += (0.0 - self.editor_camera.position.y) * self.lerp_time

            self.editor_camera.zoom = self.editor_camera.zoom + (1.0 - self.editor_camera.zoom) * self.lerp_time

            self.lerp_time += 0.1 * dt

            if abs(self.editor_camera.position.x) <= 5 and abs(self.editor_camera.position.y) <= 5:
                self.lerp_time = 0
                self.editor_camera.position = vec2(0, 0)
                self.editor_camera.zoom = 1
                self.reset = False

    def editor_update(self, dt):
        if self.e['Input'].pressed(self.listener) and self.drag_debounce > 0:
            self.click_origin = self.e['Mouse'].get_world()
            self.drag_debounce -= dt
            return
        elif self.e['Input'].holding(self.listener) and self.e['Mouse'].moved:
            mouse_pos = self.e['Mouse'].get_world()
            delta = mouse_pos - self.click_origin
            self.editor_camera.position -= delta * dt * self.drag_sensitivity
            self.click_origin = self.click_origin * (1 - dt) + mouse_pos * dt

        if self.drag_debounce <= 0 and not self.e['Input'].holding(self.listener):
            self.drag_debounce = 0.032

        if self.e['Mouse'].get_scroll_y() != 0 and self.e['Mouse'].in_viewport_boundary():
            add_value = abs(self.e['Mouse'].get_scroll_y() * self.scroll_sensitivity) ** (1 / self.editor_camera.zoom)
            add_value *= -math.copysign(1.0, self.e['Mouse'].get_scroll_y())
            self.editor_camera.zoom += add_value

        # re-center
        if self.e['Input'].pressed('recenter'):
            self.reset = True

        if self.reset:
            self.editor_camera.position.x += (0.0 - self.editor_camera.position.x) * self.lerp_time
            self.editor_camera.position.y += (0.0 - self.editor_camera.position.y) * self.lerp_time
            
            self.editor_camera.zoom = self.editor_camera.zoom + (1.0 - self.editor_camera.zoom) * self.lerp_time

            self.lerp_time += 0.1 * dt

            if abs(self.editor_camera.position.x) <= 0.01 and abs(self.editor_camera.position.y) <= 0.01:
                self.lerp_time = 0
                self.editor_camera.position = vec2(0, 0)
                self.editor_camera.zoom = 1
                self.reset = False