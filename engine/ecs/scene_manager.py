from ..utils.elements import ElementSingleton

class SceneManager(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.current_scene = 'default'
