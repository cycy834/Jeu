import pygame                                                                                                                                           class Player(pygame.sprite.Sprite):                                                                                                                         def __init__(self, x, y):                                                       super().__init__()                                                          self.sprite_sheet = pygame.image.load("Chemin a mettre pour avoir l'image du perso")
        self.image =self.get_image(0, 0)
        self.image.set_colorkey([0, 0, 0])
        self.rect = self.image.get_rect()
        self.position = [x, y]
        self.images = {'down': self.get_image(0, 0),
                       'left': self.get_image(0, 32),
                       'right': self.get_image(0, 64),
                       'up': self.get_image(0, 96) }
        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5 , 12)
        self.old_position = self.position.copy()
        self.speed = 2
#definir old position
    def save_location(self):
        self.old_position = self.position.copy()

#faire changer le perso selon mouvement
    def change(self, name):
        self.image.set_colorkey((0, 0, 0))
        self.image = self.images[name]

#faire les deplacement
    def move_right(self):
        self.position[0] += self.speed

    def move_left(self):
        self.position[0] -= self.speed

    def move_up(self):
        self.position[1] -= self.speed

    def move_down(self):
        self.position[1] +=  self.speed
# creation d'une methode qui se met h24 a jour pour la position du joueur
    def update(self):
        self.rect.topleft = self.position

    def move_back(self):
        self.position =self.old_position
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, x, y):
        image = pygame.Surface([32, 32])
        image.blit(self.sprite_sheet, (0, 0), (x, y, 32, 32))
        return image

