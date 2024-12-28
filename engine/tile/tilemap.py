import pygame
import numpy as np
from ..utils.elements import Element
from ..utils.io import read_tjson
from ..data_structures.quads import Quads
from .tile import Tile
from ..rendering.lib.tile import TileRenderer
from ..primitives.vec2 import vec2

from array import array

SHADER_PATH = 'engine/rendering/shaders'

class Tilemap(Element):
    def __init__(self, scene, map_id, tilesize=(16, 16), dimensions=(16, 16), scale_ratio=3, resolution=(1080, 720)):
        super().__init__()
        self.scene = scene
        self.map = map_id
        self.tilesize = tilesize
        self.dimensions = dimensions
        self.scale_ratio = scale_ratio
        self.resolution = resolution
        self.grid_tiles = {}
        self.dimensions = tuple(dimensions)
        self.dimensional_lock = True

        self.rerender = True
        self.tile_renderer = TileRenderer(f'{SHADER_PATH}/vsDefault.glsl', f'{SHADER_PATH}/default.glsl')

        self.load_map(map_id)
        self.set_shader()

    def load_map(self, map_name):
        self.clear()
        self.reset()

        data = read_tjson(f'data/maps/{map_name}.pmap')

        self.dimensions = data['dimensions']
        self.minimap_base = pygame.Surface(self.dimensions)
        self.wall_map = pygame.Surface(self.dimensions, pygame.SRCALPHA)

        for loc in data['grid_tiles']:
            tile_stack = data['grid_tiles'][loc]
            for layer in tile_stack:
                tile = tile_stack[layer]
                group_conf = self.e['Assets'].spritesheets[tile['group']]['config']
                tile_id = tuple(tile['tile_id'])
                if tile_id in group_conf:
                    tile_conf = group_conf[tile_id]
                    categories = ['floor']

                    if 'categories' in tile_conf:
                        categories = tile_conf['categories']
                    if 'solid' in categories:
                        self.solids[loc] = Tile(self, tile['group'], loc, 'solid', variant=tile_id)
                    if 'floor' in categories:
                        if (loc not in self.floor) and (loc not in self.walls):
                            self.floor[loc] = Tile(self, tile['group'], loc, 'floor', variant=tile_id)

        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if not any([(x, y) in section for section in [self.walls, self.solids, self.floor, self.gaps]]):
                    self.gaps[(x, y)] = Tile(self, 'water_wall', 'water_wall', (x, y))
                    self.minimap_base.set_at((x, y), (74, 156, 223))

        for x in range(self.dimensions[0]):
            for y in range(self.dimensions[1]):
                if not self.is_open_space((x, y)):
                    self.wall_map.set_at((x, y), (0, 0, 255, 255))

    def is_open_space(self, loc):
        if (loc not in self.solids) and (loc not in self.gaps):
            return True
        return False

    def clear(self):
        self.floor = {}
        self.walls = {}
        self.solids = {}
        self.gaps = {}

    def reset(self):
        self.grid_tiles = {}
        self.physics_map = {}
        self.offgrid_tiles = Quads((self.tilesize[0] + self.tilesize[1]) * 3)

    def physics_gridtile(self, pos):
        grid_pos = (pos[0] // self.tilesize[0], pos[1] // self.tilesize[1])
        if grid_pos in self.physics_map:
            return self.physics_map[grid_pos][0][2]
    
    def set_shader(self):
        self.rerender = False
        cam_r = self.scene.camera.rect
        tl = (cam_r.left // self.tilesize[0], cam_r.top // self.tilesize[1] - 1)
        br = (cam_r.right // self.tilesize[0], cam_r.bottom // self.tilesize[1])

        self.instance_data = []
        for y in range(tl[1], br[1] + 2):
            for x in range(tl[0], br[0] + 1):
                loc = (x, y)
                if loc in self.floor:
                    tile = self.floor[loc]
                    atlas_data = self.scene.atlas_coords[f'{tile.group}/{tile.type}']
                    self.instance_data.append((
                        x * self.tilesize[0] * self.scale_ratio,        # aOffset.x
                        -y * self.tilesize[1] * self.scale_ratio,       # aOffset.y
                        atlas_data['tex_x'],
                        atlas_data['tex_y'],
                        atlas_data['tex_w'],
                        atlas_data['tex_h']
                        ))

        instance_buffer = self.e['Renderer'].ctx.buffer(np.array(self.instance_data, dtype='f4').tobytes())

        render_size = vec2(self.tilesize[0] * self.scale_ratio, self.tilesize[1] * self.scale_ratio)
        vertex_array = self.e['Renderer'].ctx.buffer(data=array('f', [
                        0,   self.resolution[1],                       0.0, 1.0, # tl
                        0,   self.resolution[1] - render_size.y,       1.0, 1.0, # bl
            render_size.x,   self.resolution[1],                       0.0, 0.0, # tr
            render_size.x,   self.resolution[1] - render_size.y,       1.0, 0.0, # br
        ]))

        """ vertex_array = self.e['Renderer'].ctx.buffer(data=array('f', [
                        0,   self.resolution[1],                       0.0, 1.0,    #tl
                        0,   self.resolution[1] - render_size.y,       0.0, 1.0 - 0.1875,    #bl
            render_size.x,   self.resolution[1],                       0.1875, 1.0,    #tr
            render_size.x,   self.resolution[1] - render_size.y,       0.1875, 1.0 - 0.1875,    #br
        ])) """




        self.tile_renderer.create_vao([
            (vertex_array, '2f 2f', 'aPos', 'aTexCoords'),
            (instance_buffer, '2f 4f', 'aOffset', 'aAtlasRegion')
        ])

    def render(self):
        if self.rerender:
            self.set_shader()

        self.e['Renderer'].blit(self.tile_renderer, uniforms={
            'uProjection': self.e['Camera'].get_projection_matrix(),
            'uView': self.e['Camera'].get_view_matrix(),
            'TEX_ATLAS': self.scene.atlas
        }, instances=self.instance_data)
