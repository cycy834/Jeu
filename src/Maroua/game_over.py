import pygame
import sys
from src.audio import audio_manager as audio


class Hitbox:
    def __init__(self, rel_x, rel_y, rel_w, rel_h):
        self.rel_x = rel_x; self.rel_y = rel_y
        self.rel_w = rel_w; self.rel_h = rel_h
        self.current_rect = pygame.Rect(0, 0, 0, 0)

    def update_rect(self, bg_rect):
        self.current_rect = pygame.Rect(
            bg_rect.x + self.rel_x * bg_rect.width,
            bg_rect.y + self.rel_y * bg_rect.height,
            self.rel_w * bg_rect.width,
            self.rel_h * bg_rect.height,
        )

    def draw_hover(self, surface, mouse_pos):
        if self.current_rect.collidepoint(mouse_pos):
            ov = pygame.Surface((self.current_rect.width, self.current_rect.height), pygame.SRCALPHA)
            ov.fill((0, 0, 0, 80))
            surface.blit(ov, self.current_rect.topleft)


class GameOver:
    def __init__(self, screen, manager):
        self.screen  = screen
        self.manager = manager

        try:
            self.bg_orig = pygame.image.load('assets/images/Game_over.png').convert()
        except Exception:
            self.bg_orig = pygame.Surface((1280, 720))
            self.bg_orig.fill((20, 0, 0))

        self.btn_play = Hitbox(0.358, 0.655, 0.138, 0.065)
        self.btn_no   = Hitbox(0.510, 0.655, 0.138, 0.065)
        self._update_layout()

    def _update_layout(self):
        w, h = self.screen.get_size()
        iw, ih = self.bg_orig.get_size()
        scale = max(w / iw, h / ih)
        nw, nh = int(iw * scale), int(ih * scale)
        self.scaled_bg = pygame.transform.smoothscale(self.bg_orig, (nw, nh))
        self.bg_rect   = self.scaled_bg.get_rect(center=(w // 2, h // 2))
        self.btn_play.update_rect(self.bg_rect)
        self.btn_no.update_rect(self.bg_rect)

    def handle_event(self, event):
        if event.type == pygame.VIDEORESIZE:
            self._update_layout()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mp = pygame.mouse.get_pos()
            if self.btn_play.current_rect.collidepoint(mp):
                from src.Cynthia.jeu import Jeu
                audio.play_music(audio.MUSIC_CALM)
                self.manager.scene = Jeu(self.screen, self.manager)
            elif self.btn_no.current_rect.collidepoint(mp):
                from src.Cynthia.accueil import Accueil
                audio.play_music(audio.MUSIC_MENU)
                self.manager.scene = Accueil(self.screen, self.manager)

    def update(self, dt=0):
        pass

    def draw(self):
        mp = pygame.mouse.get_pos()
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.scaled_bg, self.bg_rect)
        self.btn_play.draw_hover(self.screen, mp)
        self.btn_no.draw_hover(self.screen, mp)
