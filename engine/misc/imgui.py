import imgui
from imgui.integrations.pygame import PygameRenderer
from ..utils.elements import ElementSingleton
from .game_view_window import GameViewWindow

FONT_PATH = 'data/fonts'

class ImGui(ElementSingleton):
    def __init__(self, resolution):
        super().__init__()
        imgui.create_context()
        self.renderer = PygameRenderer()
        self.resolution = resolution
        self.io = imgui.get_io()
        self.io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
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

    def setup_dock_space(self):
        window_flags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING

        imgui.set_next_window_position(0, 0, imgui.ALWAYS)
        imgui.set_next_window_size(self.resolution[0], self.resolution[1])

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        window_flags = window_flags | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | \
                imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | \
                imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS
        imgui.begin("Dockspace", True, window_flags)
        imgui.pop_style_var(2)

        # dockspace
        imgui.dockspace(imgui.get_id("Dockspace"))

    def update(self, dt, scene):
        self.start_frame()

        self.setup_dock_space()

        scene.scene_imgui()

        imgui.show_test_window()
        GameViewWindow.imgui(self.e)
        imgui.end()

        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def shutdown(self):
        self.renderer.shutdown()