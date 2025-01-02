import math
from .component import Component
from ..utils.elements import ElementSingleton
from ..primitives import vec2

class EditorCamera(Component, ElementSingleton):
    def __init__(self, editor_camera):
        Component.__init__(self)
        ElementSingleton.__init__(self)
        self.editor_camera = editor_camera
        self.drag_debounce = 0.032
        self.drag_sensitivity = 180
        self.click_origin = vec2()
        self.scroll_sensitivity = 0.01
        self.reset = False
        self.lerp_time = 0

        self.listener = 'space'

    def update(self, dt):
        if self.e['Input'].holding(self.listener) and self.drag_debounce > 0:
            self.click_origin = vec2(self.e['Input'].mouse.get_ortho_x(), self.e['Input'].mouse.get_ortho_y())
            self.drag_debounce -= dt
            return
        elif self.e['Input'].holding(self.listener):
            mouse_pos = vec2(self.e['Input'].mouse.get_ortho_x(), self.e['Input'].mouse.get_ortho_y())
            delta = mouse_pos - self.click_origin
            self.editor_camera.position -= delta * dt * self.drag_sensitivity
            #self.click_origin = self.click_origin * (1 - dt) + mouse_pos * dt
            self.click_origin = mouse_pos

        if (self.drag_debounce <= 0 and not self.e['Input'].holding(self.listener)):
            self.drag_debounce = 0.032

        if self.e['Input'].mouse.get_scroll_y() != 0:
            add_value = abs(self.e['Input'].mouse.get_scroll_y() * self.scroll_sensitivity) ** (1 / self.editor_camera.zoom)
            add_value *= -math.copysign(1.0, self.e['Input'].mouse.get_scroll_y())
            self.editor_camera.zoom += add_value

        # re-center
        if self.e['Input'].pressed('recenter'):
            self.reset = True

        if self.reset:
            self.editor_camera.position.x += (0.0 - self.editor_camera.position.x) * self.lerp_time
            self.editor_camera.position.y += (0.0 - self.editor_camera.position.y) * self.lerp_time
            
            self.editor_camera.zoom = self.editor_camera.zoom + ((1.0 - self.editor_camera.zoom)) * self.lerp_time

            self.lerp_time += 0.1 * dt

            if abs(self.editor_camera.position.x) <= 5 and abs(self.editor_camera.position.y) <= 5:
                self.lerp_time = 0
                self.editor_camera.position = vec2(0, 0)
                self.editor_camera.zoom = 1
                self.reset = False