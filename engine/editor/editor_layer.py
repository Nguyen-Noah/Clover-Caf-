from engine.editor.gridlines import GridLines
from engine.editor.mouse_controls import MouseControls
from engine.utils.elements import ElementSingleton


class EditorUtils(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.mouse_controls = MouseControls()
        self.gridlines = GridLines()

    def update(self, dt):
        self.mouse_controls.update(dt)
        self.gridlines.update()