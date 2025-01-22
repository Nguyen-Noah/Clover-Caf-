import moderngl, pygame
from ..utils.elements import ElementSingleton
from ..components.sprite_renderer import SpriteRenderer
from .render_batch import RenderBatch

class Renderer(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.current_shader = ('vsDefault.glsl', 'default.glsl')
        self.rebind_shader = False

        self.max_batch_size = 1000
        self.batches = []

    def add(self, entity):
        spr = entity.get_component(SpriteRenderer)

        if spr is not None:
            self._add(spr)

    def _add(self, sprite):
        added = False
        for batch in self.batches:
            if batch.can_accept(sprite) and batch.has_room and batch.z_index == sprite.entity.transform.z_index:
                tex = sprite.get_texture()
                if tex is None or batch.has_texture(tex) or batch.has_texture_room():
                    batch.add_sprite(sprite)
                    added = True
                    break

        if not added:
            texture_size = sprite.get_texture().size if sprite.get_texture() else None
            new_batch = RenderBatch(z_index=sprite.entity.transform.z_index, max_batch_size=self.max_batch_size, texture_size=texture_size)
            self.batches.append(new_batch)
            new_batch.add_sprite(sprite)
            self.batches.sort(key=lambda batch: batch.z_index)

    def destroy_entity(self, entity):
        if entity.get_component(SpriteRenderer) is None:
            return

        for batch in self.batches:
            if batch.destroy_if_exists(entity):
                pass

    def bind_shader(self, shader: tuple):
        self.current_shader = self.e['Assets'].get_shader(*shader)

    def render(self):
        for batch in self.batches:
            batch.render()