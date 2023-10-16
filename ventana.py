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
woodCounter = 0
rotate = pygame.transform.rotate(barrera.imagen, angulo)
rotation = 5

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
       
        #Evento de rotacion, movimiento y cambio de barrera
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
        
    # Dibuja la imagen en la ventana
    screen.fill(bgColor)
    rotate = pygame.transform.rotate(barrera.imagen, angulo)
    rect_rotate = rotate.get_rect(center=(width // 2 + x, height // 2 + y))
    clock.tick(FPS)
    # Dibuja la imagen rotada en la ventana
    screen.blit(rotate, rect_rotate)
    pygame.display.update()