import pygame
from src.Cynthia.scene_manager import SceneManager
from src.Cynthia.accueil import Accueil

pygame.init()

info = pygame.display.Info()
screen = pygame.display.set_mode((1280, 720))

icon = pygame.image.load("assets/images/louvre_escape_logo.png")
pygame.display.set_icon(icon)
pygame.display.set_caption("Louvre Escape")

manager = SceneManager()
manager.scene = Accueil(screen, manager)

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000.0

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        manager.handle_event(event)

    manager.update(dt)
    manager.draw()

    pygame.display.flip()

pygame.quit()
