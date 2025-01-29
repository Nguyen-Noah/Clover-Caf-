from engine import Scene
from engine.core.layer import Layer
from engine.editor.scene_hierarchy_window import SceneHierarchyWindow
from engine.rendering.framebuffer import Framebuffer
from engine.rendering.picking_texture import PickingTexture


class EditorLayer(Layer):
    def __init__(self):
        super().__init__(name="EditorLayer")
        self.fbo = None
        self.editor_scene = None
        self.active_scene = None


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

    def update(self, dt):
        if not self.active_scene or not self.fbo:
            return

