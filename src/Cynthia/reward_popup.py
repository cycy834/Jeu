import math
import pygame

GOLD    = (220, 190, 100)
DARK    = (20, 16, 12)
WHITE   = (255, 255, 255)
SHINE   = (255, 240, 160)


class RewardPopup:
    DURATION = 240

    def __init__(self, bijou_name):
        self.bijou_name = bijou_name
        self.timer      = self.DURATION
        self.font_title = pygame.font.Font(None, 52)
        self.font_bijou = pygame.font.Font(None, 38)
        self.font_hint  = pygame.font.Font(None, 26)
        self._particles = [
            {'x': 0, 'y': 0, 'vx': 0, 'vy': 0, 'life': 0}
            for _ in range(20)
        ]
        self._spawn_particles()

    def _spawn_particles(self):
        import random
        for p in self._particles:
            p['x']    = 0
            p['y']    = 0
            p['vx']   = (random.random() - 0.5) * 4
            p['vy']   = -(random.random() * 3 + 1)
            p['life'] = random.randint(40, 100)

    def is_done(self):
        return self.timer <= 0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE, pygame.K_ESCAPE):
            self.timer = 0
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.timer = 0

    def update(self, dt=None):
        self.timer -= 1
        for p in self._particles:
            if p['life'] > 0:
                p['x']  += p['vx']
                p['y']  += p['vy']
                p['vy'] += 0.1
                p['life'] -= 1

    def draw(self, screen):
        if self.timer <= 0:
            return
        sw, sh = screen.get_size()
        alpha  = min(255, self.timer * 4) if self.timer < 60 else 255

        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        t    = (self.DURATION - self.timer) / self.DURATION
        scale = 1.0 + 0.06 * math.sin(t * math.pi * 6) * max(0, 1 - t * 3)
        bw, bh = int(480 * scale), int(220 * scale)
        bx, by = sw // 2 - bw // 2, sh // 2 - bh // 2

        box = pygame.Surface((bw, bh), pygame.SRCALPHA)
        pygame.draw.rect(box, (*DARK, 230), (0, 0, bw, bh), border_radius=18)
        pygame.draw.rect(box, (*GOLD, 200), (0, 0, bw, bh), 3, border_radius=18)
        screen.blit(box, (bx, by))

        cx, cy = sw // 2, sh // 2

        for p in self._particles:
            if p['life'] > 0:
                px = int(cx + p['x'] * 40)
                py = int(cy + p['y'] * 30)
                r  = max(1, int(p['life'] / 20))
                col = SHINE if p['life'] > 50 else GOLD
                pygame.draw.circle(screen, col, (px, py), r)

        gem_r = int(28 * scale)
        gem_x, gem_y = cx, by + int(50 * scale)
        pts = []
        for i in range(6):
            a = math.radians(60 * i - 90)
            pts.append((gem_x + int(gem_r * math.cos(a)), gem_y + int(gem_r * math.sin(a))))
        pygame.draw.polygon(screen, GOLD, pts)
        pygame.draw.polygon(screen, SHINE, pts, 2)

        title_surf = self.font_title.render("Bravo ! Vous avez vole :", True, GOLD)
        screen.blit(title_surf, title_surf.get_rect(center=(cx, by + int(100 * scale))))

        bijou_surf = self.font_bijou.render(self.bijou_name, True, WHITE)
        screen.blit(bijou_surf, bijou_surf.get_rect(center=(cx, by + int(148 * scale))))

        hint = self.font_hint.render("Clic ou Entree pour continuer", True, (150, 150, 150))
        screen.blit(hint, hint.get_rect(midbottom=(cx, by + bh - 10)))
