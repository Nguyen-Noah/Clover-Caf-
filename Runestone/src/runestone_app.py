import engine
from Runestone.src.editor_layer import EditorLayer
from engine.core.application import ApplicationSpecification



class Game(engine.Application):
    def __init__(self, spec):
        """
        Constructor for Runestone.
        :param spec: An object containing application specifications.
        """
        super().__init__(spec)
        self.push_layer(EditorLayer())

def create_application():
    """
    Factory function to create and return an instance of Runestone.
    :param args: TODO Command-line arguments for the application.
    :return: An instance of Runestone.
    """
    spec = ApplicationSpecification()
    spec.name = "Runestone"
    spec.resolution = (1080, 720)
    spec.fps_cap = 240
    spec.working_directory = ""
    return Game(spec)

if __name__ == "__main__":
    game = create_application()
    game.run()