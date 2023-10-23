import pygame


pygame.init()
screenInfo = pygame.display.Info()
screenWidth = screenInfo.current_w
screenHeigth = screenInfo.current_h
originalWidth, originalHeight = 1920, 1080
# Calculate the scaling factors to fit the image to the screen
scaleFactorWidth = screenWidth / originalWidth
scaleFactorHeigth = screenHeigth / originalHeight

class Aguila:
    def __init__(self, skin):
        if skin == 1:
            skinEagle = pygame.image.load("visuals/eagles/eagle1.png")
        if skin == 2:
            skinEagle = pygame.image.load("visuals/eagles/eagle2.png")
        if skin == 3:
            skinEagle = pygame.image.load("visuals/eagles/eagle3.png")
        if skin == 4:
            skinEagle = pygame.image.load("visuals/eagles/eagle4.png")
        skinEagle = pygame.transform.scale(skinEagle, (150 * scaleFactorWidth, 150 * scaleFactorHeigth))
        self.imagen = skinEagle
        self.rect = self.imagen.get_rect()
        self.velocidad = 10
        self.vida = 100

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
        

