import imgui
from ..utils.elements import Element
from ..primitives.vec3 import vec3
from ..primitives.vec4 import vec4

class Component:
    ID_COUNTER = 0      # gloabl to component

    def __init__(self):
        self.entity = None  
        self.uid = -1       # unique to object

    def start(self):
        pass

    def update(self, dt):
        pass

    def imgui(self):
        try:
            for field_name, value in vars(self).items():
                field_type = type(value)
                name = field_name.capitalize()

                if field_type == int:
                    im_val = [value]
                    changed, im_val[0] = imgui.drag_int(f"{name}", im_val[0])
                    if changed:
                        setattr(self, field_name, im_val[0])

                elif field_type == float:
                    im_val = [value]
                    changed, im_val[0] = imgui.drag_float(f"{name}", im_val[0])
                    if changed:
                        setattr(self, field_name, im_val[0])

                elif field_type == vec3:
                    im_vec = [value.x, value.y, value.z]
                    changed, im_vec = imgui.drag_float3(f"{name}", *im_vec)
                    if changed:
                        value.x, value.y, value.z = im_vec
                        setattr(self, field_name, value)

                elif field_type == vec4:
                    im_vec = [value.x, value.y, value.z, value.w]
                    changed, im_vec = imgui.drag_float4(f"{name}", *im_vec)
                    if changed:
                        value.x, value.y, value.z, value.w = im_vec
                        setattr(self, field_name, value)

                elif field_type == bool:
                    changed, im_val = imgui.checkbox(f"{name}", value)
                    if changed:
                        setattr(self, field_name, im_val)

        except Exception as e:
            print(e)

    def generate_id(self):
        if self.uid == -1:
            self.uid = Component.ID_COUNTER
            Component.ID_COUNTER += 1

    def init(max_id):
        Component.ID_COUNTER = max_id

    def serialize(self):
        return {
            "type": self.__class__.__name__,
            "uid": self.uid
            }
    
    