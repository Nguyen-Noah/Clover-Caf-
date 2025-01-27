from math import floor

import esper

from engine.editor.mouse_controls import MouseControls
from engine.components.non_pickable import NonPickable
from engine.components.sprite_renderer import SpriteRenderer
from engine.ecs.system import System
from engine.editor.game_view_window import GameViewWindow
from engine.utils.settings import Settings
from engine.primitives import vec2, vec3, vec4


# should this even be a system? find a better place for this
class EditorSystem(System):
    def __init__(self):
        super().__init__()

    def process(self, dt):
        self._process_mouse(dt)
        self._render_gridlines()

    def _process_mouse(self, dt):
        for _, mc in esper.get_component(MouseControls):
            mc.debounce -= dt
            if mc.holding_entity is not None and mc.debounce <= 0:
                position = mc.holding_entity.transform.position
                position.x = self.e['Mouse'].get_world_x()
                position.y = self.e['Mouse'].get_world_y()

                position.x = (floor(position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH) + Settings.GRID_WIDTH / 2
                position.y = (floor(position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT) + Settings.GRID_HEIGHT / 2

                # check if we moved tile
                if position != mc.last_pos:
                    mc.last_pos = position.copy()
                    moved = True
                moved = False

                if GameViewWindow.is_focused or GameViewWindow.is_hovered:
                    if self.e['Input'].pressed('left_click'):
                        self._place()
                        self.debounce = mc.debounce_time

                    if self.e['Input'].holding('left_click') and moved:
                        self._place()
                        self.debounce = mc.debounce_time

                    if self.e['Input'].pressed('right_click'):
                        mc.holding_entity.destroy()
                        mc.holding_entity = None

    def _pickup_entity(self, entity):
        if self.holding_entity is not None:
            self.holding_entity.destroy()

        self.holding_entity = entity
        self.holding_entity.get_component(SpriteRenderer).set_color(vec4(0.8, 0.8, 0.8, 0.5))
        self.holding_entity.add_component(NonPickable())
        self.e['Game'].current_scene.add_entity_to_scene(entity)

    def _place(self):
        new_entity = self.holding_entity.copy()
        new_entity.remove_component(NonPickable)
        new_entity.get_component(SpriteRenderer).set_color(vec4(1, 1, 1, 1))
        self.e['Game'].current_scene.add_entity_to_scene(new_entity)

    def _render_gridlines(self):
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



