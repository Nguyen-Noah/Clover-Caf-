import moderngl
import numpy as np
from engine.utils.elements import ElementSingleton
from .line2d import Line2D
from engine.primitives import vec2, vec3
from engine.utils.jmath import JMath

class DebugDraw(ElementSingleton):
    MAX_LINES = 500

    def __init__(self):
        super().__init__()
        self.lines = []
        # 6 floats per vertex, 2 vertices per line
        #self.vertices = [0.0] * (DebugDraw.MAX_LINES * 6 * 2)
        self.vertices = np.zeros((DebugDraw.MAX_LINES * 2 * 6), dtype='f4')
        self.shader = self.e['Assets'].get_shader('vsDebugLine2D.glsl', 'debugLine2D.glsl')

        self.started = False
        self.vao = None
        self.vbo = None
        self.setup_buffers()

    def setup_buffers(self):
        self.vbo = self.e['Game'].ctx.buffer(np.array(self.vertices, dtype='f4').tobytes())

        self.vao = self.e['Game'].ctx.vertex_array(
            self.shader.program,
            [(self.vbo, '3f 3f', 'aPos', 'aColor')]
        )

    def reset_vertices(self):
        self.vertices = np.zeros_like(self.vertices)

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
        self.reset_vertices()       # eventually want to find a better place for this
        for line in self.lines:
            pos_from = line.get_from()
            pos_to = line.get_to()
            color = line.color

            # First vertex (from_point)
            self.vertices[index:index + 3] = [pos_from.x, pos_from.y, -10]
            self.vertices[index + 3:index + 6] = [color.x, color.y, color.z]

            # Second vertex (to_point)
            self.vertices[index + 6:index + 9] = [pos_to.x, pos_to.y, -10]
            self.vertices[index + 9:index + 12] = [color.x, color.y, color.z]

            index += 12

        self.vbo.write(self.vertices.tobytes())

        self.shader.render(vao=self.vao, render_method=moderngl.LINES, uniforms={
            'uProjection': self.e['Camera'].get_projection_matrix(),
            'uView': self.e['Camera'].get_view_matrix(),
        })


    
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

        vertices = [
            vec2(bl.x, bl.y),
            vec2(bl.x, tr.y),
            vec2(tr.x, tr.y),
            vec2(tr.x, bl.y)
        ]

        if rotation != 0:
            for vert in vertices:
                JMath.rotate(vert, rotation, center)

        self.add_line_2d(vertices[0], vertices[1], color, lifetime)
        self.add_line_2d(vertices[0], vertices[3], color, lifetime)
        self.add_line_2d(vertices[1], vertices[2], color, lifetime)
        self.add_line_2d(vertices[2], vertices[3], color, lifetime)

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