import os
import random
import pygame

from localMultiplayer import setVariables

# input       : The 2 users that are going to play and the lenguage
# output      : The coin flip Window
# descritpion : A window used to see who´s going to attack first

def startCoinFlip(user1, user2, lenguage):
    print("llegó bien")
    winnerText = []
    if lenguage == "en":
        winnerText = [user1 +" Attacks", user2+" Attacks", "Continue", user1+" selects his side of the coin"]

    if lenguage == "es":
        winnerText = [user1 +" Ataca", user2 +" Ataca", "Continuar", user1+" selecciona su lado de la moneda"]


    # Inicializar Pygame
    pygame.init()

    # Definir colores
    WHITE = (255, 255, 255)

    # Inicializar la pantalla
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeigth = screenInfo.current_h
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Pantalla con Botones")

    # Calculate the center of the screen
    centerX = screenWidth // 2
    centerY = screenHeigth // 2


    # Definir botones y su estado
    coin1Visible = True
    coin2Visible = True
    winnerLabelVisible = False
    continueLabelVisible = False
    selectLabelVisible = True

    font = pygame.font.Font(None, 36)

    # Directory containing the animation images
    framesPath = os.getcwd() + "\\visuals\\frames"
    faceFolder  = framesPath+'\gif_face'
    clawFolder = framesPath + '\gif_claw'
    gacha = [faceFolder, clawFolder]
    randomNumber = random.randint(0, 1) #0 is face  ---- #1 is claw
    n = -1

    # Load images from the directory into a list
    faceIMG = pygame.image.load(faceFolder+'\\frame_82_delay-0.18s.gif')
    clawIMG = pygame.image.load(clawFolder+'\\frame_85_delay-0.09s.gif')




    images = [pygame.image.load(os.path.join(gacha[randomNumber], img)) for img in os.listdir(gacha[randomNumber])]
    scaledImages = []
    for image in images:
        originalWidth, originalHeight = 1920, 1080
        # Calculate the scaling factors to fit the image to the screen
        scaleFactorWidth = screenWidth / originalWidth
        scaleFactorHeigth = screenHeigth / originalHeight
        minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)
        newWidth = int(originalWidth * minScaleFactor)
        newHeigth = int(originalHeight * minScaleFactor)
        scaledImage = pygame.transform.scale(image, (newWidth, newHeigth))
        scaledImages.append(scaledImage)

    # Set the animation speed
    animationSpeed = 15  # in milliseconds
    index = 0
    animationTriggered = False
    clock = pygame.time.Clock()


    # Bucle principal del juego
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if coin1Visible and coin2Visible:
                    if coin1Button.collidepoint(mouse_pos):
                        n = 0
                        coin1Visible = False
                        coin2Visible = False
                        selectLabelVisible = False
                        animationTriggered = True

                    if coin2Button.collidepoint(mouse_pos):
                        n = 1
                        coin1Visible = False
                        coin2Visible = False
                        selectLabelVisible = False
                        animationTriggered = True


                elif winnerLabelVisible:
                    if winnerButton.collidepoint(mouse_pos) or continueButton.collidepoint(mouse_pos):
                        if n == randomNumber:
                            setVariables(user1, user2, lenguage, None, 0, 0, 0)
                            running = False
                        else:
                            setVariables(user2, user1, lenguage, None, 0, 0, 0)
                            running = False

        screen.fill((0, 0, 0))
        if animationTriggered:
            scaledImages[index] = pygame.transform.scale(scaledImages[index], (250*scaleFactorWidth, 500*scaleFactorHeigth))
            screen.blit(scaledImages[index], (centerX - centerX/7.2, centerY/2))
            index += 1

        if index >= len(scaledImages):
            winnerLabelVisible = True
            continueLabelVisible = True
            index = index-1

        pygame.time.delay(animationSpeed)
        clock.tick(60)

        buttonWidth = 100 * scaleFactorWidth
        button_height = 50 * scaleFactorHeigth
        buttonPadding = 200
        startX = (screenWidth - 2 * buttonWidth - buttonPadding) // 2
        buttonY = 250 * scaleFactorHeigth

        if coin1Visible:
            coin1Button = pygame.draw.rect(screen, (0, 0, 255), (
            startX * scaleFactorWidth, buttonY * scaleFactorHeigth, buttonWidth * scaleFactorWidth,
            button_height * scaleFactorHeigth))
            faceIMG = pygame.transform.scale(faceIMG, (250 * scaleFactorWidth, 500 * scaleFactorHeigth))
            screen.blit(faceIMG, (startX - startX / 9.5, buttonY - buttonY / 1.3))

        if coin2Visible:
            coin2Button = pygame.draw.rect(screen, (0, 0, 255), (
            (startX + buttonWidth + buttonPadding) * scaleFactorWidth, buttonY * scaleFactorHeigth, buttonWidth,
            button_height * scaleFactorHeigth))
            clawIMG = pygame.transform.scale(clawIMG, (270 * scaleFactorWidth, 540 * scaleFactorHeigth))
            screen.blit(clawIMG, (startX + startX / 3.5, buttonY - buttonY / 1.18))

        if winnerLabelVisible:
            if n == randomNumber:
                winnerButton = pygame.draw.rect(screen, (0, 0, 0),
                                                (startX * scaleFactorWidth, buttonY * scaleFactorHeigth,
                                                 (2 * buttonWidth + buttonPadding) * scaleFactorWidth,
                                                 button_height * scaleFactorHeigth))
                text = font.render(winnerText[0], True, WHITE)
                text_rect = text.get_rect(center=winnerButton.center)
                screen.blit(text, text_rect)
            else:
                winnerButton = pygame.draw.rect(screen, (0, 0, 0),
                                                (startX * scaleFactorWidth, buttonY * scaleFactorHeigth,
                                                 (2 * buttonWidth + buttonPadding) * scaleFactorWidth,
                                                 button_height * scaleFactorHeigth))
                text = font.render(winnerText[1], True, WHITE)
                text_rect = text.get_rect(center=winnerButton.center)
                screen.blit(text, text_rect)

        if continueLabelVisible:
            continueButton = pygame.draw.rect(screen, (169, 7, 7),
                                              (startX * scaleFactorWidth, (buttonY * 3.3) * scaleFactorHeigth,
                                               (2 * buttonWidth + buttonPadding) * scaleFactorWidth,
                                               button_height * scaleFactorHeigth))
            text = font.render(winnerText[2], True, WHITE)
            text_rect = text.get_rect(center=continueButton.center)
            screen.blit(text, text_rect)

        if selectLabelVisible:
            selectLabelText = pygame.draw.rect(screen, (169, 7, 7),
                                               (startX * scaleFactorWidth, (buttonY * 3.3) * scaleFactorHeigth,
                                                (2 * buttonWidth + buttonPadding + 100) * scaleFactorWidth,
                                                button_height * scaleFactorHeigth))
            text = font.render(winnerText[3], True, WHITE)
            text_rect = text.get_rect(center=selectLabelText.center)
            screen.blit(text, text_rect)
        pygame.display.flip()
    pygame.quit()


#startCoinFlip("DryGoz", "Carlos", "es") # Usage example.