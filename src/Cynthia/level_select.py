import json
import os
import pygame
from src.audio import audio_manager as audio

GOLD      = (196, 166, 114)
DARK      = (28, 24, 20)
DARK_BTN  = (45, 38, 32)
WHITE     = (255, 255, 255)
GREY      = (120, 120, 120)
LOCKED_COL = (50, 40, 35)

SAVE_FILE = 'save.json'

LEVEL_INFO = [
    {'id': 1, 'name': 'Egypte Antique',      'desc': 'Sarcophages et hieroglyphes',    'color': (180, 140,  60)},
    {'id': 2, 'name': 'Grece Antique',        'desc': 'Statues et amphores',            'color': ( 80, 140, 200)},
    {'id': 3, 'name': 'Renaissance',          'desc': 'Peintures et maitres italiens',  'color': (180,  80,  60)},
    {'id': 4, 'name': 'France Royale',        'desc': 'Joyaux de la couronne',          'color': (140,  60, 180)},
    {'id': 5, 'name': 'La Grande Finale',     'desc': 'Le butin ultime du Louvre',      'color': (220, 180,  40)},
]


def load_save():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                return json.load(f)
        except Exception:
            pass
    return {'unlocked': 1, 'completed': []}


def write_save(data):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(data, f)
    except Exception:
        pass


def unlock_next_level(level_id):
    data = load_save()
    if level_id not in data['completed']:
        data['completed'].append(level_id)
    if data['unlocked'] < level_id + 1 <= len(LEVEL_INFO):
        data['unlocked'] = level_id + 1
    write_save(data)


class LevelSelect:
    def __init__(self, screen, manager, character):
        self.screen    = screen
        self.manager   = manager
        self.character = character
        self.save      = load_save()
        self.hovered   = -1
        self.font_title = pygame.font.Font(None, 72)
        self.font_name  = pygame.font.Font(None, 40)
        self.font_desc  = pygame.font.Font(None, 28)
        self.font_hint  = pygame.font.Font(None, 26)
        self._cards     = []

    def _draw_lock(self, cx, cy):
        body_w, body_h = 22, 18
        bx, by = cx - body_w // 2, cy - body_h // 2
        pygame.draw.rect(self.screen, GREY, (bx, by, body_w, body_h), border_radius=3)
        arc_rect = pygame.Rect(cx - 8, by - 12, 16, 16)
        pygame.draw.arc(self.screen, GREY, arc_rect, 0, 3.14159, 3)
        pygame.draw.circle(self.screen, DARK, (cx, cy - 2), 3)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mp = pygame.mouse.get_pos()
            for i, rect in enumerate(self._cards):
                if rect.collidepoint(mp):
                    lvl = LEVEL_INFO[i]
                    if lvl['id'] <= self.save['unlocked']:
                        audio.play_sfx('hover')
                        self._launch(lvl['id'])

        if event.type == pygame.MOUSEMOTION:
            mp = pygame.mouse.get_pos()
            self.hovered = -1
            for i, rect in enumerate(self._cards):
                if rect.collidepoint(mp):
                    self.hovered = i

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            from src.Cynthia.character_select import CharacterSelect
            self.manager.scene = CharacterSelect(self.screen, self.manager)

    def _launch(self, level_id):
        from src.Cynthia.jeu import Jeu
        audio.play_music(audio.MUSIC_CALM)
        self.manager.scene = Jeu(self.screen, self.manager,
                                  character=self.character, level_id=level_id)

    def update(self, dt=0):
        pass

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(DARK)

        title = self.font_title.render("Choisissez un niveau", True, GOLD)
        self.screen.blit(title, title.get_rect(midtop=(w // 2, 30)))

        n     = len(LEVEL_INFO)
        cw    = min(220, (w - 80) // n - 20)
        ch    = 280
        gap   = (w - n * cw) // (n + 1)
        cy    = h // 2 - ch // 2 + 20

        self._cards = []
        for i, lvl in enumerate(LEVEL_INFO):
            cx    = gap + i * (cw + gap)
            rect  = pygame.Rect(cx, cy, cw, ch)
            self._cards.append(rect)

            locked   = lvl['id'] > self.save['unlocked']
            complete = lvl['id'] in self.save['completed']
            hov      = (i == self.hovered) and not locked

            bg_col = LOCKED_COL if locked else (DARK_BTN if not hov else (60, 52, 44))
            border  = GREY if locked else (GOLD if not complete else (80, 200, 80))

            pygame.draw.rect(self.screen, bg_col, rect, border_radius=14)
            pygame.draw.rect(self.screen, border, rect, 2, border_radius=14)

            if complete:
                check = self.font_name.render("✓", True, (80, 200, 80))
                self.screen.blit(check, check.get_rect(topright=(rect.right - 8, rect.top + 6)))

            num_col  = GREY if locked else lvl['color']
            num_surf = pygame.font.Font(None, 80).render(str(lvl['id']), True, num_col)
            self.screen.blit(num_surf, num_surf.get_rect(midtop=(rect.centerx, rect.top + 16)))

            name_col = GREY if locked else WHITE
            nm = self.font_name.render(lvl['name'], True, name_col)
            if nm.get_width() > cw - 16:
                nm = pygame.transform.scale(nm, (cw - 16, nm.get_height()))
            self.screen.blit(nm, nm.get_rect(midtop=(rect.centerx, rect.top + 100)))

            dc = self.font_desc.render(lvl['desc'], True, GREY)
            if dc.get_width() > cw - 16:
                dc = pygame.transform.scale(dc, (cw - 16, dc.get_height()))
            self.screen.blit(dc, dc.get_rect(midtop=(rect.centerx, rect.top + 148)))

            if locked:
                self._draw_lock(rect.centerx, rect.bottom - 28)
            else:
                rooms_txt = self.font_desc.render("5 salles", True, GOLD)
                self.screen.blit(rooms_txt, rooms_txt.get_rect(midbottom=(rect.centerx, rect.bottom - 12)))

        hint = self.font_hint.render("Echap : retour  |  Clic : jouer", True, GREY)
        self.screen.blit(hint, hint.get_rect(midbottom=(w // 2, h - 10)))
