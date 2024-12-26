from engine.ecs.scene import Scene
from engine.ecs.entity import Entity
from engine.misc.camera import Camera
from engine.tile.tilemap import Tilemap
from ..constants.window import Screen

class TestScene(Scene):
    def __init__(self):
        print('Creating test scene')
        super().__init__()
        self.test_entity = Entity('test')
        self.add_entity_to_scene(self.test_entity)

        self.atlas, self.atlas_coords = self.e['Assets'].create_texture_atlas(atlas_size=(256, 256))

        print(self.atlas_coords)
        self.camera = Camera(Screen.RESOLUTION)
        self.tilemap = Tilemap(self, 'test', scale_ratio=Screen.SCALE_RATIO)

    def update(self, dt):
        self.camera.update()
        for entity in self.entities:
            entity.update(dt)

    def render(self):
        self.tilemap.render()