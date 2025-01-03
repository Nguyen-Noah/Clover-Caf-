import pygame, sys, math, os, time
from pygame.locals import *
from editor.editor_tilemap import Tilemap, Tile
from editor.camera import Camera
from editor.input import Input
from editor.textbox import Textbox
from editor.text import Text as pText
from editor.editor_renderer import Renderer
from engine.assets.spritesheets import load_spritesheets
from engine.utils.io import read_json, write_json

from tkinter import filedialog
from tkinter import *

def rectify(p1, p2):
    tl = (min(p1[0], p2[0]), min(p1[1], p2[1]))
    br = (max(p1[0], p2[0]), max(p1[1], p2[1]))
    return pygame.Rect(*tl, br[0] - tl[0] + 1, br[1] - tl[1] + 1)

KEY_MAPPINGS = {
	'quit': ['keyboard', 27],                   # escape
    'camera_up': ['keyboard', 119],             # w
    'camera_left': ['keyboard', 97],            # a
    'camera_down': ['keyboard', 115],           # s
    'camera_right': ['keyboard', 100],          # d
    'select': ['keyboard', 101],                # e
    'floodfill': ['keyboard', 102],             # f
    'load': ['keyboard', 105],                  # i
    'save': ['keyboard', 111],                  # o
    'grid_toggle': ['keyboard', 103],           # g
    'layer_toggle': ['keyboard', 108],          # l
    'autotile': ['keyboard', 116],              # t
    'lctrl': ['keyboard', 1073742048],          # lctrl
    'place': ['mouse', 1],                      # left click
    'remove': ['mouse', 3],                     # right click
    'layer_up': ['mouse', 4],                   # scroll up
    'layer_down': ['mouse', 5],                 # scroll down
    'custom_data': ['keyboard', 99],            # c
    'deselect': ['keyboard', 97],               # a
    'optimize': ['keyboard', 121],              # y
}

if not os.path.exists('editor/assets'):
    os.mkdir('editor/assets')
if not os.path.exists('editor/assets/level_editor_keys.json'):
    write_json('editor/assets/level_editor_keys.json', KEY_MAPPINGS)
if not os.path.exists('editor/assets/level_editor_config.json'):
    write_json('editor/assets/level_editor_config.json', {'tile_size': [16, 16], 'spritesheet_path': None})
level_editor_config = read_json('editor/assets/level_editor_config.json')

class Assets:
    def __init__(self, game, spritesheet_path):
        # dummy class
        colorkey = (255, 255, 255)
        self.spritesheets = load_spritesheets(spritesheet_path, colorkey=colorkey) if spritesheet_path else {}

class Draggable:
    def __init__(self, game, pos, radius=10, snap=(8, 8)):
        self.game = game
        self.pos = list(pos)
        self.dragging = False
        self.radius = radius
        self.hovered = False
        self.last_mpos = [0, 0]
        self.snap = tuple(snap)

    @property
    def reduced_snap_pos(self):
        return (math.floor((self.pos[0] + self.snap[0] / 2) / self.snap[0]), math.floor((self.pos[1] + self.snap[1] / 2) / self.snap[1]))
    
    @property
    def snap_pos(self):
        return (math.floor((self.pos[0] + self.snap[0] / 2) / self.snap[0]) * self.snap[0], math.floor((self.pos[1] + self.snap[1] / 2) / self.snap[1]) * self.snap[1])
    
    @property
    def rect(self):
        return pygame.Rect(self.pos[0] - self.radius / 2, self.pos[1] - self.radius / 2, self.radius, self.radius)
    
    def update(self, mpos):
        self.hovered = False
        if self.rect.collidepoint(mpos):
            self.hovered = True
            if self.game.input.pressed('place'):
                self.dragging = True
        if self.game.input.released('place'):
            self.dragging = False
            self.pos = list(self.snap_pos)

        if self.dragging:
            self.pos[0] += mpos[0] - self.last_mpos[0]
            self.pos[1] += mpos[1] - self.last_mpos[1]
        self.last_mpos = list(mpos)

    def render(self, offset=(0, 0)):
        color = (255, 255, 255) if (self.hovered or self.dragging) else (100, 100, 100)
        radius = self.radius if (self.hovered or self.dragging) else self.radius / 2
        width = 2 if self.dragging else 1
        self.game.renderer.renderf(pygame.draw.circle, color, (self.snap_pos[0] - offset[0], self.snap_pos[1] - offset[1]), radius, width, z=999996)

