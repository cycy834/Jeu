import pygame


class Policier:
    def __init__(self, x, y, patrol_points, speed=1.5, vision_range=100):
        self.start_pos = pygame.Vector2(x, y)
        self.pos = pygame.Vector2(x, y)

        self.speed = speed
        self.vision_range = vision_range
        self.state = "PATROL"

        self.patrol_points = patrol_points
        self.current_point = 0
        self.memory_timer = 0.0

        self.width = 60
        self.height = 90
        self.capture_distance = 40

    def can_see_player(self, player_pos):
        return self.pos.distance_to(player_pos) < self.vision_range

    def can_catch_player(self, player_pos):
        return self.pos.distance_to(player_pos) < self.capture_distance

    def patrol(self):
        target = self.patrol_points[self.current_point]
        direction = target - self.pos

        if direction.length() > 0:
            self.pos += direction.normalize() * self.speed

        if self.pos.distance_to(target) < 5:
            self.current_point = (self.current_point + 1) % len(self.patrol_points)

    def chase(self, player_pos):
        direction = player_pos - self.pos
        if direction.length() > 0:
            self.pos += direction.normalize() * self.speed

    def update(self, player_pos, dt):
        if self.state == "PATROL":
            self.patrol()
            if self.can_see_player(player_pos):
                self.state = "CHASE"

        elif self.state == "CHASE":
            self.chase(player_pos)

            if not self.can_see_player(player_pos):
                self.memory_timer += dt
                if self.memory_timer > 3:
                    self.memory_timer = 0.0
                    self.state = "PATROL"
            else:
                self.memory_timer = 0.0

        return self.can_catch_player(player_pos)

    def draw(self, screen):
        rect = pygame.Rect(
            int(self.pos.x - self.width // 2),
            int(self.pos.y - self.height // 2),
            self.width,
            self.height
        )

        pygame.draw.rect(screen, (255, 0, 0), rect)
        pygame.draw.circle(screen, (255, 120, 120), (int(self.pos.x), int(self.pos.y)), int(self.vision_range), 2)

    def reset(self):
        self.pos = self.start_pos.copy()
        self.state = "PATROL"
        self.current_point = 0
        self.memory_timer = 0.0
