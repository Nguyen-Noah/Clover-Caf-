import imgui
from .entity import Entity
from ..utils.elements import Element
from ..rendering.renderer import Renderer
from ..utils.io import write_json, read_json

class Scene(Element):
    def __init__(self):
        super().__init__()
        self.camera = None
        self.running = False
        self.entities = []
        self.renderer = Renderer()
        self.active_entity = None
        self.loaded = False

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

    def scene_imgui(self):
        if self.active_entity is not None:
            imgui.begin('Inspector')
            self.active_entity.imgui()
            imgui.end()

        self.imgui()

    def imgui(self):
        pass

    def update(self, dt):
        pass


    # might want to add some safety checks here
    def load(self, path):
        data = read_json(path)
        for entity in data:
            entry = Entity.deserialize(entity)
            self.add_entity_to_scene(entry)

    def save_exit(self):
        data = []
        for entity in self.entities:
            data.append(entity.serialize())
        write_json('level.json', data)