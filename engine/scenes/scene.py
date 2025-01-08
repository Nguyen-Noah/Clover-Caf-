import imgui

from engine.misc.camera import Camera
from engine.components.component import Component
from engine.ecs.entity import Entity
from engine.components.transform import Transform
from engine.utils.elements import Element
from engine.rendering.renderer import Renderer
from engine.utils.io import write_json, read_json

class Scene(Element):
    def __init__(self, scene_initializer):
        super().__init__()
        self.renderer = Renderer()
        self.camera = None
        self.running = False
        self.entities = []

        self._scene_initializer = scene_initializer

    def init(self):
        self.camera = Camera(self.e['Game'].resolution)
        self._scene_initializer.load_resources(self)
        self._scene_initializer.init(self)

    def start(self):
        for entity in self.entities:
            entity.start()
            self.renderer.add(entity)
            # self.physics_shit.add(enity)
        self.running = True

    def add_entity_to_scene(self, entity):
        self.entities.append(entity)
        if self.running:
            entity.start()
            self.renderer.add(entity)
            # self.physics_shit.add(entity)

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
        self._scene_initializer.imgui()

    def editor_update(self, dt):
        self.camera.adjust_projection()
        for i, entity in enumerate(self.entities):
            alive = entity.editor_update(dt)
            if not alive:
                self.renderer.destroy_entity(entity)
                # this.physics2D.destroy(entity)             DO THIS ONCE YOU IMPLEMENT
                self.entities.pop(i)

    def update(self, dt):
        self.camera.adjust_projection()

        for i, entity in enumerate(self.entities):
            alive = entity.update(dt)
            if not alive:
                self.renderer.destroy_entity(entity)
                #this.physics2D.destroy(entity)             DO THIS ONCE YOU IMPLEMENT
                self.entities.pop(i)

    def render(self):
        self.renderer.render()

    def destroy(self):
        for entity in self.entities:
            entity.destroy()

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

    def save(self):
        data = []
        for entity in self.entities:
            if entity.do_serialization:
                data.append(entity.serialize())
        write_json('level.json', data)