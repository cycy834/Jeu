import math
import pygame

_sprite = None


def _load_sprite():
    global _sprite
    if _sprite is not None:
        return _sprite
    try:
        raw = pygame.image.load('assets/images/camera2_design.png').convert_alpha()
        _sprite = pygame.transform.scale(raw, (88, 54))
    except Exception as e:
        print(f'[Camera] sprite manquant : {e}')
        _sprite = False
    return _sprite


class Camera:
    def __init__(self, x, y, detection_range=420, alert_time=3.0,
                 half_fov=28, sweep_amp=22, sweep_speed=30):
        self.pos          = pygame.Vector2(x, y)
        self.range        = detection_range
        self.alert_time   = alert_time
        self.half_fov     = half_fov
        self.sweep_amp    = sweep_amp
        self.sweep_speed  = sweep_speed
        self.state        = 'SURVEILLANCE'
        self.timer        = 0.0
        self.sweep_t      = 0.0
        self.center_angle = 90.0

    def _in_cone(self, player_pos):
        dx   = player_pos.x - self.pos.x
        dy   = player_pos.y - self.pos.y
        dist = math.hypot(dx, dy)
        if dist > self.range:
            return False
        if dist == 0:
            return True
        ca    = math.radians(self.center_angle)
        cos_a = (dx * math.cos(ca) + dy * math.sin(ca)) / dist
        return cos_a > math.cos(math.radians(self.half_fov))

    def update(self, player_pos, dt):
        self.sweep_t      += dt * self.sweep_speed
        self.center_angle  = 90.0 + self.sweep_amp * math.sin(math.radians(self.sweep_t))

        if self._in_cone(player_pos):
            self.timer += dt
            if self.timer >= self.alert_time:
                self.state = 'ALERT'
            elif self.timer >= self.alert_time * 0.4:
                self.state = 'WARNING'
            else:
                self.state = 'DETECTED'
        else:
            self.timer = 0.0
            self.state = 'SURVEILLANCE'
        return self.state == 'ALERT'

    def _cone_color(self):
        if self.state == 'SURVEILLANCE':
            return (255, 230, 60, 40)
        progress = min(1.0, self.timer / self.alert_time)
        r = 255
        g = int(200 * (1.0 - progress))
        b = 0
        a = int(50 + 70 * progress)
        return (r, g, b, a)

    def draw(self, screen):
        x, y = int(self.pos.x), int(self.pos.y)

        # --- Cône ---
        # On étend le range visuel jusqu'au bas du canvas (479) depuis y
        visual_range = max(self.range, 479 - y + 20)
        r = int(visual_range)

        cone_color = self._cone_color()
        surf_w = r * 2 + 4
        surf_h = r * 2 + 4
        cone_surf = pygame.Surface((surf_w, surf_h), pygame.SRCALPHA)
        ox, oy = r + 2, r + 2
        a_start = self.center_angle - self.half_fov
        a_end   = self.center_angle + self.half_fov
        pts = [(ox, oy)]
        for i in range(30):
            a = math.radians(a_start + (a_end - a_start) * i / 29)
            pts.append((ox + math.cos(a) * r, oy + math.sin(a) * r))
        pygame.draw.polygon(cone_surf, cone_color, pts)
        screen.blit(cone_surf, (x - r - 2, y - r - 2))

        # --- Barre de progression ---
        if self.state != 'SURVEILLANCE':
            progress = min(1.0, self.timer / self.alert_time)
            bar_w    = int(60 * progress)
            bar_col  = (255, int(180 * (1 - progress)), 0)
            bar_y    = y - 16
            pygame.draw.rect(screen, (40, 40, 40), (x - 30, bar_y, 60, 7), border_radius=3)
            if bar_w > 0:
                pygame.draw.rect(screen, bar_col,
                                 (x - 30, bar_y, bar_w, 7), border_radius=3)

        # --- Sprite ---
        sprite = _load_sprite()
        if sprite:
            rect = sprite.get_rect(midbottom=(x, y + 12))
            screen.blit(sprite, rect)
        else:
            col = (255, 40, 40) if self.state == 'ALERT' else (80, 140, 255)
            pygame.draw.rect(screen, col, (x - 20, y - 14, 40, 28), border_radius=4)

    def reset(self):
        self.state        = 'SURVEILLANCE'
        self.timer        = 0.0
        self.sweep_t      = 0.0
        self.center_angle = 90.0
