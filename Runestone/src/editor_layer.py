import imgui
import moderngl
import pygame

from Runestone.src.panels.content_browser_panel import ContentBrowserPanel
from Runestone.src.panels.scene_hierarchy_panel import SceneHierarchyWindow
from engine import Scene
from engine.core.layer import Layer
from engine.editor.game_view_window import GameViewWindow
from engine.observers.event_system import EventSystem
from engine.observers.events import EventType
from engine.observers.events.event import Event
from engine.rendering.debug_draw import DebugDraw
from engine.rendering.framebuffer import Framebuffer
from engine.rendering.picking_texture import PickingTexture


class EditorLayer(Layer):
    def __init__(self):
        super().__init__(name="EditorLayer")
        self.fbo = None
        self.editor_scene = None
        self.active_scene = None
        self.debug_draw = None


        # Load editor textures


        # Panels
        self.picking_texture = PickingTexture(*self.e['Window'].resolution)
        self.scene_hierarchy_panel = SceneHierarchyWindow(self.picking_texture)
        self.content_browser_panel = ContentBrowserPanel()


        # Other placeables
        self.hovered_entity = None
        self.show_physics_colliders = False
        self.viewport_focused = False
        self.viewport_hovered = False


    def on_attach(self):
        print('EditorLayer on_attach')

        self.fbo = Framebuffer(self.e['Window'].resolution)

        # TODO: Move editor_initializer and just dump it here
        self.editor_scene = Scene()
        self.active_scene = self.editor_scene
        self.debug_draw = DebugDraw()

    def update(self, dt):
        if not self.active_scene or not self.fbo:
            return

        self.scene_hierarchy_panel.update(dt, self.active_scene)

        # once the viewport is changed, update it here for resize events
        if self.e['Window'].resize_event:
            self.fbo.resize(*self.e['Window'].resolution)
            self.picking_texture.resize(*self.e['Window'].resolution)

        # render pass 1 for picking texture
        """
        TODO: Find a way to do this in a single draw call
        """
        self.picking_texture.enable_writing()
        self.e['Game'].ctx.viewport = (0, 0, *self.e['Window'].resolution)
        self.e['Game'].ctx.clear(0, 0, 0, 0)

        self.e['Renderer'].bind_shader(('vsPickingShader.glsl', 'pickingShader.glsl'))
        self.active_scene.render()

        self.picking_texture.disable_writing()
        self.e['Game'].ctx.enable(moderngl.BLEND)

        # render pass 2 for actual rendering
        self.debug_draw.begin_frame()

        self.fbo.use()
        self.e['Game'].ctx.clear(0.306, 0.353, 0.396, 1.0)

        self.debug_draw.draw()
        self.e['Renderer'].bind_shader(('vsDefault.glsl', 'default.glsl'))

        self.active_scene.update(self.e['Window'].dt)
        self.active_scene.render()

        self.fbo.unbind()

        self.e['Game'].ctx.disable(moderngl.BLEND)
        pygame.display.flip()

    def imgui_render(self):

        # set up the dockspace
        window_flags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING

        style = imgui.get_style()
        original_size = style.window_min_size
        style.window_min_size = imgui.Vec2(370, original_size.y)

        imgui.set_next_window_position(0, 0, imgui.ALWAYS)
        imgui.set_next_window_size(*self.e['Window'].resolution)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        window_flags = window_flags | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | \
                       imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | \
                       imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS
        imgui.begin("Dockspace", True, window_flags)
        imgui.pop_style_var(2)

        # dockspace
        imgui.dockspace(imgui.get_id("Dockspace"))

        style.window_min_size = original_size

        # tab bar thing at the top
        with imgui.begin_main_menu_bar():
            if imgui.begin_menu('File').opened:
                clicked, _ = imgui.menu_item('Save', 'Ctrl+S')
                if clicked:
                    EventSystem.notify(Event(EventType.SAVE_LEVEL))

                clicked, _ = imgui.menu_item('Load', 'Ctrl+O')
                if clicked:
                    EventSystem.notify(Event(EventType.LOAD_LEVEL))

                imgui.end_menu()

            is_playing = GameViewWindow.is_playing
            clicked, _ = imgui.menu_item('Play', '', is_playing, not is_playing)
            if clicked:
                is_playing = True
                EventSystem.notify(Event(EventType.GAME_ENGINE_START_PLAY))

            clicked, _ = imgui.menu_item('Stop', '', not is_playing, is_playing)
            if clicked:
                is_playing = False
                EventSystem.notify(Event(EventType.GAME_ENGINE_STOP_PLAY))
            GameViewWindow.is_playing = is_playing

        # scene hierarchy panel
        self.scene_hierarchy_panel.imgui()
        self.content_browser_panel.imgui()


        imgui.end()