import imgui
from imgui.integrations.pygame import PygameRenderer

from engine.core.layer import Layer


class ImGuiLayer(Layer):
    def __init__(self, name="ImGuiLayer"):
        super().__init__(name)
        self.block_events = True
        self.renderer = None
        self.io = None
        self.font = None

    def on_attach(self):
        imgui.create_context()
        self.io = imgui.get_io()
        self.io.config_flags |= imgui.CONFIG_DOCKING_ENABLE

        # setting default font
        font_size = 16
        self.font = self.io.fonts.add_font_from_file_ttf("data/fonts/OpenSans-Semibold.ttf", font_size)
        self.renderer.refresh_font_texture()

        self.set_dark_theme_v2_colors()

        self.renderer = PygameRenderer()

    def on_detach(self):
        if self.renderer:
            self.renderer.shutdown()
            imgui.destroy_context()

    # needed?
    def on_event(self):
        pass

    def begin(self):
        self.renderer.process_inputs()
        imgui.new_frame()

    def end(self):
        self.io.display_size = self.e['Window'].resolution

        imgui.render()
        self.renderer.render(imgui.get_draw_data())

    @staticmethod
    def set_dark_theme_v2_colors():
        style = imgui.get_style()
        colors = style.colors

        # Headers
        colors[imgui.COLOR_HEADER] = imgui.Vec4(0.176, 0.176, 0.176, 1.0)
        colors[imgui.COLOR_HEADER_HOVERED] = imgui.Vec4(0.176, 0.176, 0.176, 1.0)
        colors[imgui.COLOR_HEADER_ACTIVE] = imgui.Vec4(0.176, 0.176, 0.176, 1.0)

        # Buttons
        colors[imgui.COLOR_BUTTON] = imgui.Vec4(0.22, 0.22, 0.22, 0.784)
        colors[imgui.COLOR_BUTTON_HOVERED] = imgui.Vec4(0.275, 0.275, 0.275, 1.0)
        colors[imgui.COLOR_BUTTON_ACTIVE] = imgui.Vec4(0.22, 0.22, 0.22, 0.588)

        # Frame Background
        colors[imgui.COLOR_FRAME_BACKGROUND] = imgui.Vec4(0.157, 0.157, 0.157, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_HOVERED] = imgui.Vec4(0.157, 0.157, 0.157, 1.0)
        colors[imgui.COLOR_FRAME_BACKGROUND_ACTIVE] = imgui.Vec4(0.157, 0.157, 0.157, 1.0)

        # Tabs
        colors[imgui.COLOR_TAB] = imgui.Vec4(0.137, 0.137, 0.137, 1.0)
        colors[imgui.COLOR_TAB_HOVERED] = imgui.Vec4(1.0, 0.882, 0.529, 0.118)
        colors[imgui.COLOR_TAB_ACTIVE] = imgui.Vec4(1.0, 0.882, 0.529, 0.235)
        colors[imgui.COLOR_TAB_UNFOCUSED] = imgui.Vec4(0.137, 0.137, 0.137, 1.0)
        colors[imgui.COLOR_TAB_UNFOCUSED_ACTIVE] = colors[imgui.COLOR_TAB_HOVERED]

        # Title Background
        colors[imgui.COLOR_TITLE_BACKGROUND] = imgui.Vec4(0.137, 0.137, 0.137, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_ACTIVE] = imgui.Vec4(0.137, 0.137, 0.137, 1.0)
        colors[imgui.COLOR_TITLE_BACKGROUND_COLLAPSED] = imgui.Vec4(0.15, 0.1505, 0.151, 1.0)

        # Resize Grip
        colors[imgui.COLOR_RESIZE_GRIP] = imgui.Vec4(0.91, 0.91, 0.91, 0.25)
        colors[imgui.COLOR_RESIZE_GRIP_HOVERED] = imgui.Vec4(0.81, 0.81, 0.81, 0.67)
        colors[imgui.COLOR_RESIZE_GRIP_ACTIVE] = imgui.Vec4(0.46, 0.46, 0.46, 0.95)

        # Scrollbar
        colors[imgui.COLOR_SCROLLBAR_BACKGROUND] = imgui.Vec4(0.02, 0.02, 0.02, 0.53)
        colors[imgui.COLOR_SCROLLBAR_GRAB] = imgui.Vec4(0.31, 0.31, 0.31, 1.0)
        colors[imgui.COLOR_SCROLLBAR_GRAB_HOVERED] = imgui.Vec4(0.41, 0.41, 0.41, 1.0)
        colors[imgui.COLOR_SCROLLBAR_GRAB_ACTIVE] = imgui.Vec4(0.51, 0.51, 0.51, 1.0)

        # Check Mark
        colors[imgui.COLOR_CHECK_MARK] = imgui.Vec4(0.784, 0.784, 0.784, 1.0)

        # Separator
        colors[imgui.COLOR_SEPARATOR] = imgui.Vec4(0.098, 0.098, 0.098, 1.0)
        colors[imgui.COLOR_SEPARATOR_ACTIVE] = imgui.Vec4(0.196, 0.588, 0.784, 1.0)
        colors[imgui.COLOR_SEPARATOR_HOVERED] = imgui.Vec4(0.153, 0.725, 0.949, 0.588)

        # Window Background
        colors[imgui.COLOR_WINDOW_BACKGROUND] = imgui.Vec4(0.137, 0.137, 0.137, 1.0)
        colors[imgui.COLOR_CHILD_BACKGROUND] = imgui.Vec4(0.098, 0.098, 0.098, 1.0)
        colors[imgui.COLOR_POPUP_BACKGROUND] = imgui.Vec4(0.078, 0.078, 0.078, 1.0)
        colors[imgui.COLOR_BORDER] = imgui.Vec4(0.098, 0.098, 0.098, 1.0)

        # Tables
        colors[imgui.COLOR_TABLE_HEADER_BACKGROUND] = imgui.Vec4(0.176, 0.176, 0.176, 1.0)
        colors[imgui.COLOR_TABLE_BORDER_LIGHT] = imgui.Vec4(0.098, 0.098, 0.098, 1.0)

        # Menubar
        colors[imgui.COLOR_MENUBAR_BACKGROUND] = imgui.Vec4(0.0, 0.0, 0.0, 0.0)

        # Style settings
        style.frame_rounding = 2.5
        style.frame_border_size = 1.0
        style.indent_spacing = 11.0