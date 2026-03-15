import pygame
from src.Benji.mouvements_v2 import run_game
# Couleurs cohérentes avec l'accueil
GOLD = (196, 166, 114)
DARK = (28, 24, 20)
DARK_BTN = (45, 38, 32)


class Jeu:
    def __init__(self, screen, manager):
        # Fenêtre principale
        self.screen = screen

        # SceneManager
        self.manager = manager
        
        # Police
        self.font = pygame.font.Font(None, 34)
    
        # Bouton "Retour" (haut gauche)
        self.back_rect = pygame.Rect(40, # Position X 
                                     40, # Position Y
                                     190, # largeur
                                     65) # hauteur

        run_game()
    # Gestion des événements
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.back_rect.collidepoint(event.pos):
                # Import local pour éviter import circulaire
                from src.Cynthia.accueil import Accueil
                self.manager.scene = Accueil(self.screen, self.manager)

    def update(self):
        pass # on verra

    def draw(self):
        # Fond sombre
        self.screen.fill(DARK)

        # Bouton retour
        pygame.draw.rect(self.screen, DARK_BTN, self.back_rect, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, self.back_rect, 2, border_radius=8)

        txt = self.font.render("Retour", True, GOLD)
        self.screen.blit(txt, txt.get_rect(center=self.back_rect.center))

