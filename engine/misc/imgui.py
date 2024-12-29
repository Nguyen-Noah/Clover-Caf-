from ..utils.elements import ElementSingleton
import imgui, sys
from imgui.integrations.pygame import PygameRenderer

FONT_PATH = 'data/fonts'

class ImGui(ElementSingleton):
    def __init__(self, resolution):
        super().__init__()
        imgui.create_context()
        self.renderer = PygameRenderer()
        self.io = imgui.get_io()
        self.io.display_size = resolution
        self.io.ini_file_name = 'imgui.ini'

        self.load_font('LEMONMILK.otf', 20)

    def process_event(self, event):
        self.renderer.process_event(event)

    def start_frame(self):
        try:
            imgui.new_frame()
        except imgui.core.ImGuiError as e:
            pass

    def load_font(self, font_path, font_size):
        io = imgui.get_io()
        io.fonts.add_font_from_file_ttf(f'{FONT_PATH}/{font_path}', font_size)
        self.renderer.refresh_font_texture()

    def update(self, dt, scene):
        self.start_frame()
        scene.scene_imgui()

        imgui.show_test_window()

        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def shutdown(self):
        self.renderer.shutdown()