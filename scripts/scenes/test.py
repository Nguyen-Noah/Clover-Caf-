from engine.ecs.scene import Scene
from engine.ecs.entity import Entity
from engine.misc.camera import Camera
from ..constants.window import Screen

class TestScene(Scene):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.test_entity = Entity('test')
        self.add_entity_to_scene(self.test_entity)

        self.camera = Camera(Screen.RESOLUTION)
        