import esper
import imgui

from engine.assets.assets import Assets
from engine.components.gizmo_system import GizmoSystem
from engine.components.non_pickable import NonPickable
from engine.editor.editor_layer import EditorUtils
from engine.misc.prefabs import Prefabs
from engine.components.editor_camera import EditorCamera

from engine.editor.mouse_controls import MouseControls
from engine.scenes.scene import Scene
from engine.scenes.scene_initializer import SceneInitializer
from engine.systems.editor_system import EditorSystem
from engine.systems.state_machine_system import StateMachineSystem


class EditorInitializer(SceneInitializer):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.sprites = None
        self.tiles = None
        self.gizmos = None
        self.editor_utils = EditorUtils()

    def init(self, scene: Scene):
        #esper.add_processor(StateMachineSystem())   # abstract this to self.add_processor()
        #esper.add_processor(EditorSystem())

        self.sprites = self.e['Assets'].get_spritesheet('veggies.png')
        self.tiles = self.e['Assets'].get_spritesheet('interior_free.png')      # test
        self.gizmos = self.e['Assets'].get_spritesheet('gizmos.png')

        scene.load('level.json')

    def load_resources(self, scene: Scene):
        a: Assets = self.e['Assets']
        a.get_shader('vsDefault.glsl', 'default.glsl')
        a.add_spritesheet('gizmos.png', 24, 48, 3, 0)
        a.add_spritesheet('veggies.png', 16, 16, 8, 0)

        a.add_spritesheet('interior_free.png', 16, 16, 42, 0)

        a.add_spritesheets('animations/player/idle', 15, 15, 12, 32, colorkey=(0, 0, 0))

    # TODO: find a better place for this
    def update(self, dt):
        self.editor_utils.update(dt)

    def imgui(self):
        imgui.begin('Plants')

        with imgui.begin_tab_bar('WindowTabBar'):
            if imgui.begin_tab_item('Plants').selected:
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
                        self.editor_utils.mouse_controls.pickup_entity(entity)
                    imgui.pop_id()

                    last_button_pos = imgui.get_item_rect_max()
                    last_button_x2 = last_button_pos.x
                    next_button_x2 = last_button_x2 + item_spacing.x + sprite_width
                    if i + 1 < active.size() and next_button_x2 < window_x2:
                        imgui.same_line()
                imgui.end_tab_item()

            if imgui.begin_tab_item('Prefabs').selected:
                #player_sprites = self.e['Assets'].get_spritesheet('animations/player/idle.png')
                player_sprites = self.e['Assets'].get_spritesheets('animations/player/idle')

                sprite = player_sprites.get_state_sprite('idle_down', 0)
                sprite_width = sprite.width * 4
                sprite_height = sprite.height * 4
                tex_coords = sprite.tex_coords
                tex_id = sprite.get_tex_id()

                if imgui.image_button(tex_id, sprite_width, sprite_height,
                                      (tex_coords[2].x, tex_coords[0].y),
                                      (tex_coords[0].x, tex_coords[2].y)):
                    entity = Prefabs.generate_player(self.e, 0.25, 0.25)
                    self.editor_utils.get_component(MouseControls).pickup_entity(entity)
                imgui.same_line()
                imgui.end_tab_item()

        imgui.end()