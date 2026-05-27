import pygame
from src.audio import audio_manager as audio

GOLD     = (196, 166, 114)
DARK     = (28, 24, 20)
DARK_BTN = (45, 38, 32)
WHITE    = (255, 255, 255)
GREY     = (160, 160, 160)


class ModeSelect:
    def __init__(self, screen, manager):
        self.screen  = screen
        self.manager = manager
        self.font_title = pygame.font.Font(None, 68)
        self.font_label = pygame.font.Font(None, 46)
        self.font_desc  = pygame.font.Font(None, 30)
        self.font_hint  = pygame.font.Font(None, 24)
        self._btn_solo  = pygame.Rect(0, 0, 280, 72)
        self._btn_multi = pygame.Rect(0, 0, 280, 72)
        self._btn_back  = pygame.Rect(0, 0, 120, 40)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from src.Cynthia.accueil import Accueil
                self.manager.scene = Accueil(self.screen, self.manager)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mp = pygame.mouse.get_pos()
            if self._btn_back.collidepoint(mp):
                audio.play_sfx('hover')
                from src.Cynthia.accueil import Accueil
                self.manager.scene = Accueil(self.screen, self.manager)
            elif self._btn_solo.collidepoint(mp):
                audio.play_sfx('hover')
                from src.Cynthia.character_select import CharacterSelect
                self.manager.scene = CharacterSelect(self.screen, self.manager)
            elif self._btn_multi.collidepoint(mp):
                audio.play_sfx('hover')
                from src.Cynthia.multi_lobby import MultiLobby
                self.manager.scene = MultiLobby(self.screen, self.manager)

    def update(self, dt=0):
        pass

    def draw(self):
        w, h = self.screen.get_size()
        self.screen.fill(DARK)

        self._btn_back.topleft = (18, 18)
        pygame.draw.rect(self.screen, DARK_BTN, self._btn_back, border_radius=10)
        pygame.draw.rect(self.screen, GOLD,     self._btn_back, 2, border_radius=10)
        back_txt = self.font_hint.render("< Retour", True, GOLD)
        self.screen.blit(back_txt, back_txt.get_rect(center=self._btn_back.center))

        title = self.font_title.render("Mode de jeu", True, GOLD)
        self.screen.blit(title, title.get_rect(midtop=(w // 2, 24)))

        line_y = 24 + self.font_title.get_height() + 10
        pygame.draw.line(self.screen, (70, 60, 45),
                         (w // 2 - 160, line_y), (w // 2 + 160, line_y), 1)

        gap      = 28
        total_h  = self._btn_solo.height * 2 + gap
        start_y  = (h - total_h) // 2

        self._btn_solo.midtop  = (w // 2, start_y)
        self._btn_multi.midtop = (w // 2, start_y + self._btn_solo.height + gap)

        for btn, label, desc, available in [
            (self._btn_solo,  'Solo',        'Jouer seul',              True),
            (self._btn_multi, 'Multijoueur', 'Jouer en ligne',      True),
        ]:
            mp = pygame.mouse.get_pos()
            hovered = btn.collidepoint(mp) and available
            bg_col  = (60, 50, 38) if hovered else DARK_BTN
            border  = GOLD if available else (80, 70, 55)
            txt_col = GOLD if available else (100, 90, 70)

            shadow = pygame.Surface((btn.width + 8, btn.height + 8), pygame.SRCALPHA)
            shadow.fill((0, 0, 0, 90))
            self.screen.blit(shadow, (btn.x - 4, btn.y + 6))

            pygame.draw.rect(self.screen, bg_col,   btn, border_radius=14)
            pygame.draw.rect(self.screen, border,   btn, 2, border_radius=14)

            lbl = self.font_label.render(label, True, txt_col)
            self.screen.blit(lbl, lbl.get_rect(center=(btn.centerx, btn.centery - 8)))

            sub = self.font_desc.render(desc, True, (120, 110, 90) if not available else GREY)
            self.screen.blit(sub, sub.get_rect(center=(btn.centerx, btn.centery + 18)))

        hint = pygame.font.Font(None, 24).render("Echap : retour", True, (70, 62, 48))
        self.screen.blit(hint, hint.get_rect(midbottom=(w // 2, h - 14)))
