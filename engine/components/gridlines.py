from .component import Component
from ..utils.settings import Settings
from ..primitives import vec2, vec3

class GridLines(Component):
    def __init__(self):
        super().__init__()

    def editor_update(self, dt):
        camera_pos = self.e['Camera'].position
        projection_size = self.e['Camera'].projection_size

        first_x = ((camera_pos.x // Settings.GRID_WIDTH) - 1) * Settings.GRID_WIDTH
        first_y = ((camera_pos.y // Settings.GRID_HEIGHT) - 1) * Settings.GRID_HEIGHT

        num_vt_lines = (projection_size.x * self.e['Camera'].zoom / Settings.GRID_WIDTH) + 2
        num_hz_lines = (projection_size.y * self.e['Camera'].zoom / Settings.GRID_HEIGHT) + 2

        height = (projection_size.y * self.e['Camera'].zoom) + Settings.GRID_HEIGHT * 2
        width = (projection_size.x * self.e['Camera'].zoom) + Settings.GRID_WIDTH * 2

        max_lines = max(num_hz_lines, num_vt_lines)
        color = vec3()
        for i in range(int(max_lines)):
            x = first_x + (Settings.GRID_WIDTH * i)
            y = first_y + (Settings.GRID_WIDTH * i)

            if i < num_vt_lines:
                self.e['Game'].debug_draw.add_line_2d(vec2(x, first_y), vec2(x, first_y + height), color, 1)

            if i < num_hz_lines:
                self.e['Game'].debug_draw.add_line_2d(vec2(first_x, y), vec2(first_x + width, y), color)