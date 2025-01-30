from engine.utils.elements import ElementSingleton


class Layer(ElementSingleton):
    def __init__(self, name="Layer"):
        super().__init__()
        self.name = name

    def on_attach(self):
        pass

    def on_detach(self):
        pass

    def update(self, dt):
        pass

    def imgui_render(self):
        pass