import pygame
import sys 
from fence import Fence
from random import randint

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("defensor")
clock = pygame.time.Clock()
FPS = 60

barrera = Fence("fence.png")
wood = True
stone = False
steel = False

#Variables
bgColor = (1,150, 70)
barrera_rect = barrera.imagen.get_rect()
barrera_rect.center = (width//2,height//2)
angulo = 0
speed = 0.3
x = 0
y = 0
rotate = pygame.transform.rotate(barrera.imagen, angulo)
rotation = 5
barrera_positions = []
placing_barrier = False
counterWood = 0
counterStone = 0
counterSteel = 0
wood = True
stone = False
steel = False
increment_wood = False
increment_Stone = False
increment_Steel = False

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       
        #Evento de rotacion, movimiento, cambio de barrera y posicionamiento 
        keys = pygame.key.get_pressed()
        if keys[pygame.K_q]:
            angulo += rotation
        if keys[pygame.K_e]:
            angulo -= rotation
        if keys[pygame.K_2]:
            stone = True
            wood = False
            steel = False
            nueva_imagen = "stoneF.png"
            barrera.cambiar_imagen(nueva_imagen)
        if keys[pygame.K_3]:
            stone = False
            wood = False
            steel = True
            nueva_imagen = "steelF.png"
            barrera.cambiar_imagen(nueva_imagen)
        if keys[pygame.K_1]:
            stone = False
            wood = True
            steel = False
            nueva_imagen = "fence.png"
            barrera.cambiar_imagen(nueva_imagen)
        if keys[pygame.K_w]:
            y -=10 
        if keys[pygame.K_s]:
            y +=10 
        if keys[pygame.K_a]:
            x -=10 
        if keys[pygame.K_d]:
            x +=10 
        if keys[pygame.K_r]:
            if wood:
                if counterWood < 10:
                    placing_barrier = True
                    barrera_positions.append((x, y, angulo, barrera.imagen))
                    if not increment_wood:
                        counterWood += 1
                        increment_wood = True
                    else:
                        increment_wood = False
            elif stone:
                if counterStone < 10:
                    placing_barrier = True
                    barrera_positions.append((x, y, angulo, barrera.imagen))
                    if not increment_Stone:
                        counterStone += 1
                        increment_Stone = True
                    else:
                        increment_Stone = False
            elif steel:
                if counterSteel < 10:
                    placing_barrier = True
                    barrera_positions.append((x, y, angulo, barrera.imagen))
                    if not increment_Steel:
                        counterSteel += 1
                        increment_Steel = True
                    else:
                        increment_Steel = False
                
    # Dibuja la imagen en la ventana
    screen.fill(bgColor)
    rotate = pygame.transform.rotate(barrera.imagen, angulo)
    rect_rotate = rotate.get_rect(center=(width // 2 + x, height // 2 + y))
    clock.tick(FPS)
    # Dibuja la imagen rotada en la ventana
    screen.blit(rotate, rect_rotate)

    #Coloca la imagen donde el jugador la quiere
    for pos_x, pos_y, pos_angulo, pos_imagen in barrera_positions:
        rotated_barrier = pygame.transform.rotate(pos_imagen, pos_angulo)
        barrier_rect = rotated_barrier.get_rect(center=(width // 2 + pos_x, height // 2 + pos_y))
        screen.blit(rotated_barrier, barrier_rect)
        
    pygame.display.update()