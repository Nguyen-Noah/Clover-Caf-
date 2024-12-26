from ..utils.elements import Element

class Scene(Element):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.running = False
        self.entities = []

    def init(self):
        pass

    def start(self):
        for entity in self.entities:
            entity.start()
        self.running = True

    def add_entity_to_scene(self, entity):
        self.entities.append(entity)
        if self.running:
            entity.start()

    def update(self, dt):
        pass