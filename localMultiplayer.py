import pygame
import sys
import os
import math

global power, skinGoblin, skinProjectile, paletteAtacker, eagleSkin, boxSkin, paletteDefender

power = 1

def setVariables(firstUser, secondUser, language):
    global skinGoblin, skinProjectile, paletteAtacker, eagleSkin, boxSkin, paletteDefender
    try:
        datapath = os.getcwd() + "\Data"
        personPath = datapath + "\\" + firstUser
        configurationFile = personPath + "\\configuration.txt"
        file = open(configurationFile, "r")
        text = file.read()
        firstAttributes = text.split("\n")

        datapath = os.getcwd() + "\Data"
        personPath = datapath + "\\" + secondUser
        configurationFile = personPath + "\\configuration.txt"
        file = open(configurationFile, "r")
        text = file.read()
        secondAttributes = text.split("\n")

    except:
        print("error")
        firstAttributes = None
        secondAttributes = None

    skinGoblin = firstAttributes[4]
    skinProjectile = firstAttributes[2]
    paletteAtacker = firstAttributes[0]

    eagleSkin = secondAttributes[3]
    boxSkin = secondAttributes[2]
    paletteDefender = secondAttributes[0]

    startGame()

def startGame():
    global power, skinGoblin, skinProjectile, paletteAtacker, eagleSkin, boxSkin, paletteDefender, running

    pygame.init()

    # Constants
    goblinSpeed = 5
    projectileSpeed = 10
    projectileSize = 45
    projectileColor = (255, 0, 0)

    waterQuantity = 10
    fireQuantity = 10
    dynamiteQuantity = 10

    waterProjectile = None
    fireProjectile = None
    dynamiteProjectile = None

    screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Initialize the display
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
    pygame.display.set_caption("Goblin and Projectile")


    # Load the goblin image
    if skinGoblin == "goblin1":
        goblinImage = pygame.image.load("visuals/goblin/redGob.png")
    if skinGoblin == "goblin2":
        goblinImage = pygame.image.load("visuals/goblin/purpleGob.png")
    if skinGoblin == "goblin3":
        goblinImage = pygame.image.load("visuals/goblin/blueGob.png")
    if skinGoblin == "goblin4":
        goblinImage = pygame.image.load("visuals/goblin/pinkGob.png")
    if skinGoblin == "goblin5":
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


        def draw(self, type):
            if type == "water":
                screen.blit(waterImage, self.rect)
            if type == "fire":
                screen.blit(fireImage, self.rect)
            if type == "dynamite":
                screen.blit(dynamiteImage, self.rect)

    goblin = Goblin(screenWidth - 120, screenHeight // 2)
    projectile = None
    trajectoryPointsWater = []
    trajectoryPointsFire = []
    trajectoryPointsDynamite = []

    power1Rect = pygame.Rect(990 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
    power2Rect = pygame.Rect(1135 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
    power3Rect = pygame.Rect(1280 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)


    clock = pygame.time.Clock()

    running = True

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
        if keys[pygame.K_1]:
            power = 1
        if keys[pygame.K_2]:
            power = 2
        if keys[pygame.K_3]:
            power = 3
        if keys[pygame.K_UP]:
            goblin.move(0, -goblinSpeed)
        if keys[pygame.K_DOWN]:
            goblin.move(0, goblinSpeed)

        if keys[pygame.K_LEFT]:
            goblin.rotate(-2)
        if keys[pygame.K_RIGHT]:
            goblin.rotate(2)

        if keys[pygame.K_SPACE]:
            if waterProjectile is None and power == 1:
                waterQuantity -= 1
                waterProjectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)
                trajectoryPointsWater.clear()

            if fireProjectile is None and power == 2:
                fireQuantity -= 1
                fireProjectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)
                trajectoryPointsFire.clear()

            if dynamiteProjectile is None and power == 3:
                dynamiteQuantity -= 1
                dynamiteProjectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)
                trajectoryPointsDynamite.clear()


        screen.fill((0, 0, 0))

        screen.blit(scaledAtackerImage, (960, 0))
        screen.blit(scaledDefenderImage, (0, 0))

        if len(trajectoryPointsWater) >= 2:
            pygame.draw.lines(screen, "#aeddeb", False, trajectoryPointsWater, 2)
        if len(trajectoryPointsFire) >= 2:
            pygame.draw.lines(screen, "#ffa947", False, trajectoryPointsFire, 2)
        if len(trajectoryPointsDynamite) >= 2:
            pygame.draw.lines(screen, "#5c432c", False, trajectoryPointsDynamite, 2)

        if waterProjectile is not None:
            trajectoryPointsWater.append(waterProjectile.rect.center)
            waterProjectile.move()
            waterProjectile.draw("water")
            if waterProjectile.rect.x < 0 or waterProjectile.rect.y > screenHeight:
                waterProjectile = None

        if fireProjectile is not None:
            trajectoryPointsFire.append(fireProjectile.rect.center)
            fireProjectile.move()
            fireProjectile.draw("fire")
            if fireProjectile.rect.x < 0 or fireProjectile.rect.y > screenHeight:
                fireProjectile = None

        if dynamiteProjectile is not None:
            trajectoryPointsDynamite.append(dynamiteProjectile.rect.center)
            dynamiteProjectile.move()
            dynamiteProjectile.draw("dynamite")
            if dynamiteProjectile.rect.x < 0 or dynamiteProjectile.rect.y > screenHeight:
                dynamiteProjectile = None


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
        angle_text_rect.topleft = (1700 * scaleFactorWidth, 20 *  scaleFactorHeight)
        x_text = font.render(f"X: {goblin.rect.x:.2f}", True, white)
        x_text_rect = x_text.get_rect()
        x_text_rect.topleft = (1700 * scaleFactorWidth, 60 *  scaleFactorHeight)
        y_text = font.render(f"Y: {goblin.rect.y:.2f}", True, white)
        y_text_rect = y_text.get_rect()
        y_text_rect.topleft = (1700 * scaleFactorWidth, 100 *  scaleFactorHeight)

        waterText = font.render(f"x{waterQuantity}", True, white)
        watertext_rect = waterText.get_rect()
        watertext_rect.topleft = (1000 * scaleFactorWidth, 1022 *  scaleFactorHeight)
        fireText = font.render(f"x{fireQuantity}", True, white)
        firetext_rect = fireText.get_rect()
        firetext_rect.topleft = (1147 * scaleFactorWidth, 1022 *  scaleFactorHeight)
        dynamiteText = font.render(f"x{dynamiteQuantity}", True, white)
        dynamitetext_rect = dynamiteText.get_rect()
        dynamitetext_rect.topleft = (1290 * scaleFactorWidth, 1022 *  scaleFactorHeight)

        buttonText1_rect = font.render("[1]",True, white).get_rect()
        buttonText1_rect.topleft = (1000 * scaleFactorWidth, 933 *  scaleFactorHeight)
        buttonText2_rect = font.render("[2]", True, white).get_rect()
        buttonText2_rect.topleft = (1147 * scaleFactorWidth, 933 * scaleFactorHeight)
        buttonText3_rect = font.render("[3]", True, white).get_rect()
        buttonText3_rect.topleft = (1290 * scaleFactorWidth, 933 * scaleFactorHeight)


        screen.blit(angle_text, angle_text_rect)
        screen.blit(x_text, x_text_rect)
        screen.blit(y_text, y_text_rect)
        screen.blit(waterText,watertext_rect)
        screen.blit(fireText, firetext_rect)
        screen.blit(dynamiteText, dynamitetext_rect)
        screen.blit(font.render("[1]",True, white),buttonText1_rect)
        screen.blit(font.render("[2]",True, white), buttonText2_rect)
        screen.blit(font.render("[3]",True, white), buttonText3_rect)

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()

