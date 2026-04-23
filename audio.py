"""
audio.py — Gerenciamento de áudio do jogo.

Inicializa o mixer do pygame sob demanda e provê funções para:
  - Tocar/parar música de fundo.
  - Tocar efeitos sonoros por arquivo.
  - Obter o tempo de reprodução da música (usado para sincronização).
  - Gerar sons simples programaticamente (beeps para botões).
"""

import os
import math
import pygame

_ready = False
_playing = False
_start_ticks = 0
_sfx: dict = {}
_gen_sfx: dict = {}   # sons gerados programaticamente


def _init():
    """Inicializa o mixer do pygame se ainda não foi inicializado."""
    global _ready
    if not _ready:
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            _ready = True
        except pygame.error:
            pass


def play_music(path: str):
    """
    Carrega e reproduz uma faixa de música em loop.

    Args:
        path: Caminho para o arquivo de áudio (.ogg, .mp3, etc.).
    """
    global _playing, _start_ticks
    _init()
    _start_ticks = pygame.time.get_ticks()
    if not _ready or not os.path.isfile(path):
        _playing = False
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1)
        _playing = True
    except pygame.error:
        _playing = False


def get_time() -> float:
    """
    Retorna o tempo de reprodução da música em segundos.

    Se a música não estiver tocando, usa o tempo do pygame como fallback
    para manter a sincronização de obstáculos.

    Returns:
        Tempo em segundos.
    """
    if _playing:
        pos = pygame.mixer.music.get_pos()
        if pos >= 0:
            return pos / 1000.0
    return (pygame.time.get_ticks() - _start_ticks) / 1000.0


def stop():
    """Para a reprodução da música."""
    if _ready:
        pygame.mixer.music.stop()
    global _playing
    _playing = False


def play_sfx(path: str):
    """
    Toca um efeito sonoro por caminho de arquivo.

    Cacheia o Sound para evitar recarregamentos. Falha silenciosamente
    se o arquivo não existir ou o mixer não estiver disponível.

    Args:
        path: Caminho para o arquivo de som (.wav, .ogg, etc.).
    """
    if not _ready or not os.path.isfile(path):
        return
    if path not in _sfx:
        try:
            _sfx[path] = pygame.mixer.Sound(path)
        except pygame.error:
            return
    _sfx[path].play()


def _make_beep(freq: float, duration: float, volume: float = 0.3):
    """
    Gera um som de beep sintético usando senóide com fade-out.

    Args:
        freq: Frequência do beep em Hz.
        duration: Duração em segundos.
        volume: Volume de 0.0 a 1.0.

    Returns:
        Objeto Sound do pygame, ou None se o mixer não estiver disponível.
    """
    _init()
    if not _ready:
        return None
    try:
        sample_rate = 44100
        n_samples   = int(sample_rate * duration)
        buf = bytearray(n_samples * 2)   # 16-bit mono
        for i in range(n_samples):
            t   = i / sample_rate
            env = max(0.0, 1.0 - t / duration)   # fade-out linear
            val = int(32767 * volume * env * math.sin(2 * math.pi * freq * t))
            val = max(-32768, min(32767, val))
            buf[i*2]     = val & 0xFF
            buf[i*2 + 1] = (val >> 8) & 0xFF
        return pygame.mixer.Sound(buffer=bytes(buf))
    except Exception:
        return None


def play_click():
    """Toca um clique curto de botão (beep de 800 Hz, 80 ms)."""
    _init()
    if not _ready:
        return
    key = "click"
    if key not in _gen_sfx:
        _gen_sfx[key] = _make_beep(800, 0.08, volume=0.25)
    snd = _gen_sfx[key]
    if snd:
        snd.play()


def play_hover():
    """Toca um beep suave de hover em botão (400 Hz, 40 ms)."""
    _init()
    if not _ready:
        return
    key = "hover"
    if key not in _gen_sfx:
        _gen_sfx[key] = _make_beep(400, 0.04, volume=0.12)
    snd = _gen_sfx[key]
    if snd:
        snd.play()
