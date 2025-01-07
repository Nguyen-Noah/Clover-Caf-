import imgui

from ..components.non_pickable import NonPickable
from ..utils.elements import Element

class PropertiesWindow(Element):
    def __init__(self, picking_texture):
        super().__init__()
        self.active_entity = None
        self.picking_texture = picking_texture
        self.debounce = 0.2

    def imgui(self):
            if self.active_entity is not None:
                imgui.begin('Properties')
                self.active_entity.imgui()
                imgui.end()

    # properties panel disappears when i try to move imgui panel, so i added a check
    # not the end of the world, but could be changed in the future
    def update(self, dt, current_scene):
        self.debounce -= dt
        if self.e['Input'].pressed('left_click') and self.debounce < 0:
            x = self.e['Input'].mouse.get_screen_x()
            y = self.e['Input'].mouse.get_screen_y()
            entity_id = current_scene.get_entity(self.picking_texture.read_pixel(x, y))
            if entity_id is not None and entity_id.get_component(NonPickable) is None:
                self.active_entity = entity_id
            elif entity_id is None and self.e['Mouse'].is_dragging():
                self.active_entity = None
            self.debounce = 0.2