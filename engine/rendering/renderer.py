import moderngl, pygame
from ..utils.elements import ElementSingleton
from ..components.sprite_renderer import SpriteRenderer
from .render_batch import RenderBatch

class Renderer(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.ctx = moderngl.create_context(require=330)

        self.max_batch_size = 1000
        self.batches = []

    def add(self, entity):
        spr = entity.get_component(SpriteRenderer)

        if spr != None:
            self._add(spr)

    def _add(self, sprite):
        added = False
        for batch in self.batches:
            if batch.has_room and batch.z_index == sprite.entity.z_index:
                tex = sprite.get_texture()
                if tex is None or batch.has_texture(tex) or batch.has_texture_room():
                    batch.add_sprite(sprite)
                    added = True
                    break

        if not added:
            new_batch = RenderBatch(z_index=sprite.entity.z_index, max_batch_size=self.max_batch_size)
            self.batches.append(new_batch)
            new_batch.add_sprite(sprite)
            self.batches.sort(key=lambda batch: batch.z_index)

    def render(self, dest=None):
        for batch in self.batches:
            batch.render(dest=dest)