import pygame
import sys
from HoFConfig import checkNewHighScores


def startWinnerWindow(winner, loser, points, time, language):
    pygame.init()
    screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Initialize the display
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
    pygame.display.set_caption("Winner!")

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
    if language == "es":
        background = pygame.image.load("visuals/imágenesEspañol/win.png")
    if language == "en":
        background = pygame.image.load("visuals/imágenesInglés/win.png")

    scaledImage = pygame.transform.scale(background, (newWidth, newHeigth))

    font = pygame.font.Font("visuals/Chromium One Std Regular.ttf", 70 * int(scaleFactorWidth))
    font2 = pygame.font.Font("visuals/Chromium One Std Regular.ttf", 40 * int(scaleFactorWidth))


    winnerText = pygame.Rect(900 * scaleFactorWidth, 460 * scaleFactorHeight, 100 * scaleFactorWidth, 100 * scaleFactorHeight)
    pointsText = pygame.Rect(900 * scaleFactorWidth, 700 * scaleFactorHeight, 100 * scaleFactorWidth,100 * scaleFactorHeight)
    hofText = pygame.Rect(900 * scaleFactorWidth, 850 * scaleFactorHeight, 100 * scaleFactorWidth,
                             100 * scaleFactorHeight)

    hofVariable = checkNewHighScores(winner, loser, time, points, language)
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(scaledImage,((screenWidth - newWidth) // 2, (screenHeight - newHeigth) // 2))

        #pygame.draw.rect(screen, (255,255,255), hofText,0)
        text1 = font.render(winner, True, ("#EDDEDE"))
        textRect1 = text1.get_rect(center=winnerText.center)
        screen.blit(text1, textRect1)

        text2 = font.render(str(points), True, ("#EDDEDE"))
        textRect2 = text2.get_rect(center=pointsText.center)
        screen.blit(text2, textRect2)


        if hofVariable == 1:
            if language == "es":
                text3 = font2.render(f"¡Felicidades {winner}, entraste a las mejores puntuaciones!", True, ("#EDDEDE"))
            if language == "en":
                text3 = font2.render(f"Congratulations {winner}, you are now in the hall of fame!", True, ("#EDDEDE"))
            textRect3 = text3.get_rect(center=hofText.center)
            screen.blit(text3, textRect3)

        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()




def startWinnerWindowSolo(winner, points, language):
    pygame.init()
    screenWidth, screenHeight = pygame.display.Info().current_w, pygame.display.Info().current_h

    # Initialize the display
    screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.FULLSCREEN)
    pygame.display.set_caption("Winner!")

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
    if language == "es":
        background = pygame.image.load("visuals/imágenesEspañol/win.png")
    if language == "en":
        background = pygame.image.load("visuals/imágenesInglés/win.png")

    scaledImage = pygame.transform.scale(background, (newWidth, newHeigth))

    font = pygame.font.Font("visuals/Chromium One Std Regular.ttf", 70 * int(scaleFactorWidth))
    font2 = pygame.font.Font("visuals/Chromium One Std Regular.ttf", 40 * int(scaleFactorWidth))


    winnerText = pygame.Rect(900 * scaleFactorWidth, 460 * scaleFactorHeight, 100 * scaleFactorWidth, 100 * scaleFactorHeight)
    pointsText = pygame.Rect(900 * scaleFactorWidth, 700 * scaleFactorHeight, 100 * scaleFactorWidth,100 * scaleFactorHeight)
    hofText = pygame.Rect(900 * scaleFactorWidth, 850 * scaleFactorHeight, 100 * scaleFactorWidth,
                             100 * scaleFactorHeight)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        screen.blit(scaledImage,((screenWidth - newWidth) // 2, (screenHeight - newHeigth) // 2))

        #pygame.draw.rect(screen, (255,255,255), hofText,0)
        text1 = font.render(winner, True, ("#EDDEDE"))
        textRect1 = text1.get_rect(center=winnerText.center)
        screen.blit(text1, textRect1)

        text2 = font.render(str(points), True, ("#EDDEDE"))
        textRect2 = text2.get_rect(center=pointsText.center)
        screen.blit(text2, textRect2)


        pygame.display.flip()

    # Quit pygame
    pygame.quit()
    sys.exit()
#startWinnerWindowSolo("Felipe", 811.0, "es")