from ..utils.elements import Element
from .texture import Texture

class Framebuffer(Element):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height

        self.texture = Texture(width=self.width, height=self.height)
        self.fbo = self.e['Game'].ctx.framebuffer(
            color_attachments = [self.texture.texture]
        )

    def use(self):
        self.fbo.use()

    def unbind(self):
        self.e['Game'].ctx.screen.use()

    def get_id(self):
        return self.texture.get_id()