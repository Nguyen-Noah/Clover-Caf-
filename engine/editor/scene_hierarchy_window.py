import imgui
from engine.components.non_pickable import NonPickable
from engine.components.sprite_renderer import SpriteRenderer
from engine.components.tag import TagComponent
from engine.components.transform import TransformComponent
from engine.editor.game_view_window import GameViewWindow
from engine.editor.pimgui import PImGui
from engine.physics2d.components.box2d_collider import Box2DCollider
from engine.physics2d.components.circle_collider import CircleCollider
from engine.physics2d.components.rigidbody2d import RigidBody2D
from engine.utils.elements import ElementSingleton

class SceneHierarchyWindow(ElementSingleton):
    def __init__(self, picking_texture):
        super().__init__()
        self.active_entity = None

        # Entity picking
        self.picking_texture = picking_texture
        self.debounce = 0.2

    def imgui(self):
        imgui.begin('Scene Hierarchy')
        self._draw_entity_node()

        if self.e['Input'].pressed('left_click') and imgui.is_window_hovered():
            self.active_entity = None

        imgui.end()

        if self.active_entity is not None:
            imgui.begin('Properties')
            self._draw_components()
            imgui.end()

    def _draw_entity_node(self):
        entities = self.e['Game'].current_scene.get_all_entities()
        index = 0
        for entity in entities:
            if entity.try_component(NonPickable):
                continue

            tree_node_open = self._do_tree_node(entity, index)
            if tree_node_open:
                imgui.tree_pop()

            index += 1

    def _do_tree_node(self, entity, index):
        imgui.push_id(str(index))
        tree_node_open = imgui.tree_node(entity.get_component(TagComponent).name,
                                         imgui.TREE_NODE_DEFAULT_OPEN | imgui.TREE_NODE_FRAME_PADDING | imgui.TREE_NODE_OPEN_ON_ARROW | imgui.TREE_NODE_SPAN_AVAILABLE_WIDTH,
                                         )

        if imgui.is_item_clicked():
            self.active_entity = entity

        imgui.pop_id()

        # if imgui.begin_drag_drop_source():
        #     imgui.set_drag_drop_payload('SceneHierarchy', 'hi')
        #     imgui.text(entity.name)
        #
        #     imgui.end_drag_drop_source()
        #
        # if imgui.begin_drag_drop_target():
        #     payload_obj = imgui.accept_drag_drop_payload('SceneHierarchy')
        #     print(payload_obj)
        #     if payload_obj is not None:
        #         print(payload_obj.__class__)
        #
        #     imgui.end_drag_drop_target()

        return tree_node_open

    def _draw_components(self):
        if self.active_entity.has_component(TagComponent):
            tag = self.active_entity.get_component(TagComponent)
            name = PImGui.input_text('Tag: ', tag.name)
            tag.name = name

        if self.active_entity.has_component(TransformComponent):
            if imgui.tree_node("Transform", imgui.TREE_NODE_DEFAULT_OPEN):
                transform: TransformComponent = self.active_entity.get_component(TransformComponent)
                PImGui.draw_vec2_control('Position: ', transform.position)
                PImGui.draw_vec2_control('Scale: ', transform.scale)
                c, val = PImGui.drag_float('Rotation: ', transform.rotation)
                if c:
                    transform.rotation = val
                c, val = PImGui.drag_int('z-index: ', transform.z_index)
                if c:
                    transform.z_index = val

                imgui.tree_pop()

        if self.active_entity.has_component(SpriteRenderer):
            if imgui.tree_node("SpriteRenderer", imgui.TREE_NODE_DEFAULT_OPEN):
                sprite: SpriteRenderer = self.active_entity.get_component(SpriteRenderer)
                PImGui.draw_color(sprite)

                imgui.tree_pop()

    def update(self, dt, current_scene):
        self.debounce -= dt
        if self.e['Input'].pressed('left_click') and self.debounce < 0 and GameViewWindow.is_focused:
            x = self.e['Mouse'].get_screen_x()
            y = self.e['Mouse'].get_screen_y()
            entity_id = current_scene.get_entity(self.picking_texture.read_pixel(x, y))
            if entity_id is not None and entity_id.get_component(NonPickable) is None:
                self.active_entity = entity_id
            elif entity_id is None and self.e['Mouse'].is_dragging():
                self.active_entity = None
            self.debounce = 0.2
