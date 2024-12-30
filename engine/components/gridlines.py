from .component import Component
from ..utils.elements import Element
from ..utils.settings import Settings
from ..primitives import vec2, vec3

class GridLines(Component, Element):
    def __init__(self):
        Component.__init__(self)
        Element.__init__(self)

    def update(self, dt):
        camera_pos = self.e['Camera'].camera_offset
        projection_size = self.e['Camera'].size

        first_x = ((camera_pos.x / Settings.GRID_WIDTH) - 1) * Settings.GRID_WIDTH
        first_y = ((camera_pos.y / Settings.GRID_HEIGHT) - 1) * Settings.GRID_HEIGHT

        num_vt_lines = (projection_size.x / Settings.GRID_WIDTH) + 2
        num_hz_lines = (projection_size.y / Settings.GRID_HEIGHT) + 2

        height = projection_size.y + Settings.GRID_HEIGHT * 2
        width = projection_size.x + Settings.GRID_WIDTH * 2

        max_lines = max(num_hz_lines, num_vt_lines)
        color = vec3()
        for i in range(int(max_lines)):
            x = first_x + (Settings.GRID_WIDTH * i)
            y = first_y + (Settings.GRID_WIDTH * i)

            if i < num_vt_lines:
                self.e['Game'].debug_draw.add_line_2d(vec2(x, first_y), vec2(x, y + height), color)

            if i < num_hz_lines:
                self.e['Game'].debug_draw.add_line_2d(vec2(first_x, y), vec2(first_x + width, y), color)