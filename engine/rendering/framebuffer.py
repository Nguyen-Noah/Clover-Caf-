from ..utils.elements import Element
from .texture import Texture

class Framebuffer(Element):
    def __init__(self, width, height):
        super().__init__()
        self.width = width
        self.height = height
        self.fbo = None
        self.texture = None

        self.build()

    def build(self):
        self.texture = Texture(width=self.width, height=self.height)
        self.fbo = self.e['Game'].ctx.framebuffer(
            color_attachments=[self.texture.texture]
        )

    def resize(self, new_width, new_height):
        if (new_width == self.width) and (new_height == self.height):
            return

        self.width = new_width
        self.height = new_height

        self.fbo.release()
        self.texture.release()

        self.build()

    def use(self):
        self.fbo.use()

    def unbind(self):
        self.e['Game'].ctx.screen.use()

    def get_id(self):
        return self.texture.get_id()