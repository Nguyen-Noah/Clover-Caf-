import imgui, pygame
from imgui.integrations.pygame import PygameRenderer

from engine.editor.scene_hierarchy_window import SceneHierarchyWindow
from engine.utils.elements import ElementSingleton
from engine.editor.game_view_window import GameViewWindow
from engine.editor.properties_window import PropertiesWindow
from engine.editor.menu_bar import MenuBar

FONT_PATH = 'data/fonts'

class ImGui(ElementSingleton):
    def __init__(self, resolution, picking_texture):
        super().__init__()
        imgui.create_context()
        self.renderer = PygameRenderer()
        self.resolution = resolution
        self.io = imgui.get_io()
        self.io.config_flags |= imgui.CONFIG_DOCKING_ENABLE
        self.io.display_size = resolution
        self.io.ini_file_name = 'imgui.ini'

        self.load_font('LEMONMILK.otf', 20)

        self.properties_window = PropertiesWindow(picking_texture)
        self.scene_hierarchy_window = SceneHierarchyWindow()

        self.menu_bar = MenuBar()

    def process_event(self, event):
        self.renderer.process_event(event)  # Default PygameRenderer event handling

        io = imgui.get_io()
        mods = pygame.key.get_mods()

        # Synchronize modifier keys
        io.key_ctrl = mods & pygame.KMOD_CTRL
        io.key_shift = mods & pygame.KMOD_SHIFT
        io.key_alt = mods & pygame.KMOD_ALT
        io.key_super = mods & pygame.KMOD_GUI

    def start_frame(self):
        try:
            io = imgui.get_io()
            io.key_ctrl = False
            io.key_shift = False
            io.key_alt = False
            io.key_super = False
            imgui.new_frame()
        except imgui.core.ImGuiError as e:
            pass
            #print(f"Error in ImGui.new_frame(): {e}")

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
        scene.imgui()

        #imgui.show_test_window()
        GameViewWindow.imgui(self.e)

        self.properties_window.update(dt, scene)
        self.properties_window.imgui()

        self.scene_hierarchy_window.imgui()

        self.menu_bar.imgui()

        imgui.end()

        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    def shutdown(self):
        self.renderer.shutdown()