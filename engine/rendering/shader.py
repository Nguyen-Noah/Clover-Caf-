from ..utils.io import read_f
from ..utils.elements import Element, ElementSingleton
import moderngl, glm
import numpy as np

class ShaderRegistry(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.shaders = {}

    def register_shader(self, shader):
        name = shader.__class__.__name__
        if name not in self.shaders:
            self.shaders[name] = shader
        else:
            pass
    
    def delete_shader(self, shader):
        if shader in self.shaders:
            del self.shaders[shader]

class Shader(Element):
    def __init__(self, vert_path, frag_path):
        super().__init__()
        self.e['ShaderRegistry'].register_shader(self)
        self.vertex = vert_path
        self.fragment = frag_path
        self.program = self.e['Game'].ctx.program(vertex_shader=read_f(self.vertex), fragment_shader=read_f(self.fragment))
        self.vao = None
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

    def create_vao(self, vbo_info, ibo):
        """
        Creates a Vertex Array Object (VAO)

        Parameters:
            vbo_info: list of tuples - List containing VBO and attribute mapping information.
                                        Format: [(vbo, format, *attributes), ...]
            ibo: moderngl.Buffer or None - Optional Index Buffer Object (IBO)

        Returns:
            moderngl.VertexArray - The created VAO
        """
        self.vao = self.e['Game'].ctx.vertex_array(self.program, vbo_info, ibo)

    def delete(self):
        self.program.release()
        if self.vao:
            self.vao.release()
        if self.ibo:
            self.ibo.release()
        for vbo, _, _ in self.vbo_info:
            vbo.release()

    def render(self, dest=None, uniforms={}, instances=None):
        if not dest:
            dest = self.e['Game'].ctx.screen

        dest.use()

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
            self.vao.render(mode=moderngl.TRIANGLES, instances=len(instances))
        else:
            self.vao.render(mode=moderngl.TRIANGLES)
        
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