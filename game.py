import moderngl, pygame
import engine as engine
from scripts.constants.window import Screen
from scripts.scenes.editor import TestScene

from engine.rendering.debug_draw import DebugDraw
from engine.rendering.framebuffer import Framebuffer
from engine.rendering.picking_texture import PickingTexture
from engine.misc.imgui import ImGui

# TODO: - make all paths absolute when they are loaded
#       - current level editor's origin is top left, 
#         eventually make a new level editor with origin at bottom right
#           - this is why all the rendering is upside down/zoom is weird

class Game(engine.Game):
    def load(self):
        self.aspect_ratio = Screen.ASPECT_RATIO[0] / Screen.ASPECT_RATIO[1]

        engine.init(
            resolution=Screen.RESOLUTION,
            input_path='data/config/key_mappings.json',
            fps_cap=Screen.FPS,
            opengl=True,
            shader_path='scripts/rendering/shaders',
            spritesheet_path='data/assets/spritesheets'
            )
        self.ctx = moderngl.create_context(debug=True, require=330)
        self.e['Assets'].load_folder('data/assets/floor', colorkey=(0, 0, 0))
        
        self.debug_draw = DebugDraw()

        self.current_scene = TestScene()
        self.current_scene.start()


        self.fbo = Framebuffer(*Screen.RESOLUTION)
        self.ctx.viewport = (0, 0, *Screen.RESOLUTION)

        self.picking_texture = PickingTexture(*Screen.RESOLUTION)
        self.picking_shader = ('vsPickingShader.glsl', 'pickingShader.glsl')
        self.imgui = ImGui(Screen.RESOLUTION, self.picking_texture)

    def update(self):
        self.e['Window'].update()
        self.e['ImGui'].start_frame()
        self.e['Input'].update()

        # Render pass 1. Render to picking texture
        self.picking_texture.enable_writing()
        self.ctx.viewport = (0, 0, *Screen.RESOLUTION)
        self.ctx.clear(0, 0, 0, 0)

        self.e['Renderer'].bind_shader(self.picking_shader)
        self.current_scene.render()

        self.picking_texture.disable_writing()
        self.e['Game'].ctx.enable(moderngl.BLEND)

        # Render pass 2. Render actual game

        self.debug_draw.begin_frame()

        self.fbo.use()
        self.e['Game'].ctx.clear(0.90, 0.90, 0.90, 1.0)
        

        self.debug_draw.draw()
        self.e['Renderer'].bind_shader(('vsDefault.glsl', 'default.glsl'))
        self.current_scene.update(self.e['Window'].dt)
        self.current_scene.render()

        self.fbo.unbind()

        self.e['ImGui'].update(self.e['Window'].dt, self.current_scene)

        self.e['Game'].ctx.disable(moderngl.BLEND)
        pygame.display.flip()

if __name__ == '__main__':
    Game().run()

# fruit sushi
# chocolate/dessert burrito