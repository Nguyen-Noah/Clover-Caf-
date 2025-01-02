import moderngl
import numpy as np
from ..utils.elements import ElementSingleton
from .shader import Shader
from .line2d import Line2D
from ..primitives import vec2, vec3
from ..utils.jmath import JMath

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
        self.lines = [line for line in self.lines if line.begin_frame() >= 0]

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
        """ self.verticies = [
            0.0, 0.0, -10.0, 1.0, 0.0, 0.0,  # Start of line (red)
            200.0, 200.0, -10.0, 0.0, 1.0, 0.0   # End of line (green)
        ] """

        self.setup_buffers()
        self.shader.render(render_method=moderngl.LINES, uniforms={
            'uProjection': self.e['Camera'].get_projection_matrix(),
            'uView': self.e['Camera'].get_view_matrix(),
        })
        #print(self.verticies)


    
    # ===============================
    # Add line2D methods
    # ===============================
    def add_line_2d(self, from_point, to_point, color=vec3(0, 1, 0), lifetime=1):
        if len(self.lines) > DebugDraw.MAX_LINES:
            return
        self.lines.append(Line2D(from_point, to_point, color, lifetime))

    def add_box_2d(self, center: vec2, dimensions: vec2, rotation=0, color=vec3(0, 1, 0), lifetime=1):
        if len(self.lines) > DebugDraw.MAX_LINES:
            return
        bl = center - (dimensions / 2)
        tr = center + (dimensions / 2)

        verticies = [
            vec2(bl.x, bl.y),
            vec2(bl.x, tr.y),
            vec2(tr.x, tr.y),
            vec2(tr.x, bl.y)
        ]

        if rotation != 0:
            for vert in verticies:
                JMath.rotate(vert, rotation, center)

        self.add_line_2d(verticies[0], verticies[1], color, lifetime)
        self.add_line_2d(verticies[0], verticies[3], color, lifetime)
        self.add_line_2d(verticies[1], verticies[2], color, lifetime)
        self.add_line_2d(verticies[2], verticies[3], color, lifetime)

    def add_circle(self, center, radius, color=vec3(0, 1, 0), lifetime=1):
        if len(self.lines) > DebugDraw.MAX_LINES:
            return
        points = [0.0] * 20
        increment = 360 / len(points)
        curr_angle = 0

        for i in range(len(points)):
            tmp = vec2(radius, 0)
            JMath.rotate(tmp, curr_angle, vec2())
            points[i] = tmp + center

            if i > 0:
                self.add_line_2d(points[i - 1], points[i], color, lifetime)

            curr_angle += increment

        self.add_line_2d(points[-1], points[0], color, lifetime)