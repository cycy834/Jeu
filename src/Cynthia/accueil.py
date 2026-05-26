import pygame
from src.audio import audio_manager as audio


# -----------------------------
# COULEURS (DA Louvre)
# -----------------------------

GOLD = (196, 166, 114) # Doré ancien (texte + bordures)
DARK = (28, 24, 20) # Fond sombre
DARK_BTN = (45, 38, 32) # Fond des boutons
OVERLAY = (0, 0, 0, 160) # Noir semi-transparent (menu popup)

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
        
        audio.init()
        audio.play_music(audio.MUSIC_MENU)
        self.volume = audio.get_volume_music_0_10()
        self.music_on = audio.get_music_on()
        
        #overlay animation pour boutons - et +
        self.btn_overlay_surface = None
        self.btn_overlay_alpha = 0
        self.btn_overlay_rect = None
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
        self.button_plusminus_font = pygame.font.Font(None, 55)


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

        # Boutons "-" et "+"
        self.btn_minus = pygame.Rect(0, 0, 50, 40)
        self.btn_plus = pygame.Rect(0, 0, 50, 40)

        # Boutons musique "ON" "OFF"
        self.btn_on = pygame.Rect(0, 0, 80, 40)
        self.btn_off = pygame.Rect(0, 0, 80, 40)

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

                if self.btn_minus.collidepoint(event.pos):
                    self.volume = max(0, self.volume - 1)
                    audio.set_volume_music(self.volume)
                    audio.set_volume_sfx(self.volume)
                    self.btn_overlay_surface = pygame.Surface(self.btn_minus.size, pygame.SRCALPHA)
                    self.btn_overlay_alpha = 120
                    self.btn_overlay_rect = self.btn_minus
                    return
                if self.btn_plus.collidepoint(event.pos):
                    self.volume = min(10, self.volume + 1)
                    audio.set_volume_music(self.volume)
                    audio.set_volume_sfx(self.volume)
                    self.btn_overlay_surface = pygame.Surface(self.btn_plus.size, pygame.SRCALPHA)
                    self.btn_overlay_alpha = 120
                    self.btn_overlay_rect = self.btn_plus
                    return
                if self.btn_on.collidepoint(event.pos):
                    self.music_on = True
                    audio.set_music_on(True)
                    return
                if self.btn_off.collidepoint(event.pos):
                    self.music_on = False
                    audio.set_music_on(False)
                    return
                # Si on clique en dehors du popup → on ferme
                if not self.popup_rect.collidepoint(event.pos):
                    self.show_menu = False
                    return
                

            if self.play_rect.collidepoint(event.pos):
                audio.play_sfx('hover')
                from src.Cynthia.mode_select import ModeSelect
                self.manager.scene = ModeSelect(self.screen, self.manager)
            elif self.menu_rect.collidepoint(event.pos):
                audio.play_sfx('hover')
                self.show_menu = True
       

# -----------------------------
# Update (logique)
# -----------------------------    

    def update(self, dt=0):
        if self.btn_overlay_alpha > 0:
            self.btn_overlay_alpha -= 12
            if self.btn_overlay_alpha < 0:
                self.btn_overlay_alpha = 0

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
        title = self.button_font.render("Menu du jeu", True, GOLD)
        self.screen.blit(title, title.get_rect(midtop=(self.popup_rect.centerx, self.popup_rect.top + 20)))

        # texte menu : SON
        y = self.popup_rect.top + 80

        txt = self.button_font.render("Son", True, GOLD)
        self.screen.blit(txt, (self.popup_rect.left + 30, y))

        #positon boutons - et + ici comme ca c'est à la bonne position
        self.btn_minus.topleft = (self.popup_rect.left + 100, y + 40)
        self.btn_plus.topleft = (self.popup_rect.left + 260, y + 40)

        #bouton "-"
        pygame.draw.rect(self.screen, GOLD, self.btn_minus, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, self.btn_minus, 2, border_radius=8)

        txt = self.button_plusminus_font.render("-", True, DARK_BTN)
        self.screen.blit(txt, txt.get_rect(center=self.btn_minus.center))

        #bouton "+"
        pygame.draw.rect(self.screen, GOLD, self.btn_plus, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, self.btn_plus, 2, border_radius=8)

        txt = self.button_plusminus_font.render("+", True, DARK_BTN)
        self.screen.blit(txt, txt.get_rect(center=(self.btn_plus.centerx, self.btn_plus.centery - 3)))

        #texte menu : MUSIQUE 
        y += 120

        txt = self.button_font.render("Musique", True, GOLD)
        self.screen.blit(txt, (self.popup_rect.left + 30, y))

        #positions boutons ON et OFF
        self.btn_on.topleft = (self.popup_rect.left + 80, y + 40)
        self.btn_off.topleft = (self.popup_rect.left + 250, y + 40)

        #bouton ON 
        pygame.draw.rect(self.screen, GOLD, self.btn_on, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, self.btn_on, 2, border_radius=8)

        txt_on = self.button_font.render("ON", True, DARK_BTN)
        self.screen.blit(txt_on, txt_on.get_rect(center=self.btn_on.center))

        #bouton OFF 
        pygame.draw.rect(self.screen, GOLD, self.btn_off, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, self.btn_off, 2, border_radius=8)

        txt_off = self.button_font.render("OFF", True, DARK_BTN)
        self.screen.blit(txt_off, txt_off.get_rect(center=self.btn_off.center))
        
        #overlay sur bouton actif
        overlay = pygame.Surface(self.btn_on.size, pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 90))

        if self.music_on :
            self.screen.blit(overlay, self.btn_on.topleft)
        else :
            self.screen.blit(overlay, self.btn_off.topleft)

        #animation overlay pour les boutons + et -
        if self.btn_overlay_alpha > 0 and self.btn_overlay_surface :
            self.btn_overlay_surface.set_alpha(self.btn_overlay_alpha)
            self.btn_overlay_surface.fill((0, 0, 0))
            self.screen.blit(self.btn_overlay_surface, self.btn_overlay_rect.topleft)
