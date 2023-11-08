import pygame
from eagle import Aguila

aguila = Aguila(1)

pygame.init()
screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeigth = screenInfo.current_h
originalWidth, originalHeight = 1920, 1080
# Calculate the scaling factors to fit the image to the screen
scaleFactorWidth = screenWidth / originalWidth
scaleFactorHeigth = screenHeigth / originalHeight

class Fence:

    def __init__(self, x, y, tipo, angulo, skin):
        self.x = x
        self.y = y
        self.tipo = tipo  # Tipo de barrera: 1, 2 o 3
        self.velocidad = 10
        self.angulo_rotacion = angulo
        self.inicializar_vida()
        self.opacity = 255
        if skin == 1:
            wood = pygame.image.load("visuals/boxes/madera1.png")
            steel = pygame.image.load("visuals/boxes/acero1.png")
            concrete = pygame.image.load("visuals/boxes/concreto1.png")
            wood = pygame.transform.scale(wood, (80 * scaleFactorWidth, 80 * scaleFactorHeigth))
            steel = pygame.transform.scale(steel, (80 * scaleFactorWidth, 60 * scaleFactorHeigth))
            concrete = pygame.transform.scale(concrete, (80 * scaleFactorWidth, 70 * scaleFactorHeigth))
        if skin == 2:
            wood = pygame.image.load("visuals/boxes/madera2.png")
            steel = pygame.image.load("visuals/boxes/acero2.png")
            concrete = pygame.image.load("visuals/boxes/concreto2.png")
            wood = pygame.transform.scale(wood, (80 * scaleFactorWidth, 80 * scaleFactorHeigth))
            steel = pygame.transform.scale(steel, (80 * scaleFactorWidth, 80 * scaleFactorHeigth))
            concrete = pygame.transform.scale(concrete, (100 * scaleFactorWidth, 80 * scaleFactorHeigth))

        #self.imagenes = [wood, steel, concrete]
        self.imagenes = [wood, steel, concrete]
        self.imagen_actual = self.imagenes[self.tipo - 1]
        self.rect = self.imagen_actual.get_rect(topleft=(x, y))
        self.rect.center = (x, y)
        
    
    def inicializar_vida(self):
        if self.tipo == 1:
            self.vida = 1
        elif self.tipo == 2:
            self.vida = 2
        elif self.tipo == 3:
            self.vida = 3

    def rotar(self, sentido):
        if sentido == "Q":
            self.angulo_rotacion += 5  # Rotar 5 grados en sentido antihorario
        elif sentido == "E":
            self.angulo_rotacion -= 5  # Rotar 5 grados en sentido horario

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def actualizarOpacidad(self, proyectil):
        if self.tipo == 2:
            if proyectil == "water":
                self.opacity -= 120
            if proyectil == "fire":
                self.opacity -= 170
            if proyectil == "dynamite":
                self.opacity -= 255
        if self.tipo == 3:
            if proyectil == "water":
                self.opacity -= 80
            if proyectil == "fire":
                self.opacity -= 150
            if proyectil == "dynamite":
                self.opacity -= 255
        self.opacity = max(0,self.opacity)


    def dibujar(self, pantalla):
        imagen_rotada = pygame.transform.rotate(self.imagenes[self.tipo - 1], self.angulo_rotacion)
        self.imagen_actual = imagen_rotada
        self.rect = self.imagen_actual.get_rect(center=self.rect.center)
        self.imagen_actual.set_alpha(self.opacity)
        pantalla.blit(self.imagen_actual, self.rect)
            

    


    


    

