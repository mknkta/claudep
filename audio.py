import os
import pygame

_ready = False
_playing = False
_start_ticks = 0
_sfx: dict = {}

def _init():
    global _ready
    if not _ready:
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            _ready = True
        except pygame.error:
            pass

def play_music(path: str):
    global _playing, _start_ticks
    _init()
    _start_ticks = pygame.time.get_ticks()
    if not _ready or not os.path.isfile(path):
        _playing = False; return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
        _playing = True
    except pygame.error:
        _playing = False

def get_time() -> float:
    if _playing:
        pos = pygame.mixer.music.get_pos()
        if pos >= 0:
            return pos / 1000.0
    return (pygame.time.get_ticks() - _start_ticks) / 1000.0

def stop():
    if _ready:
        pygame.mixer.music.stop()
    global _playing
    _playing = False

def play_sfx(path: str):
    if not _ready or not os.path.isfile(path): return
    if path not in _sfx:
        try: _sfx[path] = pygame.mixer.Sound(path)
        except pygame.error: return
    _sfx[path].play()
