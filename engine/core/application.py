from pathlib import Path
from dataclasses import dataclass

from engine.misc.imgui_layer import ImGuiLayer
from engine.misc.input import Input
from engine.misc.window import Window
from engine.rendering.renderer import Renderer
from engine.utils.io import set_working_dir

"""
TODO:
    - remove all calls to ImguiLayer from the engine
        - input.py
    - update input.py path to use the working directory variable
"""




@dataclass
class ApplicationSpecification:
    """
    Initializer for Application
    """
    name: str = "Rune Application",
    resolution: tuple = (1080, 720),
    fps_cap: int = 60,
    working_directory: str = "",
    command_line_args = None

# remake of __init__.py to initialize applications dynamically
class Application:
    _instance = None

    def __init__(self, specification: ApplicationSpecification):
        if Application._instance is not None:
            raise Exception("Application already exists.")
        Application._instance = self

        self.spec = specification
        self.running = True
        self.minimized = False      # needed?

        if self.spec.working_directory:
            set_working_dir(Path(self.spec.working_directory))

        # initialize the window
        self.window = Window(resolution=self.spec.resolution, caption=self.spec.name, fps_cap=self.spec.fps_cap)

        # initialize input
        self.input = Input(PATH)

        # initialize the renderer
        self.renderer = Renderer()

        # initialize imgui
        self.imgui_layer = ImGuiLayer(self.spec.resolution, "INITIALIZE PICKING TEXTURE SOMEWHERE")

        print("Application initialized.")

    @staticmethod
    def get():
        if Application._instance is not None:
            return Application._instance

    def run(self):
        while self.running:
            self.window.update()
            self.input.update()

            if not self.minimized:
                pass

        self.shutdown()

    # needed?
    def shutdown(self):
        """
        Cleans up resources before closing application
        """
        print("Application shutting down.")