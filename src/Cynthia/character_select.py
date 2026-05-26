import pygame
from src.audio import audio_manager as audio

GOLD     = (196, 166, 114)
DARK     = (28, 24, 20)
DARK_BTN = (45, 38, 32)
WHITE    = (255, 255, 255)
GREY     = (160, 160, 160)

# Ordre : Anne, Rémy, Sophie
CHARACTERS = [
    {
        'id': 'smart',
        'name': 'Anne',
        'desc': 'Experte en enigmes',
        'sprite': 'assets/images/sprite2.png',
        'stats': {'vitesse': 2, 'discretion': 3, 'intelligence': 5, 'endurance': 3},
        'lives': 3,
        'speed_mult': 0.9,
        'stealth_mult': 1.0,
        'color': (160, 220, 100),
    },
    {
        'id': 'balanced',
        'name': 'Sophie',
        'desc': 'Polyvalent',
        'sprite': 'assets/images/sprite4.png',
        'stats': {'vitesse': 3, 'discretion': 3, 'intelligence': 3, 'endurance': 4},
        'lives': 4,
        'speed_mult': 1.0,
        'stealth_mult': 1.0,
        'color': (180, 140, 220),
    },
    {
        'id': 'discreet',
        'name': 'Rémy',
        'desc': 'Voleuse discrete',
        'sprite': 'assets/images/sprite3.png',
        'stats': {'vitesse': 2, 'discretion': 5, 'intelligence': 4, 'endurance': 2},
        'lives': 3,
        'speed_mult': 0.8,
        'stealth_mult': 1.4,
        'color': (100, 160, 220),
    },
]

STAT_COLORS = {
    1: (180, 50,  50),
    2: (200, 100, 50),
    3: (200, 180, 50),
    4: (100, 180, 50),
    5: (50,  200, 80),
}


