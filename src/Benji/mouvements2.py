import pygame
import random
pygame.init()
WIDTH = 1588
HEIGHT = 479
screen = pygame.display.set_mode([WIDTH, HEIGHT])

background = pygame.image.load("../../assets/images/background2.png")
background = background.convert()
background_niveau2 = pygame.image.load("../../assets/images/background3.png").convert()
current_background = background
icon = pygame.image.load("../../assets/images/louvre_escape_logo.png")
pygame.display.set_icon(icon)
font = pygame.font.Font(None, 36)
pygame. display.set_caption('Louvre Escape!')
pygame.mixer.init()
pygame.mixer.music.load("../../assets/music/musique.mp3")
x_direction = 0
y_direction = 0
timer = pygame.time. Clock()
fps = 60
joueur_x = 300
joueur_y = 300
vitesse_joueur = 10
one = False
two = False
three = True
vitesse_opps = 10
obstacles = [WIDTH - 100, WIDTH + 100, WIDTH + 300]
perso_1 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite.png"),(80,120))
perso_2 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite2.png"),(80,120))
perso_3 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite3.png"),(80,120))
perso_4 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite4.png"),(80,120))
image = perso_1
niveau = 1
porte_x = 1200
porte_y = 190
porte_largeur = 100
porte_hauteur = 150


def dessiner_joueur():
    pygame.draw.rect(screen, 'blue', [joueur_x, joueur_y, 100, 100], 0, 5)

def draw_world():
    pygame.draw.rect(screen,'blue',[0, HEIGHT-100, WIDTH, 100])
    for i in range(len(obstacles)):
        pygame.draw.rect(screen, 'red', [obstacles[i], HEIGHT-150, 40, 50])

def draw_pnj():
    #pygame.draw.rect(screen, 'blue', [0, HEIGHT - 100, WIDTH, 100])
    screen.blit(image, (joueur_x, joueur_y))

def check_near_door():
    """Vérifie si le joueur est proche de la porte"""
    distance_x = abs(joueur_x - porte_x)
    distance_y = abs(joueur_y - porte_y)
    return distance_x < 100 and distance_y < 100

def draw_interaction_prompt():
    """Affiche le message 'Appuie sur E' si proche de la porte"""
    if check_near_door() and niveau == 1:
        text = font.render("Appuie sur E pour ouvrir", True, (255, 255, 0))
        screen.blit(text, (joueur_x - 50, joueur_y - 50))    

run = True
while run:
    timer.tick(fps)
    screen.blit(current_background,(0,0))
    #if one or two:
     #   dessiner_joueur()
    if two:
        draw_world()
    if three:
        draw_pnj()
        draw_interaction_prompt()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e and check_near_door() and niveau == 1:
                # Changer de niveau
                niveau = 2
                current_background = background_niveau2
                joueur_x = 100 # Réinitialiser la position du joueur
                joueur_y = 300
                print("Porte ouverte ! Niveau 2") 
            elif event.key == pygame.K_m:
                pygame.mixer.music.play()
            elif event.key == pygame.K_l:
                pygame.mixer.music.stop()  
            
        if one or three:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_direction = 1
                elif event.key == pygame.K_LEFT:
                    x_direction = -1
                elif event.key == pygame.K_UP:
                    y_direction = -1
                if event.key == pygame.K_DOWN:
                    y_direction = 1
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    x_direction = 0
                elif event.key == pygame.K_LEFT:
                    x_direction = 0
                elif event.key == pygame.K_UP:
                    y_direction = 0
                if event.key == pygame.K_DOWN:
                    y_direction = 0
        elif two:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    x_direction = 1
                elif event.key == pygame.K_LEFT:
                    x_direction = -1

                
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    x_direction = 0
                elif event.key == pygame.K_LEFT:
                    x_direction = 0
                
    if one or three:
        joueur_x += vitesse_joueur * x_direction
        joueur_y += vitesse_joueur * y_direction
    
    if two:
        for j in range(len(obstacles)):
            obstacles[j] -= vitesse_opps * x_direction
            if obstacles[j]<-300:
                obstacles[j] = WIDTH + random.randint(0,300)
            elif obstacles[j] > WIDTH + 300:
                obstacles[j] = WIDTH + random.randint(-300, 0)
        
    pygame.display.flip()
pygame.quit()
