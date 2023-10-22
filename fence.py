import pygame

class Fence:
    
    def __init__(self, imagen):
        self.imagen = pygame.image.load(imagen)

    def cambiar_imagen(self, nueva_imagen):
        self.imagen = pygame.image.load(nueva_imagen)