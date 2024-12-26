import engine as engine
from engine.misc.camera import Camera
from scripts.constants.window import Screen

class Game(engine.Game):
    def load(self):
        scale_ratio = Screen.SCALE_RATIO

        self.camera = Camera(Screen.RESOLUTION)

        engine.init(
            resolution=Screen.RESOLUTION,
            input_path='data/config/key_mappings.json',
            fps_cap=Screen.FPS,
            opengl=True,
            shader_path='scripts/rendering/shaders',
            spritesheet_path='data/assets/spritesheets'
            )
        
        
        
        self.e['Assets'].load_folder('data/assets/floor', scale=3, colorkey=(0, 0, 0))

    def update(self):
        self.e['Window'].update()
        self.e['Input'].update()
         #self.e['GSManager'].update()

        self.camera.update()

        self.e['Tilemap'].render()
        self.e['Renderer'].render()

if __name__ == '__main__':
    Game().run()