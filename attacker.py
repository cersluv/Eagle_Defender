import pygame
import sys
import math

global power
power = 1


skinGoblin = "4"
skinProjectile = "1"
paletteAtacker = "Palette 3"
paletteDefender = "Palette 5"

pygame.init()

# Constants
goblinSpeed = 5
projectileSpeed = 10
projectileSize = 45
projectileColor = (255, 0, 0)
screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

# Initialize the display
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
pygame.display.set_caption("Goblin and Projectile")



# Load the goblin image
if skinGoblin == "1":
    goblinImage = pygame.image.load("visuals/goblin/redGob.png")
if skinGoblin == "2":
    goblinImage = pygame.image.load("visuals/goblin/purpleGob.png")
if skinGoblin == "3":
    goblinImage = pygame.image.load("visuals/goblin/blueGob.png")
if skinGoblin == "4":
    goblinImage = pygame.image.load("visuals/goblin/pinkGob.png")
if skinGoblin == "5":
    goblinImage = pygame.image.load("visuals/goblin/greenGob.png")

goblinImage = pygame.transform.scale(goblinImage, (150, 150))

# Load the projectile image
if skinProjectile == "1":
    waterImage = pygame.image.load("visuals/projectile/w1.png")
    fireImage = pygame.image.load("visuals/projectile/f1.png")
    dynamiteImage = pygame.image.load("visuals/projectile/d1.png")

    waterImage = pygame.transform.scale(waterImage, (projectileSize, projectileSize))
    waterImage = pygame.transform.rotate(waterImage, 25)
    dynamiteImage = pygame.transform.scale(dynamiteImage, (projectileSize + 10, projectileSize + 10))

if skinProjectile == "2":
    waterImage = pygame.image.load("visuals/projectile/w2.png")
    fireImage = pygame.image.load("visuals/projectile/f2.png")
    dynamiteImage = pygame.image.load("visuals/projectile/d2.png")

    waterImage = pygame.transform.scale(waterImage, (projectileSize + 20, projectileSize + 10))
    dynamiteImage = pygame.transform.scale(dynamiteImage, (projectileSize -10, projectileSize))

fireImage = pygame.transform.scale(fireImage, (projectileSize + 40, projectileSize))

if paletteAtacker == "Palette 1":
    atackerGameplay = pygame.image.load("visuals/gameWindows/3.png")
if paletteDefender == "Palette 1":
    defenderGameplay = pygame.image.load("visuals/gameWindows/8.png")
if paletteAtacker == "Palette 2":
    atackerGameplay = pygame.image.load("visuals/gameWindows/4.png")
if paletteDefender == "Palette 2":
    defenderGameplay = pygame.image.load("visuals/gameWindows/9.png")
if paletteAtacker == "Palette 3":
    atackerGameplay = pygame.image.load("visuals/gameWindows/5.png")
if paletteDefender == "Palette 3":
    defenderGameplay = pygame.image.load("visuals/gameWindows/10.png")
if paletteAtacker == "Palette 4":
    atackerGameplay = pygame.image.load("visuals/gameWindows/6.png")
if paletteDefender == "Palette 4":
    defenderGameplay = pygame.image.load("visuals/gameWindows/11.png")
if paletteAtacker == "Palette 5":
    atackerGameplay = pygame.image.load("visuals/gameWindows/7.png")
if paletteDefender == "Palette 5":
    defenderGameplay = pygame.image.load("visuals/gameWindows/12.png")

# Get the image's original dimensions
originalWidth, originalHeigth = pygame.image.load("visuals/gameWindows/aaa.png").get_size()

# Calculate the scaling factors to fit the image to the screen
scaleFactorWidth = screenWidth / originalWidth
scaleFactorHeight = screenHeight / originalHeigth

# Choose the minimum scaling factor to maintain aspect ratio
minScaleFactor = min(scaleFactorWidth, scaleFactorHeight)

# Scale the image while maintaining aspect ratio
newWidth = int(originalWidth * minScaleFactor)
newHeigth = int(originalHeigth * minScaleFactor)

scaledAtackerImage = pygame.transform.scale(atackerGameplay, (newWidth/2, newHeigth))
scaledDefenderImage = pygame.transform.scale(defenderGameplay, (newWidth/2, newHeigth))

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
        global power

        if power == 1:
            self.rect = waterImage.get_rect()
        if power == 2:
            self.rect = fireImage.get_rect()
        if power == 3:
            self.rect = dynamiteImage.get_rect()
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
        if power == 1:
            screen.blit(waterImage, self.rect)
        if power == 2:
            screen.blit(fireImage, self.rect)
        if power == 3:
            screen.blit(dynamiteImage, self.rect)

goblin = Goblin(screenWidth - 120, screenHeight // 2)
projectile = None
trajectoryPoints = []

power1Rect = pygame.Rect(990 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
power2Rect = pygame.Rect(1135 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
power3Rect = pygame.Rect(1280 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)


running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if power1Rect.collidepoint(event.pos):
                power = 1
            if power2Rect.collidepoint(event.pos):
                power = 2
            if power3Rect.collidepoint(event.pos):
                power = 3

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

    screen.blit(scaledAtackerImage, (960, 0))
    screen.blit(scaledDefenderImage, (0, 0))

    if len(trajectoryPoints) >= 2:
        pygame.draw.lines(screen, white, False, trajectoryPoints, 2)

    if projectile is not None:
        trajectoryPoints.append(projectile.rect.center)
        projectile.move()
        projectile.draw()
        if projectile.rect.x < 0 or projectile.rect.y > screenHeight:
            projectile = None


    goblin.draw()
    powers1 = pygame.draw.rect(screen, "#2e2f30", power1Rect, 0)
    screen.blit(pygame.transform.scale(waterImage, (120 * scaleFactorWidth, 80 * scaleFactorHeight)), (1000 * scaleFactorWidth, 950* scaleFactorHeight))
    powers2 = pygame.draw.rect(screen, "#1a1b1c", power2Rect, 0)
    screen.blit(pygame.transform.scale(fireImage, (120 * scaleFactorWidth, 60 * scaleFactorHeight)), (1155 * scaleFactorWidth, 955* scaleFactorHeight))
    powers3 = pygame.draw.rect(screen, "#2e2f30", power3Rect, 0)
    screen.blit(pygame.transform.scale(dynamiteImage, (80 * scaleFactorWidth, 80* scaleFactorHeight)), (1310 * scaleFactorWidth, 950* scaleFactorHeight))




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
