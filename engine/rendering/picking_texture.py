import moderngl
import numpy as np
from ..utils.elements import Element
from .texture import Texture
import OpenGL.GL as gl

from OpenGL.GL import (
    glBindFramebuffer,
    glReadPixels,
    glGetIntegerv,
    glReadBuffer,
    GL_READ_FRAMEBUFFER,
    GL_FRAMEBUFFER_BINDING,
    GL_COLOR_ATTACHMENT0,
    GL_RGB,
    GL_FLOAT,
)

# engine editor specific, shouldnt be in the engine
class PickingTexture(Element):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.picking_texture = None
        self.fbo = None
        self.depth_texture = None

        #self.texture = Texture(width=self.width, height=self.height)
        self.picking_texture = self.e['Game'].ctx.texture(
            (self.width, self.height), 3, dtype='f4'
        )
        self.picking_texture.filter = (moderngl.NEAREST, moderngl.NEAREST)

        self.depth_texture = self.e['Game'].ctx.depth_texture((self.width, self.height))

        self.fbo = self.e['Game'].ctx.framebuffer(
            color_attachments = [self.picking_texture],
            depth_attachment=self.depth_texture
        )

    def enable_writing(self):
        self.fbo.use()

    def disable_writing(self):
        self.e['Game'].ctx.screen.use()

    def read_pixel(self, x, y):
        prev_fbo = glGetIntegerv(GL_FRAMEBUFFER_BINDING)

        glBindFramebuffer(GL_READ_FRAMEBUFFER, self.fbo.glo)
        glReadBuffer(GL_COLOR_ATTACHMENT0)

        pixels = np.zeros(3, dtype=np.float32)

        glReadPixels(x, y, 1, 1, GL_RGB, GL_FLOAT, pixels)

        glBindFramebuffer(GL_READ_FRAMEBUFFER, prev_fbo)

        print(int(pixels[0]))

        return int(pixels[0])