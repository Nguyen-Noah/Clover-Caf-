from engine.scenes.scene import Scene
from engine.utils.elements import Element


class SceneInitializer(Element):
    def __init__(self):
        super().__init__()
        self.placeholder_sprite = self.e['Assets'].add_spritesheet('placeholder.png', 16, 16, 1, 0)
    
    def init(self, scene: Scene):
        pass

    def load_resources(self, scene: Scene):
        pass

    def imgui(self):
        pass