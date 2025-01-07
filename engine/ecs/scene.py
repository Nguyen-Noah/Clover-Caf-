import imgui
from ..components.component import Component
from .entity import Entity
from ..components.transform import Transform
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

    def create_entity(self, name):
        entity = Entity(name)
        entity.add_component(Transform())
        entity.transform = entity.get_component(Transform)
        return entity

    def get_entity(self, uid):
        result = next(
            (entity for entity in self.entities if entity.uid == uid),
            None
        )
        return result

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
            if entity.do_serialization:
                data.append(entity.serialize())
        write_json('level.json', data)