import moderngl, pygame
import engine as engine
from scripts.constants.window import Screen
from scripts.scenes.test import TestScene

from engine.rendering.debug_draw import DebugDraw

# TODO: - make all paths absolute when they are loaded
#       - current level editor's origin is top left, 
#         eventually make a new level editor with origin at bottom right
#           - this is why all the rendering is upside down/zoom is weird

class Game(engine.Game):
    def load(self):
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

    def update(self):
        self.e['Window'].update()
        self.e['ImGui'].start_frame()
        self.e['Input'].update()
        #self.e['GSManager'].update()

        self.debug_draw.begin_frame()

        self.e['Game'].ctx.clear(0.90, 0.90, 0.90, 1.0)
        self.e['Game'].ctx.enable(moderngl.BLEND)

        self.debug_draw.draw()
        self.current_scene.update(self.e['Window'].dt)
        self.current_scene.render()

        self.e['ImGui'].update(self.e['Window'].dt, self.current_scene)

        self.e['Game'].ctx.disable(moderngl.BLEND)
        pygame.display.flip()

if __name__ == '__main__':
    Game().run()

# fruit sushi
# chocolate/dessert burrito