class CharacterSelect:
    def __init__(self, screen, manager):
        self.screen   = screen
        self.manager  = manager
        self.selected = 0
        self.font_title = pygame.font.Font(None, 68)
        self.font_name  = pygame.font.Font(None, 46)
        self.font_stat  = pygame.font.Font(None, 28)
        self.font_desc  = pygame.font.Font(None, 30)
        self.font_hint  = pygame.font.Font(None, 24)
        self._load_sprites()
        self._btn_left  = pygame.Rect(0, 0, 52, 52)
        self._btn_right = pygame.Rect(0, 0, 52, 52)
        self._btn_play  = pygame.Rect(0, 0, 210, 58)
        self._btn_back  = pygame.Rect(0, 0, 120, 40)

    def _load_sprites(self):
        self._sprites = []
        for ch in CHARACTERS:
            try:
                img = pygame.image.load(ch['sprite']).convert_alpha()
                img = pygame.transform.scale(img, (90, 135))
            except Exception:
                img = pygame.Surface((90, 135), pygame.SRCALPHA)
                img.fill(ch['color'])
            self._sprites.append(img)

    def _back(self):
        audio.play_sfx('hover')
        from src.Cynthia.mode_select import ModeSelect
        self.manager.scene = ModeSelect(self.screen, self.manager)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._back()
            elif event.key in (pygame.K_LEFT, pygame.K_a):
                self.selected = (self.selected - 1) % len(CHARACTERS)
                audio.play_sfx('hover')
            elif event.key in (pygame.K_RIGHT, pygame.K_d):
                self.selected = (self.selected + 1) % len(CHARACTERS)
                audio.play_sfx('hover')
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._launch()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mp = pygame.mouse.get_pos()
            if self._btn_back.collidepoint(mp):
                self._back()
            elif self._btn_left.collidepoint(mp):
                self.selected = (self.selected - 1) % len(CHARACTERS)
                audio.play_sfx('hover')
            elif self._btn_right.collidepoint(mp):
                self.selected = (self.selected + 1) % len(CHARACTERS)
                audio.play_sfx('hover')
            elif self._btn_play.collidepoint(mp):
                self._launch()

    def _launch(self):
        from src.Cynthia.level_select import LevelSelect
        audio.play_sfx('hover')
        self.manager.scene = LevelSelect(self.screen, self.manager, CHARACTERS[self.selected])

    def update(self, dt=0):
        pass

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(DARK)

        # ── Bouton Retour (haut gauche) ────────────────────────────────────
        self._btn_back.topleft = (18, 18)
        pygame.draw.rect(self.screen, DARK_BTN, self._btn_back, border_radius=10)
        pygame.draw.rect(self.screen, GOLD,     self._btn_back, 2, border_radius=10)
        back_txt = self.font_hint.render("< Retour", True, GOLD)
        self.screen.blit(back_txt, back_txt.get_rect(center=self._btn_back.center))

        # ── Titre ──────────────────────────────────────────────────────────
        title = self.font_title.render("Choisissez votre personnage", True, GOLD)
        self.screen.blit(title, title.get_rect(midtop=(w // 2, 20)))

        # ── Layout : card + dots + bouton empilés, centrés verticalement ───
        card_w, card_h = 320, 430
        btn_h          = 54
        dots_gap       = 18   # espace card→dots
        btn_gap        = 14   # espace dots→bouton

        block_h = card_h + dots_gap + 16 + btn_gap + btn_h
        title_bottom = 20 + self.font_title.get_height()
        top_margin   = title_bottom + 14
        card_y = top_margin + max(0, (h - top_margin - 20 - block_h) // 2)
        card_x = w // 2 - card_w // 2

        shadow = pygame.Surface((card_w + 8, card_h + 8), pygame.SRCALPHA)
        shadow.fill((0, 0, 0, 110))
        self.screen.blit(shadow, (card_x - 4, card_y + 6))

        pygame.draw.rect(self.screen, DARK_BTN, (card_x, card_y, card_w, card_h), border_radius=18)
        pygame.draw.rect(self.screen, GOLD,     (card_x, card_y, card_w, card_h), 2, border_radius=18)

        ch = CHARACTERS[self.selected]

        # Sprite
        sprite = self._sprites[self.selected]
        sr = sprite.get_rect(midtop=(w // 2, card_y + 18))
        self.screen.blit(sprite, sr)

        # Nom
        name_surf = self.font_name.render(ch['name'], True, GOLD)
        self.screen.blit(name_surf, name_surf.get_rect(midtop=(w // 2, sr.bottom + 10)))

        # Description
        desc_surf = self.font_desc.render(ch['desc'], True, GREY)
        self.screen.blit(desc_surf, desc_surf.get_rect(midtop=(w // 2, sr.bottom + 46)))

        # Séparateur
        sep_y = sr.bottom + 72
        pygame.draw.line(self.screen, (70, 60, 45),
                         (card_x + 20, sep_y), (card_x + card_w - 20, sep_y), 1)

        # Stats
        sy = sep_y + 12
        for key, label in [('vitesse', 'Vitesse'), ('discretion', 'Discretion'),
                            ('intelligence', 'Intelligence'), ('endurance', 'Endurance')]:
            val = ch['stats'][key]
            lbl = self.font_stat.render(label, True, WHITE)
            self.screen.blit(lbl, (card_x + 20, sy + 2))
            for i in range(5):
                col = STAT_COLORS.get(i + 1, GREY) if i < val else (50, 50, 50)
                pygame.draw.rect(self.screen, col,
                                 (card_x + 166 + i * 26, sy + 3, 20, 14), border_radius=3)
            sy += 28

        # Vies
        lives_txt = self.font_stat.render(f'Vies de depart : {ch["lives"]}', True, (220, 80, 80))
        self.screen.blit(lives_txt, lives_txt.get_rect(midtop=(w // 2, sy + 6)))

        # ── Flèches de navigation ──────────────────────────────────────────
        arrow_y = card_y + card_h // 2
        self._btn_left.center  = (card_x - 42, arrow_y)
        self._btn_right.center = (card_x + card_w + 42, arrow_y)

        for btn, txt in [(self._btn_left, '<'), (self._btn_right, '>')]:
            pygame.draw.rect(self.screen, DARK_BTN, btn, border_radius=10)
            pygame.draw.rect(self.screen, GOLD, btn, 2, border_radius=10)
            t = self.font_name.render(txt, True, GOLD)
            self.screen.blit(t, t.get_rect(center=btn.center))

        # ── Points de navigation ───────────────────────────────────────────
        dots_y = card_y + card_h + dots_gap
        for i in range(len(CHARACTERS)):
            cx = w // 2 + (i - 1) * 26
            col = GOLD if i == self.selected else (65, 55, 40)
            pygame.draw.circle(self.screen, col, (cx, dots_y), 7)
            pygame.draw.circle(self.screen, GOLD, (cx, dots_y), 7, 1)

        # ── Bouton Jouer (juste sous les points) ──────────────────────────
        self._btn_play.size = (210, btn_h)
        self._btn_play.midtop = (w // 2, dots_y + 14)
        pygame.draw.rect(self.screen, DARK_BTN, self._btn_play, border_radius=12)
        pygame.draw.rect(self.screen, GOLD,     self._btn_play, 2, border_radius=12)
        play_txt = self.font_name.render("Jouer", True, GOLD)
        self.screen.blit(play_txt, play_txt.get_rect(center=self._btn_play.center))
