import pygame


class Camera:
    def __init__(self, x, y, detection_range=120, alert_time=2.0):
        self.pos = pygame.Vector2(x, y)
        self.range = detection_range
        self.alert_time = alert_time
        self.state = "SURVEILLANCE"
        self.timer = 0.0

        self.size = 30

    def detect(self, player_pos, dt):
        if self.pos.distance_to(player_pos) < self.range:
            self.timer += dt
            if self.timer >= self.alert_time:
                self.state = "ALERT"
        else:
            self.timer = 0.0
            self.state = "SURVEILLANCE"

        return self.state == "ALERT"

    def update(self, player_pos, dt):
        return self.detect(player_pos, dt)

    def draw(self, screen):
        color = (255, 0, 0) if self.state == "ALERT" else (200, 200, 100)

        pygame.draw.circle(screen, color, (int(self.pos.x), int(self.pos.y)), self.size // 2)
        pygame.draw.circle(screen, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), int(self.range), 2)

    def reset(self):
        self.state = "SURVEILLANCE"
        self.timer = 0.0
