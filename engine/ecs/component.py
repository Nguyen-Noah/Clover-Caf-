

class Component:
    def __init__(self):
        self.entity = None

    def start(self):
        pass

    def imgui(self):
        pass

    def update(self, dt):
        pass

    def serialize(self):
        return {"type": self.__class__.__name__}
    
    def imgui(self):
        try:
            fields = vars(self)
            for field in fields:
                print(field)
        except Exception as e:
            print(e)