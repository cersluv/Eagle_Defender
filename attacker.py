import pygame
import sys
import math

pygame.init()

# Constants
goblinSpeed = 5
projectileSpeed = 10
projectileSize = 20
projectileColor = (255, 0, 0)
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

# Initialize the display
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
pygame.display.set_caption("Goblin and Projectile")

# Load the goblin image
goblinImage = pygame.image.load("visuals/goblin.png")
goblinImage = pygame.transform.scale(goblinImage, (100, 100))

# Load the projectile image
projectileImage = pygame.image.load("visuals/projectile.png")
projectileImage = pygame.transform.scale(projectileImage, (projectileSize, projectileSize))

# Colors
white = (255, 255, 255)

# Font
font = pygame.font.Font(None, 36)

class Goblin:
    def __init__(self, x, y):
        self.rect = goblinImage.get_rect()
        self.rect.center = (x, y)
        self.angle = 0

    def rotate(self, angle):
        self.angle += angle

    def move(self, dx, dy):
        self.rect.x += dx
        self.rect.y += dy

    def draw(self):
        rotated = pygame.transform.rotate(goblinImage, self.angle)
        screen.blit(rotated, self.rect)

class Projectile:
    def __init__(self, x, y, angle):
        self.rect = projectileImage.get_rect()
        self.rect.center = (x, y)
        self.angle = angle
        self.velocity = -projectileSpeed  # Shoot to the left
        self.startX = x
        self.startY = y
        self.time = 0
        self.scaleFactor = screenWidth / 1920  # Adjust 1920 to the desired width
        self.initialVerticalVelocity = 8  # Adjust for flatter trajectory
        self.gravity = 0.1  # Adjust for flatter trajectory

    def move(self):
        self.time += 1
        self.rect.x = self.startX + self.velocity * self.time * math.cos(math.radians(self.angle)) * self.scaleFactor
        self.rect.y = self.startY - (self.initialVerticalVelocity * self.time - 0.5 * self.gravity * (self.time ** 2)) * self.scaleFactor


    def draw(self):
        screen.blit(projectileImage, self.rect)

goblin = Goblin(screenWidth - 120, screenHeight // 2)
projectile = None
trajectoryPoints = []

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        goblin.move(0, -goblinSpeed)
    if keys[pygame.K_DOWN]:
        goblin.move(0, goblinSpeed)

    if keys[pygame.K_LEFT]:
        goblin.rotate(-2)
    if keys[pygame.K_RIGHT]:
        goblin.rotate(2)

    if keys[pygame.K_SPACE]:
        if trajectoryPoints:
            trajectoryPoints.clear()
        if projectile is None:
            projectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)

    screen.fill((0, 0, 0))

    if len(trajectoryPoints) >= 2:
        pygame.draw.lines(screen, white, False, trajectoryPoints, 2)

    if projectile is not None:
        trajectoryPoints.append(projectile.rect.center)
        projectile.move()
        projectile.draw()
        if projectile.rect.x < 0 or projectile.rect.y > screenHeight:
            projectile = None

    goblin.draw()

    # Display angle, x, and y values
    angle_text = font.render(f"Angle: {goblin.angle} degrees", True, white)
    angle_text_rect = angle_text.get_rect()
    angle_text_rect.topleft = (20, 20)
    x_text = font.render(f"X: {goblin.rect.x:.2f}", True, white)
    x_text_rect = x_text.get_rect()
    x_text_rect.topleft = (20, 60)
    y_text = font.render(f"Y: {goblin.rect.y:.2f}", True, white)
    y_text_rect = y_text.get_rect()
    y_text_rect.topleft = (20, 100)

    screen.blit(angle_text, angle_text_rect)
    screen.blit(x_text, x_text_rect)
    screen.blit(y_text, y_text_rect)

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()
