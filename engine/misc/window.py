import pygame, time, os
from ..utils.elements import ElementSingleton

class Window(ElementSingleton):
    def __init__(self, resolution=(640, 480), caption='game', flags=0, fps_cap=60, dt_cap=1, opengl=True, shader_path=None):
        super().__init__()
        self.opengl = opengl
        self.shader_path = shader_path
        self.resolution = resolution
        self.flags = flags
        
        pygame.init()
        if self.opengl:
            self.flags = self.flags | pygame.DOUBLEBUF | pygame.OPENGL
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MAJOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_MINOR_VERSION, 3)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_PROFILE_MASK, pygame.GL_CONTEXT_PROFILE_CORE)
            pygame.display.gl_set_attribute(pygame.GL_CONTEXT_FLAGS, pygame.GL_CONTEXT_FORWARD_COMPATIBLE_FLAG) 
        self.background_color = (0, 0, 0)

        # fps and timers
        self.fps_cap = fps_cap
        self.dt_cap = dt_cap
        self.time = time.time()
        self.start_time = time.time()
        self.frames = 0
        self.frame_log = []
        self.native_resolution = None

        pygame.display.set_caption(caption)
        self.reload_display(self.resolution, ignore_mgl=True)
        
        self.clock = pygame.time.Clock()
        self.last_frame = time.time()
        self.dt = 0.1

    @property
    def fps(self):
        return int(len(self.frame_log) / sum(self.frame_log))

    def reload_display(self, size, ignore_mgl=False):
        try:
            fullscreen = self.e['Settings'].fullscreen
        except Exception:
            fullscreen = False
        
        self.fullscreen_flag = pygame.FULLSCREEN if fullscreen else 0

        if fullscreen and ignore_mgl:
            size = (pygame.display.Info().current_w, pygame.display.Info().current_h)

        if not self.native_resolution:
            self.native_resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        elif not fullscreen:
            os.environ['SDL_VIDEO_CENTERED'] = '0'

        if not size:
            size = self.native_resolution
            
        self.display = pygame.display.set_mode(size, self.flags | self.fullscreen_flag)
        if not ignore_mgl:
            self.e['Renderer'].ctx.viewport = 0, 0, size[0], size[1]
        if fullscreen:
            self.resolution = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        else:
            self.resolution = tuple(size)

    def update(self):
        self.dt = min(time.time() - self.last_frame, self.dt_cap)
        self.frame_log.append(self.dt)
        self.frame_log = self.frame_log[-60:]
        self.last_frame = time.time()
        self.clock.tick(self.fps_cap)
        self.display.fill((0, 0, 0))
        self.time = time.time()
        self.frames += 1
        #print(f'fps: {self.fps}')
        pygame.display.set_caption(str(self.fps))