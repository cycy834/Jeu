import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Paramètres de base
WIDTH, HEIGHT = 1024, 768
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Louvre Escape - Break-in Simulator")

# --- CHARGEMENT ---
try:
    bg_image_original = pygame.image.load("../../assets/images/Game_over.png").convert()
except:
    print("Erreur : Image 'Game_over.jpg' introuvable.")
    sys.exit()

img_w, img_h = bg_image_original.get_size()

# --- FONCTION POUR REMPLIR L'ÉCRAN (SANS DÉFORMER) ---
def get_scaled_image_and_rect(win_w, win_h):
    # On calcule le ratio pour remplir tout l'espace (Cover)
    ratio_w = win_w / img_w
    ratio_h = win_h / img_h
    scale_factor = max(ratio_w, ratio_h)

    new_w = int(img_w * scale_factor)
    new_h = int(img_h * scale_factor)

    scaled_img = pygame.transform.smoothscale(bg_image_original, (new_w, new_h))
    # On centre l'image pour que le surplus soit coupé de chaque côté
    rect = scaled_img.get_rect(center=(win_w // 2, win_h // 2))
    return scaled_img, rect

# --- CLASSE DES BOUTONS ---
class Hitbox:
    def __init__(self, rel_x, rel_y, rel_w, rel_h):
        self.rel_x = rel_x
        self.rel_y = rel_y
        self.rel_w = rel_w
        self.rel_h = rel_h
        self.current_rect = pygame.Rect(0, 0, 0, 0)

    def update_rect(self, bg_rect):
        # Repositionne le bouton par rapport à l'image affichée (même si elle déborde)
        x = bg_rect.x + (self.rel_x * bg_rect.width)
        y = bg_rect.y + (self.rel_y * bg_rect.height)
        w = self.rel_w * bg_rect.width
        h = self.rel_h * bg_rect.height
        self.current_rect = pygame.Rect(x, y, w, h)

    def draw_hover(self, surface, mouse_pos):
        if self.current_rect.collidepoint(mouse_pos):
            # Création d'un rectangle sombre transparent
            overlay = pygame.Surface((self.current_rect.width, self.current_rect.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 80))
            surface.blit(overlay, self.current_rect.topleft)

# --- INITIALISATION DES BOUTONS ---
btn_play = Hitbox(0.358, 0.655, 0.138, 0.065)
btn_no = Hitbox(0.510, 0.655, 0.138, 0.065)

# Premier calcul de l'image et des positions
scaled_bg, bg_rect = get_scaled_image_and_rect(WIDTH, HEIGHT)
btn_play.update_rect(bg_rect)
btn_no.update_rect(bg_rect)

# --- BOUCLE PRINCIPALE ---
running = True
black_screen = False

while running:
    mouse_pos = pygame.mouse.get_pos()
    clicked_this_frame = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.VIDEORESIZE:
            # Mise à jour quand on agrandit la fenêtre
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

            # Recalcul de l'image (Cover) et des boutons
            scaled_bg, bg_rect = get_scaled_image_and_rect(WIDTH, HEIGHT)
            btn_play.update_rect(bg_rect)
            btn_no.update_rect(bg_rect)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Clic gauche
                clicked_this_frame = True

    # --- AFFICHAGE ---
    if black_screen:
        screen.fill((0, 0, 0))
    else:
        # On remplit le fond en noir (au cas où)
        screen.fill((0, 0, 0))

        # On dessine l'image (étirée pour remplir mais pas déformée)
        screen.blit(scaled_bg, bg_rect)

        # On dessine l'effet de survol
        btn_play.draw_hover(screen, mouse_pos)
        btn_no.draw_hover(screen, mouse_pos)

        # Gestion des clics
        if clicked_this_frame:
            if btn_play.current_rect.collidepoint(mouse_pos):
                print("Lancement d'une nouvelle partie...")
                # Tu peux ajouter ici le code pour relancer le jeu

            elif btn_no.current_rect.collidepoint(mouse_pos):
                print("Fermeture vers l'écran noir.")
                black_screen = True

    # Mise à jour de l'affichage
    pygame.display.flip()

pygame.quit()
sys.exit()
