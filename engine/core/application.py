from pathlib import Path
from dataclasses import dataclass

import moderngl

from Runestone.src.settings import Settings
from engine.assets.assets import Assets
from engine.core.layer import Layer
from engine.core.layer_stack import LayerStack
from engine.imgui.imgui_layer import ImGuiLayer
from engine.misc.input import Input
from engine.misc.window import Window
from engine.rendering.renderer import Renderer
from engine.utils.elements import ElementSingleton
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
    resolution: tuple = Settings.RESOLUTION,
    fps_cap: int = Settings.FPS,
    working_directory: str = "",
    command_line_args = None

# remake of __init__.py to initialize applications dynamically
class Application(ElementSingleton):
    _instance = None

    def __init__(self, specification: ApplicationSpecification):
        if Application._instance is not None:
            raise Exception("Application already exists.")
        super().__init__()
        Application._instance = self

        self.spec = specification
        self.running = True
        self.minimized = False      # needed?

        self.fps = self.spec.fps_cap

        if self.spec.working_directory:
            print(self.spec.working_directory)
            set_working_dir(Path(self.spec.working_directory))

        # initialize the window
        self.window = Window(resolution=self.spec.resolution, caption=self.spec.name, fps_cap=self.spec.fps_cap)

        # initialize layer stack
        self.layer_stack = LayerStack()

        # initialize input
        self.input = Input("data/config/key_mappings.json") # maybe make this static

        # initialize assets
        self.assets = Assets(shader_path="Runestone/assets/shaders") # TODO: maybe make this static too and use the working_dir

        # initialize the renderer
        self.ctx = moderngl.create_context(require=330)
        self.renderer = Renderer()

        # initialize imgui
        self.imgui_layer = ImGuiLayer()
        self.push_overlay(self.imgui_layer)

        print("Application initialized.")

    @staticmethod
    def get():
        if Application._instance is not None:
            return Application._instance

    # needed?
    def shutdown(self):
        """
        Cleans up resources before closing application
        """
        print("Application shutting down.")

    def push_overlay(self, layer: Layer):
        self.layer_stack.push_overlay(layer)
        layer.on_attach()

    def push_layer(self, layer: Layer):
        self.layer_stack.push_overlay(layer)
        layer.on_attach()

    def close(self):
        self.running = False

    def run(self):
        while self.running:
            self.input.update()

            if not self.minimized:
                dt = self.window.dt
                for layer in self.layer_stack:
                    layer.update(dt)

                self.imgui_layer.begin()
                for layer in self.layer_stack:
                    layer.imgui_render()
                self.imgui_layer.end()

            self.window.update()
        self.shutdown()