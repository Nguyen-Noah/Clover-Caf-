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

        self.load_font('OpenSans-Semibold.ttf', 16)

        self.properties_window = PropertiesWindow(picking_texture)
        self.scene_hierarchy_window = SceneHierarchyWindow()

        self.menu_bar = MenuBar()

    def load_font(self, font_path, font_size):
        self.font = self.io.fonts.add_font_from_file_ttf(f'{FONT_PATH}/{font_path}', font_size)
        self.renderer.refresh_font_texture()

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

            #self.set_theme()
            self.set_dark_theme_colors()
        except imgui.core.ImGuiError as e:
            pass

    def setup_dock_space(self):
        window_flags = imgui.WINDOW_MENU_BAR | imgui.WINDOW_NO_DOCKING

        style = imgui.get_style()
        original_size = style.window_min_size
        style.window_min_size = imgui.Vec2(370, original_size.y)

        imgui.set_next_window_position(0, 0, imgui.ALWAYS)
        imgui.set_next_window_size(*self.e['Window'].resolution)

        imgui.push_style_var(imgui.STYLE_WINDOW_ROUNDING, 0)
        imgui.push_style_var(imgui.STYLE_WINDOW_BORDERSIZE, 0)
        window_flags = window_flags | imgui.WINDOW_NO_TITLE_BAR | imgui.WINDOW_NO_COLLAPSE | \
                imgui.WINDOW_NO_RESIZE | imgui.WINDOW_NO_MOVE | \
                imgui.WINDOW_NO_BRING_TO_FRONT_ON_FOCUS | imgui.WINDOW_NO_NAV_FOCUS
        imgui.begin("Dockspace", True, window_flags)
        imgui.pop_style_var(2)

        # dockspace
        imgui.dockspace(imgui.get_id("Dockspace"))

        style.window_min_size = original_size

    def update(self, dt, scene):
        if self.e['Window'].resize_event:
            self.io.display_size = self.e['Window'].resolution

        imgui.push_font(self.font)

        self.start_frame()
        self.setup_dock_space()
        scene.imgui()

        #imgui.show_test_window()
        GameViewWindow.imgui(self.e)

        self.properties_window.update(dt, scene)
        self.properties_window.imgui()

        self.scene_hierarchy_window.imgui()

        self.menu_bar.imgui()

        imgui.pop_font()

        imgui.end()

        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    # these can be abstracted later on to support custom themes
    def set_dark_theme_colors(self):
        style = imgui.get_style()
        colors = style.colors

        # Window background
        colors[imgui.COLOR_WINDOW_BACKGROUND] = imgui.Vec4(0.1, 0.105, 0.11, 1.0)

        # Headers
        colors[imgui.COLOR_HEADER] = imgui.Vec4(0.2, 0.205, 0.21, 1.0)
        colors[imgui.COLOR_HEADER_HOVERED] = imgui.Vec4(0.3, 0.305, 0.31, 1.0)
        colors[imgui.COLOR_HEADER_ACTIVE] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)

        # Buttons
        colors[imgui.COLOR_BUTTON] = imgui.Vec4(0.2, 0.205, 0.21, 1.0)
        colors[imgui.COLOR_BUTTON_HOVERED] = imgui.Vec4(0.3, 0.305, 0.31, 1.0)
        colors[imgui.COLOR_BUTTON_ACTIVE] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)

        # Frame background
        colors[imgui.COLOR_FRAME_BACKGROUND] = imgui.Vec4(0.2, 0.205, 0.21, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = imgui.Vec4(0.3, 0.305, 0.31, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)

        # Tabs
        colors[imgui.COLOR_TAB] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)
        colors[imgui.COLOR_TAB_HOVERED] = imgui.Vec4(0.38, 0.385, 0.38, 1.0)
        colors[imgui.COLOR_TAB_ACTIVE] = imgui.Vec4(0.28, 0.288, 0.288, 1.0)
        colors[imgui.COLOR_TAB_UNFOCUSED] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)
        colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE] = imgui.Vec4(0.2, 0.205, 0.21, 1.0)

        # Title background
        colors[imgui.COLOR_TITLE_BACKGROUND] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = imgui.Vec4(0.95, 0.1505, 0.951, 1.0)

    def set_theme(self):
        style = imgui.get_style()

        # A darker window background (bluish-gray tint).
        # Feel free to push it even darker if you like.
        style.colors[imgui.COLOR_WINDOW_BACKGROUND] = (0.12, 0.14, 0.15, 1.0)  # ~ #1E2327

        # Frame backgrounds (for text fields, input boxes, etc.)
        # Make each state a bit more distinct.
        style.colors[imgui.COLOR_FRAME_BACKGROUND] = (0.15, 0.17, 0.18, 1.0)  # ~ #262B2F
        style.colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = (0.19, 0.21, 0.22, 1.0)  # ~ #30363A
        style.colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = (0.23, 0.25, 0.27, 1.0)  # ~ #394046

        # Tabs: remove the blue tint and keep them neutral/dark.
        style.colors[imgui.COLOR_TAB] = (0.15, 0.17, 0.18, 1.0)
        style.colors[imgui.COLOR_TAB_HOVERED] = (0.19, 0.21, 0.22, 1.0)
        style.colors[imgui.COLOR_TAB_ACTIVE] = (0.23, 0.25, 0.27, 1.0)

        # Text colors
        # Use a slightly lighter text color to stand out against darker backgrounds.
        style.colors[imgui.COLOR_TEXT] = (0.85, 0.85, 0.85, 1.0)  # ~ #D9D9D9
        style.colors[imgui.COLOR_TEXT_DISABLED] = (0.5, 0.5, 0.5, 1.0)

        # Buttons: neutral grays with hover/active states
        style.colors[imgui.COLOR_BUTTON] = (0.15, 0.17, 0.18, 1.0)
        style.colors[imgui.COLOR_BUTTON_HOVERED] = (0.19, 0.21, 0.22, 1.0)
        style.colors[imgui.COLOR_BUTTON_ACTIVE] = (0.23, 0.25, 0.27, 1.0)

        # Collapsing headers:
        # If you want them to stay neutral, just use slightly lighter shades instead of bright accents.
        style.colors[imgui.COLOR_HEADER] = (0.20, 0.22, 0.24, 1.0)
        style.colors[imgui.COLOR_HEADER_HOVERED] = (0.24, 0.26, 0.28, 1.0)
        style.colors[imgui.COLOR_HEADER_ACTIVE] = (0.28, 0.30, 0.32, 1.0)

        # Borders / separators
        style.colors[imgui.COLOR_BORDER] = (0.25, 0.25, 0.25, 1.0)
        style.colors[imgui.COLOR_SEPARATOR] = (0.25, 0.25, 0.25, 1.0)

        # Some UI rounding & spacing
        style.window_rounding = 4.0
        style.frame_rounding = 2.0
        style.item_spacing = (8, 6)
        style.window_padding = (8, 8)
        style.scrollbar_size = 15.0

        # If you still want a subtle highlight for sliders or checkboxes, you can use a gray or very muted blue:
        style.colors[imgui.COLOR_SLIDER_GRAB] = (0.60, 0.60, 0.60, 1.0)
        style.colors[imgui.COLOR_SLIDER_GRAB_ACTIVE] = (0.70, 0.70, 0.70, 1.0)
        style.colors[imgui.COLOR_CHECK_MARK] = (0.65, 0.65, 0.65, 1.0)