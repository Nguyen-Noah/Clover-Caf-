from engine.scenes.scene import Scene
from engine.utils.elements import Element

class System(Element):
    def __init__(self):
        super().__init__()
        """
        Base system class that all other systems inherit from.
        This class provides a standardized interface for processing entities.
        """
        self.enabled = True
        self.world: Scene = self.e['Game'].current_scene

    def update(self, dt):
        """
        Process all entities with relevant components.

        :param dt: Delta time for frame update.
        """
        raise NotImplementedError('Systems must implement the update method.')

    def start(self):
        """
        Optional initialization logic.
        :return:
        """

    def on_entity_add(self, entity):
        """
        Called when an entity with the required components is added to the ECS.

        :param entity: The entity ID
        """
        pass

    def on_entity_removed(self, entity):
        """
        Called when an entity with the required components is removed from the ECS.

        :param entity: The entity ID
        """
        pass

    # coule probably inherit Observer for this
    def handle_event(self, event):
        """
        Handle game events such as input actions or collisions.

        :param event: The event.
        """
        pass