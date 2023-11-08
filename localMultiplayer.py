import pygame
import time
import sys
import os
import math
from eagle import Aguila
from fence import Fence
from musicHandler import playMusicUser, getMusicFeatures
from winnerWindow import startWinnerWindow

global power, skinGoblin, skinProjectile, paletteAtacker, eagleSkin, boxSkin, paletteDefender, lang, winnerGlobal, points, firstPlayer, secondPlayer, lastTime, lastSongDuration

power = 1

def setVariables(firstUser, secondUser, language, winner, winnerPoints, timeAttacker, lastDuration):
    global skinGoblin, skinProjectile, paletteAtacker, eagleSkin, boxSkin, paletteDefender, lang, winnerGlobal, points, firstPlayer, secondPlayer, lastTime, lastSongDuration
    lang = language
    points = winnerPoints
    winnerGlobal = winner
    firstPlayer = firstUser
    secondPlayer = secondUser
    lastTime = timeAttacker
    lastSongDuration = lastDuration

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
    global power, skinGoblin, skinProjectile, paletteAtacker, eagleSkin, boxSkin, paletteDefender, running, lang, winnerGlobal, points, firstPlayer, secondPlayer, lastTime, lastSongDuration

    playMusicUser(secondPlayer)

    popularity, danceability, acoustics, tempo, duration = getMusicFeatures(firstPlayer)

    songMinutesDuration = duration//60000
    songSecondsDuration = duration//1000 - songMinutesDuration*60

    bps = tempo/60

    regeneration = int(30/bps)

    popularity2, danceability2, acoustics2, tempo2, duration2 = getMusicFeatures(secondPlayer)

    songMinutesDuration2 = duration2//60000
    songSecondsDuration2 = duration2//1000 - songMinutesDuration2*60

    pygame.init()

    # Constants
    goblinSpeed = 5
    projectileSpeed = 10
    projectileSize = 45
    projectileColor = (255, 0, 0)

    waterQuantity = 3
    fireQuantity = 2
    dynamiteQuantity = 4

    woodQuantity = 10
    steelQuantity = 10
    concreteQuantity = 10

    waterProjectile = None
    fireProjectile = None
    dynamiteProjectile = None

    attackingPhase = False

    screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Initialize the display
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
    pygame.display.set_caption("Goblin and Projectile")

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



    # Colors
    white = (255, 255, 255)

    # Font
    font = pygame.font.Font(None, 36)


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

    if boxSkin == "1":
        woodSkin = pygame.image.load("visuals/boxes/madera1.png")
        steelSkin = pygame.image.load("visuals/boxes/acero1.png")
        concreteSkin = pygame.image.load("visuals/boxes/concreto1.png")
        woodSkin = pygame.transform.scale(woodSkin, (80 * scaleFactorWidth, 80 * scaleFactorHeight))
        steelSkin = pygame.transform.scale(steelSkin, (80 * scaleFactorWidth, 60 * scaleFactorHeight))
        concreteSkin = pygame.transform.scale(concreteSkin, (80 * scaleFactorWidth, 70 * scaleFactorHeight))
        boxes = 1
    if boxSkin == "2":
        woodSkin = pygame.image.load("visuals/boxes/madera2.png")
        steelSkin = pygame.image.load("visuals/boxes/acero2.png")
        concreteSkin = pygame.image.load("visuals/boxes/concreto2.png")
        woodSkin = pygame.transform.scale(woodSkin, (80 * scaleFactorWidth, 80 * scaleFactorHeight))
        steelSkin = pygame.transform.scale(steelSkin, (80 * scaleFactorWidth, 80 * scaleFactorHeight))
        concreteSkin = pygame.transform.scale(concreteSkin, (100 * scaleFactorWidth, 80 * scaleFactorHeight))
        boxes = 2

    if eagleSkin == "eagle1":
        skinEagle = 1
    if eagleSkin == "eagle2":
        skinEagle = 2
    if eagleSkin == "eagle3":
        skinEagle = 3
    if eagleSkin == "eagle4":
        skinEagle = 4

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

    scaledAtackerImage = pygame.transform.scale(atackerGameplay, (newWidth / 2, newHeigth))
    scaledDefenderImage = pygame.transform.scale(defenderGameplay, (newWidth / 2, newHeigth))


    if lang == "es":
        keysAttacker = pygame.image.load("visuals/gameWindows/keysEsAt.png")
        keysDefender = pygame.image.load("visuals/gameWindows/keysEsDef.png")

    if lang == "en":
        keysAttacker = pygame.image.load("visuals/gameWindows/keysEnAt.png")
        keysDefender = pygame.image.load("visuals/gameWindows/keysEnDef.png")


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

    eagle = Aguila(skinEagle)
    barrera = Fence(50, 50, 1, 0, boxes)
    aguila_Movement = True
    barrera_Movement = False
    placing_Barrier = True
    barrerasTipo1 = []
    barrerasTipo2 = []
    barrerasTipo3 = []
    barreras = [barrerasTipo1, barrerasTipo2, barrerasTipo3]
    se_creo_nueva_barrera = False

    projectiles = []


    goblin = Goblin(screenWidth - 120, screenHeight // 2)
    projectile = None
    trajectoryPointsWater = []
    trajectoryPointsFire = []
    trajectoryPointsDynamite = []

    power1Rect = pygame.Rect(990 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
    power2Rect = pygame.Rect(1135 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
    power3Rect = pygame.Rect(1280 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)

    box1Rect = pygame.Rect(500 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
    box2Rect = pygame.Rect(645 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)
    box3Rect = pygame.Rect(790 * scaleFactorWidth, 930 * scaleFactorHeight, 140 * scaleFactorWidth, 120 * scaleFactorHeight)


    clock = pygame.time.Clock()

    totalTimeSeconds = 60 * 1

    startTime = time.time()

    winningTime = 0


    totalTimeSecondsAttacking = (60 * songMinutesDuration) + songSecondsDuration
    startAttackingTime = time.time() + 60

    running = True

    destroyedBlocks = 0

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

        elapsedTimeSeconds = int(time.time() - startTime)
        currentTimeSeconds = max(0, totalTimeSeconds - elapsedTimeSeconds)

        minutes = currentTimeSeconds // 60
        seconds = currentTimeSeconds % 60

        if currentTimeSeconds == 0 and not attackingPhase:
            attackingPhase = True
            regenCounter = time.time()
            timerStarter = time.time()
            playMusicUser(firstPlayer)

        if attackingPhase:
            elapsedTimeSecondsAttacking = int(time.time() - startAttackingTime)
            currentTimeSecondsAttacking = max(0, totalTimeSecondsAttacking - elapsedTimeSecondsAttacking)

            minutesAttacking = currentTimeSecondsAttacking // 60
            secondsAttacking = currentTimeSecondsAttacking % 60

            regenerationTime = int(time.time() - regenCounter)



            if regenerationTime == regeneration:
                waterQuantity += 1
                fireQuantity += 1
                dynamiteQuantity += 1
                regenCounter = time.time()

        if aguila_Movement:
            # Movimiento del aguila
            if keys[pygame.K_a]:
                eagle.mover(-eagle.velocidad, 0)
            if keys[pygame.K_d]:
                eagle.mover(eagle.velocidad, 0)
            if keys[pygame.K_w]:
                eagle.mover(0, -eagle.velocidad)
            if keys[pygame.K_s]:
                eagle.mover(0, eagle.velocidad)

            # Posicionamiento del aguila
            if keys[pygame.K_r]:
                aguila_Movement = False
                barrera_Movement = True

        if barrera_Movement:
            # Cambio de barrera
            if keys[pygame.K_1]:
                barrera = Fence(50, 50, 1, 0, boxes)
            elif keys[pygame.K_2]:
                barrera = Fence(50, 50, 2, 0, boxes)
            elif keys[pygame.K_3]:
                barrera = Fence(50, 50, 3, 0, boxes)

            # Rotacion de las barreras
            if keys[pygame.K_q]:
                barrera.rotar("Q")
            elif keys[pygame.K_e]:
                barrera.rotar("E")

            # Movimiento de las barreras
            if keys[pygame.K_w]:
                barrera.mover(0, -barrera.velocidad)
            if keys[pygame.K_s]:
                barrera.mover(0, barrera.velocidad)
            if keys[pygame.K_a]:
                barrera.mover(-barrera.velocidad, 0)
            if keys[pygame.K_d]:
                barrera.mover(barrera.velocidad, 0)

            if keys[pygame.K_f] and not barrera.rect.colliderect(eagle.rect):
                if barrera.tipo == 1:
                    if len(barrerasTipo1) == 10:
                        pass
                    else:
                        if not se_creo_nueva_barrera:
                            if barrera.rect.x < 870:
                                newBarrera = Fence(barrera.rect.x + 50, barrera.rect.y + 25, barrera.tipo,
                                                   barrera.angulo_rotacion, boxes)
                                barrerasTipo1.append(newBarrera)
                                woodQuantity -= 1
                                se_creo_nueva_barrera = True
                elif barrera.tipo == 2:
                    if len(barrerasTipo2) == 10:
                        pass
                    else:
                        if not se_creo_nueva_barrera:
                            if barrera.rect.x < 870:
                                newBarrera = Fence(barrera.rect.x + 50, barrera.rect.y + 25, barrera.tipo,
                                                   barrera.angulo_rotacion, boxes)
                                barrerasTipo2.append(newBarrera)
                                steelQuantity -= 1
                                se_creo_nueva_barrera = True
                elif barrera.tipo == 3:
                    if len(barrerasTipo3) == 10:
                        pass
                    else:
                        if not se_creo_nueva_barrera:
                            if barrera.rect.x < 870:
                                newBarrera = Fence(barrera.rect.x + 50, barrera.rect.y + 25, barrera.tipo,
                                                   barrera.angulo_rotacion, boxes)
                                barrerasTipo3.append(newBarrera)
                                concreteQuantity -= 1
                                se_creo_nueva_barrera = True
            else:
                se_creo_nueva_barrera = False

        if attackingPhase:
            if keys[pygame.K_8]:
                power = 1
            if keys[pygame.K_9]:
                power = 2
            if keys[pygame.K_0]:
                power = 3
            if goblin.rect.y > 0 :
                if keys[pygame.K_UP]:
                    goblin.move(0, -goblinSpeed)
            if 1050 > goblin.rect.y:
                if keys[pygame.K_DOWN]:
                    goblin.move(0, goblinSpeed)
            if 1900 > goblin.rect.x:
                if keys[pygame.K_RIGHT]:
                    goblin.move(goblinSpeed, 0)
            if goblin.rect.x > 960:
                if keys[pygame.K_LEFT]:
                    goblin.move(-goblinSpeed, 0)


            if keys[pygame.K_o]:
                goblin.rotate(2)
            if keys[pygame.K_p]:
                goblin.rotate(-2)

            if keys[pygame.K_SPACE]:
                if waterProjectile is None and power == 1:
                    waterQuantity -= 1
                    waterProjectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)
                    list = [waterProjectile, "water"]
                    projectiles.append(list)
                    trajectoryPointsWater.clear()

                if fireProjectile is None and power == 2:
                    fireQuantity -= 1
                    fireProjectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)
                    list = [fireProjectile, "fire"]
                    projectiles.append(list)
                    trajectoryPointsFire.clear()

                if dynamiteProjectile is None and power == 3:
                    dynamiteQuantity -= 1
                    dynamiteProjectile = Projectile(goblin.rect.x, goblin.rect.y, goblin.angle)
                    list = [dynamiteProjectile, "dynamite"]
                    projectiles.append(list)
                    trajectoryPointsDynamite.clear()


        screen.fill((0, 0, 0))

        screen.blit(scaledAtackerImage, (960*scaleFactorWidth, 0))
        screen.blit(scaledDefenderImage, (0, 0))
        #rectangulo1 = pygame.Rect(100, 230, 270, 475)
        #rectangulo = pygame.draw.rect(screen, "#FF241F", rectangulo1, 0)

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
            #if rectangulo1.collidepoint(waterProjectile.rect.x, waterProjectile.rect.y):
             #   print("Chocaron")
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

        box1 = pygame.draw.rect(screen, "#2e2f30", box1Rect, 0)
        screen.blit(pygame.transform.scale(woodSkin, (70 * scaleFactorWidth, 70 * scaleFactorHeight)), (535 * scaleFactorWidth, 955* scaleFactorHeight))
        box2 = pygame.draw.rect(screen, "#1a1b1c", box2Rect, 0)
        screen.blit(pygame.transform.scale(steelSkin, (80 * scaleFactorWidth, 60 * scaleFactorHeight)),(675 * scaleFactorWidth, 960 * scaleFactorHeight))
        box3 = pygame.draw.rect(screen, "#2e2f30", box3Rect, 0)
        if boxes == 1:
            screen.blit(pygame.transform.scale(concreteSkin, (100 * scaleFactorWidth, 80 * scaleFactorHeight)),(810 * scaleFactorWidth, 950 * scaleFactorHeight))
        if boxes == 2:
            screen.blit(pygame.transform.scale(concreteSkin, (70 * scaleFactorWidth, 70 * scaleFactorHeight)),(825 * scaleFactorWidth, 955 * scaleFactorHeight))



        # Display angle, x, and y values
        if lang == "es":
            angle_text = font.render(f"Ángulo: {goblin.angle}°", True, white)
            angle_text_rect = angle_text.get_rect()
            angle_text_rect.topleft = (1700 * scaleFactorWidth, 20 *  scaleFactorHeight)
        if lang == "en":
            angle_text = font.render(f"Angle: {goblin.angle}°", True, white)
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

        buttonText1_rect = font.render("[8]",True, white).get_rect()
        buttonText1_rect.topleft = (1000 * scaleFactorWidth, 933 *  scaleFactorHeight)
        buttonText2_rect = font.render("[9]", True, white).get_rect()
        buttonText2_rect.topleft = (1147 * scaleFactorWidth, 933 * scaleFactorHeight)
        buttonText3_rect = font.render("[0]", True, white).get_rect()
        buttonText3_rect.topleft = (1290 * scaleFactorWidth, 933 * scaleFactorHeight)


        woodText = font.render(f"x{woodQuantity}", True, white)
        woodtext_rect = woodText.get_rect()
        woodtext_rect.topleft = (510 * scaleFactorWidth, 1022 * scaleFactorHeight)
        steelText = font.render(f"x{steelQuantity}", True, white)
        steeltext_rect = steelText.get_rect()
        steeltext_rect.topleft = (657 * scaleFactorWidth, 1022 * scaleFactorHeight)
        concreteText = font.render(f"x{concreteQuantity}", True, white)
        concretetext_rect = concreteText.get_rect()
        concretetext_rect.topleft = (800 * scaleFactorWidth, 1022 * scaleFactorHeight)

        buttonText4_rect = font.render("[1]", True, white).get_rect()
        buttonText4_rect.topleft = (510 * scaleFactorWidth, 933 * scaleFactorHeight)
        buttonText5_rect = font.render("[2]", True, white).get_rect()
        buttonText5_rect.topleft = (657 * scaleFactorWidth, 933 * scaleFactorHeight)
        buttonText6_rect = font.render("[3]", True, white).get_rect()
        buttonText6_rect.topleft = (800 * scaleFactorWidth, 933 * scaleFactorHeight)

        def drawTimeText(text, x, y, size):
            font = pygame.font.Font("visuals/LEMONMILK-Bold.ttf", size * int(scaleFactorWidth))
            renderedText = font.render(text, True, (255, 255, 255))
            screen.blit(renderedText, (x * scaleFactorWidth, y * scaleFactorHeight))

        if not attackingPhase:
            drawTimeText(f"{minutes:02d}:{seconds:02d}", 880, 15, 50)

        if attackingPhase:
            drawTimeText(f"{minutesAttacking:02d}:{secondsAttacking:02d}", 880, 15, 50)


        screen.blit(angle_text, angle_text_rect)
        screen.blit(x_text, x_text_rect)
        screen.blit(y_text, y_text_rect)
        screen.blit(waterText,watertext_rect)
        screen.blit(fireText, firetext_rect)
        screen.blit(dynamiteText, dynamitetext_rect)
        screen.blit(woodText,woodtext_rect)
        screen.blit(steelText, steeltext_rect)
        screen.blit(concreteText, concretetext_rect)
        screen.blit(font.render("[8]",True, white),buttonText1_rect)
        screen.blit(font.render("[9]",True, white), buttonText2_rect)
        screen.blit(font.render("[0]",True, white), buttonText3_rect)
        screen.blit(font.render("[1]", True, white), buttonText4_rect)
        screen.blit(font.render("[2]", True, white), buttonText5_rect)
        screen.blit(font.render("[3]", True, white), buttonText6_rect)


        eagle.dibujar(screen)
        if barrera_Movement:
            barrera.dibujar(screen)

            for cantBarreras in barreras:
                for cantTipos in cantBarreras:
                    cantTipos.dibujar(screen)

                    # LOGICA COLLIDE Y DESTRUIR BARRERAS
                    for projectileNumber in projectiles:
                        if projectileNumber[0].rect.colliderect(cantTipos.rect):
                            if projectileNumber[1] == "water":
                                if cantTipos.tipo == 1 and waterProjectile != None:
                                    cantTipos.vida -= 1
                                    waterProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("water")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                                if cantTipos.tipo == 2 and waterProjectile != None:
                                    cantTipos.vida -= 1
                                    waterProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("water")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                                if cantTipos.tipo == 3 and waterProjectile != None:
                                    cantTipos.vida -= 1
                                    waterProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("water")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                            if projectileNumber[1] == "fire":
                                if cantTipos.tipo == 1:
                                    cantTipos.vida -= 2
                                    fireProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("fire")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                                if cantTipos.tipo == 2:
                                    cantTipos.vida -= 2
                                    fireProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("fire")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                                if cantTipos.tipo == 3:
                                    cantTipos.vida -= 2
                                    fireProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("fire")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                            if projectileNumber[1] == "dynamite":
                                if cantTipos.tipo == 1:
                                    cantTipos.vida -= 3
                                    dynamiteProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("dynamite")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                                if cantTipos.tipo == 2:
                                    cantTipos.vida -= 3
                                    dynamiteProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("dynamite")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)

                                if cantTipos.tipo == 3:
                                    cantTipos.vida -= 3
                                    dynamiteProjectile.startX = -1000
                                    cantTipos.actualizarOpacidad("dynamite")
                                    if cantTipos.vida <= 0:
                                        destroyedBlocks += 1
                                        cantBarreras.remove(cantTipos)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    for cantidad in barreras:
                        for tipos in cantidad:
                            if tipos.rect.collidepoint(event.pos):
                                cantidad.remove(tipos)
                                if tipos.tipo == 1:
                                    woodQuantity += 1
                                if tipos.tipo == 2:
                                    steelQuantity += 1
                                if tipos.tipo == 3:
                                    concreteQuantity += 1

        def drawText(text, x, y, size):
            font = pygame.font.Font("visuals/LEMONMILK-Bold.ttf", size * int(scaleFactorWidth))
            renderedText = font.render(text, True, (255, 255, 255))
            screen.blit(renderedText, (x * scaleFactorWidth, y * scaleFactorHeight))

        seconds = duration // 1000

        drawText(f"{firstPlayer}", 1300, 10, 30)
        drawText(f"{secondPlayer}", 300, 10, 30)
        if attackingPhase:
            drawText(f"{destroyedBlocks*0.5 + round((seconds-(time.time() - startAttackingTime))*0.5,1)}", 1300, 50, 20)
        else:
            drawText(f"{destroyedBlocks * 0.5 + (seconds) * 0.5}", 1300, 50, 20)
        drawText(f"{points} pts", 300, 50, 20)


        def settleScoreAttacker(blocks, timeLeft):
            score = blocks * 0.5 + timeLeft * 0.5
            return score

        for projectileNumber in projectiles:
            if projectileNumber[0].rect.colliderect(eagle.rect):
                winningTime = int(time.time() - timerStarter)
                print("puntaje primero: " + str(points))
                print("puntaje segundo: " + str(settleScoreAttacker(destroyedBlocks, seconds-winningTime)))
                if winnerGlobal == None:
                    winningTime = int(time.time() - timerStarter)
                    setVariables(secondPlayer, firstPlayer, lang, firstPlayer, settleScoreAttacker(destroyedBlocks, seconds-winningTime), seconds-winningTime, seconds)
                elif settleScoreAttacker(destroyedBlocks, seconds-winningTime) < points:
                    winningTime = int(lastTime)
                    startWinnerWindow(secondPlayer, firstPlayer, points, lastTime, lang)
                elif points < settleScoreAttacker(destroyedBlocks, seconds-winningTime):
                    winningTime = int(time.time() - timerStarter)
                    startWinnerWindow(firstPlayer, secondPlayer, settleScoreAttacker(destroyedBlocks, seconds-winningTime), seconds-winningTime, lang)
                elif points == settleScoreAttacker(destroyedBlocks, seconds-winningTime):
                    winningTime = int(lastTime)
                    setVariables(secondPlayer, firstPlayer, lang, secondPlayer, points, lastSongDuration-winningTime, lastSongDuration)


        if attackingPhase:
            if minutesAttacking == 0 and secondsAttacking == 0:
                if winnerGlobal == None:
                    winningTime = int(time.time() - timerStarter)
                    setVariables(secondPlayer, firstPlayer, lang, firstPlayer,
                                 settleScoreAttacker(destroyedBlocks, songSecondsDuration - winningTime),
                                 songSecondsDuration - winningTime, songSecondsDuration)
                elif settleScoreAttacker(destroyedBlocks, songSecondsDuration - winningTime) < points:
                    winningTime = int(lastTime)
                    startWinnerWindow(secondPlayer, firstPlayer, points, lastTime, lang)
                elif points < settleScoreAttacker(destroyedBlocks, songSecondsDuration - winningTime):
                    winningTime = int(time.time() - timerStarter)
                    startWinnerWindow(firstPlayer, secondPlayer,
                                      settleScoreAttacker(destroyedBlocks, songSecondsDuration - winningTime),
                                      songSecondsDuration - winningTime, lang)
                elif points == settleScoreAttacker(destroyedBlocks, songSecondsDuration - winningTime):
                    winningTime = int(lastTime)
                    setVariables(secondPlayer, firstPlayer, lang, secondPlayer, points, lastSongDuration - winningTime,
                                 lastSongDuration)

        screen.blit(keysAttacker, (1620*scaleFactorWidth, 930))
        screen.blit(keysDefender, (30*scaleFactorWidth, 930))


        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    sys.exit()


setVariables("Felipe", "Esteban", "en", None, 0.0, 0, 0)
