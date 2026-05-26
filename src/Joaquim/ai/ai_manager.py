import pygame
from src.Joaquim.ai.camera import Camera
from src.Joaquim.ai.policier import Policier


class AIManager:
    def __init__(self, level_id=1, room_id=1):
        self.level_id = level_id
        self.room_id  = room_id
        self.cameras  = []
        self.policier = []
        self.build_room(level_id, room_id)

    def build_room(self, level_id, room_id):
        self.cameras  = []
        self.policier = []
        V = pygame.Vector2

        # Raccourci : P(x, patrol_pts, speed, chase_mult, cone_r, cone_a,
        #                prox_r, alert_t, memory_t, capture_t)
        def P(x, pts, sp, cm, cr, ca, pr, at, mt, ct):
            return Policier(x, 340, pts,
                            speed=sp, chase_mult=cm,
                            cone_range=cr, cone_angle=ca,
                            proximity_range=pr,
                            alert_time=at,
                            chase_memory=mt,
                            capture_time=ct)

        # penalty=0 : renvoi au départ, pas de vie perdue
        # penalty=1 : vie perdue normalement
        # Toutes les captures → perte de vie (penalty=1 partout)
        # Caméras : detection_range >= 420 pour atteindre le corps du joueur (y~399)
        # half_fov : 26-34° pour une détection fiable
        configs = {
            # ================================================================
            # NIVEAU 1
            # ================================================================
            (1, 1): {
                'penalty': 1,
                'cameras': [Camera(500, 158, detection_range=390, alert_time=4.0,
                                   half_fov=22, sweep_amp=20, sweep_speed=16)],
                'policiers': [],
            },
            (1, 2): {
                'penalty': 1,
                'cameras': [],
                'policiers': [P(900, [V(700,340), V(1200,340)],
                                0.4, 1.5,  90, 45, 100,  2.5, 3.0, 3.0)],
            },
            (1, 3): {
                'penalty': 1,
                'cameras': [Camera(600, 114, detection_range=360, alert_time=3.8,
                                   half_fov=22, sweep_amp=20, sweep_speed=17),
                            Camera(1050, 114, detection_range=360, alert_time=3.8,
                                   half_fov=22, sweep_amp=20, sweep_speed=17)],
                'policiers': [],
            },
            (1, 4): {
                'penalty': 1,
                'cameras': [Camera(400, 100, detection_range=360, alert_time=3.8,
                                   half_fov=22, sweep_amp=20, sweep_speed=16),
                            Camera(1100, 100, detection_range=360, alert_time=3.8,
                                   half_fov=22, sweep_amp=20, sweep_speed=16)],
                'policiers': [P(1000, [V(800,340), V(1300,340)],
                                0.55, 1.6, 120, 52, 115,  2.0, 5.0, 2.8)],
            },
            (1, 5): {
                'penalty': 1,
                'cameras': [Camera(500, 84, detection_range=370, alert_time=3.2,
                                   half_fov=23, sweep_amp=22, sweep_speed=20)],
                'policiers': [P(1100, [V(900,340), V(1400,340)],
                                1.8, 2.4, 220, 66, 165,  0.6, 7.0, 1.0)],
            },

            # ================================================================
            # NIVEAU 2
            # ================================================================
            (2, 1): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=430, alert_time=3.0,
                                   half_fov=22, sweep_amp=22, sweep_speed=28)],
                'policiers': [],
            },
            (2, 2): {
                'penalty': 1,
                'cameras': [],
                'policiers': [P(800, [V(400,340), V(1200,340)],
                                1.0, 1.8, 165, 60, 130,  1.3, 4.0, 2.0)],
            },
            (2, 3): {
                'penalty': 1,
                'cameras': [Camera(700, 60, detection_range=435, alert_time=2.8,
                                   half_fov=23, sweep_amp=22, sweep_speed=28),
                            Camera(1200, 60, detection_range=435, alert_time=2.8,
                                   half_fov=23, sweep_amp=22, sweep_speed=28)],
                'policiers': [P(1100, [V(900,340), V(1400,340)],
                                1.1, 1.8, 175, 62, 135,  1.2, 4.5, 1.9)],
            },
            (2, 4): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=435, alert_time=2.8,
                                   half_fov=23, sweep_amp=22, sweep_speed=28),
                            Camera(1100, 60, detection_range=435, alert_time=2.8,
                                   half_fov=23, sweep_amp=22, sweep_speed=28)],
                'policiers': [P(900, [V(600,340), V(1300,340)],
                                1.2, 2.0, 180, 62, 140,  1.1, 5.0, 1.8)],
            },
            (2, 5): {
                'penalty': 1,
                'cameras': [Camera(600, 60, detection_range=440, alert_time=2.5,
                                   half_fov=24, sweep_amp=23, sweep_speed=30)],
                'policiers': [P(1200, [V(900,340), V(1450,340)],
                                2.4, 2.6, 260, 72, 178,  0.45, 6.0, 0.85)],
            },

            # ================================================================
            # NIVEAU 3
            # ================================================================
            (3, 1): {
                'penalty': 1,
                'cameras': [Camera(500, 60, detection_range=440, alert_time=2.4,
                                   half_fov=24, sweep_amp=24, sweep_speed=32)],
                'policiers': [],
            },
            (3, 2): {
                'penalty': 1,
                'cameras': [],
                'policiers': [P(700, [V(300,340), V(1200,340)],
                                1.3, 2.0, 200, 64, 145,  1.0, 5.0, 1.7)],
            },
            (3, 3): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=445, alert_time=2.3,
                                   half_fov=24, sweep_amp=25, sweep_speed=33),
                            Camera(1200, 60, detection_range=445, alert_time=2.3,
                                   half_fov=24, sweep_amp=25, sweep_speed=33)],
                'policiers': [P(1100, [V(850,340), V(1400,340)],
                                1.4, 2.0, 210, 66, 150,  0.9, 5.0, 1.6)],
            },
            (3, 4): {
                'penalty': 1,
                'cameras': [Camera(300, 60, detection_range=445, alert_time=2.2,
                                   half_fov=24, sweep_amp=26, sweep_speed=34),
                            Camera(1200, 60, detection_range=445, alert_time=2.2,
                                   half_fov=24, sweep_amp=26, sweep_speed=34)],
                'policiers': [P(750, [V(500,340), V(1200,340)],
                                1.6, 2.1, 215, 66, 155,  0.9, 5.5, 1.6)],
            },
            (3, 5): {
                'penalty': 1,
                'cameras': [Camera(700, 60, detection_range=450, alert_time=2.1,
                                   half_fov=25, sweep_amp=26, sweep_speed=35)],
                'policiers': [
                    P(300,  [V(150,340), V(700,340)],   2.8, 2.8, 285, 76, 188,  0.35, 7.0, 0.75),
                    P(1200, [V(950,340), V(1450,340)],  2.8, 2.8, 285, 76, 188,  0.35, 7.0, 0.75),
                ],
            },

            # ================================================================
            # NIVEAU 4
            # ================================================================
            (4, 1): {
                'penalty': 1,
                'cameras': [Camera(500, 60, detection_range=450, alert_time=2.0,
                                   half_fov=25, sweep_amp=27, sweep_speed=36)],
                'policiers': [],
            },
            (4, 2): {
                'penalty': 1,
                'cameras': [],
                'policiers': [P(800, [V(300,340), V(1300,340)],
                                1.7, 2.2, 235, 68, 158,  0.8, 5.0, 1.5)],
            },
            (4, 3): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=455, alert_time=1.8,
                                   half_fov=25, sweep_amp=27, sweep_speed=38),
                            Camera(1100, 60, detection_range=455, alert_time=1.8,
                                   half_fov=25, sweep_amp=27, sweep_speed=38)],
                'policiers': [P(750, [V(500,340), V(1100,340)],
                                1.8, 2.3, 245, 70, 163,  0.7, 5.0, 1.4)],
            },
            (4, 4): {
                'penalty': 1,
                'cameras': [Camera(700, 60, detection_range=460, alert_time=1.6,
                                   half_fov=26, sweep_amp=28, sweep_speed=40),
                            Camera(1300, 60, detection_range=460, alert_time=1.6,
                                   half_fov=26, sweep_amp=28, sweep_speed=40)],
                'policiers': [
                    P(300, [V(150,340), V(700,340)],    1.9, 2.3, 255, 70, 168,  0.7, 6.0, 1.3),
                ],
            },
            (4, 5): {
                'penalty': 1,
                'cameras': [Camera(500, 60, detection_range=460, alert_time=1.5,
                                   half_fov=26, sweep_amp=28, sweep_speed=40)],
                'policiers': [
                    P(300,  [V(150,340), V(700,340)],   3.5, 3.0, 315, 80, 200,  0.30, 8.0, 0.65),
                    P(1200, [V(950,340), V(1450,340)],  3.5, 3.0, 315, 80, 200,  0.30, 8.0, 0.65),
                ],
            },

            # ================================================================
            # NIVEAU 5
            # ================================================================
            (5, 1): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=465, alert_time=1.4,
                                   half_fov=26, sweep_amp=28, sweep_speed=42),
                            Camera(1150, 60, detection_range=465, alert_time=1.4,
                                   half_fov=26, sweep_amp=28, sweep_speed=42)],
                'policiers': [P(750, [V(500,340), V(1100,340)],
                                2.1, 2.4, 270, 72, 175,  0.6, 4.0, 1.3)],
            },
            (5, 2): {
                'penalty': 1,
                'cameras': [Camera(600, 60, detection_range=465, alert_time=1.3,
                                   half_fov=27, sweep_amp=28, sweep_speed=44)],
                'policiers': [
                    P(300,  [V(150,340), V(700,340)],   2.2, 2.5, 280, 74, 180,  0.5, 5.5, 1.2),
                    P(1200, [V(900,340), V(1450,340)],  2.2, 2.5, 280, 74, 180,  0.5, 5.5, 1.2),
                ],
            },
            (5, 3): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=470, alert_time=1.2,
                                   half_fov=27, sweep_amp=29, sweep_speed=45),
                            Camera(1100, 60, detection_range=470, alert_time=1.2,
                                   half_fov=27, sweep_amp=29, sweep_speed=45)],
                'policiers': [
                    P(750, [V(500,340), V(1100,340)],   2.4, 2.5, 290, 74, 185,  0.5, 5.5, 1.1),
                ],
            },
            (5, 4): {
                'penalty': 1,
                'cameras': [Camera(500, 60, detection_range=470, alert_time=1.1,
                                   half_fov=27, sweep_amp=30, sweep_speed=46),
                            Camera(1150, 60, detection_range=470, alert_time=1.1,
                                   half_fov=27, sweep_amp=30, sweep_speed=46)],
                'policiers': [
                    P(300,  [V(150,340), V(700,340)],   2.6, 2.6, 300, 76, 190,  0.4, 7.0, 1.0),
                    P(1200, [V(900,340), V(1450,340)],  2.6, 2.6, 300, 76, 190,  0.4, 7.0, 1.0),
                ],
            },
            (5, 5): {
                'penalty': 1,
                'cameras': [Camera(400, 60, detection_range=475, alert_time=1.0,
                                   half_fov=28, sweep_amp=30, sweep_speed=48),
                            Camera(1150, 60, detection_range=475, alert_time=1.0,
                                   half_fov=28, sweep_amp=30, sweep_speed=48)],
                'policiers': [
                    P(300,  [V(150,340), V(700,340)],   3.8, 3.2, 340, 84, 210,  0.25, 9.0, 0.55),
                    P(1200, [V(900,340), V(1450,340)],  3.8, 3.2, 340, 84, 210,  0.25, 9.0, 0.55),
                ],
            },
        }

        cfg = configs.get((level_id, room_id), {'cameras': [], 'policiers': [], 'penalty': 1})
        self.cameras  = cfg['cameras']
        self.policier = cfg['policiers']
        self.penalty  = cfg.get('penalty', 1)

    def update(self, player_pos, dt, cop_player_pos=None):
        if cop_player_pos is None:
            cop_player_pos = player_pos
        for cam in self.cameras:
            if cam.update(player_pos, dt):
                return True, 'Repere par une camera', self.penalty
        for cop in self.policier:
            if cop.update(cop_player_pos, dt):
                return True, 'Attrape par un policier', self.penalty
        return False, None, self.penalty

    def draw(self, screen):
        for cam in self.cameras:
            cam.draw(screen)
        for cop in self.policier:
            cop.draw(screen)

    def reset(self):
        for cam in self.cameras:
            cam.reset()
        for cop in self.policier:
            cop.reset()
