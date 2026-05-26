import pygame
import os

MUSIC_MENU    = 'menu'
MUSIC_CALM    = 'calm'
MUSIC_TENSE   = 'tense'
MUSIC_CRITICAL = 'critical'
MUSIC_GAMEOVER = 'gameover'
MUSIC_VICTORY  = 'victory'

_MUSIC_FILES = {
    MUSIC_MENU:     'assets/music/musique.mp3',
    MUSIC_CALM:     'assets/music/music.mp3',
    MUSIC_TENSE:    'assets/music/music.mp3',
    MUSIC_CRITICAL: 'assets/music/music.mp3',
    MUSIC_GAMEOVER: 'assets/music/musique.mp3',
    MUSIC_VICTORY:  'assets/music/musique.mp3',
}

_SOUND_FILES = {
    'porte':      'assets/sounds/ouverture_porte.mp3',
    'succes':     'assets/sounds/ouverture_porte.mp3',
    'pas':        'assets/sounds/pas.mp3',
    'alarme':     None,
    'vie_perdue': None,
    'bijou':      None,
    'hover':      None,
    'detection':  None,
}

_initialized   = False
_music_on      = True
_volume_music  = 0.6
_volume_sfx    = 0.8
_current_music = None
_sounds        = {}


def init():
    global _initialized
    if _initialized:
        return
    try:
        pygame.mixer.init()
        _initialized = True
        _load_sounds()
    except Exception as e:
        print(f'[Audio] init failed: {e}')


def _load_sounds():
    global _sounds
    for name, path in _SOUND_FILES.items():
        if path and os.path.exists(path):
            try:
                _sounds[name] = pygame.mixer.Sound(path)
                _sounds[name].set_volume(_volume_sfx)
            except Exception:
                _sounds[name] = None
        else:
            _sounds[name] = None


def play_music(state, loop=-1):
    global _current_music
    if not _initialized or not _music_on:
        return
    if state == _current_music:
        return
    path = _MUSIC_FILES.get(state)
    if not path or not os.path.exists(path):
        return
    try:
        pygame.mixer.music.load(path)
        pygame.mixer.music.set_volume(_volume_music)
        pygame.mixer.music.play(loop)
        _current_music = state
    except Exception as e:
        print(f'[Audio] play_music {state}: {e}')


def stop_music():
    global _current_music
    if not _initialized:
        return
    try:
        pygame.mixer.music.stop()
        _current_music = None
    except Exception:
        pass


def play_sfx(name):
    if not _initialized:
        return
    snd = _sounds.get(name)
    if snd:
        snd.play()


def set_volume_music(vol_0_10):
    global _volume_music, _current_music
    _volume_music = max(0.0, min(1.0, vol_0_10 / 10.0))
    if _initialized:
        try:
            pygame.mixer.music.set_volume(_volume_music)
        except Exception:
            pass


def set_volume_sfx(vol_0_10):
    global _volume_sfx
    _volume_sfx = max(0.0, min(1.0, vol_0_10 / 10.0))
    for snd in _sounds.values():
        if snd:
            snd.set_volume(_volume_sfx)


def set_music_on(enabled):
    global _music_on, _current_music
    _music_on = enabled
    if not _initialized:
        return
    if not enabled:
        try:
            pygame.mixer.music.pause()
        except Exception:
            pass
    else:
        try:
            if _current_music:
                pygame.mixer.music.unpause()
            else:
                play_music(MUSIC_MENU)
        except Exception:
            pass


def get_volume_music_0_10():
    return round(_volume_music * 10)


def get_music_on():
    return _music_on


def register_sound(name, path):
    if not _initialized or not os.path.exists(path):
        return
    try:
        _sounds[name] = pygame.mixer.Sound(path)
        _sounds[name].set_volume(_volume_sfx)
    except Exception:
        pass
