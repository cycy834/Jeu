import math
import random
import pygame

_sprite_r = None
_sprite_l = None
_FONT     = None

_GRAVITY  = 0.5
_FLOOR_Y  = 479 - 140   # 339

_SPRITE_W = 90
_SPRITE_H = 135


def _load_sprites():
    global _sprite_r, _sprite_l
    if _sprite_r is not None:
        return _sprite_r, _sprite_l
    try:
        img      = pygame.image.load('assets/images/policier_design.png').convert_alpha()
        _sprite_r = pygame.transform.scale(img, (_SPRITE_W, _SPRITE_H))
        _sprite_l = pygame.transform.flip(_sprite_r, True, False)
    except Exception as e:
        print(f'[Policier] sprite manquant : {e}')
        _sprite_r = False
        _sprite_l = False
    return _sprite_r, _sprite_l


def _get_font():
    global _FONT
    if _FONT is None:
        _FONT = pygame.font.Font(None, 26)
    return _FONT


_DIAL_PATROL = ['Zzz...', 'Ronde normale...', 'Tout est calme.', 'Didier veille.']
_DIAL_SLEEP  = ['Zzz...', '...zzz', 'Zzz...']
_DIAL_ALERT  = ['Hmm ?', 'Il y a quelqu un ?', 'Qui est la ?', 'Didier a vu quelque chose !']
_DIAL_CHASE  = ['Halte ! Didier est la !', 'Stop !', 'Je vous vois !', 'Arretez-vous !']
_DIAL_LOST   = ['Ou est-il ?', 'Didier ne se laisse pas avoir...', 'Bizarre...']


