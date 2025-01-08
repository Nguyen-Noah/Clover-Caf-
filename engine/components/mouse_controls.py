from .component import Component
from ..utils.settings import Settings

# pretty much a helper component
class MouseControls(Component):
    def __init__(self):
        super().__init__()
        self.holding_entity = None

    def pickup_entity(self, entity):
        self.holding_entity = entity
        self.e['Game'].current_scene.add_entity_to_scene(entity)

    def place(self):
        self.holding_entity = None

    def editor_update(self, dt):
        # temporary
        if self.holding_entity is not None:
            position = self.holding_entity.transform.position
            position.x = self.e['Input'].mouse.get_ortho_x()
            position.y = self.e['Input'].mouse.get_ortho_y()
            position.x = (position.x // Settings.GRID_WIDTH) * Settings.GRID_WIDTH
            position.y = (position.y // Settings.GRID_HEIGHT) * Settings.GRID_HEIGHT

            if self.e['Input'].pressed('left_click'):
                self.place()