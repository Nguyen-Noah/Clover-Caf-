import pygame, moderngl

def load_img(path, ctx=None, alpha=False, scale=1, colorkey=(255, 255, 255)):
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
    tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
    return tex

def load_texture(path, ctx, colorkey=(255, 255, 255)):
    return pg2tex(load_img(path, alpha=True, colorkey=colorkey), ctx)

# def load_img_dir(path, ctx=None, alpha=None, scale=1, colorkey=None):
#     return recursive_file_op(path, lambda x: load_img(x, ctx, alpha=alpha, scale=scale, colorkey=colorkey))