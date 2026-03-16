import pygame
import sys

from src.Joaquim.network.runtime import NetworkRuntime

pygame.init()

# --- Constantes ---
WIDTH, HEIGHT = 1588, 479
FPS = 60
VITESSE_JOUEUR = 3

# --- Couleurs ---
WHITE = (255, 255, 255)
GOLD = (220, 190, 100)
GREEN = (80, 255, 80)
RED = (255, 80, 80)
YELLOW = (255, 255, 0)
BLUE = (100, 180, 255)

# --- Chargement ressources ---
def load_img(path, size=None):
    img = pygame.image.load(path).convert_alpha()
    if size:
        img = pygame.transform.scale(img, size)
    return img

def load_bg(path):
    img = pygame.image.load(path).convert()
    return pygame.transform.scale(img, (WIDTH, HEIGHT))


try:
    backgrounds = {
        1: load_bg('assets/images/background2.png'),
        2: load_bg('assets/images/background3.png'),
        3: load_bg('assets/images/background2.png'),
        4: load_bg('assets/images/background3.png'),
        5: load_bg('assets/images/background2.png'),
    }
    sprite_idle = load_img('assets/images/sprite.png', (80, 120))
    sprite_right = load_img('assets/images/sprite2.png', (80, 120))
    sprite_left = load_img('assets/images/sprite3.png', (80, 120))
except Exception as e:
    print(f"[AVERTISSEMENT] Ressource manquante : {e}")
    backgrounds = {i: pygame.Surface((WIDTH, HEIGHT)) for i in range(1, 6)}
    for i, col in enumerate([(20, 20, 40), (30, 20, 20), (20, 30, 20), (20, 20, 50), (40, 20, 20)], 1):
        backgrounds[i].fill(col)
    sprite_idle = pygame.Surface((80, 120))
    sprite_idle.fill((100, 180, 255))
    sprite_right = sprite_idle
    sprite_left = sprite_idle

try:
    pygame.mixer.init()
    pygame.mixer.music.load("assets/music/musique.mp3")
    son_porte = pygame.mixer.Sound("assets/sounds/ouverture_porte.mp3")
    son_succes = son_porte
except Exception:
    son_porte = None
    son_succes = None


def play_sound(s):
    if s:
        s.play()


