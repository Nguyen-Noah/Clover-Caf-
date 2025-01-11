import imgui

from engine.components.gizmo_system import GizmoSystem
from engine.components.non_pickable import NonPickable
from engine.components.spritesheet import Spritesheet
from engine.misc.prefabs import Prefabs
from engine.components.gridlines import GridLines
from engine.components.editor_camera import EditorCamera

from engine.components.mouse_controls import MouseControls
from engine.scenes.scene import Scene
from engine.scenes.scene_initializer import SceneInitializer

class EditorInitializer(SceneInitializer):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.sprites = None
        self.tiles = None
        self.gizmos = None
        self.editor_utils = None

    def init(self, scene: Scene):
        self.sprites = self.e['Assets'].get_spritesheet('veggies.png')
        self.tiles = self.e['Assets'].get_spritesheet('interior_free.png')      # test
        self.gizmos = self.e['Assets'].get_spritesheet('gizmos.png')

        scene.load('level.json')

        self.editor_utils = scene.create_entity('LevelEditor')
        self.editor_utils.set_no_serialize()
        self.editor_utils.add_component(MouseControls())
        self.editor_utils.add_component(GridLines())
        self.editor_utils.add_component(EditorCamera(scene.camera))
        if not self.e['Game'].runtime_playing:
            self.editor_utils.add_component(GizmoSystem(self.gizmos))
            self.editor_utils.add_component(NonPickable())
        scene.add_entity_to_scene(self.editor_utils)

    def load_resources(self, scene: Scene):
        self.e['Assets'].get_shader('vsDefault.glsl', 'default.glsl')
        self.e['Assets'].add_spritesheet('gizmos.png',
                                         Spritesheet(self.e['Assets'].get_texture('gizmos.png'),
                                                     24, 48, 3, 0))
        self.e['Assets'].add_spritesheet('veggies.png',
                                         Spritesheet(self.e['Assets'].get_texture('veggies.png'),
                                        16, 16, 8, 0))

        self.e['Assets'].add_spritesheet('interior_free.png',
                                         Spritesheet(self.e['Assets'].get_texture('interior_free.png'),
                                        16, 16, 42, 0))

    def imgui(self):
        imgui.begin('Level Editor Stuff')
        self.editor_utils.imgui()
        imgui.end()

        imgui.begin('Test window')
        window_pos = imgui.get_window_position()
        window_size = imgui.get_window_size()
        item_spacing = imgui.get_style().item_spacing
        window_x2 = window_pos.x + window_size.x

        active = self.sprites
        for i in range(active.size()):
            sprite = active.get_sprite(i)
            sprite_width = sprite.width * 4
            sprite_height = sprite.height * 4
            tex_coords = sprite.tex_coords
            tex_id = sprite.get_tex_id()

            imgui.push_id(str(i))
            if imgui.image_button(tex_id, sprite_width, sprite_height, 
                                  (tex_coords[2].x, tex_coords[0].y),
                                  (tex_coords[0].x, tex_coords[2].y)):
                entity = Prefabs.generate_sprite_object(self.e, sprite, 0.25, 0.25)
                self.editor_utils.get_component(MouseControls).pickup_entity(entity)
            imgui.pop_id()

            last_button_pos = imgui.get_item_rect_max()
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width
            if i + 1 < active.size() and next_button_x2 < window_x2:
                imgui.same_line()

        imgui.end()