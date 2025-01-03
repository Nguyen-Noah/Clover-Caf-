import numpy as np
import moderngl
from ..utils.elements import Element
from ..components.sprite_renderer import SpriteRenderer

SHADER_PATH = 'engine/rendering/shaders'

class RenderBatch(Element):
    def __init__(self, z_index=0, max_batch_size=1000):
        super().__init__()
        """
        Vertex
        ========    
        Pos                 Color                           tex coords      tex id
        float, float,       float, float, float, float      float, float    float
        """
        self.POS_SIZE = 2
        self.COLOR_SIZE = 4
        self.TEX_COORDS_SIZE = 2
        self.TEX_ID_SIZE = 1
        self.ENTITY_ID_SIZE = 1
        self.VERTEX_SIZE = self.POS_SIZE + self.COLOR_SIZE + self.TEX_COORDS_SIZE + self.TEX_ID_SIZE + self.ENTITY_ID_SIZE

        self.sprites = [None] * max_batch_size           # SpriteRenderer
        self.num_sprites = 0
        self.has_room = True

        self.vao = None
        self.picking_vao = None         # not the greatest approach, but it works
        self.vbo = None

        self.MAX_BATCH_SIZE = max_batch_size
        self.shader = self.e['Assets'].get_shader('vsDefault.glsl', 'default.glsl')

        self.vertices = [0.0] * (self.MAX_BATCH_SIZE * 4 * self.VERTEX_SIZE)

        self.textures = []
        self.texture_array = None

        self.z_index = z_index

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
    
    def load_element_indices(self, elements, index):
        offset = 4 * index

        elements.append(offset + 3)
        elements.append(offset + 2)
        elements.append(offset + 0)

        elements.append(offset + 0)
        elements.append(offset + 2)
        elements.append(offset + 1)

    def add_sprite(self, sprite: SpriteRenderer):
        index = self.num_sprites
        self.sprites[index] = sprite
        self.num_sprites += 1

        if sprite.get_texture() is not None and sprite.get_texture() not in self.textures:
            self.textures.append(sprite.get_texture())
            self.create_texture_array()

        self.load_vertex_properties(index)

        if self.num_sprites >= self.MAX_BATCH_SIZE:
            self.has_room = False

    def load_vertex_properties(self, index):
        sprite = self.sprites[index]

        color = sprite.color
        tex_coords = sprite.get_tex_coords()

        offset = index * 4 * self.VERTEX_SIZE

        tex_id = 0
        if sprite.get_texture() is not None:
            for i, tex in enumerate(self.textures):
                if tex == sprite.get_texture():
                    tex_id = i + 1
                    break

        # add vertices with the appropriate properties
        x_add = 1.0
        y_add = 1.0
        for i in range(4):
            if i == 1:
                y_add = 0.0
            elif i == 2:
                x_add = 0.0
            elif i == 3:
                y_add = 1.0

            # Load positions
            tr = sprite.entity.transform
            self.vertices[offset] = tr.position.x + (x_add * tr.scale.x)
            self.vertices[offset + 1] = tr.position.y + (y_add * tr.scale.y)

            # Load color
            self.vertices[offset + 2] = color[0]
            self.vertices[offset + 3] = color[1]
            self.vertices[offset + 4] = color[2]
            self.vertices[offset + 5] = color[3]

            # Load texture coordinates
            self.vertices[offset + 6] = tex_coords[i].x
            self.vertices[offset + 7] = tex_coords[i].y

            # Load texture ID
            self.vertices[offset + 8] = tex_id

            # Load entity ID
            self.vertices[offset + 9] = sprite.entity.uid

            offset += self.VERTEX_SIZE

    # MOVE TO ASSETS FILE
    def create_texture_array(self):
        width, height = self.textures[0].size
        components = 4

        for tex in self.textures:
            if tex.size != (width, height):
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
        rebuffer_data = False
        for i in range(self.num_sprites):
            if self.sprites[i] is None:
                break
            spr = self.sprites[i]
            if spr.is_dirty():
                self.load_vertex_properties(i)
                spr.clean()
                rebuffer_data = True

        if rebuffer_data:
            self.vbo.write(np.array(self.vertices, dtype='f4').tobytes())

        # temporary solution until i figure out dynamic program swapping
        if self.e['Renderer'].current_shader == self.e['Assets'].get_shader('vsPickingShader.glsl', 'pickingShader.glsl'):
            self.active_vao = self.picking_vao
        else:
            self.active_vao = self.vao

        self.shader = self.e['Renderer'].current_shader
        self.create_texture_array()
        self.shader.render(vao=self.active_vao, uniforms={
            'uProjection': self.e['Camera'].get_projection_matrix(),
            'uView': self.e['Camera'].get_view_matrix(),
            'uTextures': self.texture_array
        })