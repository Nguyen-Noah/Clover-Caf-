from ..utils.io import read_f
from ..utils.elements import Element, ElementSingleton
import moderngl, glm
import numpy as np

class Shader(Element):
    def __init__(self, vert_path, frag_path, geo_path=None):
        super().__init__()
        self.vertex = vert_path
        self.fragment = frag_path
        self.geometry = geo_path
        if self.geometry:
            self.program = self.e['Game'].ctx.program(
                vertex_shader=read_f(self.vertex), 
                geometry_shader=read_f(self.geometry), 
                fragment_shader=read_f(self.fragment))
        else:
            self.program = self.e['Game'].ctx.program(
                vertex_shader=read_f(self.vertex), 
                fragment_shader=read_f(self.fragment))
        self.vbo = []

        self.uniform_cache = {}

        self.textures = []

    def create_vbo(self, data, dtype='f4'):
        """
        Creates a Vertex Buffer Object (VBO)

        Parameters:
            data: np.ndarray or list - Data to upload to the VBO
            dtype: str - Data type of the buffer (default is f4)
            dynamic: bool - If True, creates a dynamic buffer for frequently updated data
        
            Returns:
                moderngl.Buffer - The created VBO
        """

        buffer_data = np.array(data, dtype=dtype).tobytes()
        vbo = self.e['Game'].ctx.buffer(buffer_data)
        self.vbo.append(vbo)
        return vbo

    def delete(self):
        self.program.release()
        if self.vao:
            self.vao.release()
        if self.ibo:
            self.ibo.release()
        for vbo, _, _ in self.vbo_info:
            vbo.release()

    def render(self, vao, uniforms={}, instances=None, render_method = moderngl.TRIANGLES):

        # Update loop
        tex_id = 0
        uniform_list = list(self.program)
        for uniform in uniforms:
            if uniform in uniform_list:
                if uniform in self.uniform_cache:
                    cached_value = self.uniform_cache[uniform]
                    new_value = uniforms[uniform]

                    if isinstance(cached_value, np.ndarray) and isinstance(new_value, np.ndarray):
                        if not np.array_equal(cached_value, new_value):
                            self._update_uniform(uniform, new_value, tex_id)
                    else:
                        if cached_value != new_value:
                            self._update_uniform(uniform, new_value, tex_id)
                else:
                    self._update_uniform(uniform, uniforms[uniform], tex_id)

        # Render with instances or default
        if instances:
            vao.render(mode=render_method, instances=len(instances))
        else:
            vao.render(mode=render_method)
        
        self.detatch_textures()

    def _update_uniform(self, uniform, value, tex_id):
        if isinstance(value, moderngl.Texture) or isinstance(value, moderngl.TextureArray):
            # Bind texture to the next ID
            value.use(tex_id)
            # Specify texture ID as uniform target
            self.program[uniform].value = tex_id
            tex_id += 1
            self.textures.append(value)
        elif isinstance(value, glm.mat4):
            self.program[uniform].write(value.to_bytes())
        else:
            self.program[uniform].value = value

    def detatch_textures(self):
        for tex in self.textures:
            tex.release()

        self.textures = []