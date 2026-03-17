import pygame

# Couleurs cohérentes avec l'accueil
GOLD = (196, 166, 114)
DARK = (28, 24, 20)
DARK_BTN = (45, 38, 32)


class Jeu:

    def __init__(self, screen, manager):

        # Fenêtre
        self.screen = screen

        # SceneManager
        self.manager = manager

        # Police
        self.font = pygame.font.Font(None, 34)

        # Bouton retour
        self.back_rect = pygame.Rect(40, 40, 190, 65)

        # niveaux
        self.niveau_max = 1
        self.level_rects = []
        
        # resizing
        self.create_ui()


    def create_ui(self):
        w, h = self.screen.get_size()
        
        start_y = int(h * 0.25)
        self.level_rects = []
        
        for i in range(5):
            rect = pygame.Rect(
                w//2 - 150, 
                start_y + i* 90, 
                300, 
                70
                )
            self.level_rects.append(rect)

    # gestion events
    def handle_event(self, event):

        if event.type == pygame.VIDEORESIZE:
            self.screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
            self.create_ui()

        if event.type == pygame.MOUSEBUTTONDOWN:

            # bouton retour
            if self.back_rect.collidepoint(event.pos):

                from src.Cynthia.accueil import Accueil
                self.manager.scene = Accueil(self.screen, self.manager)

            # clic niveaux
            for i, rect in enumerate(self.level_rects):

                if rect.collidepoint(event.pos):

                    niveau = i + 1

                    if niveau <= self.niveau_max:

                        if niveau == 1:
                            from src.Benji.mouvements_v2 import run_game
                            run_game()

    def update(self):
        pass

    def draw(self):

        # fond
        self.screen.fill(DARK)

        # bouton retour
        pygame.draw.rect(self.screen, DARK_BTN, self.back_rect, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, self.back_rect, 2, border_radius=8)

        txt = self.font.render("Retour", True, GOLD)
        self.screen.blit(txt, txt.get_rect(center=self.back_rect.center))

        # titre
        titre = self.font.render("Choisir un niveau", True, GOLD)
        
        w, h = self.screen.get_size()
        titre_rect = titre.get_rect(center=(w//2, int(h*0.15)))
        
        self.screen.blit(titre, titre_rect)

        # niveaux
        for i, rect in enumerate(self.level_rects):

            pygame.draw.rect(self.screen, DARK_BTN, rect, border_radius=8)
            pygame.draw.rect(self.screen, GOLD, rect, 2, border_radius=8)

            txt = self.font.render(f"Niveau {i+1}", True, GOLD)
            self.screen.blit(txt, txt.get_rect(center=rect.center))

            # verrouillage
            if i + 1 > self.niveau_max:

                overlay = pygame.Surface((rect.width, rect.height))
                overlay.set_alpha(180)
                overlay.fill((0, 0, 0))

                self.screen.blit(overlay, rect.topleft)

                # cadenas simple
                pygame.draw.rect(
                    self.screen,
                    GOLD,
                    (rect.right - 40, rect.y + 25, 20, 20),
                    2
                )

                pygame.draw.arc(
                    self.screen,
                    GOLD,
                    (rect.right - 40, rect.y + 10, 20, 20),
                    3.14,
                    0,
                    2
                )
