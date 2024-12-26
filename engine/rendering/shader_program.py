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

class ShaderProgram(Element):
    def __init__(self, vert_path, frag_path):
        super().__init__()
        self.e['ShaderRegistry'].register_shader(self)
        self.vertex = vert_path
        self.fragment = frag_path
        self.program = self.e['Renderer'].ctx.program(vertex_shader=read_f(self.vertex), fragment_shader=read_f(self.fragment))
        self.vao = None
        self.vbo = []

        self.uniform_cache = {}

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
        vbo = self.e['Renderer'].ctx.buffer(buffer_data)
        self.vbo.append(vbo)
        return vbo
    
    def create_ibo(self, indices, dtype='f4'):
        ibo = self.e['Renderer'].ctx.buffer(np.array(indices, dtype=dtype).tobyte())
        self.ibo = ibo
        return ibo

    def create_vao(self, vbo_info):
        """
        Creates a Vertex Array Object (VAO)

        Parameters:
            vbo_info: list of tuples - List containing VBO and attribute mapping information.
                                        Format: [(vbo, format, *attributes), ...]
            ibo: moderngl.Buffer or None - Optional Index Buffer Object (IBO)

        Returns:
            moderngl.VertexArray - The created VAO
        """
        print(vbo_info)
        self.vao = self.e['Renderer'].ctx.vertex_array(self.program, vbo_info)

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
            dest = self.e['Renderer'].ctx.screen

        dest.use()

        # update loop
        tex_id = 0
        uniform_list = list(self.program)
        for uniform in uniforms:
            if uniform in uniform_list:
                if self.uniform_cache.get(uniform) != uniforms[uniform]:
                    if type(uniforms[uniform]) == moderngl.Texture:
                        # bind tex to next ID
                        uniforms[uniform].use(tex_id)
                        # specify tex ID as uniform target
                        self.program[uniform].value = tex_id
                        tex_id += 1
                    elif isinstance(uniforms[uniform], glm.mat4):
                        #self.program[uniform].value = uniforms[uniform].to_bytes()
                        self.program[uniform].write(uniforms[uniform].to_bytes())
                    else:
                        self.program[uniform].value = uniforms[uniform]
                    self.uniform_cache[uniform] = uniforms[uniform]

        if instances:
            self.vao.render(mode=moderngl.TRIANGLE_STRIP, instances=len(instances))
        else:
            self.vao.render(mode=moderngl.TRIANGLE_STRIP)