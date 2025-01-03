import pygame, math, glm
from ..utils.elements import ElementSingleton
from ..utils.game_math import clamp_between
from ..primitives.vec2 import vec2

# CHANGE TO NON SINGLETON (?)
class Camera(ElementSingleton):
    def __init__(self, size):
        super().__init__()
        self.size = vec2(*size)
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
        self.projection_matrix = glm.ortho(0.0, self.size[0] * self.zoom, 0.0, self.size[1] * self.zoom, 0.0, 100.0)
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

    @property
    def rect(self):
        return pygame.Rect(*self.int_pos, *self.size)
    
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

    @property
    def target(self):
        if self.track_entity:
            if self.track_entity.type == 'player':
                target_pos = vec2(self.track_entity.pos.copy())
                if self.track_entity.weapon:
                    angle = math.radians(self.track_entity.weapon.angle)
                    dis = math.sqrt((self.e['Input'].mouse.pos[1] - self.track_entity.center[1] + self.render_offset[1]) ** 2 + (self.e['Input'].mouse.pos[0] - self.track_entity.center[0] + self.render_offset[0]) ** 2)
                    target_pos[0] += math.cos(angle) * (dis / 8)
                    target_pos[1] += math.sin(angle) * (dis / 8)
            return vec2(target_pos.x - self.e['Window'].display.get_width() // 2, target_pos.y - self.e['Window'].get_height() // 2)
        
    def update(self):
        pass

        """ target = self.target
        if target:
            self.position[0] += math.floor(target[0] - self.position[0]) / (self.rate / self.e['Window'].dt)
            self.position[1] += math.floor(target[1] - self.position[1]) / (self.rate / self.e['Window'].dt)

        if self.restriction_point:
            if self.position[0] + self.e['Window'].display.get_width() // 2 - self.restriction_point[0] > self.lock_distance[0]:
                self.position[0] = self.restriction_point[0] - self.e['Window'].display.get_width() // 2 + self.lock_distance[0]
            if self.position[0] + self.e['Window'].display.get_width() // 2 - self.restriction_point[0] < -self.lock_distance[0]:
                self.position[0] = self.restriction_point[0] - self.e['Window'].display.get_width() // 2 - self.lock_distance[0]
            if self.position[1] + self.e['Window'].display.get_height() // 2 - self.restriction_point[1] > self.lock_distance[1]:
                self.position[1] = self.restriction_point[1] - self.e['Window'].display.get_height() // 2 + self.lock_distance[1]
            if self.position[1] + self.e['Window'].display.get_height() // 2 - self.restriction_point[1] < -self.lock_distance[1]:
                self.position[1] = self.restriction_point[1] - self.e['Window'].display.get_height() // 2 - self.lock_distance[1]
        
        if self.e['Input'].pressed('zoom_in'):
            self.zoom += 1
        if self.e['Input'].pressed('zoom_out'):
            self.zoom -= 1
        self.zoom = clamp_between(self.zoom, 1, 10) """