class Game:
    def __init__(self, spritesheet_path):
        self.screen = pygame.display.set_mode((1080, 720))
        self.display = pygame.Surface((1080 / 3, 720 / 3))
        self.dt = 0.016
        self.input = Input(self, path='editor/assets/level_editor_keys.json')
        self.tilemap = Tilemap(self, tile_size=level_editor_config['tile_size'])
        self.tile_size = self.tilemap.tile_size

        self.renderer = Renderer(self)

        self.camera = Camera(self, (1080, 720))

        self.assets = Assets(self, spritesheet_path)

        self.font_path = 'editor/assets/fonts' if os.path.exists('editor/assets/fonts') else None
        self.text = pText(self, self.font_path)

        self.time = time.time()
        self.clock = pygame.time.Clock()

        self.spritesheet_thumbs = {}
        for spritesheet_id, spritesheet in self.assets.spritesheets.items():
            self.spritesheet_thumbs[spritesheet_id] = self.generate_spritesheet_thumb(spritesheet)
        self.thumb_keys = list(self.spritesheet_thumbs.keys())
        self.menu_scroll = [0, 0, 0]
        self.selected_ss_index = 0
        self.current_tile = 0
        self.grid_mode = True
        self.layer = 0
        self.custom_data = ''
        self.mpos = (0, 0)
        self.mouse_idle = [(0, 0), 0]
        self.layer_opacity = False
        self.selection = [False, False]
        self.dimension_selector = Draggable(self, (self.tile_size[0] * self.tilemap.dimensions[0], self.tile_size[1] * self.tilemap.dimensions[1]), snap=tuple(self.tile_size))
        self.metrics = {
            'tile': self.current_tile,
            'pos': (0, 0),
            'layer': self.layer,
            'map': str(self.tilemap.dimensions[0]) + 'x' + str(self.tilemap.dimensions[1]) + ' (' + str(self.tile_size[0]) + 'x' + str(self.tile_size[1]) + ')',
            'total': 0,
            'visible': 0,
            'grid': 0,
            'offgrid': 0,
            'vlc': tuple(),
            'custom': self.custom_data
            }
        self.metrics_order = ['tile', 'pos', 'layer', 'map', 'total', 'visible', 'grid', 'offgrid', 'vlc', 'custom']
        self.textbox = Textbox(self, 'small_font', 200, return_event=lambda buffer: self.set_custom_data(buffer.text))

        self.custom_tile_renderers = {}

    def enable(self, *args, **kwargs):
        pass

    def set_custom_data(self, data):
        self.custom_data = data
        self.metrics['custom'] = self.custom_data

    @property
    def selected_ss(self):
        if len(self.thumb_keys):
            ss_id = self.thumb_keys[self.selected_ss_index]
            return self.assets.spritesheets[ss_id]
        
    @property
    def hovered_loc(self):
        if self.grid_mode:
            return (int((self.mpos[0] + self.camera[0]) // self.tile_size[0]), int((self.mpos[1] + self.camera[1]) // self.tile_size[1]))
        else:
            return (math.floor(self.mpos[0] + self.camera[0]), math.floor(self.mpos[1] + self.camera[1]))
        
    @property
    def offgrid_hovered_loc(self):
        return (math.floor(self.mpos[0] + self.camera[0]), math.floor(self.mpos[1] + self.camera[1]))
    
    @property
    def selection_rect(self):
        if self.selection[1]:
            return rectify(self.selection[0], self.selection[1])
        
    def generate_spritesheet_thumb(self, spritesheet):
        thumb_surf = pygame.Surface((64, 16), pygame.SRCALPHA)
        i = 0
        for loc in spritesheet['assets']:
            if loc[0] == 0:
                thumb_surf.blit(pygame.transform.scale(spritesheet['assets'][loc], (16, 16)), (i * 8, 0))
                i += 1
        return thumb_surf
    
    def update_metrics(self):
        tcount = self.tilemap.count_tiles()
        vcount = self.tilemap.count_rect_tiles(pygame.Rect(*self.camera, *self.display.get_size()))
        self.metrics = {'map': str(self.tilemap.dimensions[0]) + 'x' + str(self.tilemap.dimensions[1]) + ' (' + str(self.tile_size[0]) + 'x' + str(self.tile_size[1]) + ')',
                        'total': sum(tcount.values()), 'visible': vcount, 'grid': tcount['grid'], 'offgrid': tcount['offgrid'],
                        'vlc': tuple(self.tilemap.visible_layer_contains(pygame.Rect(*self.camera, *self.display.get_size()), self.layer)), 'custom': self.custom_data}
        
    def update(self):
        self.input.update()
        self.display.fill((0, 0, 0))

        camera_movement = [0, 0]
        if not self.input.holding('lctrl'):
            if self.input.holding('camera_right'):
                camera_movement[0] += self.tile_size[0] / 4
            if self.input.holding('camera_left'):
                camera_movement[0] -= self.tile_size[0] / 4
            if self.input.holding('camera_down'):
                camera_movement[1] += self.tile_size[1] / 4
            if self.input.holding('camera_up'):
                camera_movement[1] -= self.tile_size[1] / 4
        self.camera.move(camera_movement)
        self.camera.update()

        mpos = (self.input.mouse.pos[0] // 3, self.input.mouse.pos[1] // 3)
        self.mpos = mpos
        hovering = 'world'
        if mpos[0] < 70:
            hovering = 'tile_select'
            if mpos[1] < 80:
                hovering = 'ss_select'

        if mpos != self.mouse_idle[0]:
            self.mouse_idle = [mpos, 0]
        else:
            self.mouse_idle[1] += self.dt
        if self.mouse_idle[1] > 1.5:
            self.update_metrics()
            self.mouse_idle[1] = 0

        self.dimension_selector.update((mpos[0] + self.camera[0], mpos[1] + self.camera[1]))
        self.dimension_selector.pos[0] = max(self.tile_size[0] * 2, self.dimension_selector.pos[0])
        self.dimension_selector.pos[1] = max(self.tile_size[1] * 2, self.dimension_selector.pos[1])
        self.tilemap.dimensions = self.dimension_selector.reduced_snap_pos

        for blit in sorted(self.tilemap.render_prep(pygame.Rect(*self.camera, *self.display.get_size()), offset=self.camera), key=lambda x: x[2]):
            if self.layer_opacity and (blit[2] != self.layer):
                blit[0].set_alpha(100)
            self.display.blit(blit[0], blit[1])
            blit[0].set_alpha(255)
        offset = (self.camera.pos[0] % self.tile_size[0], self.camera.pos[1] % self.tile_size[1])
        grid_surf = pygame.Surface(self.display.get_size(), pygame.SRCALPHA)
        pygame.draw.line(grid_surf, (0, 255, 255), (-self.camera[0], 0), (-self.camera[0], self.display.get_height()), 3)
        pygame.draw.line(grid_surf, (0, 255, 255), (0, -self.camera[1]), (self.display.get_width(), -self.camera[1]), 3)
        pygame.draw.line(grid_surf, (255, 255, 0), (self.tilemap.dimensions[0] * self.tilemap.tile_size[0] - self.camera[0], max(0, -self.camera[1])), (self.tilemap.dimensions[0] * self.tilemap.tile_size[0] - self.camera[0], min(self.display.get_height(), self.tilemap.dimensions[1] * self.tilemap.tile_size[1] - self.camera[1])), 3)
        pygame.draw.line(grid_surf, (255, 255, 0), (max(0, -self.camera[0]), self.tilemap.dimensions[1] * self.tilemap.tile_size[1] - self.camera[1]), (min(self.display.get_width(), self.tilemap.dimensions[0] * self.tilemap.tile_size[0] - self.camera[0]), self.tilemap.dimensions[1] * self.tilemap.tile_size[1] - self.camera[1]), 3)
        for x in range(self.display.get_width() // self.tile_size[0] + 1):
            pygame.draw.line(grid_surf, (100, 100, 100), (x * self.tile_size[0] - offset[0], 0), (x * self.tile_size[0] - offset[0], self.display.get_height()))
        for y in range(self.display.get_height() // self.tile_size[0] + 1):
            pygame.draw.line(grid_surf, (100, 100, 100), (0, y * self.tile_size[1] - offset[1]), (self.display.get_width(), y * self.tile_size[1] - offset[1]))
        grid_surf.set_alpha(100)
        self.renderer.blit(grid_surf, (0, 0), z=999996)

        self.dimension_selector.render(offset=self.camera)
        
        if self.selection[0]:
            endpoint = self.selection[1] if self.selection[1] else self.offgrid_hovered_loc
            rect = rectify(self.selection[0], endpoint)
            rect.x -= self.camera[0]
            rect.y -= self.camera[1]
            self.renderer.renderf(pygame.draw.rect, (255, 0, 255), rect, 1, z=999997)

        menu_surf = pygame.Surface((70, self.display.get_height()), pygame.SRCALPHA)
        menu_surf.fill((0, 40, 60, 180))
        if len(self.thumb_keys):
            for i in range(4):
                lookup_i = (self.menu_scroll[0] + i) % len(self.thumb_keys)
                thumb = self.spritesheet_thumbs[self.thumb_keys[lookup_i]]
                thumb_r = pygame.Rect(3, 3 + i * 19, 64, 16)
                if thumb_r.collidepoint(mpos):
                    if self.input.pressed('place'):
                        self.selected_ss_index = lookup_i
                        self.menu_scroll[1] = 0
                        self.menu_scroll[2] = 0
                menu_surf.blit(thumb, (3, 3 + i * 19))
        if self.selected_ss:
            for tile_loc in self.selected_ss['assets']:
                tile = self.selected_ss['assets'][tile_loc]
                if tile_loc[1] - self.menu_scroll[2] >= 0:
                    tile_r = pygame.Rect(3 + (tile_loc[0] - self.menu_scroll[1]) * 18, 83 + (tile_loc[1] - self.menu_scroll[2]) * 18, 16, 16)
                    if tile_r.collidepoint(mpos):
                        if self.input.pressed('place'):
                            self.current_tile = (self.thumb_keys[self.selected_ss_index], tile_loc)
                    menu_surf.blit(pygame.transform.scale(tile, (16, 16)), (3 + (tile_loc[0] - self.menu_scroll[1]) * 18, 83 + (tile_loc[1] - self.menu_scroll[2]) * 18))
        pygame.draw.line(menu_surf, (0, 80, 120), (menu_surf.get_width() - 1, 0), (menu_surf.get_width() - 1, menu_surf.get_height() - 1))
        pygame.draw.line(menu_surf, (0, 80, 120), (0, 80), (70, 80))
        self.renderer.blit(menu_surf, (0, 0), z=999998)

        if self.current_tile:
            tile_img = self.assets.spritesheets[self.current_tile[0]]['assets'][self.current_tile[1]].copy()
            tile_img.set_alpha(128)
            if self.grid_mode:
                pos = (self.hovered_loc[0] * self.tile_size[0] - self.camera[0], self.hovered_loc[1] * self.tile_size[1] - self.camera[1])
                self.renderer.renderf(pygame.draw.rect, (255, 255, 255), pygame.Rect(*pos, *self.tile_size), 1, z=999998)
                self.renderer.blit(tile_img, pos, z=999998)
            else:
                self.renderer.blit(tile_img, mpos, z=999998)
        
        if self.font_path:
            self.metrics['tile'] = self.current_tile
            self.metrics['layer'] = self.layer
            self.metrics['pos'] = self.hovered_loc
            for i, metric in enumerate(self.metrics_order):
                text = metric + ': ' + str(self.metrics[metric])
                w = self.text['small_font'].width(text)
                self.text['small_font'].renderz(text, (self.display.get_width() - 4 - w, 4 + 10 * i), z=999999)
            
            if self.textbox.bound:
                self.renderer.blit(self.textbox.surf, (100, 100), z=999999)

        self.renderer.cycle({'default': self.display})

        if self.input.pressed('quit'):
            pygame.quit()
            sys.exit()

        if self.input.pressed('layer_up'):
            if hovering == 'ss_select':
                self.menu_scroll[0] -= 1
            elif hovering == 'tile_select':
                if self.input.holding('lctrl'):
                    self.menu_scroll[1] += 1
                else:
                    self.menu_scroll[2] += 1
            elif hovering == 'world':
                self.layer += 1
        if self.input.pressed('layer_down'):
            if hovering == 'ss_select':
                self.menu_scroll[0] += 1
            elif hovering == 'tile_select':
                if self.input.holding('lctrl'):
                    self.menu_scroll[1] = max(0, self.menu_scroll[2] - 1)
                else:
                    self.menu_scroll[2] = max(0, self.menu_scroll[1] - 1)
            elif hovering == 'world':
                self.layer -= 1

        if self.input.pressed('custom_data'):
            self.textbox.bind()
        if self.input.pressed('grid_toggle'):
            self.grid_mode = not self.grid_mode
        if self.input.pressed('layer_toggle'):
            self.layer_opacity = not self.layer_opacity
        if self.input.pressed('select'):
            if not self.selection[0]:
                self.selection[0] = self.offgrid_hovered_loc
            elif not self.selection[1]:
                self.selection[1] = self.offgrid_hovered_loc
        if self.input.holding('lctrl'):
            if self.input.pressed('deselect'):
                self.selection = [None, None]
            if self.input.pressed('delete'):
                if self.selection_rect:
                    self.tilemap.rect_delete(self.selection_rect, layer=self.layer)
            if self.input.pressed('autotile'):
                if self.selection_rect:
                    self.tilemap.autotile(layer=self.layer, rect=self.selection_rect)
            if self.input.pressed('optimize'):
                if self.selection_rect:
                    self.tilemap.optimize_area(layer=self.layer, rect=self.selection_rect)
        if self.input.pressed('save'):
            self.tilemap.save('data/maps/save.pmap')
        if self.input.pressed('load'):
            root = Tk()
            root.withdraw()
            filename = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select Map",filetypes = (("pygpen maps", "*.pmap"), ("json files","*.json"), ("all files","*.*")))
            if filename != '':
                self.tilemap.load(filename)
                self.dimension_selector.pos = [self.tile_size[0] * self.tilemap.dimensions[0], self.tile_size[1] * self.tilemap.dimensions[1]]
                self.dimension_selector.snap = tuple(self.tile_size)

        if self.current_tile and not self.dimension_selector.dragging:
            if hovering == 'world':
                next_tile = Tile(self, *self.current_tile, self.hovered_loc, layer=self.layer, custom_data=self.custom_data)
                if self.grid_mode:
                    if self.input.holding('place'):
                        self.tilemap.insert(next_tile)
                    if self.input.pressed('floodfill'):
                        self.tilemap.floodfill(next_tile)
                else:
                    if self.input.pressed('place'):
                        self.tilemap.insert(next_tile, ongrid=False, ignore_lock=True)
                if self.input.holding('remove'):
                    self.tilemap.rect_delete(pygame.Rect(*self.offgrid_hovered_loc, 2, 2), layer=self.layer)
        
        self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
        self.cycle()

    def run(self):
        while True:
            self.update()

    def cycle(self):
        pygame.display.update()
        self.clock.tick(60)
        self.screen.fill((0, 0, 0))
        self.time = time.time()

game = Game('data/assets/spritesheets')
game.run()