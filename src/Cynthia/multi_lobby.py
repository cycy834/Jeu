import socket
import pygame
from src.audio import audio_manager as audio

GOLD     = (196, 166, 114)
DARK     = (28, 24, 20)
DARK_BTN = (45, 38, 32)
WHITE    = (255, 255, 255)
GREY     = (160, 160, 160)
PORT     = 8765


def _local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return '127.0.0.1'


def _make_uri(text):
    text = text.strip()
    if text.startswith('ws://') or text.startswith('wss://'):
        return text
    if ':' in text:
        return f'ws://{text}'
    return f'ws://{text}:{PORT}'


class _TextInput:
    def __init__(self, placeholder='', max_len=50):
        self.text        = ''
        self.placeholder = placeholder
        self.max_len     = max_len
        self.active      = False

    def handle_key(self, event):
        if not self.active:
            return
        if event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
        elif event.unicode and event.unicode.isprintable() and len(self.text) < self.max_len:
            self.text += event.unicode

    def draw(self, screen, rect, font):
        border = GOLD if self.active else (80, 70, 55)
        pygame.draw.rect(screen, (35, 30, 24), rect, border_radius=8)
        pygame.draw.rect(screen, border, rect, 2, border_radius=8)
        display = self.text + ('|' if self.active else '')
        col  = WHITE if self.text else (80, 70, 60)
        txt  = font.render(display or self.placeholder, True, col if self.text or self.active else (70, 62, 48))
        screen.blit(txt, txt.get_rect(midleft=(rect.x + 12, rect.centery)))


