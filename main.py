import pygame
from src.scene_manager import SceneManager
from src.accueil import Accueil

pygame.init()

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
pygame.display.set_caption("Louvre Escape")

manager = SceneManager()
manager.scene = Accueil(screen, manager)

clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        manager.handle_event(event)

    manager.update()
    manager.draw()
    pygame.display.flip()

pygame.quit()

