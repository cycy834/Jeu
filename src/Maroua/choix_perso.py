import pygame
import sys

# Initialisation de Pygame
pygame.init()

# Plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
SCREEN_W, SCREEN_H = screen.get_size()
pygame.display.set_caption("Braquage au Louvre")

# Couleurs
GOLD = (212, 175, 55)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

# Polices
font_title = pygame.font.SysFont('serif', int(SCREEN_H * 0.08), bold=True)
font_text = pygame.font.SysFont('arial', int(SCREEN_H * 0.035), bold=True)
font_arrow = pygame.font.SysFont('arial', int(SCREEN_H * 0.1), bold=True)

# Chemin des assets
PATH = "../../assets/images/"

# Chargement des images
try:
    bg = pygame.image.load(f"{PATH}background_perso.png").convert()
    bg = pygame.transform.smoothscale(bg, (SCREEN_W, SCREEN_H))

    char_h = int(SCREEN_H * 0.5) # Perso un peu plus grand puisqu'il est seul
    def load_char(name):
        img = pygame.image.load(f"{PATH}{name}").convert_alpha()
        ratio = img.get_width() / img.get_height()
        return pygame.transform.smoothscale(img, (int(char_h * ratio), char_h))

    # Liste des personnages
    characters = [load_char("sprite4.png"), load_char("sprite2.png"), load_char("sprite3.png")]
    char_names = ["L'EXPERTE", "LE CERVEAU", "L'INFILTRÉE"]
except Exception as e:
    print(f"Erreur : {e}")
    pygame.quit()
    sys.exit()

# Variables d'état
current_char_idx = 0  # Index du personnage affiché
username = ""
input_active = False
running = True

# Coordonnées des éléments
input_box = pygame.Rect(0, 0, 500, 50)
input_box.center = (SCREEN_W // 2, SCREEN_H * 0.22)

# Flèches (Rectangles pour la détection de clic)
arrow_left_rect = pygame.Rect(SCREEN_W * 0.2, SCREEN_H * 0.5, 80, 80)
arrow_right_rect = pygame.Rect(SCREEN_W * 0.8 - 80, SCREEN_H * 0.5, 80, 80)

# Bouton Valider
valider_rect = pygame.Rect(0, 0, 450, 70)
valider_rect.center = (SCREEN_W // 2, SCREEN_H * 0.9)

while running:
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if input_active:
                if event.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                elif len(username) < 15 and event.unicode.isprintable():
                    username += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Activer l'input
            input_active = input_box.collidepoint(event.pos)

            # Flèche Gauche
            if arrow_left_rect.collidepoint(event.pos):
                current_char_idx = (current_char_idx - 1) % len(characters)

            # Flèche Droite
            if arrow_right_rect.collidepoint(event.pos):
                current_char_idx = (current_char_idx + 1) % len(characters)

            # Bouton Valider
            if username != "":
                if valider_rect.collidepoint(event.pos):
                    print(f"Mission : {username} avec {char_names[current_char_idx]}")
                    running = False

    # --- DESSIN ---
    screen.blit(bg, (0, 0))

    overlay = pygame.Surface((SCREEN_W, SCREEN_H), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 160))
    screen.blit(overlay, (0, 0))

    # Titre
    title_surf = font_title.render("SÉLECTION DE L'AGENT", True, GOLD)
    screen.blit(title_surf, (SCREEN_W // 2 - title_surf.get_width() // 2, SCREEN_H * 0.05))

    # Input Nom
    box_color = WHITE if input_active else GRAY
    pygame.draw.rect(screen, box_color, input_box, 2, border_radius=10)
    display_name = username if username != "" else "Tapez votre nom..."
    text_color = WHITE if username != "" else GRAY
    name_surf = font_text.render(display_name, True, text_color)
    screen.blit(name_surf, (input_box.x + 15, input_box.y + 10))

    # Affichage du Personnage Actuel (Centré)
    current_img = characters[current_char_idx]
    char_pos = current_img.get_rect(center=(SCREEN_W // 2, SCREEN_H * 0.58))
    screen.blit(current_img, char_pos)

    # Nom du personnage sous l'image
    name_tag = font_text.render(char_names[current_char_idx], True, GOLD)
    screen.blit(name_tag, (SCREEN_W // 2 - name_tag.get_width() // 2, SCREEN_H * 0.8))

    # Dessin des Flèches
    def draw_arrow(rect, text, is_hover):
        color = GOLD if is_hover else WHITE
        surf = font_arrow.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=rect.center))

    draw_arrow(arrow_left_rect, "<", arrow_left_rect.collidepoint(mouse_pos))
    draw_arrow(arrow_right_rect, ">", arrow_right_rect.collidepoint(mouse_pos))

    # Bouton Valider
    if username != "":
        pygame.draw.rect(screen, GOLD, valider_rect, border_radius=35)
        btn_text = font_text.render("LANCER LA MISSION", True, BLACK)
        screen.blit(btn_text, btn_text.get_rect(center=valider_rect.center))

    pygame.display.flip()

pygame.quit()
