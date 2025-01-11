import glm
from ..utils.elements import ElementSingleton
from ..primitives.vec2 import vec2

# CHANGE TO NON SINGLETON (?)
class Camera(ElementSingleton):
    def __init__(self, size):
        super().__init__()
        self.projection_size = vec2(*size)
        self.position = vec2()     # same as pos
        self.int_pos = vec2()
        self.target_pos = vec2()
        self.rate = 0.25
        self.track_entity = None
        self.restriction_point = None
        self.mode = None
        self.screen_shake = 0
        self.shake_amount = 'medium'
        self.zoom = 1

        self.projection_matrix = glm.mat4()
        self.view_matrix = glm.mat4()
        self.inverse_projection = glm.mat4()
        self.inverse_view = glm.mat4()

        self.adjust_projection()

    def adjust_projection(self):
        self.projection_matrix = glm.ortho(0.0, self.projection_size.x * self.zoom, 0.0, self.projection_size.y * self.zoom, 0.0, 100.0)
        self.inverse_projection = glm.inverse(self.projection_matrix)

    def get_view_matrix(self):
        camera_front = glm.vec3(0.0, 0.0, -1.0)
        camera_up = glm.vec3(0.0, 1.0, 0.0)
        self.view_matrix = glm.lookAt(glm.vec3(self.position.x, self.position.y, 20.0),
                                        camera_front + glm.vec3(self.position.x, self.position.y, 0.0),
                                        camera_up)
        self.inverse_view = glm.inverse(self.view_matrix)

        return self.view_matrix
    
    def get_projection_matrix(self):
        return self.projection_matrix
    
    def focus(self):
        self.update()
        self.true_pos = self.target_pos.copy()

    def move(self, movement):
        self.position.x += movement[0]
        self.position.y += movement[1]

    def set_tracked_entity(self, entity):
        self.track_entity = entity

    def set_restriction(self, pos):
        self.restriction_point = list(pos)

    def add_screen_shake(self, duration, amt='medium'):
        self.screen_shake = duration
        self.shake_amount = amt

    def get_scroll_y(self):
        return self.zoom