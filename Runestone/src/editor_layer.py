import moderngl
import pygame

from engine import Scene
from engine.core.layer import Layer
from engine.editor.scene_hierarchy_window import SceneHierarchyWindow
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