import imgui
from ..components.component import Component
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
        try:
            max_entity_id = -1
            max_comp_id = -1

            data = read_json(path)
            for entity in data:
                entry = Entity.deserialize(entity)
                self.add_entity_to_scene(entry)

                for component in entry.components:
                    if component.uid > max_comp_id:
                        max_comp_id = component.uid

                if entry.uid > max_entity_id:
                    max_entity_id = entry.uid

            max_entity_id += 1
            max_comp_id += 1
            Entity.init(max_entity_id)
            Component.init(max_comp_id)

            self.loaded = True
        except Exception as e:
            print('Level not found, starting new level.')
            self.entities = []
            self.loaded = True

    def save_exit(self):
        data = []
        for entity in self.entities:
            data.append(entity.serialize())
        write_json('level.json', data)