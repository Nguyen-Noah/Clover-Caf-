import esper

from engine.components.tag import TagComponent


class Entity:
    def __init__(self, uid: int, scene):
        self.uid = uid
        self.scene = scene
        self.do_serialization = True

    def add_component(self, component):
        esper.add_component(self.uid, component)

    def has_component(self, component):
        return esper.has_component(self.uid, component)

    def has_components(self, components):
        return esper.has_components(self.uid, components)

    def get_component(self, component):
        return esper.component_for_entity(self.uid, component)

    def try_component(self, component):
        return esper.has_component(self.uid, component)

    def get_all_components(self):
        return esper.components_for_entity(self.uid)

    def remove_component(self, component):
        esper.remove_component(self.uid, component)

    def set_no_serialize(self):
        self.do_serialization = False

    def copy(self):
        new_entity = self.scene.create_entity()
        for component in esper.components_for_entity(self.uid):
            new_entity.add_component(component)
        return new_entity

    def destroy(self):
        esper.delete_entity(self.uid)
        self.scene.destroy_entity(self)

    def serialize(self):
        return self.__dict__

    @classmethod
    def deserialize(cls, data):
        return cls(data.get('uid'))

    # ID_COUNTER = 1
    #
    # def __init__(self, name):
    #     super().__init__()
    #     self.name = name
    #     self.components = {}
    #     self.transform = None
    #     self.uid = Entity.ID_COUNTER
    #     Entity.ID_COUNTER += 1
    #     self.do_serialization = True
    #     self.alive = True
    #
    # def start(self):
    #     new_components = {}
    #
    #     for name, component in self.components.items():
    #         component.start()
    #
    #         if hasattr(component, 'new_components'):
    #             new_components.update(component.new_components)
    #
    #     for _, component in new_components.items():
    #
    #         self.add_component(component)
    #         component.start()
    #
    # def add_component(self, c):
    #     c.generate_id()
    #     self.components[c.__class__.__name__] = c
    #     c.entity = self
    #
    # def get_component(self, component_class):
    #     if component_class.__name__ in self.components:
    #         return self.components[component_class.__name__]
    #     return None
    #
    # def remove_component(self, component_class):
    #     if component_class.__name__ in self.components:
    #         del self.components[component_class.__name__]
    #
    # def has_component(self, component_type):
    #     if component_type.__name__ in self.components:
    #         return self.components[component_type.__name__]
    #     return None
    #
    # def has_components(self, component_types):
    #     return all(ct.__name__ in self.components for ct in component_types)
    #
    # def destroy(self):
    #     self.alive = False
    #     for component in self.components:
    #         self.components[component].destroy()
    #
    # def imgui(self):
    #     for component in self.components:
    #         show, _ = imgui.collapsing_header(self.components[component].__class__.__name__)
    #         if show:
    #             self.components[component].imgui()
    #
    # def init(max_id):
    #     Entity.ID_COUNTER = max_id
    #
    # def set_no_serialize(self):
    #     self.do_serialization = False
    #
    # def editor_update(self, dt):
    #     for component in self.components:
    #         if component == 'StateMachine':
    #             continue
    #         self.components[component].editor_update(dt)
    #
    #     return self.alive
    #
    # def update(self, dt):
    #     for component in self.components:
    #         self.components[component].update(dt)
    #
    #     return self.alive
    #
    # def copy(self):
    #     return Entity.deserialize(self.serialize())
    #
    # def serialize(self):
    #     return {
    #         "uid": self.uid,
    #         "name": self.name,
    #         "components": {name: comp.serialize() for name, comp in self.components.items()}
    #     }
    #
    # @classmethod
    # def deserialize(cls, data):
    #     entity = cls(data["name"])
    #
    #     for _, component_data in data["components"].items():
    #         component_type = deserialize_component(component_data)
    #         entity.add_component(component_type)
    #     entity.transform = entity.get_component(TransformComponent)
    #
    #     return entity