class Policier:
    """
    3 etats : PATROL → ALERT → CHASE
    2 detecteurs : cone de vision + cercle de proximite
    Esquive : saut > 55 px au-dessus du policier = capture suspendue
    """

    PATROL = 'PATROL'
    ALERT  = 'ALERT'
    CHASE  = 'CHASE'

    _SLEEP_CHANCE    = 0.001
    _SLEEP_DURATION  = 180
    _DIALOG_INTERVAL = 200

    def __init__(self, x, y, patrol_points,
                 speed          = 1.0,
                 chase_mult     = 1.8,
                 cone_range     = 150,
                 cone_angle     = 60,
                 proximity_range= 70,
                 alert_time     = 1.2,
                 chase_memory   = 4.0,
                 capture_time   = 2.0):

        self.start_pos        = pygame.Vector2(x, _FLOOR_Y)
        self.pos              = pygame.Vector2(x, _FLOOR_Y)
        self.speed            = speed
        self.chase_speed      = speed * chase_mult
        self.cone_range       = cone_range
        self.cone_angle       = cone_angle
        self.proximity_range  = proximity_range
        self.alert_time       = alert_time
        self.chase_memory     = chase_memory
        self.capture_time     = capture_time
        self.capture_distance = 62

        self.patrol_points    = patrol_points
        self.current_point    = 0
        self.state            = self.PATROL
        self.facing_left      = False

        self.alert_timer      = 0.0
        self.memory_timer     = 0.0
        self.capture_timer    = 0.0

        self.width            = _SPRITE_W
        self.height           = _SPRITE_H
        self.sleep_timer      = 0
        self.dialog_text      = ''
        self.dialog_timer     = 0
        self._next_dialog     = random.randint(60, self._DIALOG_INTERVAL)
        self.vel_y            = 0

    # ------------------------------------------------------------------ #
    #  Detection                                                           #
    # ------------------------------------------------------------------ #

    def _in_cone(self, player_pos):
        dx   = player_pos.x - self.pos.x
        dy   = player_pos.y - self.pos.y
        dist = math.hypot(dx, dy)
        if dist > self.cone_range:
            return False
        if dist == 0:
            return True
        fx    = -1.0 if self.facing_left else 1.0
        cos_a = (dx * fx) / dist   # fy=0, cone is horizontal
        return cos_a >= math.cos(math.radians(self.cone_angle / 2))

    def _in_proximity(self, player_pos):
        return self.pos.distance_to(player_pos) < self.proximity_range

    def _detects(self, player_pos):
        if self.sleep_timer > 0:
            return self._in_proximity(player_pos)   # endormi : cone eteint
        return self._in_cone(player_pos) or self._in_proximity(player_pos)

    # ------------------------------------------------------------------ #
    #  Capture (jump-evasion built-in)                                    #
    # ------------------------------------------------------------------ #

    def _catchable(self, player_pos):
        horiz = abs(self.pos.x - player_pos.x)
        vert  = self.pos.y - player_pos.y   # positif si joueur AU-DESSUS
        return horiz < self.capture_distance and vert < 55

    # ------------------------------------------------------------------ #
    #  Movement                                                            #
    # ------------------------------------------------------------------ #

    def _patrol_step(self):
        target = self.patrol_points[self.current_point]
        dx     = target.x - self.pos.x
        if abs(dx) > self.speed:
            self.pos.x      += self.speed if dx > 0 else -self.speed
            self.facing_left = dx < 0
        else:
            self.pos.x = target.x
            self.current_point = (self.current_point + 1) % len(self.patrol_points)

    def _chase_step(self, player_pos):
        dx = player_pos.x - self.pos.x
        if abs(dx) > 0:
            self.pos.x      += self.chase_speed if dx > 0 else -self.chase_speed
            self.facing_left = dx < 0

    def _say(self, lines, dur=90):
        self.dialog_text  = random.choice(lines)
        self.dialog_timer = dur

    # ------------------------------------------------------------------ #
    #  Main update                                                         #
    # ------------------------------------------------------------------ #

    def update(self, player_pos, dt):
        # Gravity
        self.vel_y += _GRAVITY
        self.pos.y += self.vel_y
        if self.pos.y >= _FLOOR_Y:
            self.pos.y = _FLOOR_Y
            self.vel_y = 0

        if self.dialog_timer > 0:
            self.dialog_timer -= 1

        detected = self._detects(player_pos)

        # ---- PATROL -------------------------------------------------- #
        if self.state == self.PATROL:
            if self.sleep_timer > 0:
                self.sleep_timer -= 1
                if self.sleep_timer % 60 == 0:
                    self._say(_DIAL_SLEEP, 55)
                if detected:                              # reveille en sursaut
                    self.sleep_timer = 0
                    self.state       = self.ALERT
                    self.alert_timer = 0.0
                    self._say(_DIAL_ALERT, 100)
            else:
                self._patrol_step()
                if random.random() < self._SLEEP_CHANCE:
                    self.sleep_timer = self._SLEEP_DURATION
                    self._say(_DIAL_SLEEP, 70)
                elif detected:
                    self.state       = self.ALERT
                    self.alert_timer = 0.0
                    self._say(_DIAL_ALERT, 100)
                else:
                    self._next_dialog -= 1
                    if self._next_dialog <= 0:
                        self._say(_DIAL_PATROL, 80)
                        self._next_dialog = random.randint(80, self._DIALOG_INTERVAL)

        # ---- ALERT ---------------------------------------------------- #
        elif self.state == self.ALERT:
            # Se tourne vers le joueur
            self.facing_left = player_pos.x < self.pos.x

            if detected:
                self.alert_timer += dt
                if self.alert_timer >= self.alert_time:
                    self.state         = self.CHASE
                    self.memory_timer  = 0.0
                    self.capture_timer = 0.0
                    self._say(_DIAL_CHASE, 80)
            else:
                # Joueur disparu avant la fin de l'alerte → retour
                self.alert_timer -= dt * 0.8
                if self.alert_timer <= 0.0:
                    self.alert_timer = 0.0
                    self.state       = self.PATROL
                    self._say(_DIAL_PATROL, 70)

        # ---- CHASE ---------------------------------------------------- #
        elif self.state == self.CHASE:
            self._chase_step(player_pos)
            if self.dialog_timer == 0:
                self._say(_DIAL_CHASE, 70)

            if detected:
                self.memory_timer = 0.0
            else:
                self.memory_timer += dt
                if self.memory_timer >= self.chase_memory:
                    self.state         = self.PATROL
                    self.memory_timer  = 0.0
                    self.capture_timer = 0.0
                    self._say(_DIAL_LOST, 80)
                    return False

            # Capture (jump-evasion : vert >= 55 → pas de capture)
            if self._catchable(player_pos):
                self.capture_timer += dt
                if self.capture_timer >= self.capture_time:
                    self.capture_timer = 0.0
                    return True
            else:
                self.capture_timer = max(0.0, self.capture_timer - dt * 0.6)

        return False

    # ------------------------------------------------------------------ #
    #  Draw                                                                #
    # ------------------------------------------------------------------ #

    def draw(self, screen):
        x = int(self.pos.x)
        y = int(self.pos.y)

        # --- Cercle de proximité (transparent) ---
        pr  = self.proximity_range
        if self.state == self.CHASE:
            pcol = (255, 60, 60, 38)
        elif self.state == self.ALERT:
            pcol = (255, 180, 0, 35)
        else:
            pcol = (255, 200, 100, 20)
        psurf = pygame.Surface((pr * 2, pr * 2), pygame.SRCALPHA)
        pygame.draw.circle(psurf, pcol, (pr, pr), pr)
        screen.blit(psurf, (x - pr, y + _SPRITE_H // 2 - pr))
        pygame.draw.circle(screen, pcol[:3],
                           (x, y + _SPRITE_H // 2), pr, 1)

        # --- Cône de vision ---
        if self.state == self.PATROL:
            ccol = (255, 220, 60, 30)
        elif self.state == self.ALERT:
            ccol = (255, 140, 0, 55)
        else:
            ccol = (255, 50, 50, 65)

        cx      = -1.0 if self.facing_left else 1.0
        a_center = math.atan2(0.0, cx)
        half    = math.radians(self.cone_angle / 2)
        cr      = self.cone_range
        eye_x   = x
        eye_y   = y + 18          # hauteur des yeux

        csurf = pygame.Surface((cr * 2 + 4, cr * 2 + 4), pygame.SRCALPHA)
        ox, oy = cr + 2, cr + 2
        pts = [(ox, oy)]
        for i in range(21):
            a = a_center - half + (2 * half) * i / 20
            pts.append((ox + math.cos(a) * cr, oy + math.sin(a) * cr))
        pygame.draw.polygon(csurf, ccol, pts)
        screen.blit(csurf, (eye_x - cr - 2, eye_y - cr - 2))

        # --- Sprite ---
        sprite_r, sprite_l = _load_sprites()
        if sprite_r:
            img = sprite_l if self.facing_left else sprite_r
            screen.blit(img, (x - _SPRITE_W // 2, y))

            head_y = y - 10
            if self.state == self.CHASE:
                pygame.draw.circle(screen, (255, 0, 0), (x, head_y), 7)
            elif self.state == self.ALERT:
                pygame.draw.circle(screen, (255, 200, 0), (x, head_y), 7)
                fnt = _get_font()
                q   = fnt.render('?', True, (255, 200, 0))
                screen.blit(q, (x - q.get_width() // 2, head_y - 16))
            elif self.sleep_timer > 0:
                zs = _get_font().render('Zzz', True, (180, 220, 255))
                screen.blit(zs, (x + _SPRITE_W // 2 + 2, y))
        else:
            color = (255, 50, 50)  if self.state == self.CHASE  else \
                    (255, 200, 0)  if self.state == self.ALERT  else \
                    (200, 100, 100)
            pygame.draw.rect(screen, color,
                             pygame.Rect(x - _SPRITE_W // 2, y, _SPRITE_W, _SPRITE_H))

        # --- Barre de capture (danger) ---
        if self.state == self.CHASE and self.capture_timer > 0:
            progress = min(1.0, self.capture_timer / self.capture_time)
            bw       = int(50 * progress)
            bar_col  = (255, int(180 * (1.0 - progress)), 0)
            pygame.draw.rect(screen, (30, 30, 30), (x - 25, y - 20, 50, 6), border_radius=3)
            if bw > 0:
                pygame.draw.rect(screen, bar_col,
                                 (x - 25, y - 20, bw, 6), border_radius=3)

        # --- Bulle de dialogue ---
        if self.dialog_timer > 0 and self.dialog_text:
            fnt   = _get_font()
            alpha = min(255, self.dialog_timer * 5)
            txt   = fnt.render(self.dialog_text, True, (255, 255, 200))
            bw2, bh = txt.get_width() + 12, txt.get_height() + 8
            bx  = x - bw2 // 2
            by  = y - bh - 14
            bbl = pygame.Surface((bw2, bh), pygame.SRCALPHA)
            bbl.fill((30, 28, 24, min(210, alpha)))
            pygame.draw.rect(bbl, (200, 180, 100, alpha),
                             (0, 0, bw2, bh), 1, border_radius=6)
            screen.blit(bbl, (bx, by))
            txt.set_alpha(alpha)
            screen.blit(txt, (bx + 6, by + 4))

    # ------------------------------------------------------------------ #
    #  Reset                                                               #
    # ------------------------------------------------------------------ #

    def reset(self):
        self.pos           = pygame.Vector2(self.start_pos.x, self.start_pos.y)
        self.state         = self.PATROL
        self.current_point = 0
        self.facing_left   = False
        self.alert_timer   = 0.0
        self.memory_timer  = 0.0
        self.capture_timer = 0.0
        self.sleep_timer   = 0
        self.dialog_text   = ''
        self.dialog_timer  = 0
        self.vel_y         = 0
        self._next_dialog  = random.randint(60, self._DIALOG_INTERVAL)
