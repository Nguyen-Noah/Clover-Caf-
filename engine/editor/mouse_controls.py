from math import floor

from engine.components.non_pickable import NonPickable
from engine.components.sprite_renderer import SpriteRenderer
from engine.components.transform import TransformComponent
from engine.editor.game_view_window import GameViewWindow
from engine.primitives import vec2, vec4
from engine.utils.elements import Element
from engine.utils.settings import Settings

# pretty much a helper component
class MouseControls(Element):
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

    def place(self):
        new_entity = self.holding_entity.copy()
        new_entity.remove_component(NonPickable)
        new_entity.get_component(SpriteRenderer).set_color(vec4(1, 1, 1, 1))

    def update(self, dt):
        self.debounce -= dt
        if self.holding_entity is not None and self.debounce <= 0:
            position = self.holding_entity.get_component(TransformComponent).position
            position.x = self.e['Mouse'].get_world_x()
            position.y = self.e['Mouse'].get_world_y()
            position.x = (floor(position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH) + Settings.GRID_WIDTH / 2
            position.y = (floor(position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT) + Settings.GRID_HEIGHT / 2

            moved = self.moved_tile(position)
            if GameViewWindow.is_focused or GameViewWindow.is_hovered:
                if self.e['Input'].pressed('left_click'):
                    self.place()
                    self.debounce = self.debounce_time

                if self.e['Input'].holding('left_click') and moved:
                    self.place()
                    self.debounce = self.debounce_time

                if self.e['Input'].pressed('right_click'):
                    self.holding_entity.destroy()
                    self.holding_entity = None