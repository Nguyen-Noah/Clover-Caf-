import pygame

def rectify(p1, p2):
    tl = (min(p1[0], p2[0]), min(p1[1], p2[1]))
    br = (max(p1[0], p2[0]), max(p1[1], p2[1]))
    return pygame.Rect(*tl, br[0] - tl[0] + 1, br[1] - tl[1] + 1)

def clamp_between(value, min_offset=1, max_offset=4):
    return max(min_offset, min(value, max_offset))