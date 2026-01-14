import pygame
import random
pygame.init()

WIDTH = 800
HEIGHT = 500
icon = pygame.image.load("../../assets/images/louvre_escape_logo.png")
pygame.display.set_icon(icon)
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Louvre Escape!')
x_direction = 0
y_direction = 0
timer = pygame.time. Clock()
fps = 60
joueur_x = 300
joueur_y = 300
vitesse_joueur = 3
one = True
two = True
three = True
vitesse_opps = 10
obstacles = [WIDTH - 100, WIDTH + 100, WIDTH + 300]
perso_1 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite.png"),(80,120))
perso_2 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite2.png"),(80,120))
perso_3 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite3.png"),(80,120))
perso_4 = pygame.transform.scale(pygame.image.load("../../assets/images/sprite4.png"),(80,120))

def dessiner_joueur():
    pygame.draw.rect(screen, 'blue', [joueur_x, joueur_y, 100, 100], 0, 5)

def draw_world():
    pygame.draw.rect(screen,'orange',[0, HEIGHT-100, WIDTH, 100])
    for i in range(len(obstacles)):
        pygame.draw.rect(screen, 'red', [obstacles[i], HEIGHT-150, 40, 50])

def draw_pnj():
    animation_counter = 1
    pygame.draw.rect(screen, 'brown', [0, HEIGHT - 100, WIDTH, 100])
    if x_direction != 0:
        animation_counter += 1
        if animation_counter < 15: 
            image = perso_1
        elif animation_counter < 30:
            image = perso_2
        elif animation_counter < 45:
            image = perso_3
        else:
            image = perso_4
        if x_direction == -1 :
            image = pygame.transform.flip(image, True, False)
    else:
        image = perso_1
    
    if animation_counter >= 60:
        animation_counter = 0
    if joueur_y < HEIGHT - 200:
        image = perso_4
    screen.blit(image, (joueur_x, joueur_y))

        
run = True
while run:
    timer.tick(fps)
    screen.fill('black')
    #if one or two:
     #   dessiner_joueur()
    if two:
        draw_world()
    if three:
        draw_pnj()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
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

