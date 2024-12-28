import moderngl
import engine as engine
from scripts.constants.window import Screen
from scripts.scenes.test import TestScene

# TODO: - make all paths absolute when they are loaded
#       - current level editor's origin is top left, 
#         eventually make a new level editor with origin at bottom right
#           - this is why all the rendering is upside down/zoom is weird

class Game(engine.Game):
    def load(self):
        scale_ratio = Screen.SCALE_RATIO

        engine.init(
            resolution=Screen.RESOLUTION,
            input_path='data/config/key_mappings.json',
            fps_cap=Screen.FPS,
            opengl=True,
            shader_path='scripts/rendering/shaders',
            spritesheet_path='data/assets/spritesheets'
            )
        self.ctx = moderngl.create_context(require=330)
        self.e['Assets'].load_folder('data/assets/floor', colorkey=(0, 0, 0))
        
        
        self.current_scene = TestScene()
        self.current_scene.start()

    def update(self):
        self.e['Window'].update()
        self.e['Input'].update()
        #self.e['GSManager'].update()

        self.current_scene.update(self.e['Window'].dt)
        self.current_scene.render()

if __name__ == '__main__':
    Game().run()