SALLES = {
    1: {
        'bg': 1,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': '1234',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'tableau',
                'x': 400, 'y': 200,
                'largeur': 80, 'hauteur': 100,
                'label': 'Tableau mysterieux',
                'indice': (
                    "Un tableau represente une femme avec un sourire enigmatique.\n"
                    "Sous le cadre : « Mon nom est aussi celebre que le musee. »\n"
                    "Quel est ce prenom en 4 lettres ?"
                ),
                'reponse': 'mona',
                'resolu': False,
                'digit_index': 0,
                'digit_value': 4,
            }
        ],
    },
    2: {
        'bg': 2,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': '5678',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'coffre',
                'x': 600, 'y': 260,
                'largeur': 100, 'hauteur': 80,
                'label': 'Coffre ancien',
                'indice': (
                    "Sur le coffre est gravee une plaque :\n"
                    "« Je suis ne en 1793, je suis le plus grand musee de France.\n"
                    "Mon code est l annee de ma fondation. »"
                ),
                'reponse': '1793',
                'resolu': False,
                'digit_index': 1,
                'digit_value': 1,
            }
        ],
    },
    3: {
        'bg': 3,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'aphrodite',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'statue',
                'x': 700, 'y': 150,
                'largeur': 60, 'hauteur': 130,
                'label': 'Statue sans bras',
                'indice': (
                    "Une statue de femme sans bras vous observe.\n"
                    "Sur le socle : « Je suis la deesse de l amour grec.\n"
                    "Quel est mon nom ? »"
                ),
                'reponse': 'aphrodite',
                'resolu': False,
                'digit_index': 2,
                'digit_value': 7,
            }
        ],
    },
    4: {
        'bg': 4,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'rosette',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'pierre',
                'x': 500, 'y': 200,
                'largeur': 90, 'hauteur': 110,
                'label': 'Pierre aux hieroglyphes',
                'indice': (
                    "Une pierre couverte de symboles egyptiens.\n"
                    "Une note dit : « Cette pierre celebre permit de\n"
                    "dechiffrer les hieroglyphes. Son nom ? »"
                ),
                'reponse': 'rosette',
                'resolu': False,
                'digit_index': 3,
                'digit_value': 3,
            }
        ],
    },
    5: {
        'bg': 5,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': '6',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'panneau',
                'x': 800, 'y': 220,
                'largeur': 80, 'hauteur': 100,
                'label': 'Panneau de sortie',
                'indice': (
                    "Un panneau electronique clignote :\n"
                    "« Code de securite final :\n"
                    "Combien de lettres dans le mot LOUVRE ? »"
                ),
                'reponse': '6',
                'resolu': False,
                'digit_index': 0,
                'digit_value': 6,
            }
        ],
    },
    6: {
        'bg': 1,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'art',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'tableaux',
                'x': 400, 'y': 200,
                'largeur': 80, 'hauteur': 100,
                'label': 'Tableaux numerotes',
                'indice': (
                    "Derriere chaque tableau, un numero indique son ordre.\n"
                    "La phrase a reconstituer : Le musee ouvre en 1793.\n"
                    "Retrouvez l ordre des tableaux selon cette annee."
                ),
                'reponse': '1-7-9-3',
                'resolu': False,
                'digit_index': 1,
                'digit_value': 9,
            }
        ],
    },
    7: {
        'bg': 2,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'voleur',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'mot_desordre',
                'x': 500, 'y': 220,
                'largeur': 100, 'hauteur': 80,
                'label': 'Mot a remettre en ordre',
                'indice': (
                    "Les lettres du mot sont melangees : VREOLU.\n"
                    "Quel est le mot correct ?"
                ),
                'reponse': 'louvre',
                'resolu': False,
                'digit_index': 2,
                'digit_value': 5,
            }
        ],
    },
    8: {
        'bg': 3,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'garde',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'traces_sol',
                'x': 600, 'y': 200,
                'largeur': 80, 'hauteur': 80,
                'label': 'Traces au sol',
                'indice': (
                    "Suivez les traces sur le sol jusqu a l objet cache.\n"
                    "Combien de pas avez-vous faits pour le trouver ?"
                ),
                'reponse': '12',
                'resolu': False,
                'digit_index': 3,
                'digit_value': 2,
            }
        ],
    },
    9: {
        'bg': 4,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'tresor',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'equation',
                'x': 700, 'y': 150,
                'largeur': 60, 'hauteur': 130,
                'label': 'Equation facile',
                'indice': (
                    "Resolvez l equation : 4x + 12 = 0\n"
                    "Que vaut x ?"
                ),
                'reponse': '-3',
                'resolu': False,
                'digit_index': 0,
                'digit_value': 8,
            }
        ],
    },
    10: {
        'bg': 5,
        'depart': (100, 300),
        'porte': (1460, 180),
        'code_porte': 'paris',
        'porte_resolue': False,
        'enigmes': [
            {
                'id': 'code_couleur',
                'x': 800, 'y': 220,
                'largeur': 80, 'hauteur': 100,
                'label': 'Code couleur',
                'indice': (
                    "Remettez les couleurs dans l ordre du drapeau francais :\n"
                    "bleu, blanc, rouge"
                ),
                'reponse': 'bleu-blanc-rouge',
                'resolu': False,
                'digit_index': 1,
                'digit_value': 0,
            }
        ],
    },
}

NB_SALLES = len(SALLES)


