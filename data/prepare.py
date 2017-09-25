import os
import sys
import pygame as pg

from . import tools


SCREEN_SIZE = (800, 600)
ORIGINAL_CAPTION = 'Fifteen Puzzle'

# pg.mixer.pre_init(44100, -16, 1, 512)
pg.init()
os.environ['SDL_VIDEO_CENTERED'] = 'TRUE'
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()

BG_COLOR = pg.Color('#E3DFC8')


def graphics_from_directories(directories):
    """
    Calls the tools.load_all_graphics() function for all directories passed.
    """
    base_path = os.path.join("resources", "graphics")
    GFX = {}
    for directory in directories:
        if getattr(sys, 'frozen', False):
            path = os.path.join(os.path.dirname(sys.executable), 'graphics',
                                directory)
        else:
            path = os.path.join(base_path, directory)
        GFX[directory] = tools.load_all_gfx(path)
    return GFX

# _SUB_DIRECTORIES = ['player', 'enemies', 'ground', 'misc']
# GFX = graphics_from_directories(_SUB_DIRECTORIES)

# fonts_path = os.path.join('resources', 'fonts')
# FONTS = tools.load_all_fonts(fonts_path)

# sfx_path = os.path.join('resources', 'sounds')
# SFX = tools.load_all_sfx(sfx_path)

# music_path = os.path.join('resources', 'music')
# MUSIC = tools.load_all_music(music_path)
