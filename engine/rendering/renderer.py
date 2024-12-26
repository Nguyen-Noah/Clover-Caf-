import moderngl, pygame
from array import array
from ..utils.elements import ElementSingleton

class Renderer(ElementSingleton):
    def __init__(self, groups=['default']):
        super().__init__()
        self.ctx = moderngl.create_context(require=330)
        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y) , texture coordinates (x, y)
            -1.0, 1.0, 0.0, 0.0,
            -1.0, -1.0, 0.0, 1.0,
            1.0, 1.0, 1.0, 0.0,
            1.0, -1.0, 1.0, 1.0,
        ]))
        
        self.quad_buffer_notex = self.ctx.buffer(data=array('f', [
            # position (x, y)
            -1.0, 1.0,
            -1.0, -1.0,
            1.0, 1.0,
            1.0, -1.0,
        ]))

        self.groups = groups
        self.render_queue = {}
        self.i = 0
        self.render_count= 0
        self.reset()

    def reset(self):
        self.i = 0
        for group in self.groups:
            self.render_queue[group] = []

    def blit(self, program, group='default', uniforms={}, instances=None):
        self.render_queue[group].append((program, uniforms, instances, self.i))
        self.i += 1

    def render(self):
        self.ctx.clear(0.1, 0.1, 0.1, 1.0)

        # render stuff
        for group in self.render_queue:
            if group in self.groups:
                for blit in self.render_queue[group]:
                    # blit structure: [0]=program, [1]=uniforms, [2]=instances, [3]=i
                    if blit[2] is None:
                        blit[0].render(uniforms=blit[1])
                    else:
                        blit[0].render(uniforms=blit[1], instances=blit[2])

        pygame.display.flip()
        self.reset()