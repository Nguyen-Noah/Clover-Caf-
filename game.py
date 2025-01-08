import moderngl, pygame, io
import engine as engine
from engine.ecs.entity import Entity
from engine.observers.events import EventType
from engine.observers.events.event import Event
from engine.scenes.scene import Scene
from engine.scenes.scene_initializer import SceneInitializer
from scripts.constants.window import Screen

from engine.rendering.debug_draw import DebugDraw
from engine.rendering.framebuffer import Framebuffer
from engine.rendering.picking_texture import PickingTexture
from engine.misc.custom_imgui import ImGui

import cProfile
import pstats

from scripts.scenes.editor_initializer import EditorInitializer


# TODO: - make all paths absolute when they are loaded
#       - current level editor's origin is top left, 
#         eventually make a new level editor with origin at bottom right
#           - this is why all the rendering is upside down/zoom is weird

def profile_run():
    profiler = cProfile.Profile()
    profiler.enable()

    # Run the game
    Game().run()

    profiler.disable()

    # Print profiling stats to the console or file
    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs().sort_stats('cumulative').print_stats(20)  # Top 20 slowest calls
    print(stream.getvalue())  # Prints to console

PROFILE = True

class Game(engine.Game):
    def __init__(self):
        super().__init__()
        self.resolution = Screen.RESOLUTION
        self.aspect_ratio = Screen.ASPECT_RATIO[0] / Screen.ASPECT_RATIO[1]
        self.fps = Screen.FPS
        self.imgui = None
        self.picking_shader = None
        self.picking_texture = None
        self.fbo = None
        self.current_scene = None
        self.debug_draw = None
        self.ctx = None
        self.runtime_playing = False

    def load(self):
        engine.init(
            resolution=Screen.RESOLUTION,
            input_path='data/config/key_mappings.json',
            fps_cap=Screen.FPS,
            opengl=True,
            shader_path='scripts/rendering/shaders',
            spritesheet_path='data/assets/spritesheets',
            flags=pygame.RESIZABLE
            )
        self.ctx = moderngl.create_context(require=330)
        self.picking_texture = PickingTexture(*Screen.RESOLUTION)
        self.picking_shader = ('vsPickingShader.glsl', 'pickingShader.glsl')
        self.imgui = ImGui(Screen.RESOLUTION, self.picking_texture)
        
        self.debug_draw = DebugDraw()

        self.change_scene(EditorInitializer())

        self.fbo = Framebuffer(*Screen.RESOLUTION)
        self.ctx.viewport = (0, 0, *Screen.RESOLUTION)

    def change_scene(self, scene: SceneInitializer):
        if self.current_scene is not None:
            self.current_scene.destroy()

        self.imgui.properties_window.active_entity = None
        self.current_scene = Scene(scene)
        self.current_scene.init()
        self.current_scene.start()

    def on_notify(self, entity: Entity, event: Event):
        if event.type == EventType.GAME_ENGINE_START_PLAY:
            print('Game starting')
            self.runtime_playing = True
            self.current_scene.save()
            self.change_scene(EditorInitializer())
        elif event.type == EventType.GAME_ENGINE_STOP_PLAY:
            print('Ending play')
            self.runtime_playing = False
            self.change_scene(EditorInitializer())
        elif event.type == EventType.LOAD_LEVEL:
            self.change_scene(EditorInitializer())
        elif event.type == EventType.SAVE_LEVEL:
            self.current_scene.save()

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
        if self.runtime_playing:
            self.current_scene.update(self.e['Window'].dt)
        else:
            self.current_scene.editor_update(self.e['Window'].dt)
        self.current_scene.render()

        self.fbo.unbind()

        self.e['ImGui'].update(self.e['Window'].dt, self.current_scene)

        self.e['Game'].ctx.disable(moderngl.BLEND)
        pygame.display.flip()

if __name__ == '__main__':
    if PROFILE:
        profile_run()
    else:
        Game().run()

# fruit sushi
# chocolate/dessert burrito