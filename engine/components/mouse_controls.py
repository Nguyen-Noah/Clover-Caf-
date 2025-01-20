from math import floor

from .component import Component
from .non_pickable import NonPickable
from .sprite_renderer import SpriteRenderer
from ..primitives import vec2, vec4
from ..utils.settings import Settings

# pretty much a helper component
class MouseControls(Component):
    def __init__(self):
        super().__init__()
        self.holding_entity = None
        self.debounce_time = 0.05
        self.debounce = self.debounce_time

        self.last_pos = vec2()

    def moved_tile(self, new_pos):
        if new_pos != self.last_pos:
            self.last_pos = new_pos.copy()
            return True
        return False

    def pickup_entity(self, entity):
        if self.holding_entity is not None:
            self.holding_entity.destroy()

        self.holding_entity = entity
        self.holding_entity.get_component(SpriteRenderer).set_color(vec4(0.8, 0.8, 0.8, 0.5))
        self.holding_entity.add_component(NonPickable())
        self.e['Game'].current_scene.add_entity_to_scene(entity)

    def place(self):
        new_entity = self.holding_entity.copy()
        new_entity.remove_component(NonPickable)
        new_entity.get_component(SpriteRenderer).set_color(vec4(1, 1, 1, 1))
        self.e['Game'].current_scene.add_entity_to_scene(new_entity)

    def editor_update(self, dt):
        self.debounce -= dt
        if self.holding_entity is not None and self.debounce <= 0:
            position = self.holding_entity.transform.position
            position.x = self.e['Mouse'].get_world_x()
            position.y = self.e['Mouse'].get_world_y()
            position.x = (floor(position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH) + Settings.GRID_WIDTH / 2
            position.y = (floor(position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT) + Settings.GRID_HEIGHT / 2

            moved = self.moved_tile(position)
            if self.e['Mouse'].in_viewport_boundary():
                if self.e['Input'].pressed('left_click'):
                    self.place()
                    self.debounce = self.debounce_time

                if self.e['Input'].holding('left_click') and moved:
                    self.place()
                    self.debounce = self.debounce_time

                if self.e['Input'].pressed('right_click'):
                    self.holding_entity.destroy()
                    self.holding_entity = None