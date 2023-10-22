import pygame

class Aguila:
    def __init__(self):
        self.imagen = pygame.image.load("eagle.png")
        self.rect = self.imagen.get_rect()
        self.velocidad = 10
        self.vida = 100

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def dibujar(self, pantalla):
        pantalla.blit(self.imagen, self.rect)
        

