from typing import Type, Iterator, Tuple, Dict

import esper

from engine.components.non_render import NonRender
from engine.components.tag import TagComponent
from engine.components.transform import TransformComponent
from engine.misc.camera import Camera
from engine.components.component import Component
from engine.ecs.entity import Entity
from engine.utils.elements import Element
from engine.rendering.renderer import Renderer
from engine.utils.io import write_json, read_json
from engine.physics2d.physics2D import Physics2D

class Scene(Element):
    def __init__(self, scene_initializer):
        super().__init__()
        self.renderer = Renderer()
        self.camera = None
        self.physics2D = Physics2D()
        self.running = False
        self.entity_map: Dict[int, Entity] = {}

        self._scene_initializer = scene_initializer


    def init(self):
        self.camera = Camera((3, 2))#self.e['Game'].resolution
        self._scene_initializer.load_resources(self)
        self._scene_initializer.init(self)

    def create_entity(self, name):
        uid = esper.create_entity()
        entity = Entity(uid)
        entity.add_component(TagComponent(name))
        entity.add_component(TransformComponent())
        self.entity_map[uid] = entity
        return entity

    def get_component(self, component):
        for entity_id, component in esper.get_component(component):
            entity = self.get_entity_by_id(entity_id)
            if entity:
                yield entity, component

    def get_components(self, components):
        for entity_id, components in esper.get_components(*components):
            entity = self.get_entity_by_id(entity_id)
            if entity:
                yield (entity,) + tuple(components)

    def get_entity_by_id(self, entity_id):
        return self.entity_map.get(entity_id, None)

    def get_all_entities(self):
        return list(self.entity_map.values())

    def destroy_entity(self, entity):
        if entity.uid in self.entity_map:
            esper.delete_entity(entity.uid)
            del self.entity_map[entity.uid]

    def imgui(self):
        self._scene_initializer.imgui()

    def editor_update(self, dt):
        self.camera.adjust_projection()

        self._scene_initializer.update(dt)
        esper.process(dt)   # TODO: abstract this to a function self.process()

    def update(self, dt):
        self.camera.adjust_projection()
        self.physics2D.update(dt)

        for i, entity in enumerate(self.entities):
            alive = entity.update(dt)
            if not alive:
                self.renderer.destroy_entity(entity)
                self.physics2D.destroy_entity(entity)
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

                for name, component in entry.components.items():
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
            print(e)
            print('Level not found, starting new level.')
            self.loaded = True

    def save(self):
        data = []
        for entity in self.entities:
            if entity.do_serialization:
                data.append(entity.serialize())
        write_json('level.json', data)