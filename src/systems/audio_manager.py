# audio_manager.py — gerencia música e efeitos sonoros
#
# Sincronia de áudio:
#   pygame.mixer.music.get_pos() retorna quantos ms a música tocou desde o
#   último play(). Usar isso como fonte da verdade garante que, mesmo se o
#   jogo travar por 1 frame, os obstáculos se reposicionam corretamente na
#   próxima frame — em vez de acumular erro de dt.

import os
import pygame

# Garante que o mixer está inicializado antes de qualquer chamada.
# Chamado aqui para que o módulo seja seguro mesmo fora do pygame.init().
_mixer_ready = False


def _ensure_mixer():
    global _mixer_ready
    if not _mixer_ready:
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
            _mixer_ready = True
        except pygame.error:
            pass


# ------------------------------------------------------------------
# MÚSICA
# ------------------------------------------------------------------

_music_start_ticks: int = 0   # pygame.time.get_ticks() quando play() foi chamado
_music_playing:     bool = False


def play_music(path: str, loop: bool = True) -> bool:
    """
    Carrega e toca a música. Retorna True se bem-sucedido.
    Se o arquivo não existir, usa silêncio e o fallback de tempo por ticks.
    """
    global _music_playing, _music_start_ticks
    _ensure_mixer()

    if not _mixer_ready:
        return False

    if not os.path.isfile(path):
        # Arquivo ausente: marca início para fallback por ticks.
        _music_start_ticks = pygame.time.get_ticks()
        _music_playing = False
        return False

    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1 if loop else 0)
        _music_start_ticks = pygame.time.get_ticks()
        _music_playing = True
        return True
    except pygame.error:
        _music_start_ticks = pygame.time.get_ticks()
        _music_playing = False
        return False


def get_music_time() -> float:
    """
    Retorna o tempo atual da música em segundos.
    - Se a música estiver tocando: usa get_pos() (preciso, não acumula erro).
    - Fallback: tempo baseado em get_ticks() desde o play().
    """
    if _music_playing:
        pos = pygame.mixer.music.get_pos()
        if pos >= 0:
            return pos / 1000.0
    # Fallback: tempo de relógio desde que play_music() foi chamado.
    return (pygame.time.get_ticks() - _music_start_ticks) / 1000.0


def stop_music():
    if _mixer_ready:
        pygame.mixer.music.stop()


# ------------------------------------------------------------------
# EFEITOS SONOROS
# ------------------------------------------------------------------

_sfx_cache: dict[str, pygame.mixer.Sound] = {}


def play_sfx(path: str):
    """Toca um efeito sonoro curto. Silencioso se o arquivo não existir."""
    if not _mixer_ready:
        return
    if not os.path.isfile(path):
        return

    if path not in _sfx_cache:
        try:
            _sfx_cache[path] = pygame.mixer.Sound(path)
        except pygame.error:
            return

    _sfx_cache[path].play()
