class Component:
    ID_COUNTER = 0      # global to component

    def __init__(self):
        self.entity = None  
        self.uid = -1       # unique to object

    def init(max_id):
        Component.ID_COUNTER = max_id

    def start(self):
        pass

    # can be used for things like: weapons breaking sound, hit sounds, etc.
    def destroy(self):
        pass

    def generate_id(self):
        if self.uid == -1:
            self.uid = Component.ID_COUNTER
            Component.ID_COUNTER += 1

    def serialize(self):
        return self.__dict__
