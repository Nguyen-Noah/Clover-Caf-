import imgui, math
from engine.ecs.scene import Scene
from engine.misc.camera import Camera
from ..constants.window import Screen
from engine.components.spritesheet import Spritesheet
from engine.misc.prefabs import Prefabs
from engine.components.rigidbody import RigidBody

from engine.components.mouse_controls import MouseControls

from engine.primitives import vec2, vec3

class TestScene(Scene):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.load_resources()
        self.sprites = self.e['Assets'].get_spritesheet('veggies.png')

        self.load('level.json')

        self.active_entity = self.entities[0]

        self.camera = Camera(Screen.RESOLUTION)

        self.mouse_controls = MouseControls()

    def load_resources(self):
        self.e['Assets'].get_shader('vsDefault.glsl', 'default.glsl')
        self.e['Assets'].add_spritesheet('veggies.png', 
                            Spritesheet(self.e['Assets'].get_texture('veggies.png'),
                                        16, 16, 8, 0))

    def imgui(self):
        imgui.begin('Test window')
        window_pos = imgui.get_window_position()
        window_size = imgui.get_window_size()
        item_spacing = imgui.get_style().item_spacing
        window_x2 = window_pos.x + window_size.x
        
        for i in range(self.sprites.size()):
            sprite = self.sprites.get_sprite(i)
            sprite_width = sprite.width * 4
            sprite_height = sprite.height * 4
            tex_coords = sprite.tex_coords
            tex_id = sprite.get_tex_id()

            imgui.push_id(str(i))
            if imgui.image_button(tex_id, sprite_width, sprite_height, 
                                  (tex_coords[0].x, tex_coords[0].y),
                                  (tex_coords[2].x, tex_coords[2].y)):
                entity = Prefabs.generate_sprite_object(sprite, sprite_width, sprite_height)
                self.mouse_controls.pickup_entity(entity)
            imgui.pop_id()

            last_button_pos = imgui.get_item_rect_max()
            last_button_x2 = last_button_pos.x
            next_button_x2 = last_button_x2 + item_spacing.x + sprite_width
            if (i + 1 < self.sprites.size() and next_button_x2 < window_x2):
                imgui.same_line()

        imgui.end()

    def update(self, dt):
        self.camera.update()

        self.mouse_controls.update(dt)
        for entity in self.entities:
            entity.update(dt)

        self.renderer.render()

    def render(self):
        pass
        #self.tilemap.render()