def draw_text_wrapped(surface, text, x, y, max_width, color=WHITE, font_obj=None):
    if font_obj is None:
        font_obj = pygame.font.Font(None, 28)

    for line in text.split('\n'):
        words = line.split(' ')
        current_line = ''
        for word in words:
            test = current_line + (' ' if current_line else '') + word
            if font_obj.size(test)[0] <= max_width:
                current_line = test
            else:
                if current_line:
                    surface.blit(font_obj.render(current_line, True, color), (x, y))
                    y += font_obj.get_linesize()
                current_line = word
        if current_line:
            surface.blit(font_obj.render(current_line, True, color), (x, y))
            y += font_obj.get_linesize()
    return y


def get_enigme_proche(salle_actuelle, joueur_x, joueur_y):
    salle = SALLES[salle_actuelle]
    joueur_rect = pygame.Rect(joueur_x, joueur_y, 80, 120)

    for enig in salle['enigmes']:
        if not enig['resolu']:
            zone = pygame.Rect(
                enig['x'] - 60,
                enig['y'] - 60,
                enig['largeur'] + 120,
                enig['hauteur'] + 120
            )
            if joueur_rect.colliderect(zone):
                return enig
    return None


def porte_proche(salle_actuelle, joueur_x, joueur_y):
    salle = SALLES[salle_actuelle]
    px, py = salle['porte']
    joueur_rect = pygame.Rect(joueur_x, joueur_y, 80, 120)
    return joueur_rect.colliderect(pygame.Rect(px - 80, py - 60, 240, 250))


