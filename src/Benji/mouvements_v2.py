import copy
import math
import pygame
import sys


def _draw_heart(surf, color, cx, cy, size, filled=True):
    r = size
    w = 0 if filled else 2
    pygame.draw.circle(surf, color, (cx - r // 2, cy - r // 4), r // 2 + 1, w)
    pygame.draw.circle(surf, color, (cx + r // 2, cy - r // 4), r // 2 + 1, w)
    pts = [(cx - r, cy - r // 4), (cx + r, cy - r // 4), (cx, cy + r * 3 // 4)]
    pygame.draw.polygon(surf, color, pts, w)

from src.Joaquim.network.runtime import NetworkRuntime
from src.Joaquim.ai.ai_manager import AIManager


class _DummyClient:
    last_event    = None
    players_state = {}
    player_id     = None


class _DummyRuntime:
    client = _DummyClient()
    def send_position(self, *a):       pass
    def send_puzzle_solved(self, *a):  pass
    def send_player_caught(self, *a):  pass
    def send_team_lose_life(self, *a): pass
    def start(self):                   pass

# --- Constantes ---
WIDTH, HEIGHT = 1588, 479
FPS = 60
VITESSE_JOUEUR = 3
GRAVITY   = 0.5
FLOOR_Y   = HEIGHT - 140
JUMP_VEL  = -9

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


def _load_bg_safe(path, fallback_color):
    try:
        return load_bg(path)
    except Exception:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill(fallback_color)
        return s


def _load_bg_egypt(path, ceiling_color):
    try:
        img = pygame.image.load(path).convert()
        img_w, img_h = img.get_size()
        new_h = int(img_h * WIDTH / img_w)
        scaled = pygame.transform.scale(img, (WIDTH, max(new_h, 1)))
        surf = pygame.Surface((WIDTH, HEIGHT))
        surf.fill(ceiling_color)
        oy = max(0, HEIGHT - new_h)
        surf.blit(scaled, (0, oy))
        return surf
    except Exception:
        s = pygame.Surface((WIDTH, HEIGHT))
        s.fill(ceiling_color)
        return s

try:
    sprite_idle  = load_img('assets/images/sprite2.png', (90, 135))
    sprite_right = load_img('assets/images/sprite2.png', (90, 135))
    sprite_left  = load_img('assets/images/sprite2.png', (90, 135))
except Exception as e:
    print(f"[AVERTISSEMENT] Sprite manquant : {e}")
    sprite_idle  = pygame.Surface((90, 135)); sprite_idle.fill((100, 180, 255))
    sprite_right = sprite_idle
    sprite_left  = sprite_idle

backgrounds = {
    1: _load_bg_safe('assets/images/background2.png',  (20, 20, 40)),
    2: _load_bg_safe('assets/images/background3.png',  (30, 20, 20)),
    3: _load_bg_safe('assets/images/background2.png',  (20, 30, 20)),
    4: _load_bg_safe('assets/images/background3.png',  (20, 20, 50)),
    5: _load_bg_safe('assets/images/background2.png',  (40, 20, 20)),
    6: _load_bg_egypt('assets/images/bg_egypt_1.png',   (15, 10,  5)),
    7: _load_bg_egypt('assets/images/bg_egypt_2.png',   (15, 10,  5)),
    8: _load_bg_egypt('assets/images/bg_egypt_3.png',   (15, 10,  5)),
    9: _load_bg_egypt('assets/images/bg_egypt_4.png',   (15, 10,  5)),
   10: _load_bg_egypt('assets/images/bg_egypt_5.png',   (15, 10,  5)),
}

from src.audio import audio_manager as audio

def play_sound(name):
    audio.play_sfx(name)


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
    pygame.init()
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
            play_sound('porte')
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
            play_sound('succes')

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



class GameSession:
    def __init__(self, screen, manager=None, character=None, level_id=1,
                 net_uri=None, player_name='Joueur'):
        from src.data.levels import get_room, get_nb_rooms
        self._get_room   = get_room
        self._get_nb_rooms = get_nb_rooms
        self.screen    = screen
        self.manager   = manager
        self.character = character
        self.level_id  = level_id
        self.W = WIDTH
        self.H = HEIGHT
        self.font       = pygame.font.Font(None, 34)
        self.font_small = pygame.font.Font(None, 26)
        self.font_large = pygame.font.Font(None, 60)
        self.backgrounds = backgrounds
        self.game_surf = pygame.Surface((WIDTH, HEIGHT))
        self.nb_salles = self._get_nb_rooms(level_id)
        self.salle_actuelle = 1
        self._load_salle(1)
        self.x_direction = 0
        self.vel_y       = 0
        self.on_ground   = True
        self._load_character_sprite()
        self.mode          = 'exploration'
        self.enigme_active = None
        self.saisie        = ''
        self.message_retour      = ''
        self.message_timer       = 0
        self.saisie_porte        = ''
        self.message_porte       = ''
        self.message_porte_timer = 0
        self.restart_message_timer = 0
        self.restart_message     = ''
        self._ghost_cache = {}
        if net_uri:
            sprite_path = character['sprite'] if character else ''
            self.net = NetworkRuntime(net_uri, player_name, player_sprite=sprite_path)
            self.net.start()
        else:
            self.net = _DummyRuntime()
        self.lives = character['lives'] if character else 4
        self.max_lives = self.lives
        self.invincible_timer = 0
        self.catch_msg_timer  = 0
        self._player_dialog      = ''
        self._player_dialog_timer = 0
        self._next_player_dialog  = 300
        self._player_dialogs = self._build_dialogs()
        self.ai_manager = AIManager(self.level_id, 1)
        self._reward_popup = None
        self._music_state = None
        audio.init()
        self._update_music()

    def _load_character_sprite(self):
        ch = self.character
        if ch:
            try:
                img = pygame.image.load(ch['sprite']).convert_alpha()
                self._spr_idle  = pygame.transform.scale(img, (90, 135))
                self._spr_right = self._spr_idle
                self._spr_left  = pygame.transform.flip(self._spr_idle, True, False)
                self.sprite_courant = self._spr_idle
                return
            except Exception:
                pass
        self._spr_idle  = sprite_idle
        self._spr_right = sprite_right
        self._spr_left  = sprite_left
        self.sprite_courant = sprite_idle

    def _load_salle(self, room_id):
        room = self._get_room(self.level_id, room_id)
        if room is None:
            return
        self.salle_data  = room
        self.joueur_x    = room['depart'][0]
        self.joueur_y    = FLOOR_Y
        self.vel_y       = 0
        self.on_ground   = True

    def _build_dialogs(self):
        ch_id = self.character.get('id', 'balanced') if self.character else 'balanced'
        base = {
            'smart':    ['Analysons ca.', 'Il y a une logique...', 'Interessant.', 'Anne reflechit.'],
            'balanced': ['Prudence.', 'Restons calmes.', 'On avance.', 'Pas de panique.'],
            'discreet': ['Chut !', 'Pas de bruit.', 'On reste dans l ombre.', 'Sophie veille.'],
        }
        return base.get(ch_id, base['balanced'])

    def _vitesse(self):
        if self.character:
            return int(VITESSE_JOUEUR * self.character.get('speed_mult', 1.0))
        return VITESSE_JOUEUR

    def _stealth_mult(self):
        if self.character:
            return self.character.get('stealth_mult', 1.0)
        return 1.0

    def _update_music(self):
        if self.lives <= 1:
            state = audio.MUSIC_CRITICAL
        elif self.invincible_timer > 0:
            state = audio.MUSIC_TENSE
        else:
            state = audio.MUSIC_CALM
        if state != self._music_state:
            self._music_state = state
            audio.play_music(state)

    def reset(self):
        self.salle_actuelle = 1
        self._load_salle(1)
        self.mode = 'exploration'
        self.enigme_active = None
        self.saisie = ''
        self.message_retour = ''
        self.message_timer = 0
        self.saisie_porte = ''
        self.message_porte = ''
        self.message_porte_timer = 0
        self.x_direction = 0
        self.vel_y       = 0
        self.on_ground   = True
        self._load_character_sprite()
        self.restart_message       = 'Un voleur a ete attrape !'
        self.restart_message_timer = 180
        self.lives = self.character['lives'] if self.character else 4
        self.invincible_timer = 0
        self.catch_msg_timer  = 0
        self._reward_popup = None
        self.ai_manager = AIManager(self.level_id, 1)

    def passer_salle_suivante(self):
        if self.salle_actuelle < self.nb_salles:
            self.salle_actuelle += 1
            self._load_salle(self.salle_actuelle)
            self.ai_manager = AIManager(self.level_id, self.salle_actuelle)
            play_sound('porte')
        else:
            from src.Cynthia.level_select import unlock_next_level
            unlock_next_level(self.level_id)
            self.mode = 'victoire'

    def valider_reponse(self):
        if self.enigme_active is None:
            return
        if self.saisie.strip().lower() == self.enigme_active['reponse'].lower():
            self.enigme_active['resolu'] = True
            self.message_retour = 'Bonne reponse ! Enigme resolue.'
            self.message_timer  = 120
            play_sound('succes')
            audio.play_sfx('bijou')
            bijou = self.enigme_active.get('bijou', 'Bijou mysterieux')
            from src.Cynthia.reward_popup import RewardPopup
            self._reward_popup = RewardPopup(bijou)
            self.net.send_puzzle_solved(
                self.enigme_active['id'],
                self.enigme_active['digit_index'],
                self.enigme_active['digit_value']
            )
        else:
            self.message_retour = 'Mauvaise reponse... Reessaie.'
            self.message_timer  = 90
        self.saisie = ''

    def _get_revealed_code_digits(self):
        code    = self.salle_data.get('code_porte', '0000')
        enigmes = self.salle_data['enigmes']
        n       = len(enigmes)
        revealed = ['_', '_', '_', '_']
        for i, e in enumerate(enigmes):
            if e.get('resolu'):
                if n <= 2:
                    p1, p2 = i * 2, i * 2 + 1
                    if p1 < len(code): revealed[p1] = code[p1]
                    if p2 < len(code): revealed[p2] = code[p2]
                else:
                    if i < len(code): revealed[i] = code[i]
        return revealed

    def valider_code_porte(self):
        salle    = self.salle_data
        code_ok  = salle.get('code_porte', '0000')
        if self.saisie_porte.strip() == code_ok:
            self.message_porte       = f'Code {code_ok} correct ! Porte ouverte !'
            self.message_porte_timer = 120
            salle['porte_resolue']   = True
        else:
            self.message_porte       = 'Code incorrect... Reessaie.'
            self.message_porte_timer = 90
        self.saisie_porte = ''

    def lose_life(self, broadcast=True):
        if self.invincible_timer > 0:
            return
        self.lives -= 1
        self.invincible_timer = 180
        self.catch_msg_timer  = 120
        audio.play_sfx('vie_perdue')
        self.ai_manager.reset()
        if broadcast:
            pid = self.net.client.player_id if self.net.client else None
            if pid:
                self.net.send_team_lose_life(pid)
        if self.lives <= 0:
            audio.play_music(audio.MUSIC_GAMEOVER)
            if self.manager:
                from src.Maroua.game_over import GameOver
                self.manager.scene = GameOver(self.screen, self.manager)

    def get_enigme_proche(self):
        salle = self.salle_data
        player_cx = self.joueur_x + 45
        for enig in salle['enigmes']:
            if not enig['resolu']:
                enigme_cx = enig['x'] + enig['largeur'] // 2
                if abs(player_cx - enigme_cx) <= 100:
                    return enig
        return None

    def porte_proche(self):
        salle = self.salle_data
        px, py = salle['porte']
        joueur_rect = pygame.Rect(self.joueur_x, self.joueur_y, 90, 135)
        return joueur_rect.colliderect(pygame.Rect(px - 100, py - 80, 280, 500))

    def handle_event(self, event):
        if self._reward_popup and not self._reward_popup.is_done():
            self._reward_popup.handle_event(event)
            return
        if self.mode == 'enigme':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mode = 'exploration'
                    self.enigme_active = None
                    self.saisie = ''
                elif event.key == pygame.K_RETURN:
                    self.valider_reponse()
                elif event.key == pygame.K_BACKSPACE:
                    self.saisie = self.saisie[:-1]
                elif event.unicode and event.unicode.isprintable() and len(self.saisie) < 30:
                    self.saisie += event.unicode
        elif self.mode == 'porte':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.mode = 'exploration'
                    self.saisie_porte = ''
                elif event.key == pygame.K_RETURN:
                    self.valider_code_porte()
                elif event.key == pygame.K_BACKSPACE:
                    self.saisie_porte = self.saisie_porte[:-1]
                elif event.unicode and event.unicode.isprintable() and len(self.saisie_porte) < 30:
                    self.saisie_porte += event.unicode
        elif self.mode == 'exploration':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    enig = self.get_enigme_proche()
                    if enig:
                        self.enigme_active  = enig
                        self.saisie         = ''
                        self.message_retour = ''
                        self.message_timer  = 0
                        self.mode = 'enigme'
                    elif self.porte_proche():
                        salle = self.salle_data
                        if all(e['resolu'] for e in salle['enigmes']):
                            if salle['porte_resolue']:
                                self.passer_salle_suivante()
                            else:
                                self.mode = 'porte'
                                self.saisie_porte        = ''
                                self.message_porte       = ''
                                self.message_porte_timer = 0
                elif event.key == pygame.K_RIGHT:
                    self.x_direction = 1;  self.sprite_courant = self._spr_right
                elif event.key == pygame.K_LEFT:
                    self.x_direction = -1; self.sprite_courant = self._spr_left
                elif event.key == pygame.K_SPACE:
                    if self.on_ground:
                        self.vel_y     = JUMP_VEL
                        self.on_ground = False
                elif event.key == pygame.K_c:
                    self.net.send_player_caught('Attrape par le policier')
            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT):
                    self.x_direction = 0;  self.sprite_courant = self._spr_idle
        elif self.mode == 'victoire':
            pass  # boutons gérés dans jeu.py

    def update(self, dt=1/60):
        if self._reward_popup and not self._reward_popup.is_done():
            self._reward_popup.update()
            return
        if self.restart_message_timer > 0:
            self.restart_message_timer -= 1
        if self.invincible_timer > 0:
            self.invincible_timer -= 1
        if self.catch_msg_timer > 0:
            self.catch_msg_timer -= 1
        if self.net.client and self.net.client.last_event:
            evt = self.net.client.last_event
            if evt['type'] == 'level_restart':
                self.reset()
                self.net.client.last_event = None
            elif evt['type'] == 'code_update':
                for enig in self.salle_data['enigmes']:
                    if enig['id'] == evt['puzzle_id']:
                        enig['resolu'] = True
                self.net.client.last_event = None
            elif evt['type'] == 'team_lose_life':
                self.lose_life(broadcast=False)
                self.net.client.last_event = None
        if self.mode == 'enigme':
            if self.message_timer > 0:
                self.message_timer -= 1
                if self.message_timer == 0 and self.enigme_active and self.enigme_active['resolu']:
                    self.mode = 'exploration'
                    self.enigme_active = None
        elif self.mode == 'porte':
            if self.message_porte_timer > 0:
                self.message_porte_timer -= 1
                if self.message_porte_timer == 0 and self.salle_data['porte_resolue']:
                    self.passer_salle_suivante()
                    self.mode = 'exploration'
        elif self.mode == 'exploration':
            self.joueur_x = max(0, min(self.W - 80, self.joueur_x + self._vitesse() * self.x_direction))
            self.vel_y    += GRAVITY
            self.joueur_y += self.vel_y
            if self.joueur_y >= FLOOR_Y:
                self.joueur_y  = FLOOR_Y
                self.vel_y     = 0
                self.on_ground = True
            else:
                self.on_ground = False
            self.net.send_position(self.joueur_x, self.joueur_y, self.salle_actuelle)
            if self.ai_manager:
                cam_pos = pygame.Vector2(self.joueur_x + 45, self.joueur_y + 67)
                cop_pos = pygame.Vector2(self.joueur_x + 45, self.joueur_y + 10)
                caught, _, _ = self.ai_manager.update(cam_pos, dt, cop_pos)
                if caught:
                    self.lose_life()
        if self._player_dialog_timer > 0:
            self._player_dialog_timer -= 1
        if self.mode == 'exploration' and self.invincible_timer == 0:
            self._next_player_dialog -= 1
            if self._next_player_dialog <= 0:
                import random as _r
                self._player_dialog       = _r.choice(self._player_dialogs)
                self._player_dialog_timer = 90
                self._next_player_dialog  = _r.randint(400, 700)
        self._update_music()

    def draw(self):
        _real = self.screen
        self.screen = self.game_surf
        self.screen.blit(self.backgrounds[self.salle_data['bg']], (0, 0))
        if self.mode == 'victoire':
            self._draw_victoire()
        else:
            self._draw_door()
            self._draw_objects()
            self.ai_manager.draw(self.screen)
            self._draw_player()
            self._draw_other_players()
            self._draw_interaction_hints()
            self._draw_hud()
            if self.mode == 'enigme':
                self._draw_enigme_panel()
            elif self.mode == 'porte':
                self._draw_porte_panel()
        self.screen = _real
        sw, sh = self.screen.get_size()
        game_ratio   = WIDTH / HEIGHT
        screen_ratio = sw / sh
        if screen_ratio > game_ratio:
            scale_h = sh
            scale_w = int(sh * game_ratio)
        else:
            scale_w = sw
            scale_h = int(sw / game_ratio)
        ox = (sw - scale_w) // 2
        oy = (sh - scale_h) // 2
        self.screen.fill((0, 0, 0))
        self.screen.blit(pygame.transform.scale(self.game_surf, (scale_w, scale_h)), (ox, oy))
        if self._reward_popup and not self._reward_popup.is_done():
            self._reward_popup.draw(self.screen)

    def _draw_hud(self):
        # ── Bande HUD en haut ──────────────────────────────────────────
        hud_h = 38
        hud_bg = pygame.Surface((self.W, hud_h), pygame.SRCALPHA)
        hud_bg.fill((10, 8, 6, 180))
        self.screen.blit(hud_bg, (0, 0))

        # Salle info (gauche)
        txt = self.font_small.render(
            f'Salle  {self.salle_actuelle} / {self.nb_salles}',
            True, (210, 200, 160)
        )
        self.screen.blit(txt, (12, (hud_h - txt.get_height()) // 2))

        # Code (droite)
        digits  = self._get_revealed_code_digits()
        box_w, box_h = 26, 26
        gap     = 4
        label   = self.font_small.render('CODE', True, GOLD)
        lw      = label.get_width()
        total_w = lw + 10 + 4 * box_w + 3 * gap
        lx      = self.W - 14 - total_w
        ly      = (hud_h - box_h) // 2
        self.screen.blit(label, (lx, ly + (box_h - label.get_height()) // 2))
        for i, d in enumerate(digits):
            bx      = lx + lw + 10 + i * (box_w + gap)
            by      = ly
            revealed = d != '_'
            pygame.draw.rect(self.screen,
                             (42, 32, 10) if revealed else (18, 16, 10),
                             (bx, by, box_w, box_h), border_radius=4)
            pygame.draw.rect(self.screen,
                             GOLD if revealed else (65, 52, 22),
                             (bx, by, box_w, box_h), 2, border_radius=4)
            if revealed:
                ds = self.font_small.render(d, True, GOLD)
                self.screen.blit(ds, ds.get_rect(center=(bx + box_w // 2, by + box_h // 2)))

        # Vies (centre)
        heart_gap = 34
        hx = self.W // 2 - (4 * heart_gap) // 2 + heart_gap // 2
        for i in range(4):
            color = (220, 50, 50) if i < self.lives else (60, 18, 18)
            _draw_heart(self.screen, color, hx + i * heart_gap, hud_h // 2, 11, filled=True)

        # Message de capture (centré, sous le HUD)
        if self.catch_msg_timer > 0:
            alpha = min(255, self.catch_msg_timer * 4)
            msg   = self.font.render('Didier vous a repere !  -1 vie', True, (255, 80, 80))
            msg.set_alpha(alpha)
            self.screen.blit(msg, msg.get_rect(center=(self.W // 2, 58)))

    def _draw_objects(self):
        salle = self.salle_data
        player_cx = self.joueur_x + 45
        t = pygame.time.get_ticks() / 1000.0
        for enig in salle['enigmes']:
            if enig['resolu']:
                continue
            enigme_cx = enig['x'] + enig['largeur'] // 2
            dist = abs(player_cx - enigme_cx)
            if dist <= 180:
                pulse = 0.5 + 0.5 * math.sin(t * 2.5)
                proximity = max(0.0, 1.0 - dist / 180.0)
                alpha = int((18 + 32 * pulse) * proximity)
                gw = enig['largeur'] + 44
                gh = enig['hauteur'] + 44
                glow = pygame.Surface((gw, gh), pygame.SRCALPHA)
                glow.fill((220, 185, 60, max(0, min(255, alpha))))
                self.screen.blit(glow, (enig['x'] - 22, enig['y'] - 22))

    def _draw_door(self):
        salle = self.salle_data
        px, py = salle['porte']
        player_cx = self.joueur_x + 45
        porte_cx = px + 40
        dist = abs(player_cx - porte_cx)
        if dist > 200:
            return
        all_solved = all(e['resolu'] for e in salle['enigmes'])
        t = pygame.time.get_ticks() / 1000.0
        pulse = 0.4 + 0.6 * math.sin(t * 1.8)
        proximity = max(0.0, 1.0 - dist / 200.0)
        alpha = int(38 * pulse * proximity)
        col = (40, 210, 60, max(0, alpha)) if all_solved else (200, 150, 30, max(0, alpha))
        glow = pygame.Surface((88, 150), pygame.SRCALPHA)
        glow.fill(col)
        self.screen.blit(glow, (px - 3, py - 8))

    def _draw_hint_bubble(self, text, color, cx, y):
        surf = self.font_small.render(text, True, color)
        bw, bh = surf.get_width() + 12, surf.get_height() + 8
        bx, by = cx - bw // 2, y - bh - 4
        bg = pygame.Surface((bw, bh), pygame.SRCALPHA)
        bg.fill((10, 8, 6, 190))
        pygame.draw.rect(bg, (*color, 180), (0, 0, bw, bh), 1, border_radius=5)
        self.screen.blit(bg, (bx, by))
        self.screen.blit(surf, (bx + 6, by + 4))

    def _draw_interaction_hints(self):
        if self._player_dialog_timer > 0:
            return
        salle     = self.salle_data
        player_cx = self.joueur_x + 45
        for enig in salle['enigmes']:
            if not enig['resolu']:
                enigme_cx = enig['x'] + enig['largeur'] // 2
                if abs(player_cx - enigme_cx) <= 80:
                    self._draw_hint_bubble(
                        'E  —  Examiner', (255, 220, 80),
                        player_cx, self.joueur_y)
        px, py    = salle['porte']
        porte_cx  = px + 40
        if abs(player_cx - porte_cx) <= 110:
            all_solved = all(e['resolu'] for e in salle['enigmes'])
            if all_solved:
                self._draw_hint_bubble(
                    'E  —  Salle suivante', (80, 230, 100),
                    player_cx, self.joueur_y)
            else:
                self._draw_hint_bubble(
                    'Resous les enigmes', (220, 80, 80),
                    player_cx, self.joueur_y)

    def _draw_player(self):
        self.screen.blit(self.sprite_courant, (self.joueur_x, self.joueur_y))
        if self._player_dialog_timer > 0 and self._player_dialog:
            font  = self.font_small
            alpha = min(255, self._player_dialog_timer * 6)
            txt   = font.render(self._player_dialog, True, (255, 255, 200))
            bw, bh = txt.get_width() + 14, txt.get_height() + 10
            bx = self.joueur_x + 40 - bw // 2
            by = self.joueur_y - bh - 8
            bubble = pygame.Surface((bw, bh), pygame.SRCALPHA)
            bubble.fill((30, 28, 24, min(200, alpha)))
            pygame.draw.rect(bubble, (196, 166, 114, alpha), (0, 0, bw, bh), 1, border_radius=7)
            self.screen.blit(bubble, (bx, by))
            txt.set_alpha(alpha)
            self.screen.blit(txt, (bx + 7, by + 5))

    def _get_ghost_sprite(self, sprite_path):
        if sprite_path not in self._ghost_cache:
            try:
                img = pygame.image.load(sprite_path).convert_alpha()
                self._ghost_cache[sprite_path] = pygame.transform.scale(img, (90, 135))
            except Exception:
                self._ghost_cache[sprite_path] = self._spr_idle
        return self._ghost_cache[sprite_path]

    def _draw_other_players(self):
        if not self.net.client or not self.net.client.player_id:
            return
        for pid, pdata in self.net.client.players_state.items():
            if pid == self.net.client.player_id:
                continue
            if int(pdata.get('room', 1)) != self.salle_actuelle:
                continue
            x   = int(pdata.get('x', 0))
            y   = int(pdata.get('y', 0))
            spr = self._get_ghost_sprite(pdata.get('sprite', ''))
            ghost = spr.copy()
            ghost.set_alpha(170)
            self.screen.blit(ghost, (x, y))
            pygame.draw.rect(self.screen, (80, 160, 255), (x, y, 90, 135), 2, border_radius=4)
            lbl = self.font_small.render(pdata.get('name', '?'), True, (80, 160, 255))
            self.screen.blit(lbl, lbl.get_rect(midbottom=(x + 45, y - 4)))

    def _draw_enigme_panel(self):
        W, H = self.W, self.H
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(W // 2 - 380, H // 2 - 180, 760, 360)
        pygame.draw.rect(self.screen, (30, 25, 45), panel, border_radius=14)
        pygame.draw.rect(self.screen, (180, 150, 80), panel, 2, border_radius=14)
        label = self.enigme_active['label']
        titre = self.font.render(f'--- {label} ---', True, GOLD)
        self.screen.blit(titre, titre.get_rect(midtop=(panel.centerx, panel.y + 18)))
        draw_text_wrapped(
            self.screen, self.enigme_active['indice'],
            panel.x + 30, panel.y + 70, panel.w - 60,
            color=(210, 210, 210), font_obj=self.font_small
        )
        if self.message_timer > 0:
            col = GREEN if self.message_retour.startswith('Bonne') else RED
            msg = self.font.render(self.message_retour, True, col)
            self.screen.blit(msg, msg.get_rect(midtop=(panel.centerx, panel.y + 200)))
        saisie_rect = pygame.Rect(panel.x + 30, panel.y + 240, panel.w - 60, 42)
        pygame.draw.rect(self.screen, (50, 45, 65), saisie_rect, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, saisie_rect, 2, border_radius=8)
        self.screen.blit(self.font.render(self.saisie + '|', True, WHITE),
                         (saisie_rect.x + 10, saisie_rect.y + 8))
        inst = self.font_small.render('Entree : valider   |   Echap : fermer', True, (140, 140, 140))
        self.screen.blit(inst, inst.get_rect(midtop=(panel.centerx, panel.y + 300)))

    def _draw_porte_panel(self):
        W, H = self.W, self.H
        overlay = pygame.Surface((W, H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 210))
        self.screen.blit(overlay, (0, 0))
        panel = pygame.Rect(W // 2 - 380, H // 2 - 180, 760, 360)
        pygame.draw.rect(self.screen, (30, 25, 45), panel, border_radius=14)
        pygame.draw.rect(self.screen, (180, 150, 80), panel, 2, border_radius=14)
        titre = self.font.render('--- PORTE DE SORTIE ---', True, GOLD)
        self.screen.blit(titre, titre.get_rect(midtop=(panel.centerx, panel.y + 18)))
        revealed   = self._get_revealed_code_digits()
        code_hint  = 'Code collecte : ' + ' '.join(f'[{d}]' for d in revealed)
        hint_surf  = self.font_small.render(code_hint, True, GOLD)
        self.screen.blit(hint_surf, hint_surf.get_rect(midtop=(panel.centerx, panel.y + 68)))
        indice = self.font_small.render('Entrez le code a 4 chiffres :', True, (210, 210, 210))
        self.screen.blit(indice, (panel.x + 30, panel.y + 108))
        if self.message_porte_timer > 0:
            col = GREEN if self.message_porte.startswith('Bonne') else RED
            msg = self.font.render(self.message_porte, True, col)
            self.screen.blit(msg, msg.get_rect(midtop=(panel.centerx, panel.y + 200)))
        saisie_rect = pygame.Rect(panel.x + 30, panel.y + 240, panel.w - 60, 42)
        pygame.draw.rect(self.screen, (50, 45, 65), saisie_rect, border_radius=8)
        pygame.draw.rect(self.screen, GOLD, saisie_rect, 2, border_radius=8)
        self.screen.blit(self.font.render(self.saisie_porte + '|', True, WHITE),
                         (saisie_rect.x + 10, saisie_rect.y + 8))
        inst = self.font_small.render('Entree : valider   |   Echap : fermer', True, (140, 140, 140))
        self.screen.blit(inst, inst.get_rect(midtop=(panel.centerx, panel.y + 300)))

    def _draw_victoire(self):
        overlay = pygame.Surface((self.W, self.H), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 175))
        self.screen.blit(overlay, (0, 0))
        titre = self.font_large.render('EVASION REUSSIE !', True, (255, 220, 50))
        self.screen.blit(titre, titre.get_rect(center=(self.W // 2, self.H // 2 - 90)))
        sub = self.font.render(
            'Tu as resolu toutes les enigmes et quitte le Louvre !',
            True, (220, 220, 220)
        )
        self.screen.blit(sub, sub.get_rect(center=(self.W // 2, self.H // 2 - 30)))
        # Les boutons sont dessinés par jeu.py (coordonnées écran réelles)
