import pygame


# -----------------------------
# COULEURS (DA Louvre)
# -----------------------------

GOLD = (196, 166, 114) # Doré ancien (texte + bordures)
DARK = (28, 24, 20) # Fond sombre
DARK_BTN = (45, 38, 32) # Fond des boutons
OVERLAY = (0, 0, 0, 160) # Noir semi-transparent (menu popup)
DARK_SHADOW = (40, 30, 20)   # brun très foncé

class Accueil:
    def __init__(self, screen, manager):
        # Référence à la fenêtre principale
        self.screen = screen
        
        # SceneManager (permet de changer de scène)
        self.manager = manager
        
        # Booléen : le menu popup est-il affiché ?
        self.show_menu = False
        
        # Chargement des images et polices
        self.load_assets()
        
        # Création des boutons et rectangles
        self.create_ui()


# -----------------------------
# Chargement des assets
# -----------------------------

    def load_assets(self):
        # Image de fond de l'accueil
        self.bg = pygame.image.load(
            "assets/images/accueil_background.png"
        ).convert()

        # Polices (Font(None, taille) = police par défaut)
        self.title_font = pygame.font.Font(None, 120)
        self.subtitle_font = pygame.font.Font(None, 55)
        self.button_font = pygame.font.Font(None, 40)


# -----------------------------
# Création de l'interface
# -----------------------------

    def create_ui(self):
        # Récupère la taille actuelle de la fenêtre
        w, h = self.screen.get_size()
        
        # Bouton "Jouer" (à gauche)
        self.play_rect = pygame.Rect(w//2 - 340, # position X 
                                     int(h*0.62), # position Y
                                     190, #largeur
                                     65 # hauteur
                                     )
        # Bouton "Menu" (à droite)
        self.menu_rect = pygame.Rect(w//2 + 160, int(h*0.62), 190, 65)

        # Fenêtre popup du menu (centrée)
        self.popup_rect = pygame.Rect(w//2 - 200, h//2 - 160, 400, 360)


# -----------------------------
# Gestion des événements
# -----------------------------

    def handle_event(self, event):
        # Si la fenêtre est redimensionnée
        if event.type == pygame.VIDEORESIZE:
            self.create_ui() # on recalcule les positions

        # Si clic de souris
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Si le menu popup est ouvert
            if self.show_menu:
                # Si on clique en dehors du popup → on ferme
                if not self.popup_rect.collidepoint(event.pos):
                    self.show_menu = False
                return

            # Clic sur "Jouer"
            if self.play_rect.collidepoint(event.pos):
                # Import ici pour éviter les imports circulaires
                from src.jeu import Jeu
                self.manager.scene = Jeu(self.screen, self.manager)
            
            # Clic sur "Menu"
            elif self.menu_rect.collidepoint(event.pos):
                self.show_menu = True

# -----------------------------
# Update (logique)
# -----------------------------    

    def update(self):
        pass # rien à mettre pour l'instant

# -----------------------------
# Dessin de la scène
# -----------------------------    

    def draw(self):
        # Récupère la taille de la fenêtre
        w, h = self.screen.get_size()

        # Redimensionne le background à la taille de l'écran
        bg = pygame.transform.scale(self.bg, (w, h))
        self.screen.blit(bg, (0, 0))

# -------- TITRE --------
        # Ombre du titre
        shadow = self.title_font.render("Louvre Escape", True, (0, 0, 0))
        title = self.title_font.render("Louvre Escape", True, GOLD)

        self.screen.blit(shadow, shadow.get_rect(center=(w//2+2, h*0.26+4)))
        
        # Hauteur du titre (le h * 0,26)
        self.screen.blit(title, title.get_rect(center=(w//2, h*0.26)))

        # Ombre sous-titre
        subtitle_shadow = self.subtitle_font.render("break-in simulator", True, (0, 0, 0))
        subtitle = self.subtitle_font.render("break-in simulator", True, GOLD)      
        
        self.screen.blit(subtitle_shadow, subtitle_shadow.get_rect(center=(w // 2 + 2, h * 0.35 + 2)))


        # Sous-titre
        subtitle = self.subtitle_font.render("break-in simulator", True, GOLD)
        self.screen.blit(subtitle, subtitle.get_rect(center=(w//2, h*0.35)))

        # Boutons
        self.draw_button(self.play_rect, "Jouer")
        self.draw_button(self.menu_rect, "Menu")
        
        # Si le menu est actif → on l'affiche
        if self.show_menu:
            self.draw_menu()

# -----------------------------
# Dessin d'un bouton
# -----------------------------

    def draw_button(self, rect, text):
        # Fond sombre du bouton
        pygame.draw.rect(self.screen, DARK_BTN, rect, border_radius=8)
        # Bordure dorée
        pygame.draw.rect(self.screen, GOLD, rect, 2, border_radius=8)
        
        # Texte du bouton
        txt = self.button_font.render(text, True, GOLD)
        self.screen.blit(txt, txt.get_rect(center=rect.center))

# -----------------------------
# Dessin du menu popup
# -----------------------------

    def draw_menu(self):
        # Overlay sombre sur tout l'écran
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill(OVERLAY)
        self.screen.blit(overlay, (0, 0))
        
        # Fenêtre du menu
        pygame.draw.rect(self.screen, DARK_BTN, self.popup_rect, border_radius=10)
        pygame.draw.rect(self.screen, GOLD, self.popup_rect, 2, border_radius=10)
        
        # Texte du menu
        txt = self.button_font.render("Menu du jeu", True, GOLD)
        self.screen.blit(txt, txt.get_rect(midtop=(self.popup_rect.centerx, self.popup_rect.top + 20)))