def run_game():
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    pygame.display.set_caption("Louvre Escape!")
    clock = pygame.time.Clock()

    font = pygame.font.Font(None, 36)
    font_small = pygame.font.Font(None, 28)
    font_large = pygame.font.Font(None, 64)

    salle_actuelle = 1
    joueur_x, joueur_y = SALLES[1]['depart']
    x_direction = 0
    y_direction = 0
    sprite_courant = sprite_idle

    mode = "exploration"
    enigme_active = None
    saisie = ""
    message_retour = ""
    message_timer = 0
    saisie_porte        = ""
    message_porte       = ""
    message_porte_timer = 0
    restart_message_timer = 0
    restart_message = ""

    net = NetworkRuntime("ws://127.0.0.1:8765", "Joueur")
    net.start()

    def reset_game_local():
        nonlocal salle_actuelle, joueur_x, joueur_y, mode
        nonlocal enigme_active, saisie, message_retour, message_timer
        nonlocal x_direction, y_direction, sprite_courant
        nonlocal restart_message, restart_message_timer
        nonlocal saisie_porte, message_porte, message_porte_timer
        for salle in SALLES.values():
            for e in salle['enigmes']:
                e['resolu'] = False
            salle['porte_resolue'] = False

        salle_actuelle = 1
        joueur_x, joueur_y = SALLES[1]['depart']
        mode = "exploration"
        enigme_active = None
        saisie = ""
        message_retour = ""
        message_timer = 0
        saisie_porte        = ""
        message_porte       = ""
        message_porte_timer = 0
        x_direction = 0
        y_direction = 0
        sprite_courant = sprite_idle
        restart_message = "Un voleur a ete attrape !"
        restart_message_timer = 180

    def passer_salle_suivante():
        nonlocal salle_actuelle, joueur_x, joueur_y, mode
        if salle_actuelle < NB_SALLES:
            salle_actuelle += 1
            joueur_x, joueur_y = SALLES[salle_actuelle]['depart']
            play_sound(son_porte)
        else:
            mode = "victoire"

    def valider_reponse():
        nonlocal saisie, message_retour, message_timer, mode, enigme_active

        if enigme_active is None:
            return

        if saisie.strip().lower() == enigme_active['reponse'].lower():
            enigme_active['resolu'] = True
            message_retour = "Bonne reponse ! Enigme resolue."
            message_timer = 120
            play_sound(son_succes)

            net.send_puzzle_solved(
                enigme_active['id'],
                enigme_active['digit_index'],
                enigme_active['digit_value']
            )
        else:
            message_retour = "Mauvaise reponse... Reessaie."
            message_timer = 90

        saisie = ""
    def valider_code_porte():
        nonlocal saisie_porte, message_porte, message_porte_timer
        salle = SALLES[salle_actuelle]
        if saisie_porte.strip().lower() == salle['code_porte'].lower():
            message_porte = "Bonne reponse ! Porte ouverte."
            message_porte_timer = 120
            salle['porte_resolue'] = True
        else:
            message_porte = "Mauvais code... Reessaie."
            message_porte_timer = 90
        saisie_porte = ""

    def draw_hud():
        txt = font_small.render(
            f"Salle {salle_actuelle} / {NB_SALLES}   |   Fleches : bouger   E : interagir",
            True,
            (220, 220, 180)
        )
        screen.blit(txt, (10, 10))

        code_digits = [None, None, None, None]
        if net.client:
            code_digits = net.client.level_state.get("code_digits", [None, None, None, None])

        code_text = "CODE : " + " ".join(f"[{d if d is not None else '_'}]" for d in code_digits)
        code_surface = font_small.render(code_text, True, GOLD)
        code_rect = code_surface.get_rect(topright=(WIDTH - 20, 10))
        screen.blit(code_surface, code_rect)

        if restart_message_timer > 0:
            msg = font.render(restart_message, True, RED)
            msg_rect = msg.get_rect(center=(WIDTH // 2, 40))
            screen.blit(msg, msg_rect)

    def draw_objects():
        salle = SALLES[salle_actuelle]
        for enig in salle['enigmes']:
            color = (0, 180, 0) if enig['resolu'] else (200, 150, 0)
            pygame.draw.rect(
                screen,
                color,
                [enig['x'], enig['y'], enig['largeur'], enig['hauteur']],
                3,
                6
            )
            lbl = font_small.render(enig['label'], True, color)
            screen.blit(lbl, (enig['x'], enig['y'] - 22))

    def draw_door():
        salle = SALLES[salle_actuelle]
        px, py = salle['porte']
        all_solved = all(e['resolu'] for e in salle['enigmes'])
        color = (0, 220, 50) if all_solved else (120, 60, 60)
        pygame.draw.rect(screen, color, [px, py, 80, 130], 0, 8)
        pygame.draw.rect(screen, WHITE, [px, py, 80, 130], 2, 8)
        lbl = font_small.render("SORTIE" if all_solved else "Verrouillee", True, WHITE)
        screen.blit(lbl, (px - 5, py - 24))

    def draw_interaction_hints():
        joueur_rect = pygame.Rect(joueur_x, joueur_y, 80, 120)
        salle = SALLES[salle_actuelle]

        for enig in salle['enigmes']:
            if not enig['resolu']:
                zone = pygame.Rect(
                    enig['x'] - 60,
                    enig['y'] - 60,
                    enig['largeur'] + 120,
                    enig['hauteur'] + 120
                )
                if joueur_rect.colliderect(zone):
                    hint = font_small.render("E — Examiner", True, YELLOW)
                    screen.blit(hint, (joueur_x - 20, joueur_y - 36))

        px, py = salle['porte']
        porte_zone = pygame.Rect(px - 80, py - 60, 240, 250)
        if joueur_rect.colliderect(porte_zone):
            all_solved = all(e['resolu'] for e in salle['enigmes'])
            if all_solved:
                hint = font_small.render("E — Salle suivante", True, GREEN)
            else:
                hint = font_small.render("Resous les enigmes d abord !", True, RED)
            screen.blit(hint, (joueur_x - 40, joueur_y - 36))

    def draw_player():
        screen.blit(sprite_courant, (joueur_x, joueur_y))

    def draw_other_players():
        if not net.client:
            return

        for pid, pdata in net.client.players_state.items():
            if pid == net.client.player_id:
                continue

            other_room = int(pdata.get("room", 1))
            if other_room != salle_actuelle:
                continue

            x = int(pdata.get("x", 0))
            y = int(pdata.get("y", 0))

            screen.blit(sprite_idle, (x, y))
            pygame.draw.rect(screen, BLUE, (x, y, 80, 120), 2)

            name = pdata.get("name", "Allie")
            lbl = font_small.render(name, True, BLUE)
            screen.blit(lbl, (x, y - 20))

    def draw_enigme_panel():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH // 2 - 380, HEIGHT // 2 - 180, 760, 360)
        pygame.draw.rect(screen, (30, 25, 45), panel, border_radius=14)
        pygame.draw.rect(screen, (180, 150, 80), panel, 2, border_radius=14)

        titre = font.render(f"— {enigme_active['label']} —", True, GOLD)
        screen.blit(titre, (panel.x + panel.w // 2 - titre.get_width() // 2, panel.y + 18))

        draw_text_wrapped(
            screen,
            enigme_active['indice'],
            panel.x + 30,
            panel.y + 70,
            panel.w - 60,
            color=(210, 210, 210),
            font_obj=font_small
        )

        if message_timer > 0:
            ok = message_retour.startswith("Bonne")
            col = GREEN if ok else RED
            msg = font.render(message_retour, True, col)
            screen.blit(msg, (panel.x + panel.w // 2 - msg.get_width() // 2, panel.y + 200))

        saisie_rect = pygame.Rect(panel.x + 30, panel.y + 240, panel.w - 60, 42)
        pygame.draw.rect(screen, (50, 45, 65), saisie_rect, border_radius=8)
        pygame.draw.rect(screen, GOLD, saisie_rect, 2, border_radius=8)
        saisie_txt = font.render(saisie + "|", True, WHITE)
        screen.blit(saisie_txt, (saisie_rect.x + 10, saisie_rect.y + 8))

        inst = font_small.render("Entree : valider   •   Echap : fermer", True, (140, 140, 140))
        screen.blit(inst, (panel.x + panel.w // 2 - inst.get_width() // 2, panel.y + 300))
    def draw_porte_panel():
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        screen.blit(overlay, (0, 0))

        panel = pygame.Rect(WIDTH//2 - 380, HEIGHT//2 - 180, 760, 360)
        pygame.draw.rect(screen, (30, 25, 45), panel, border_radius=14)
        pygame.draw.rect(screen, (180, 150, 80), panel, 2, border_radius=14)

        titre = font.render("— PORTE DE SORTIE —", True, GOLD)
        screen.blit(titre, (panel.x + panel.w//2 - titre.get_width()//2, panel.y + 18))

        indice = font_small.render("Entrez le code pour ouvrir la porte :", True, (210, 210, 210))
        screen.blit(indice, (panel.x + 30, panel.y + 70))

        if message_porte_timer > 0:
            ok = message_porte.startswith("Bonne")
            col = GREEN if ok else RED
            msg = font.render(message_porte, True, col)
            screen.blit(msg, (panel.x + panel.w//2 - msg.get_width()//2, panel.y + 200))

        saisie_rect = pygame.Rect(panel.x + 30, panel.y + 240, panel.w - 60, 42)
        pygame.draw.rect(screen, (50, 45, 65), saisie_rect, border_radius=8)
        pygame.draw.rect(screen, GOLD, saisie_rect, 2, border_radius=8)
        saisie_txt = font.render(saisie_porte + "|", True, WHITE)
        screen.blit(saisie_txt, (saisie_rect.x + 10, saisie_rect.y + 8))

        inst = font_small.render("Entree : valider   •   Echap : fermer", True, (140, 140, 140))
        screen.blit(inst, (panel.x + panel.w//2 - inst.get_width()//2, panel.y + 300))
    def draw_victoire():
        screen.blit(backgrounds[5], (0, 0))
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 160))
        screen.blit(overlay, (0, 0))

        titre = font_large.render("EVASION REUSSIE !", True, (255, 220, 50))
        screen.blit(titre, (WIDTH // 2 - titre.get_width() // 2, HEIGHT // 2 - 80))
        
        sub = font.render(
            "Tu as resolu toutes les enigmes et quitte le Louvre !",
            True,
            (220, 220, 220)
        )
        screen.blit(sub, (WIDTH // 2 - sub.get_width() // 2, HEIGHT // 2))
        


    run = True
    while run:
        clock.tick(FPS)

        if restart_message_timer > 0:
            restart_message_timer -= 1

        if net.client and net.client.last_event:
            event = net.client.last_event
            if event["type"] == "level_restart":
                reset_game_local()
                net.client.last_event = None
            elif event["type"] == "code_update":
                for salle in SALLES.values():
                    for enig in salle["enigmes"]:
                        if enig["id"] == event["puzzle_id"]:
                            enig["resolu"] = True
                net.client.last_event = None

        screen.blit(backgrounds[SALLES[salle_actuelle]['bg']], (0, 0))

        if mode == "victoire":
            draw_victoire()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    reset_game_local()
            pygame.display.flip()
            continue

        draw_door()
        draw_objects()
        draw_player()
        draw_other_players()
        draw_interaction_hints()
        draw_hud()

        if mode == "enigme":
            draw_enigme_panel()
            if message_timer > 0:
                message_timer -= 1
                if message_timer == 0 and enigme_active and enigme_active['resolu']:
                    mode = "exploration"
                    enigme_active = None

        if mode == "porte":
            draw_porte_panel()
            if message_porte_timer > 0:
                message_porte_timer -= 1
                if message_porte_timer == 0 and SALLES[salle_actuelle]['porte_resolue']:
                    passer_salle_suivante()
                    mode = "exploration"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if mode == "enigme":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mode = "exploration"
                        enigme_active = None
                        saisie = ""
                    elif event.key == pygame.K_RETURN:
                        valider_reponse()
                    elif event.key == pygame.K_BACKSPACE:
                        saisie = saisie[:-1]
                    elif event.unicode and event.unicode.isprintable() and len(saisie) < 30:
                        saisie += event.unicode

            elif mode == "porte":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        mode = "exploration"
                        saisie_porte = ""
                    elif event.key == pygame.K_RETURN:
                        valider_code_porte()
                    elif event.key == pygame.K_BACKSPACE:
                        saisie_porte = saisie_porte[:-1]
                    elif event.unicode and event.unicode.isprintable() and len(saisie_porte) < 30:
                        saisie_porte += event.unicode

            elif mode == "exploration":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        enig = get_enigme_proche(salle_actuelle, joueur_x, joueur_y)
                        if enig:
                            enigme_active = enig
                            saisie = ""
                            message_retour = ""
                            message_timer = 0
                            mode = "enigme"
                        elif porte_proche(salle_actuelle, joueur_x, joueur_y):
                            salle = SALLES[salle_actuelle]
                            if all(e['resolu'] for e in salle['enigmes']):
                                if salle['porte_resolue']:
                                    passer_salle_suivante()
                                else:
                                    mode = "porte"
                                    saisie_porte = ""
                                    message_porte = ""
                                    message_porte_timer = 0
                    elif event.key == pygame.K_RIGHT:
                        x_direction = 1;  sprite_courant = sprite_right
                    elif event.key == pygame.K_LEFT:
                        x_direction = -1; sprite_courant = sprite_left
                    elif event.key == pygame.K_UP:
                        y_direction = -1
                    elif event.key == pygame.K_DOWN:
                        y_direction = 1
                    elif event.key == pygame.K_c:
                        net.send_player_caught("Attrape par le policier")

                elif event.type == pygame.KEYUP:
                    if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                        x_direction = 0;  sprite_courant = sprite_idle
                    if event.key in (pygame.K_UP, pygame.K_DOWN):
                        y_direction = 0

        if mode == "exploration":
            joueur_x = max(0, min(WIDTH - 80,  joueur_x + VITESSE_JOUEUR * x_direction))
            joueur_y = max(0, min(HEIGHT - 120, joueur_y + VITESSE_JOUEUR * y_direction))
            net.send_position(joueur_x, joueur_y, salle_actuelle)

        pygame.display.flip()

    pygame.quit()
    sys.exit()

