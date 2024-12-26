from ..utils.elements import Element, ElementSingleton


"""
make change_scene() function that creates the scene once it is selected and initializes it
ref: https://youtu.be/vnqb9vdaxwA?si=CZlxopFaJ_qThhvi&t=106
"""

class Scene(Element):
    def __init__(self):
        super().__init__()
        self.renderer = None
        self.camera = None
        self.running = False
        self.game_objects = []

    def start(self):
        for object in self.game_objects:
            object.start()
            self.renderer.add(object)
        self.running = True

    def add_game_object_to_scene(self, object):
        self.game_objects.append(object)
        if self.running:
            object.start()
            self.renderer.add(object)

    def update(self, dt):
        pass

    def camera(self):
        return self.camera

class GameState(Element):
    def __init__(self):
        super().__init__()
        self.e['GSManager'].register_state(self)

    def handle_events(self, events):
        pass

    def update(self, dt):
        pass

    def render(self):
        pass

class GSManager(ElementSingleton):
    def __init__(self):
        super().__init__()
        self.states = {}
        self.current_state = 'Test'

    def register_state(self, state):
        name = state.__class__.__name__
        if name not in self.states:
            self.states[name] = state
        else:
            pass

    def delete_state(self, state):
        if state in self.states:
            del self.states[state]

    def handle_events(self, events):
        if self.current_state:
            next_state = self.states[self.current_state].handle_events(events)
            if next_state:
                self.current_state = next_state

    def update(self):
        dt = self.e['Window'].dt

        self.states[self.current_state].update(dt)

    def render(self):
        pass