class MultiLobby:
    def __init__(self, screen, manager):
        self.screen  = screen
        self.manager = manager
        self.state   = 'choice'
        self._local_ip = _local_ip()

        self.font_title = pygame.font.Font(None, 68)
        self.font_label = pygame.font.Font(None, 46)
        self.font_body  = pygame.font.Font(None, 30)
        self.font_hint  = pygame.font.Font(None, 24)
        self.font_ip    = pygame.font.Font(None, 32)

        self._btn_host   = pygame.Rect(0, 0, 280, 68)
        self._btn_join   = pygame.Rect(0, 0, 280, 68)
        self._btn_back   = pygame.Rect(0, 0, 120, 40)
        self._btn_action = pygame.Rect(0, 0, 210, 52)

        self._input_name = _TextInput('Votre nom', max_len=20)
        self._input_ip   = _TextInput(f'Ex : 192.168.1.42', max_len=50)
        self._input_name.text = 'Joueur'

        self._rect_name  = pygame.Rect(0, 0, 320, 42)
        self._rect_ip    = pygame.Rect(0, 0, 320, 42)

        self._status     = ''

    def _go_back(self):
        audio.play_sfx('hover')
        if self.state == 'choice':
            from src.Cynthia.mode_select import ModeSelect
            self.manager.scene = ModeSelect(self.screen, self.manager)
        else:
            self.state = 'choice'
            self._status = ''

    def _start_host(self):
        from src.Joaquim.network.server_runner import start as start_server
        start_server()
        name = self._input_name.text.strip() or 'Joueur'
        self.manager.net_config = {
            'uri':     f'ws://127.0.0.1:{PORT}',
            'name':    name,
            'is_host': True,
        }
        audio.play_sfx('hover')
        from src.Cynthia.character_select import CharacterSelect
        self.manager.scene = CharacterSelect(self.screen, self.manager)

    def _start_join(self):
        ip_text = self._input_ip.text.strip()
        if not ip_text:
            self._status = 'Entrez l\'adresse du serveur'
            return
        name = self._input_name.text.strip() or 'Joueur'
        self.manager.net_config = {
            'uri':     _make_uri(ip_text),
            'name':    name,
            'is_host': False,
        }
        audio.play_sfx('hover')
        from src.Cynthia.character_select import CharacterSelect
        self.manager.scene = CharacterSelect(self.screen, self.manager)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self._go_back()
                return
            if self.state == 'host':
                self._input_name.handle_key(event)
            elif self.state == 'join':
                self._input_name.handle_key(event)
                self._input_ip.handle_key(event)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mp = pygame.mouse.get_pos()

            if self._btn_back.collidepoint(mp):
                self._go_back()
                return

            if self.state == 'choice':
                if self._btn_host.collidepoint(mp):
                    audio.play_sfx('hover')
                    self.state = 'host'
                elif self._btn_join.collidepoint(mp):
                    audio.play_sfx('hover')
                    self.state = 'join'

            elif self.state == 'host':
                if self._rect_name.collidepoint(mp):
                    self._input_name.active = True
                else:
                    self._input_name.active = False
                if self._btn_action.collidepoint(mp):
                    self._start_host()

            elif self.state == 'join':
                self._input_name.active = self._rect_name.collidepoint(mp)
                self._input_ip.active   = self._rect_ip.collidepoint(mp)
                if self._btn_action.collidepoint(mp):
                    self._start_join()

    def update(self, dt=0):
        pass

    def draw(self):
        w, h = self.screen.get_size()
        cx   = w // 2
        self.screen.fill(DARK)

        self._btn_back.topleft = (18, 18)
        pygame.draw.rect(self.screen, DARK_BTN, self._btn_back, border_radius=10)
        pygame.draw.rect(self.screen, GOLD,     self._btn_back, 2,  border_radius=10)
        self.screen.blit(
            self.font_hint.render('< Retour', True, GOLD),
            self.font_hint.render('< Retour', True, GOLD).get_rect(center=self._btn_back.center))

        title = self.font_title.render('Multijoueur', True, GOLD)
        self.screen.blit(title, title.get_rect(midtop=(cx, 20)))
        line_y = 20 + title.get_height() + 8
        pygame.draw.line(self.screen, (70, 60, 45), (cx - 140, line_y), (cx + 140, line_y), 1)

        if self.state == 'choice':
            self._draw_choice(cx, h)
        elif self.state == 'host':
            self._draw_host(cx, h)
        elif self.state == 'join':
            self._draw_join(cx, h)

        if self._status:
            st = self.font_body.render(self._status, True, (220, 80, 80))
            self.screen.blit(st, st.get_rect(midbottom=(cx, h - 14)))

    def _draw_choice(self, cx, h):
        gap     = 24
        total_h = self._btn_host.height * 2 + gap
        sy      = (h - total_h) // 2

        self._btn_host.midtop = (cx, sy)
        self._btn_join.midtop = (cx, sy + self._btn_host.height + gap)

        for btn, label, sub in [
            (self._btn_host, 'Héberger', 'Créer une partie'),
            (self._btn_join, 'Rejoindre', 'Entrer chez un ami'),
        ]:
            hovered = btn.collidepoint(pygame.mouse.get_pos())
            bg = (60, 50, 38) if hovered else DARK_BTN
            sh = pygame.Surface((btn.w + 8, btn.h + 8), pygame.SRCALPHA)
            sh.fill((0, 0, 0, 90))
            self.screen.blit(sh, (btn.x - 4, btn.y + 6))
            pygame.draw.rect(self.screen, bg,   btn, border_radius=14)
            pygame.draw.rect(self.screen, GOLD, btn, 2, border_radius=14)
            self.screen.blit(
                self.font_label.render(label, True, GOLD),
                self.font_label.render(label, True, GOLD).get_rect(center=(btn.centerx, btn.centery - 8)))
            self.screen.blit(
                self.font_body.render(sub, True, GREY),
                self.font_body.render(sub, True, GREY).get_rect(center=(btn.centerx, btn.centery + 18)))

    def _draw_host(self, cx, h):
        cy = h // 2 - 60

        ip_lbl = self.font_body.render('Partagez cette adresse :', True, GREY)
        self.screen.blit(ip_lbl, ip_lbl.get_rect(midtop=(cx, cy - 60)))
        ip_val = self.font_ip.render(f'{self._local_ip}:{PORT}', True, GOLD)
        self.screen.blit(ip_val, ip_val.get_rect(midtop=(cx, cy - 34)))
        pygame.draw.line(self.screen, (70, 60, 45),
                         (cx - 160, cy - 4), (cx + 160, cy - 4), 1)

        n_lbl = self.font_body.render('Votre nom :', True, GREY)
        self.screen.blit(n_lbl, n_lbl.get_rect(midtop=(cx, cy + 8)))
        self._rect_name.midtop = (cx, cy + 34)
        self._input_name.draw(self.screen, self._rect_name, self.font_body)

        self._btn_action.midtop = (cx, cy + 92)
        hov = self._btn_action.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(self.screen, (60,50,38) if hov else DARK_BTN, self._btn_action, border_radius=12)
        pygame.draw.rect(self.screen, GOLD, self._btn_action, 2, border_radius=12)
        lbl = self.font_label.render('Démarrer', True, GOLD)
        self.screen.blit(lbl, lbl.get_rect(center=self._btn_action.center))

    def _draw_join(self, cx, h):
        cy = h // 2 - 80

        a_lbl = self.font_body.render('Adresse du serveur :', True, GREY)
        self.screen.blit(a_lbl, a_lbl.get_rect(midtop=(cx, cy)))
        self._rect_ip.midtop = (cx, cy + 26)
        self._input_ip.draw(self.screen, self._rect_ip, self.font_body)

        n_lbl = self.font_body.render('Votre nom :', True, GREY)
        self.screen.blit(n_lbl, n_lbl.get_rect(midtop=(cx, cy + 80)))
        self._rect_name.midtop = (cx, cy + 106)
        self._input_name.draw(self.screen, self._rect_name, self.font_body)

        self._btn_action.midtop = (cx, cy + 162)
        hov = self._btn_action.collidepoint(pygame.mouse.get_pos())
        pygame.draw.rect(self.screen, (60,50,38) if hov else DARK_BTN, self._btn_action, border_radius=12)
        pygame.draw.rect(self.screen, GOLD, self._btn_action, 2, border_radius=12)
        lbl = self.font_label.render('Rejoindre', True, GOLD)
        self.screen.blit(lbl, lbl.get_rect(center=self._btn_action.center))
