import pygame
import sys

class CharacterSelectionApp:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Configuration de l'écran (Plein écran)
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.SCREEN_W, self.SCREEN_H = self.screen.get_size()
        pygame.display.set_caption("Braquage au Louvre")

        # Couleurs
        self.GOLD = (212, 175, 55)
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.GRAY = (100, 100, 100)
        self.DARK_GRAY = (40, 40, 40)

        # Polices
        self.font_title = pygame.font.SysFont('serif', int(self.SCREEN_H * 0.08), bold=True)
        self.font_text = pygame.font.SysFont('arial', int(self.SCREEN_H * 0.035), bold=True)
        self.font_arrow = pygame.font.SysFont('arial', int(self.SCREEN_H * 0.1), bold=True)

        # Variables d'état
        self.current_char_idx = 0
        self.username = ""
        self.input_active = False
        self.running = True

        # Initialisation des éléments de l'interface et des assets
        self.setup_ui_rects()
        self.load_assets()

    def setup_ui_rects(self):
        """Définit les zones cliquables (Rects) de l'interface."""
        self.input_box = pygame.Rect(0, 0, 500, 50)
        self.input_box.center = (self.SCREEN_W // 2, self.SCREEN_H * 0.22)

        self.arrow_left_rect = pygame.Rect(self.SCREEN_W * 0.2, self.SCREEN_H * 0.5, 80, 80)
        self.arrow_right_rect = pygame.Rect(self.SCREEN_W * 0.8 - 80, self.SCREEN_H * 0.5, 80, 80)

        self.valider_rect = pygame.Rect(0, 0, 450, 70)
        self.valider_rect.center = (self.SCREEN_W // 2, self.SCREEN_H * 0.9)

    def load_char(self, name, path, char_h):
        """Charge et redimensionne un sprite de personnage."""
        img = pygame.image.load(f"{path}{name}").convert_alpha()
        ratio = img.get_width() / img.get_height()
        return pygame.transform.smoothscale(img, (int(char_h * ratio), char_h))

    def load_assets(self):
        """Charge les images et prépare les personnages."""
        path = "../../assets/images/"
        try:
            # Fond d'écran
            bg_img = pygame.image.load(f"{path}background_perso.png").convert()
            self.bg = pygame.transform.smoothscale(bg_img, (self.SCREEN_W, self.SCREEN_H))

            # Personnages
            char_h = int(self.SCREEN_H * 0.5)
            self.characters = [
                self.load_char("sprite4.png", path, char_h),
                self.load_char("sprite2.png", path, char_h),
                self.load_char("sprite3.png", path, char_h)
            ]
            self.char_names = ["L'EXPERTE", "LE CERVEAU", "L'INFILTRÉE"]

        except Exception as e:
            print(f"Erreur lors du chargement des assets : {e}")
            pygame.quit()
            sys.exit()

    def handle_events(self):
        """Gère les entrées clavier et souris."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False

                if self.input_active:
                    if event.key == pygame.K_BACKSPACE:
                        self.username = self.username[:-1]
                    elif len(self.username) < 15 and event.unicode.isprintable():
                        self.username += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                # Activer/Désactiver l'input
                self.input_active = self.input_box.collidepoint(event.pos)

                # Clic sur Flèche Gauche
                if self.arrow_left_rect.collidepoint(event.pos):
                    self.current_char_idx = (self.current_char_idx - 1) % len(self.characters)

                # Clic sur Flèche Droite
                if self.arrow_right_rect.collidepoint(event.pos):
                    self.current_char_idx = (self.current_char_idx + 1) % len(self.characters)

                # Clic sur Bouton Valider
                if self.username != "" and self.valider_rect.collidepoint(event.pos):
                    print(f"Mission : {self.username} avec {self.char_names[self.current_char_idx]}")
                    self.running = False

    def draw_arrow(self, rect, text, is_hover):
        """Dessine une flèche avec un effet de survol."""
        color = self.GOLD if is_hover else self.WHITE
        surf = self.font_arrow.render(text, True, color)
        self.screen.blit(surf, surf.get_rect(center=rect.center))

    def draw(self):
        """Dessine tous les éléments à l'écran."""
        mouse_pos = pygame.mouse.get_pos()

        # Fond et overlay sombre
        self.screen.blit(self.bg, (0, 0))
        overlay = pygame.Surface((self.SCREEN_W, self.SCREEN_H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        self.screen.blit(overlay, (0, 0))

        # Titre
        title_surf = self.font_title.render("SÉLECTION DE L'AGENT", True, self.GOLD)
        self.screen.blit(title_surf, (self.SCREEN_W // 2 - title_surf.get_width() // 2, self.SCREEN_H * 0.05))

        # Zone de texte (Input Nom)
        box_color = self.WHITE if self.input_active else self.GRAY
        pygame.draw.rect(self.screen, box_color, self.input_box, 2, border_radius=10)
        display_name = self.username if self.username != "" else "Tapez votre nom..."
        text_color = self.WHITE if self.username != "" else self.GRAY
        name_surf = self.font_text.render(display_name, True, text_color)
        self.screen.blit(name_surf, (self.input_box.x + 15, self.input_box.y + 10))

        # Personnage actuel
        current_img = self.characters[self.current_char_idx]
        char_pos = current_img.get_rect(center=(self.SCREEN_W // 2, self.SCREEN_H * 0.58))
        self.screen.blit(current_img, char_pos)

        # Nom du personnage
        name_tag = self.font_text.render(self.char_names[self.current_char_idx], True, self.GOLD)
        self.screen.blit(name_tag, (self.SCREEN_W // 2 - name_tag.get_width() // 2, self.SCREEN_H * 0.8))

        # Flèches
        self.draw_arrow(self.arrow_left_rect, "<", self.arrow_left_rect.collidepoint(mouse_pos))
        self.draw_arrow(self.arrow_right_rect, ">", self.arrow_right_rect.collidepoint(mouse_pos))

        # Bouton Valider (n'apparaît que si le nom est rempli)
        if self.username != "":
            pygame.draw.rect(self.screen, self.GOLD, self.valider_rect, border_radius=35)
            btn_text = self.font_text.render("LANCER LA MISSION", True, self.BLACK)
            self.screen.blit(btn_text, btn_text.get_rect(center=self.valider_rect.center))

        # Rafraîchissement de l'écran
        pygame.display.flip()

    def run(self):
        """Boucle principale du programme."""
        while self.running:
            self.handle_events()
            self.draw()

        pygame.quit()

# --- Point d'entrée du programme ---
if __name__ == "__main__":
    app = CharacterSelectionApp()
    app.run()
