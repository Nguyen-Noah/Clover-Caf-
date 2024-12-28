from engine import Shader

class TileRenderer(Shader):
    def __init__(self, vert_path, frag_path):
        super().__init__(vert_path, frag_path)