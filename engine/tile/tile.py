import pygame, random
from ..utils.elements import Element

RANDOMIZE_GROUPS = {}

class Tile(Element):
    def __init__(self, parent, tile_type, pos, group, wall=False, variant=False, z_offset=0, overhand=False):
        self.parent = parent
        self.type = tile_type
        self.pos = pos
        self.group = group
        self.wall = wall
        self.variant = variant
        self.z_offset = z_offset

        if self.type in RANDOMIZE_GROUPS:
            if random.random() < RANDOMIZE_GROUPS[self.type][0]:
                self.variant = (random.randint(0, RANDOMIZE_GROUPS[self.type][1] - 1), self.variant if self.variant[1] else 0)

    @property
    def rect(self):
        return pygame.Rect(self.pos[0], self.parent.tilesize[0], self.pos[1] * self.parent.tilesize[1], self.parent.tilesize[0], self.parent.tilesize[1])
    
    def render(self):
        rpos = (self.pos[0] * self.parent.tilesize[0], self.pos[1] * self.parent.tilesize[1])

        z = 0
        if self.wall:
            z = self.pos[1] + 1
        z += self.z_offset

        if self.variant:
            img = self.parent.e['Assets'].spritesheets[self.type]['assets'][self.variant]
        else:
            img = self.parent.e['Assets'].images['floor'][self.type]

        self.parent.e['Renderer'].blit(img, rpos, z=z)