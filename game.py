import os, debugpy
import engine as engine
from scripts.constants.window import Screen
from scripts.scenes.test import TestScene

# TODO: make all paths absolute when they are loaded

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
        
        self.e['Assets'].load_folder('data/assets/floor', scale=3, colorkey=(0, 0, 0))
        
        
        self.current_scene = TestScene()

    def update(self):
        self.e['Window'].update()
        self.e['Input'].update()
        #self.e['GSManager'].update()

        self.current_scene.update(self.e['Window'].dt)
        self.current_scene.render()
        
        self.e['Renderer'].render()

if __name__ == '__main__':
    Game().run()