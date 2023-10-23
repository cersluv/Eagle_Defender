import pygame
import sys
from eagle import Aguila
from fence import Fence

# Inicializa Pygame
pygame.init()

# Configuración de la ventana
ventana_ancho = 800
ventana_alto = 600
ventana = pygame.display.set_mode((ventana_ancho, ventana_alto))
reloj = pygame.time.Clock()
pygame.display.set_caption("Aguila en Pygame")

# Variables

rect_width, rect_height = 50, 50
rect_x, rect_y = (ventana_ancho - rect_width) // 2, (ventana_alto - rect_height) // 2
rect_speed = 5




blanco = (255, 255, 255)
aguila = Aguila()
barrera = Fence(50, 50, 1, 0)
aguila_Movement = True
barrera_Movement = False
placing_Barrier = True
barrerasTipo1 = []
barrerasTipo2 = []
barrerasTipo3 = []
barreras = [barrerasTipo1,barrerasTipo2,barrerasTipo3]
se_creo_nueva_barrera = False

# Bucle principal
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    teclas = pygame.key.get_pressed()

    if teclas[pygame.K_LEFT]:
        rect_x -= rect_speed
    if teclas[pygame.K_RIGHT]:
        rect_x += rect_speed
    if teclas[pygame.K_UP]:
        rect_y -= rect_speed
    if teclas[pygame.K_DOWN]:
        rect_y += rect_speed

    rect = pygame.Rect(rect_x, rect_y, rect_width, rect_height)










    if aguila_Movement:
        # Movimiento del aguila
        if teclas[pygame.K_a]:
            aguila.mover(-aguila.velocidad, 0)
        if teclas[pygame.K_d]:
            aguila.mover(aguila.velocidad, 0)
        if teclas[pygame.K_w]:
            aguila.mover(0, -aguila.velocidad)
        if teclas[pygame.K_s]:
            aguila.mover(0, aguila.velocidad)

        # Posicionamiento del aguila
        if teclas[pygame.K_f]:
            aguila_Movement = False
            barrera_Movement = True

    if barrera_Movement:
        # Cambio de barrera
        if teclas[pygame.K_1]:
            barrera = Fence(50, 50, 1, 0)
        elif teclas[pygame.K_2]:
            barrera = Fence(50, 50, 2, 0)
        elif teclas[pygame.K_3]:
            barrera = Fence(50, 50, 3, 0)

        # Rotacion de las barreras
        if teclas[pygame.K_q]:
            barrera.rotar("Q")
        elif teclas[pygame.K_e]:
            barrera.rotar("E")

        # Movimiento de las barreras
        if teclas[pygame.K_w]:
            barrera.mover(0, -barrera.velocidad)
        if teclas[pygame.K_s]:
            barrera.mover(0, barrera.velocidad)
        if teclas[pygame.K_a]:
            barrera.mover(-barrera.velocidad, 0)
        if teclas[pygame.K_d]:
            barrera.mover(barrera.velocidad, 0)
            
        if teclas[pygame.K_r] and not barrera.rect.colliderect(aguila.rect):
            if barrera.tipo == 1:
                if len(barrerasTipo1) == 10:
                    print("Se quedó sin madera")
                else:
                    if not se_creo_nueva_barrera:
                        print(barrera.rect.x, barrera.rect.y, barrera.tipo, barrera.angulo_rotacion)
                        newBarrera = Fence(barrera.rect.x + 50, barrera.rect.y + 25, barrera.tipo, barrera.angulo_rotacion)
                        barrerasTipo1.append(newBarrera)
                        se_creo_nueva_barrera = True
            elif barrera.tipo == 2:
                if len(barrerasTipo2) == 10:
                    print("Se quedó sin acero")
                else:
                    if not se_creo_nueva_barrera:
                        print(barrera.rect.x, barrera.rect.y, barrera.tipo, barrera.angulo_rotacion)
                        newBarrera = Fence(barrera.rect.x + 50, barrera.rect.y + 25, barrera.tipo, barrera.angulo_rotacion)
                        barrerasTipo2.append(newBarrera)
                        se_creo_nueva_barrera = True
            elif barrera.tipo == 3:
                if len(barrerasTipo3) == 10:
                    print("Se quedó sin piedra")
                else:
                    if not se_creo_nueva_barrera:
                        print(barrera.rect.x, barrera.rect.y, barrera.tipo, barrera.angulo_rotacion)
                        newBarrera = Fence(barrera.rect.x + 50, barrera.rect.y + 25, barrera.tipo, barrera.angulo_rotacion)
                        barrerasTipo3.append(newBarrera)
                        se_creo_nueva_barrera = True
        else:
            se_creo_nueva_barrera = False
    

    ventana.fill(blanco)

    pygame.draw.rect(ventana, (0, 128, 255), (rect_x, rect_y, rect_width, rect_height))


    aguila.dibujar(ventana)
    if barrera_Movement:
        barrera.dibujar(ventana)
        for cantBarreras in barreras:
            for cantTipos in cantBarreras:
                cantTipos.dibujar(ventana)
            
                #LOGICA COLLIDE Y DESTRUIR BARRERAS

                if rect.colliderect(cantTipos.rect):
                    if cantTipos.tipo == 1:
                        cantTipos.vidaAgua = 0
                        print(cantTipos.vidaAgua)
                        if cantTipos.vidaAgua == 0:
                            cantBarreras.remove(cantTipos)



    
    reloj.tick(60)
    pygame.display.update()