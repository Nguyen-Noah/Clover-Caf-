import moderngl
import numpy as np
from ..utils.elements import ElementSingleton
from .shader import Shader
from .line2d import Line2D
from ..primitives import vec2, vec3


class DebugDraw(ElementSingleton):
    MAX_LINES = 500

    def __init__(self):
        super().__init__()
        self.lines = []
        # 6 floats per vertex, 2 vertices per line
        self.verticies = [0.0] * (DebugDraw.MAX_LINES * 6 * 2)
        self.shader = Shader('engine/rendering/shaders/vsDebugLine2D.glsl', 'engine/rendering/shaders/debugLine2D.glsl')

        self.started = False

    def setup_buffers(self):
        vbo = self.e['Game'].ctx.buffer(np.array(self.verticies, dtype='f4').tobytes())
        self.shader.create_vao(
            vbo_info=[(vbo, '3f 3f', 'aPos', 'aColor')]
        )

    def begin_frame(self):
        if not self.started:
            self.setup_buffers()
            self.started = True

        # remove dead lines
        for i, line in enumerate(self.lines):
            if line.begin_frame() < 0:
                self.lines.pop(i)

    def draw(self):
        if len(self.lines) <= 0:
            return
        
        index = 0
        for line in self.lines:
            for i in range(2):
                position = line.get_from() if i == 0 else line.get_to()
                color = line.color

                # load position
                self.verticies[index] = position.x
                self.verticies[index + 1] = position.y
                self.verticies[index + 2] = -10

                # load color
                self.verticies[index + 3] = color.x
                self.verticies[index + 4] = color.y
                self.verticies[index + 5] = color.z

                index += 6

        self.setup_buffers()
        self.shader.render(render_method=moderngl.LINES, uniforms={
            'uProjection': self.e['Camera'].get_projection_matrix(),
            'uView': self.e['Camera'].get_view_matrix(),
        })
        print(self.verticies)


    
    # ===============================
    # Add line2D methods
    # ===============================
    def add_line_2d(self, from_point, to_point, color=vec3(0, 1, 0), lifetime=1):
        if len(self.lines) > DebugDraw.MAX_LINES:
            return
        self.lines.append(Line2D(from_point, to_point, color, lifetime))
