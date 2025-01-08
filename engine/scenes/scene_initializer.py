from engine.scenes.scene import Scene
from engine.utils.elements import Element


class SceneInitializer(Element):
    def __init__(self):
        super().__init__()
    
    def init(self, scene: Scene):
        pass

    def load_resources(self, scene: Scene):
        pass

    def imgui(self):
        pass