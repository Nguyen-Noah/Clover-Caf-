from ..utils.elements import Element
from ..rendering.renderer import Renderer

class Scene(Element):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.running = False
        self.entities = []
        self.renderer = Renderer()

    def init(self):
        pass

    def start(self):
        for entity in self.entities:
            entity.start()
            self.renderer.add(entity)
        self.running = True

    def add_entity_to_scene(self, entity):
        self.entities.append(entity)
        if self.running:
            entity.start()
            self.renderer.add(entity)

    def update(self, dt):
        pass