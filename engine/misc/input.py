import pygame, time, glm
from ..utils.elements import ElementSingleton
from ..primitives.vec2 import vec2
from ..utils.io import write_json, read_json

class InputState:
    def __init__(self):
        self.pressed = False
        self.just_pressed = False
        self.just_released = False
        self.held_since = 0

    def update(self):
        self.just_pressed = False
        self.just_released = False

    def press(self):
        self.pressed = True
        self.just_pressed = True
        self.held_since = time.time()

    def unpress(self):
        self.pressed = False
        self.just_released = True

class Mouse(ElementSingleton):
    def __init__(self, resolution):
        super().__init__()
        self.last_world_x = 0
        self.last_world_y = 0
        self.resolution = resolution
        self.pos = vec2()
        self.ui_pos = vec2()
        self.movement = vec2()
        self.last_pos = vec2()
        self.scroll_y = 0
        self.button_held = None
        self.moved = False

        self.game_viewport_pos = vec2()
        self.game_viewport_size = vec2()

        self.world_x = 0
        self.world_y = 0

        self.dirty_x = True
        self.dirty_y = True

        self.world_dx = 0
        self.world_dy = 0

    def get_world_dx(self):
        return self.world_x - self.last_world_x

    def get_world_dy(self):
        return self.world_y - self.last_world_y

    def reset(self):
        self.scroll_y = 0

    def get_scroll_y(self):
        return self.scroll_y

    def get_screen_x(self):
        curr_x = self.pos.x - self.game_viewport_pos.x
        curr_x = (curr_x / self.game_viewport_size.x) * self.resolution[0]

        return curr_x

    def get_screen_y(self):
        curr_y = self.pos.y - self.game_viewport_pos.y
        curr_y = self.resolution[1] - ((curr_y / self.game_viewport_size.y) * self.resolution[1])

        return curr_y

    def get_ortho_x(self):
        if self.dirty_x:
            self.calc_ortho_x()
        return self.world_x

    def calc_ortho_x(self):
        curr_x = self.pos.x - self.game_viewport_pos.x
        curr_x = (curr_x / self.game_viewport_size.x) * 2 - 1
        tmp = glm.vec4(curr_x, 0, 0, 1)
        tmp = (self.e['Game'].current_scene.camera.inverse_view *
               self.e['Game'].current_scene.camera.inverse_projection * tmp)

        self.last_world_x = self.world_x
        self.world_x = tmp.x
        self.dirty_x = False

    def get_ortho_y(self):
        if self.dirty_y:
            self.calc_ortho_y()
        return self.world_y

    def calc_ortho_y(self):
        curr_y = self.pos.y - self.game_viewport_pos.y
        curr_y = -((curr_y / self.game_viewport_size.y) * 2 - 1)
        tmp = glm.vec4(0, curr_y, 0, 1)
        tmp = (self.e['Game'].current_scene.camera.inverse_view *
               self.e['Game'].current_scene.camera.inverse_projection * tmp)

        self.last_world_y = self.world_y
        self.world_y = tmp.y
        self.dirty_y = False

    def is_dragging(self, button='left_click'):
        return self.e['Input'].holding(button) and self.moved

    def update(self):
        mpos = pygame.mouse.get_pos()
        self.movement = vec2(mpos[0] - self.pos[0], mpos[1] - self.pos[1])
        self.pos = vec2(mpos[0], mpos[1])
        self.ui_pos = vec2(mpos[0] // 2, mpos[1] // 2)

        if self.pos.x != self.last_pos.x:
            self.dirty_x = True
        if self.pos.y != self.last_pos.y:
            self.dirty_y = True

        if self.button_held:
            self.moved = self.pos != self.last_pos

        self.last_pos = self.pos

imgui_ignore = [1073742049]

class Input(ElementSingleton):
    def __init__(self, path, resolution):
        super().__init__()
        self.state = 'main'
        self.text_buffer = None

        self.path = path
        self.load_config(path)
        self.hidden_keys = ['__backspace']

        self.repeat_rate = 0.02
        self.repeat_delay = 0.5
        self.repeat_times = {key: time.time() for key in self.config}
        self.valid_chars = [' ', '.', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', ',', ';', '-', '=', '/', '\\', '[', ']', '\'']
        self.shift_mappings = {
            '1': '!',
            '8': '*',
            '9': '(',
            '0': ')',
            ';': ':',
            ',': '<',
            '.': '>',
            '/': '?',
            '\'': '"',
            '-': '_',
            '=': '+',
        }
        self.shift = False
        self.ctrl = False

        self.mouse = Mouse(resolution)

        self.binding_listen = None

    def save_config(self):
        write_json(self.path, {binding: self.config[binding] for binding in self.config if binding not in self.hidden_keys})

    def load_config(self, path):
        self.config = read_json(path)
        self.config['__backspace'] = ['button', pygame.K_BACKSPACE]
        self.input = {key: InputState() for key in self.config}

    def binding_listen_callback(self, func):
        self.binding_listen = func

    def pressed(self, key):
        return self.input[key].just_pressed if key in self.input else False
    
    def consume(self, key):
        self.input[key].just_pressed = False
        self.input[key].pressed = False

    def holding(self, key):
        return self.input[key].pressed if key in self.input else False
    
    def released(self, key):
        return self.input[key].just_released if key in self.input else False
    
    def set_text_buffer(self, text_buffer=None):
        self.text_buffer = text_buffer

    def update(self):
        for state in self.input.values():
            state.update()

        self.mouse.reset()
        self.e['Mouse'].update()

        for event in pygame.event.get():

            try:
                self.e['ImGui'].process_event(event)
            except Exception as e:
                pass

            if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN and event.key == 27):
                self.e['Game'].f = True            # uncomment if you want to profile
                #self.e['Game'].quit()

            if event.type == pygame.VIDEORESIZE:
                self.e['Window'].reload_display((event.w, event.h))

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.binding_listen:
                    self.binding_listen(['mouse', event.button])
                    self.binding_listen = None
                else:
                    for mapping in self.config:
                        if self.config[mapping][0] == 'mouse':
                            if event.button == self.config[mapping][1]:
                                self.input[mapping].press()
                                self.mouse.button_held = mapping
                            if event.button == 4:
                                self.mouse.scroll_y += 1
                            if event.button == 5:
                                self.mouse.scroll_y -= 1
            if event.type == pygame.MOUSEBUTTONUP:
                for mapping in self.config:
                    if self.config[mapping][0] == 'mouse':
                        if event.button == self.config[mapping][1]:
                            self.input[mapping].unpress()
                            self.mouse.button_held = None
            
            if event.type == pygame.KEYDOWN:
                if self.binding_listen:
                    self.binding_listen(['button', event.key])
                    self.binding_listen = None
                else:
                    if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                        self.shift = True
                    if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                        self.ctrl = True
                    if self.text_buffer:
                        for char in self.valid_chars:
                            new_char = None
                            if event.key == ord(char):
                                new_char = char
                            if new_char:
                                if self.shift:
                                    new_char = new_char.upper()
                                    if new_char in self.shift_mappings:
                                        new_char = self.shift_mappings[new_char]
                                self.text_buffer.insert(new_char)
                        
                        if event.key == pygame.K_RETURN:
                            self.text_buffer.enter()

                    mappings = self.config
                    if self.text_buffer:
                        mappings = self.hidden_keys

                    for mapping in mappings:
                        if self.config[mapping][0] == 'button':
                            if event.key == self.config[mapping][1]:
                                self.input[mapping].press()

            if event.type == pygame.KEYUP:
                for mapping in self.config:
                    if self.config[mapping][0] == 'button':
                        if event.key == self.config[mapping][1]:
                            self.input[mapping].unpress()
                
                if event.key in [pygame.K_LSHIFT, pygame.K_RSHIFT]:
                    self.shift = False

                if event.key in [pygame.K_LCTRL, pygame.K_RCTRL]:
                    self.ctrl = False

        if self.text_buffer:
            if self.pressed('__backspace'):
                self.repeat_times['__backspace'] = self.e['Window'].time
                self.text_buffer.delete()

            if self.holding('__backspace'):
                while self.e['Window'].time > self.repeat_times['__backspace']:
                    self.repeat_times['__backspace'] += self.repeat_rate
                    self.text_buffer.delete()