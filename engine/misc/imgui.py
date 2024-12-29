from ..utils.elements import ElementSingleton
import imgui, sys
from imgui.integrations.pygame import PygameRenderer

FONT_PATH = 'data/fonts'

class ImGui(ElementSingleton):
    def __init__(self, resolution):
        super().__init__()
        imgui.create_context()
        self.renderer = PygameRenderer()
        imgui.get_io().display_size = resolution

        self.load_font('LEMONMILK.otf', 20)

    def process_event(self, event):
        self.renderer.process_event(event)

    def start_frame(self):
        imgui.new_frame()

    def load_font(self, font_path, font_size):
        io = imgui.get_io()
        io.fonts.add_font_from_file_ttf(f'{FONT_PATH}/{font_path}', font_size)
        self.renderer.refresh_font_texture()

    def update(self):
        if imgui.begin_main_menu_bar():
            if imgui.begin_menu("File", True):

                clicked_quit, selected_quit = imgui.menu_item(
                    "Quit", "Cmd+Q", False, True
                )

                if clicked_quit:
                    sys.exit(0)

                imgui.end_menu()
            imgui.end_main_menu_bar()
        imgui.show_test_window()

        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def shutdown(self):
        self.renderer.shutdown()