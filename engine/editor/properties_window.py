import imgui

from engine.components.non_pickable import NonPickable
from engine.utils.elements import Element
from engine.physics2d.components.rigidbody2d import RigidBody2D
from engine.physics2d.components.box2d_collider import Box2DCollider
from engine.physics2d.components.circle_collider import CircleCollider

class PropertiesWindow(Element):
    def __init__(self, picking_texture):
        super().__init__()
        self.active_entity = None
        self.picking_texture = picking_texture
        self.debounce = 0.2

    def imgui(self):
        if self.active_entity is not None:
            imgui.begin('Properties')

            if imgui.begin_popup_context_window('Component Adder', 2):
                if imgui.menu_item('Add Rigidbody')[0]:
                    if self.active_entity.get_component(RigidBody2D) is None:
                        self.active_entity.add_component(RigidBody2D())
                        self.check_and_add_to_physics()

                if imgui.menu_item('Add Box Collider')[0]:
                    if self.active_entity.get_component(Box2DCollider) is None and self.active_entity.get_component(CircleCollider) is None:
                        self.active_entity.add_component(Box2DCollider())
                        self.check_and_add_to_physics()

                if imgui.menu_item('Add Circle Collider')[0]:
                    if self.active_entity.get_component(CircleCollider) is None and self.active_entity.get_component(Box2DCollider) is None:
                        self.active_entity.add_component(CircleCollider())
                        self.check_and_add_to_physics()

                imgui.end_popup()

            self.active_entity.imgui()
            imgui.end()

    def check_and_add_to_physics(self):
            if self.active_entity is not None:
                rb = self.active_entity.get_component(RigidBody2D)
                collider = self.active_entity.get_component(Box2DCollider) or self.active_entity.get_component(CircleCollider)
                if rb is not None and collider is not None:
                    current_scene = self.e['Game'].current_scene
                    current_scene.physics2D.add(self.active_entity)

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