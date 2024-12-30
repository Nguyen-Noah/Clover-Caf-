from .component import Component
from ..utils.elements import Element

# pretty much a helper component
class MouseControls(Component, Element):
    def __init__(self):
        Component.__init__(self)
        Element.__init__(self)
        self.holding_entity = None

    def pickup_entity(self, entity):
        self.holding_entity = entity
        self.e['Game'].current_scene.add_entity_to_scene(entity)

    def place(self):
        self.holding_entity = None

    def update(self, dt):
        # temporary
        if self.holding_entity is not None:
            self.holding_entity.transform.position.x = self.e['Input'].mouse.get_ortho_x() + 540 - 30
            self.holding_entity.transform.position.y = self.e['Input'].mouse.get_ortho_y() + 360 - 25
            print(f'held: {self.holding_entity.transform.position}')
            print(f'mine: {self.e["Input"].mouse.get_ortho_x()}, {self.e["Input"].mouse.get_ortho_y()}')

            if self.e['Input'].pressed('left_click'):
                self.place()