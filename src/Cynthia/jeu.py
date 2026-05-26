import pygame
from src.Benji.mouvements_v2 import GameSession

GOLD     = (196, 166, 114)
DARK     = (28, 24, 20)
DARK_BTN = (45, 38, 32)
GREEN_OK = (0, 210, 80)
RED_ERR  = (220, 60, 60)
MAX_LEVEL = 5

_LEAVE_FRAMES = 90


class Jeu:
    def __init__(self, screen, manager, character=None, level_id=1):
        self.screen    = screen
        self.manager   = manager
        self.character = character

        self.font      = pygame.font.Font(None, 34)
        self.font_btn  = pygame.font.Font(None, 30)
        self.font_hint = pygame.font.Font(None, 24)
        self.font_big  = pygame.font.Font(None, 48)

        self.back_rect  = pygame.Rect(40, 40, 190, 65)
        self._btn_next  = pygame.Rect(0, 0, 310, 58)
        self._btn_menu  = pygame.Rect(0, 0, 210, 58)

        net_cfg = getattr(manager, 'net_config', None)
        self._is_host     = bool(net_cfg and net_cfg.get('is_host'))
        self._server_addr = ''
        if self._is_host:
            from src.Joaquim.network.server_runner import get_local_ip, PORT
            self._server_addr = f'{get_local_ip()}:{PORT}'

        self._leaving     = False
        self._leave_timer = 0
        self._pending_nav = None

        self.session = GameSession(
            screen, manager, character=character, level_id=level_id,
            net_uri=net_cfg['uri']    if net_cfg else None,
            player_name=net_cfg['name'] if net_cfg else 'Joueur',
        )

    def _do_go_menu(self):
        if hasattr(self.manager, 'net_config'):
            self.manager.net_config = None
        from src.Cynthia.accueil import Accueil
        self.manager.scene = Accueil(self.screen, self.manager)

    def _do_go_next(self):
        next_id = self.session.level_id + 1
        if next_id > MAX_LEVEL:
            self._do_go_menu()
        else:
            self.manager.scene = Jeu(
                self.screen, self.manager,
                character=self.character, level_id=next_id)

    def _go_menu(self):
        if self._is_host:
            self._start_leaving('menu')
        else:
            self._do_go_menu()

    def _go_next(self):
        if self._is_host:
            self._start_leaving('next')
        else:
            self._do_go_next()

    def _start_leaving(self, dest):
        if self._leaving:
            return
        self._leaving     = True
        self._leave_timer = _LEAVE_FRAMES
        self._pending_nav = dest

    def handle_event(self, event):
        if self._leaving:
            return
        if self.session.mode == 'victoire':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mp = event.pos
                if self._btn_next.collidepoint(mp):
                    self._go_next()
                    return
                if self._btn_menu.collidepoint(mp):
                    self._go_menu()
                    return
            return
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                self._go_menu()
                return
        self.session.handle_event(event)

    def update(self, dt=0):
        if self._leaving:
            self._leave_timer -= 1
            if self._leave_timer <= 0:
                self._leaving = False
                if self._pending_nav == 'menu':
                    self._do_go_menu()
                else:
                    self._do_go_next()
            return
        self.session.update(dt)

    def draw(self):
        self.session.draw()
        w, h = self.screen.get_size()
        cx   = w // 2

        if self._leaving:
            progress = self._leave_timer / _LEAVE_FRAMES
            alpha    = int(200 * (1.0 - progress))
            overlay  = pygame.Surface((w, h), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, alpha))
            self.screen.blit(overlay, (0, 0))
            txt_alpha = int(255 * min(1.0, (1.0 - progress) * 3))
            msg = self.font_big.render('Serveur désactivé', True, RED_ERR)
            msg.set_alpha(txt_alpha)
            self.screen.blit(msg, msg.get_rect(center=(cx, h // 2)))
            return

        if self.session.mode == 'victoire':
            has_next = self.session.level_id < MAX_LEVEL
            if has_next:
                self._btn_next.midright = (cx - 12, h // 2 + 80)
                self._btn_menu.midleft  = (cx + 12, h // 2 + 80)
            else:
                self._btn_next.width  = 0
                self._btn_menu.center = (cx, h // 2 + 80)

            for btn, label, active in [
                (self._btn_next, 'Mission suivante', has_next),
                (self._btn_menu, 'Retour au menu',   True),
            ]:
                if not active or btn.width == 0:
                    continue
                pygame.draw.rect(self.screen, DARK_BTN, btn, border_radius=12)
                pygame.draw.rect(self.screen, GOLD,     btn, 2, border_radius=12)
                t = self.font_btn.render(label, True, GOLD)
                self.screen.blit(t, t.get_rect(center=btn.center))
        else:
            pygame.draw.rect(self.screen, DARK_BTN, self.back_rect, border_radius=8)
            pygame.draw.rect(self.screen, GOLD, self.back_rect, 2, border_radius=8)
            self.screen.blit(
                self.font.render('Retour', True, GOLD),
                self.font.render('Retour', True, GOLD).get_rect(center=self.back_rect.center))

        if self._is_host:
            ix, iy = 18, 120
            pygame.draw.circle(self.screen, GREEN_OK, (ix, iy), 6)
            lbl = self.font_hint.render(f'Serveur actif : {self._server_addr}', True, GREEN_OK)
            self.screen.blit(lbl, (ix + 14, iy - 8))
