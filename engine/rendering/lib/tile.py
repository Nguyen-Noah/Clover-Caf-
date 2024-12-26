from engine import ShaderProgram

class TileRenderer(ShaderProgram):
    def __init__(self, vert_path, frag_path):
        super().__init__(vert_path, frag_path)