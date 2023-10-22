import pygame
import sys 
from fence import Fence
from random import randint
from eagle import Eagle

pygame.init()
width, height = 1000, 800
screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("defensor")
clock = pygame.time.Clock()
FPS = 60

barrera = Fence("fence.png")
eagle = Eagle("eagle.png")

#Variables
bgColor = (1,150, 70)
x = 0
y = 0
barrera_rect = barrera.imagen.get_rect(topleft=(x, y))
barrera_rect.center = (width//2,height//2)
xEagle = 0
yEagle = 0
eagle_rect = eagle.imagen.get_rect(topleft=(xEagle, yEagle))
eagle_rect.center = (width//2,height//2)
angulo = 0
speed = 0.3
rotate = pygame.transform.rotate(barrera.imagen, angulo)
rotation = 5
barrera_positions = []
eagle_positions = []
placing_barrier = False
placing_eagle = True
counterWood = 0
counterStone = 0
counterSteel = 0
wood = True
stone = False
steel = False
eagleFlag = True
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
        if eagleFlag:
            if keys[pygame.K_w]:
                yEagle -= 10
            if keys[pygame.K_s]:
                yEagle += 10
            if keys[pygame.K_a]:
                xEagle -= 10
            if keys[pygame.K_d]:
                xEagle += 10
            if keys[pygame.K_f] and placing_eagle:
                # Colocar el águila
                eagle_positions.append((xEagle, yEagle, eagle.imagen))
                eagleFlag = False
                placing_eagle = False
                placing_barrier = True
        else:
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
                y -= 10
            if keys[pygame.K_s]:
                y += 10
            if keys[pygame.K_a]:
                x -= 10
            if keys[pygame.K_d]:
                x += 10
            if keys[pygame.K_r] and placing_barrier:
                if wood:
                    if counterWood < 10:
                        # Colocar barrera de madera
                        barrera_positions.append((x, y, angulo, barrera.imagen))
                        if not increment_wood:
                            counterWood += 1
                            increment_wood = True
                        else:
                            increment_wood = False
                elif stone:
                    if counterStone < 10:
                        # Colocar barrera de piedra
                        barrera_positions.append((x, y, angulo, barrera.imagen))
                        if not increment_Stone:
                            counterStone += 1
                            increment_Stone = True
                        else:
                            increment_Stone = False
                elif steel:
                    if counterSteel < 10:
                        # Colocar barrera de acero
                        barrera_positions.append((x, y, angulo, barrera.imagen))
                        if not increment_Steel:
                            counterSteel += 1
                            increment_Steel = True
                        else:
                            increment_Steel = False

    # Dibuja la imagen en la ventana
    screen.fill(bgColor)
    
    # Dibuja la imagen rotada en la ventana
    if placing_eagle:
        screen.blit(eagle.imagen, (xEagle, yEagle))
    else:
        rotate = pygame.transform.rotate(barrera.imagen, angulo)
        rect_rotate = rotate.get_rect(center=(width // 2 + x, height // 2 + y))
        screen.blit(rotate, rect_rotate)

    # Coloca las imágenes donde el jugador las quiere
    for pos_x, pos_y, imagen in eagle_positions:
        rect = imagen.get_rect(topleft=(pos_x, pos_y))
        screen.blit(imagen, rect)
        if rect_rotate.colliderect(rect):
            placing_barrier = False
        else:
            placing_barrier = True


    # Coloca las imágenes donde el jugador las quiere
    for pos_x, pos_y, pos_angulo, pos_imagen in barrera_positions:
        rotated_barrier = pygame.transform.rotate(pos_imagen, pos_angulo)
        barrier_rect = rotated_barrier.get_rect(center=(width // 2 + pos_x, height // 2 + pos_y))
        screen.blit(rotated_barrier, barrier_rect)
        
    print(placing_barrier)

    clock.tick(FPS)
    pygame.display.update()

