import pygame
import sys

# Inicializa Pygame
pygame.init()

# Configuración de la pantalla
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Dibujar Imagen con tecla R")

# Carga la imagen que deseas dibujar
image = pygame.image.load("fence.png")  # Reemplaza "imagen.png" con la ruta de tu imagen

# Posición inicial de la imagen
image_x = 100
image_y = 100

# Bucle principal del juego
running = True
draw_image = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                draw_image = True

    # Dibuja la pantalla
    screen.fill((0, 0, 0))  # Limpia la pantalla

    # Dibuja la imagen en la posición actual si se presionó la tecla "R"
    if draw_image:
        screen.blit(image, (image_x, image_y))

    pygame.display.flip()

pygame.quit()
sys.exit()