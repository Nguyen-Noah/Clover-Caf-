from .assets.assets import Assets
from .misc.camera import Camera
from .misc.game import Game
from .misc.window import Window
from .misc.input import Input
from .rendering.renderer import Renderer
from .rendering.shader_program import ShaderRegistry, ShaderProgram
from .states.game_state import GSManager
from .tile.tilemap import Tilemap

def init(resolution=(640, 480), 
         caption='game', 
         entity_path=None, 
         audio_path=None,
         spritesheet_path=None,
         input_path=None,
         font_path=None,
         flags=0,
         fps_cap=60,
         dt_cap=1,
         opengl=False,
         shader_path=None,
         tilesize=(16, 16),
         dimensions=(16, 16)):
    window = Window(resolution=resolution, caption=caption, flags=flags, fps_cap=fps_cap, dt_cap=dt_cap, opengl=opengl, shader_path=shader_path)
    shader_registry = ShaderRegistry()
    renderer = Renderer()
    state_manager = GSManager()
    input = Input(path=input_path)
    assets = Assets(spritesheet_path=spritesheet_path)
    tilemap = Tilemap(tilesize=tilesize, dimensions=dimensions)