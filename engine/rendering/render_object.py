import moderngl, glm
from array import array

class Renderer:
    def __init__(self, mgl, program):
        self.mgl = mgl
        self.program = program
        self.vao = None
        self.vbo = None

    def create_vao(self, args=['2f 2f', 'vert', 'texcoord'], instance=None):
        if self.vao:
            self.vao.release()
        if instance:
            arr = [(self.vbo, *args), instance]
        else:
            arr = [(self.vbo, *args)]
        self.vao = self.mgl.ctx.vertex_array(self.program, arr)

    def create_vbo(self, rect, resolution, ctx, angle=0, raw=False):
        win_w, win_h = resolution
        l, t, r, b = rect
        r_w_w = 1 / win_w
        r_w_h = 1 / win_h
        no_t = (t * r_w_h) * -2 + 1
        no_b = ((t + b) * r_w_h) * -2 + 1
        no_l = (l * r_w_w) * 2 - 1
        no_r = ((r + l) * r_w_w) * 2 - 1 

        buffer = [
                # position (x, y), uv coords (x, y)
                no_l, no_t, 0, 0,  # topleft
                no_r, no_t, 1, 0,  # topright
                no_l, no_b, 0, 1,  # bottomleft
                no_r, no_b, 1, 1,  # bottomright
            ]

        self.vbo = self.mgl.ctx.buffer(data=array('f', buffer)) if not raw else buffer
        self.create_vao()

    def update(self, uniforms={}):
        tex_id = 0
        uniform_list = list(self.program)
        for uniform in uniforms:
            if uniform in uniform_list:
                if type(uniforms[uniform]) == moderngl.Texture:
                    # bind tex to next ID
                    uniforms[uniform].use(tex_id)
                    # specify tex ID as uniform target
                    self.program[uniform].value = tex_id
                    tex_id += 1
                else:
                    if isinstance(uniforms[uniform], glm.mat4): 
                        #self.program[uniform].value = uniforms[uniform].to_bytes()
                        self.program[uniform].write(uniforms[uniform].to_bytes())
                    else:
                        self.program[uniform].value = uniforms[uniform]

    def render(self, dest=None, uniforms={}):
        if not dest:
            dest = self.mgl.ctx.screen

        dest.use()
        self.update(uniforms=uniforms)
        self.vao.render(mode=moderngl.TRIANGLE_STRIP)