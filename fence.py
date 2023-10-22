import pygame

class Fence:

    def __init__(self, x, y, tipo, angulo):
        self.x = x
        self.y = y
        self.tipo = tipo  # Tipo de barrera: 1, 2 o 3
        self.velocidad = 10
        self.angulo_rotacion = angulo
        self.inicializar_vida()
        self.imagenes = [
            pygame.image.load("fence.png"),
            pygame.image.load("stoneF.png"),
            pygame.image.load("steelF.png")
        ]
        self.imagen_actual = self.imagenes[self.tipo - 1]
        self.rect = self.imagen_actual.get_rect(topleft=(x, y))
        self.rect.center = (x, y)
    
    def inicializar_vida(self):
        if self.tipo == 1:
            self.vidaAgua = 100
            self.vidaFuego = 50
            self.vidaBomba = 30
        elif self.tipo == 2:
            self.vidaAgua = 80
            self.vidaFuego = 70
            self.vidaBomba = 40
        elif self.tipo == 3:
            self.vidaAgua = 60
            self.vidaFuego = 90
            self.vidaBomba = 60

    def rotar(self, sentido):
        if sentido == "Q":
            self.angulo_rotacion += 5  # Rotar 5 grados en sentido antihorario
        elif sentido == "E":
            self.angulo_rotacion -= 5  # Rotar 5 grados en sentido horario

    def mover(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def dibujar(self, pantalla):
        imagen_rotada = pygame.transform.rotate(self.imagenes[self.tipo - 1], self.angulo_rotacion)
        self.imagen_actual = imagen_rotada
        self.rect = self.imagen_actual.get_rect(center=self.rect.center)
        pantalla.blit(self.imagen_actual, self.rect)
    


    


    

