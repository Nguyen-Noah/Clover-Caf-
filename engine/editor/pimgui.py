

import imgui
from engine.primitives import vec2

class PImGui:
    default_column_width = 80

    @staticmethod
    def draw_vec2_control(label, values, reset_value=0.0, column_width=default_column_width):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label)
        imgui.next_column()

        imgui.push_style_var(imgui.STYLE_ITEM_SPACING, (0, 0))
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.8, 0.1, 0.15, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.9, 0.2, 0.25, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.8, 0.1, 0.15, 1.0)
        line_height = imgui.get_font_size() + imgui.get_style().frame_padding[1] * 2
        button_size = vec2(line_height + 3, line_height)
        width_each = (imgui.calculate_item_width() - button_size.x * 2) / 2

        # X and Y position
        imgui.push_item_width(width_each)
        if imgui.button('x', button_size.x, button_size.y):
            values.x = reset_value
        imgui.pop_style_color(3)
        imgui.same_line()
        c, val = imgui.drag_float('##x', values.x, 0.1)
        if c:
            values.x = val
        imgui.pop_item_width()

        imgui.same_line()

        imgui.push_item_width(width_each)
        imgui.push_style_color(imgui.COLOR_BUTTON, 0.2, 0.7, 0.2, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_HOVERED, 0.3, 0.8, 0.3, 1.0)
        imgui.push_style_color(imgui.COLOR_BUTTON_ACTIVE, 0.2, 0.7, 0.2, 1.0)
        if imgui.button('y', button_size.x, button_size.y):
            values.y = reset_value
        imgui.pop_style_color(3)
        imgui.same_line()
        c, val = imgui.drag_float('##y', values.y, 0.1)
        if c:
            values.y = val
        imgui.pop_item_width()

        imgui.pop_style_var()
        imgui.columns(1)
        imgui.pop_id()

    @staticmethod
    def drag_float(label, value, column_width=default_column_width):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label)
        imgui.next_column()

        c, val = imgui.drag_float('##drag_float', value, 0.1)

        imgui.columns(1)
        imgui.pop_id()

        return c, val

    @staticmethod
    def drag_int(label, value, column_width=default_column_width):
        imgui.push_id(label)

        imgui.columns(2)
        imgui.set_column_width(0, column_width)
        imgui.text(label)
        imgui.next_column()

        c, val = imgui.drag_int('##drag_float', value, 0.1)

        imgui.columns(1)
        imgui.pop_id()

        return c, val