import imgui

from engine.primitives import vec2

class GameViewWindow:
    is_playing = False

    @staticmethod
    def imgui(e):
        imgui.begin("Game Viewport", imgui.WINDOW_NO_SCROLLBAR | imgui.WINDOW_NO_SCROLL_WITH_MOUSE)

        window_size = GameViewWindow.get_largest_size_for_viewport(e)
        window_pos = GameViewWindow.get_centered_position_for_viewport(window_size)

        imgui.set_cursor_pos_x(window_pos.x)
        imgui.set_cursor_pos_y(window_pos.y)

        pos = imgui.get_cursor_screen_pos()
        tl = vec2(*pos)
        tl.x -= imgui.get_scroll_x()
        tl.y -= imgui.get_scroll_y()

        tex_id = e['Game'].fbo.get_id()
        imgui.image(texture_id=tex_id, width=window_size.x, height=window_size.y, uv0=(0, 1), uv1=(1, 0))

        e['Input'].mouse.game_viewport_pos = vec2(*tl)
        e['Input'].mouse.game_viewport_size = vec2(*window_size)

        imgui.end()

    @staticmethod
    def get_largest_size_for_viewport(e):
        content_region = imgui.get_content_region_available()
        window_size = vec2(content_region.x, content_region.y)

        window_size.x -= imgui.get_scroll_x()
        window_size.y -= imgui.get_scroll_y()

        aspect_width = window_size.x
        aspect_height = aspect_width / e['Game'].aspect_ratio

        if aspect_width > window_size.y:
            # switch to pillarbox mode
            aspect_height = window_size.y
            aspect_width = aspect_height * e['Game'].aspect_ratio

        return vec2(aspect_width, aspect_height)

    @staticmethod
    def get_centered_position_for_viewport(aspect_size):
        content_region = imgui.get_content_region_available()
        window_size = vec2(content_region.x, content_region.y)

        window_size.x -= imgui.get_scroll_x()
        window_size.y -= imgui.get_scroll_y()

        viewport_x = (window_size.x / 2) - (aspect_size.x / 2)
        viewport_y = (window_size.y / 2) - (aspect_size.y / 2)
        
        return vec2(viewport_x + imgui.get_cursor_pos_x(), viewport_y + imgui.get_cursor_pos_y())