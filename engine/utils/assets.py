import pygame, moderngl
import numpy as np
from .io import recursive_file_op

def load_img(path, ctx=None, alpha=False, scale=1, colorkey=None):
    if path.split('/')[-1].split('.')[-1] in ['json']:
        return

    if alpha:
        img = pygame.image.load(path).convert_alpha()
    else:
        img = pygame.image.load(path).convert()

    if scale != 1:
        img = pygame.transform.scale(img, (img.width * scale, img.height * scale))

    if colorkey:
        img.set_colorkey(colorkey)

    if ctx:
        return pg2tex(img, ctx)
    return img

def pg2tex(surf, ctx):
    w, h = surf.get_size()
    tex_data = pygame.image.tobytes(surf, 'RGBA', 1)
    tex = ctx.texture((w, h), 4, tex_data)
    tex.filter = (moderngl.LINEAR, moderngl.LINEAR)
    return tex

def load_img_dir(path, ctx=None, alpha=None, scale=1, colorkey=None):
    return recursive_file_op(path, lambda x: load_img(x, ctx, alpha=alpha, scale=scale, colorkey=colorkey))

def create_texture_array(ctx, texture_dict):
    """
    Create a texture array from a list of individual textures.

    Parameters:
        ctx: moderngl.Context - the ModernGL context
        textures: dict - A dictionary where keys are texture names and values are moderngl.Texture

    Returns:
        tuple: (texture_array, mapping)
            - texture_array: moderngl.TextureArray - The combined texture array
            - mapping: dict - A mapping of texture names to their corresponding layer indices
    """

    textures = []
    mapping = {}

    for i, (name, texture) in enumerate(texture_dict.items()):
        w, h = texture.size
        data = np.frombuffer(texture.read(), dtype=np.uint8).reshape((w, h, 4))
        textures.append(data)
        mapping[name] = i

    w, h, channels = textures[0].shape
    for tex in textures:
        if tex.shape != (w, h, channels):
            raise ValueError(f'All textures must have the sam dimensions (found mismatch: {tex.shape})')
        
    texture_array = ctx.texture_array((w, h, len(textures)), channels, dtype='f1')

    texture_array.build_mipmaps()
    print(mapping)

    return texture_array, mapping
