import sys
import numpy as np
import moderngl, glm, math

from engine.utils.elements import Element
from engine.components.sprite_renderer import SpriteRenderer

np.set_printoptions(threshold=sys.maxsize)

SHADER_PATH = 'engine/rendering/shaders'


"""
TODO: update render() to fetch all entities with a SpriteRendererComponent.
    -  Instead of manually adding entities, on the first iteration of render(), 
       check if the SpriteRenderer is dirty (which will always be True by default)
       then load the vertex properties.
"""

class RenderBatch(Element):
    """A batch responsible for drawing multiple SpriteRenderers with the same textures/size."""

    BATCH_INDEX = 0

    # Vertex attribute sizes
    POS_SIZE = 2
    COLOR_SIZE = 4
    TEX_COORDS_SIZE = 2
    TEX_ID_SIZE = 1
    ENTITY_ID_SIZE = 1
    VERTEX_SIZE = POS_SIZE + COLOR_SIZE + TEX_COORDS_SIZE + TEX_ID_SIZE + ENTITY_ID_SIZE

    def __init__(self, z_index=0, max_batch_size=1000, texture_size=None):
        super().__init__()
        """
        Vertex
        ========    
        Pos                 Color                           tex coords      tex id
        float, float,       float, float, float, float      float, float    float
        """

        # Batch info
        self.MAX_BATCH_SIZE = max_batch_size
        self.z_index = z_index
        self.batch_index = RenderBatch.BATCH_INDEX
        RenderBatch.BATCH_INDEX += 1

        # Sprite storage
        self.sprites = [None] * self.MAX_BATCH_SIZE           # SpriteRenderer
        self.num_sprites = 0
        self.has_room = True

        # GPU data
        self.vertices = np.zeros((self.MAX_BATCH_SIZE * 4 * RenderBatch.VERTEX_SIZE), dtype=np.float32)
        self.vao = None
        self.vbo = None
        self.picking_vao = None         # not the greatest approach, but it works

        # Shaders, textures
        self.shader = self.e['Assets'].get_shader('vsDefault.glsl', 'default.glsl')
        self.textures = []
        self.texture_array = None
        self.texture_size = texture_size

        # For re-buffering logic (when a sprite is dirty or removed)
        self.rebuffer_needed = False

        self.setup_buffers()

        self.active_vao = self.vao

    def setup_buffers(self):
        self.vbo = self.e['Game'].ctx.buffer(np.array(self.vertices, dtype='f4').tobytes())
        ibo = self.e['Game'].ctx.buffer(np.array(self.generate_indices(), dtype='i4').tobytes())
        self.vao = self.e['Game'].ctx.vertex_array(
            self.shader.program,
            [(self.vbo, '2f 4f 2f 1f 1f', 'aPos', 'aColor', 'aTexCoords', 'aTexId', 'aEntityId')],
            ibo
        )
        self.picking_vao = self.e['Game'].ctx.vertex_array(
            self.e['Assets'].get_shader('vsPickingShader.glsl', 'pickingShader.glsl').program,
            [(self.vbo, '2f 4f 2f 1f 1f', 'aPos', 'aColor', 'aTexCoords', 'aTexId', 'aEntityId')],
            ibo
        )

    def generate_indices(self):
        elements = []
        for i in range(self.MAX_BATCH_SIZE):
            self.load_element_indices(elements, i)
        return elements

    @staticmethod
    def load_element_indices(elements, index):
        offset = 4 * index

        elements.append(offset + 3)
        elements.append(offset + 2)
        elements.append(offset + 0)

        elements.append(offset + 0)
        elements.append(offset + 2)
        elements.append(offset + 1)

    def destroy_if_exists(self, entity):
        target = entity.get_component(SpriteRenderer)

        for i in range(self.num_sprites):
            if self.sprites[i] == target:
                last_index = self.num_sprites - 1

                # If not removing the last sprite, swap the last one into i
                if i != last_index:
                    self.sprites[i] = self.sprites[last_index]
                    self.sprites[last_index] = None
                    # Mark the moved sprite as dirty, so it updates its vertex data
                    self.sprites[i].dirty = True
                else:
                    # If it's already the last sprite, just drop it
                    self.sprites[i] = None

                self.num_sprites -= 1
                self.has_room = True

                self._clear_vertex_properties(last_index)

                self.rebuffer_needed = True
                return True
        return False

    def _clear_vertex_properties(self, index):
        """
        Zeros out the vertex data for the slot at index
        so the old sprite doesn't remain in the buffer.
        """
        offset = index * 4 * self.VERTEX_SIZE
        length = 4 * self.VERTEX_SIZE
        self.vertices[offset:offset + length] = 0

    def add_sprite(self, sprite: SpriteRenderer):
        texture = sprite.get_texture()

        if texture and self.texture_size and self.texture_size != texture.size:
            raise ValueError("Texture size mismatch in batch")

        if texture and not self.texture_size:
            self.texture_size = texture.size

        index = self.num_sprites
        self.sprites[index] = sprite
        self.num_sprites += 1

        if sprite.get_texture() is not None and sprite.get_texture() not in self.textures:
            self.textures.append(sprite.get_texture())
            self.create_texture_array()

        self.load_vertex_properties(index)

        if self.num_sprites >= self.MAX_BATCH_SIZE:
            self.has_room = False

    def can_accept(self, sprite):
        texture = sprite.sprite.texture
        return self.has_room and (self.texture_size is None or (texture and self.texture_size == texture.size))

    def load_vertex_properties(self, index):
        """
        Load the given sprite's properties into the appropriate part of self.vertices.
        """
        sprite: SpriteRenderer = self.sprites[index]
        color = sprite.color
        tex_coords = sprite.get_tex_coords()


        # Find the texture ID
        tex_id = 0
        if sprite.get_texture() is not None:
            for i, tex in enumerate(self.textures):
                if tex == sprite.get_texture():
                    tex_id = i + 1
                    break

        # Build the transform matrix if rotated
        transform_matrix = glm.mat4(1.0)
        is_rotated = sprite.entity.transform.rotation != 0.0
        if is_rotated:
            transform_matrix = glm.translate(transform_matrix,
                                             glm.vec3(sprite.entity.transform.position.x,
                                                      sprite.entity.transform.position.y,
                                                      0.0))
            transform_matrix = glm.rotate(transform_matrix,
                                          math.radians(sprite.entity.transform.rotation),
                                          glm.vec3(0, 0, 1))
            transform_matrix = glm.scale(transform_matrix,
                                         glm.vec3(sprite.entity.transform.scale.x,
                                                  sprite.entity.transform.scale.y,
                                                  1.0))

        offset = index * 4 * self.VERTEX_SIZE

        # Add vertices with the appropriate properties
        x_add = 0.5
        y_add = 0.5
        for i in range(4):
            if i == 1:
                y_add = -0.5
            elif i == 2:
                x_add = -0.5
            elif i == 3:
                y_add = 0.5

            current_pos = glm.vec4(
                sprite.entity.transform.position.x + (x_add * sprite.entity.transform.scale.x),
                sprite.entity.transform.position.y + (y_add * sprite.entity.transform.scale.y),
                0.0,
                1.0
            )

            if is_rotated:
                # Apply the transformation matrix to the local coordinates
                current_pos = transform_matrix * glm.vec4(x_add, y_add, 0.0, 1.0)

            self.vertices[offset:offset + self.VERTEX_SIZE] = [
                current_pos.x, current_pos.y,
                color[0], color[1], color[2], color[3],
                tex_coords[i].x, tex_coords[i].y,
                tex_id,
                sprite.entity.uid
            ]

            offset += self.VERTEX_SIZE

    # MOVE TO ASSETS FILE
    def create_texture_array(self):
        width, height = self.texture_size if self.texture_size is not None else self.textures[0].size
        components = 4

        for tex in self.textures:
            if tex.size != (width, height):
                self.sprite_conflict = True
                break

        data_list = []
        for tex in self.textures:
            tex = tex.texture
            data_list.append(np.frombuffer(tex.read(), dtype=np.uint8))

        tex_arr_data = np.concatenate(data_list)

        depth = len(self.textures)
        self.texture_array = self.e['Game'].ctx.texture_array((width, height, depth), components, tex_arr_data)
        self.texture_array.filter = (moderngl.NEAREST, moderngl.NEAREST)

    def has_texture_room(self):
        return len(self.textures) < 8
    
    def has_texture(self, tex):
        return tex in self.textures

    def render(self):
        """
        1) Update vertex data for dirty or moved sprites.
        2) If necessary, re-upload vertices to the GPU.
        3) Bind the appropriate shader program & texture array.
        4) Issue draw call if there's anything to draw.
        """
        # Skip if there's nothing to draw
        if self.num_sprites == 0:
            return

        rebuffer_data = self.rebuffer_needed

        for i in range(self.num_sprites):
            spr = self.sprites[i]
            if spr is None:
                continue

            if spr.is_dirty():
                self.load_vertex_properties(i)
                spr.clean()
                rebuffer_data = True

            if spr.entity.transform.z_index is not self.z_index:
                self.destroy_if_exists(spr.entity)
                self.e['Renderer'].add(spr.entity)

        if rebuffer_data:
            self.vbo.write(self.vertices.tobytes())
            self.rebuffer_needed = False

        # temporary solution until i figure out dynamic program swapping
        if self.e['Renderer'].current_shader == self.e['Assets'].get_shader('vsPickingShader.glsl', 'pickingShader.glsl'):
            self.active_vao = self.picking_vao
        else:
            self.active_vao = self.vao

        self.shader = self.e['Renderer'].current_shader
        self.shader.render(vao=self.active_vao, uniforms={
            'uProjection': self.e['Camera'].get_projection_matrix(),
            'uView': self.e['Camera'].get_view_matrix(),
            'uTextures': self.texture_array
        })

    def __repr__(self):
        return f'<RenderBatch index={self.batch_index} z_index={self.z_index} num_sprites={self.num_sprites}'