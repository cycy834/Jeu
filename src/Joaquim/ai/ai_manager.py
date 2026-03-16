import pygame

from src.Joaquim.ai.camera import Camera
from src.Joaquim.ai.policier import Policier


class AIManager:
    def __init__(self, room_id):
        self.room_id = room_id
        self.cameras = []
        self.policier = None
        self.build_room(room_id)

    def build_room(self, room_id):
        self.cameras = []
        self.policier = None

        if room_id == 1:
            self.cameras = [
                Camera(500, 100, detection_range=140, alert_time=2.0),
            ]
            self.policier = Policier(
                1000,
                300,
                patrol_points=[
                    pygame.Vector2(900, 300),
                    pygame.Vector2(1250, 300),
                ],
                speed=1.5,
                vision_range=120
            )

    def update(self, player_pos, dt):
        for camera in self.cameras:
            if camera.update(player_pos, dt):
                return True, "Repéré par une caméra"

        if self.policier is not None:
            if self.policier.update(player_pos, dt):
                return True, "Attrapé par le policier"

        return False, None

    def draw(self, screen):
        for camera in self.cameras:
            camera.draw(screen)

        if self.policier is not None:
            self.policier.draw(screen)

    def reset(self):
        for camera in self.cameras:
            camera.reset()

        if self.policier is not None:
            self.policier.reset()
