import pygame
import sys
import os
from googletrans import Translator

from loginConfig import configColorPalet, configSpecialEffect, configChangeSelectedSong
#from customSettingsSecond import startCustomSettingsSecond
#from menu import principalMenu



"""
input: user (str), language (str)
summary: It starts the custom color settings window
output: None
"""

def startCustomSettingsSecond(user, language):
    pygame.init()
# Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 30)

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeigth = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeigth))

    # Get the center of the screen
    centerX = screenWidth // 2
    centerY = screenHeigth // 2

    # Set the width and height for the input boxes
    input_box_width = 300
    input_box_height = 32

    # Load your image
    if language == "es":
        backgroundColors = pygame.image.load('visuals/imágenesEspañol/9.png')
    if language == "en":
        backgroundColors = pygame.image.load('visuals/imágenesInglés/19.png')

    # Get the image's original dimensions
    originalWidth, originalHeigth = backgroundColors.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeigth = screenHeigth / originalHeigth

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(backgroundColors, (newWidth, newHeigth))

    palette1 = pygame.Rect(157 * scaleFactorWidth, 230 * scaleFactorHeigth, 400 * scaleFactorWidth,
                           285 * scaleFactorHeigth)
    palette2 = pygame.Rect(760 * scaleFactorWidth, 230 * scaleFactorHeigth, 400 * scaleFactorWidth,
                           285 * scaleFactorHeigth)
    palette3 = pygame.Rect(1362 * scaleFactorWidth, 230 * scaleFactorHeigth, 400 * scaleFactorWidth,
                           285 * scaleFactorHeigth)
    palette4 = pygame.Rect(455 * scaleFactorWidth, 655 * scaleFactorHeigth, 400 * scaleFactorWidth,
                           285 * scaleFactorHeigth)
    palette5 = pygame.Rect(1067 * scaleFactorWidth, 655 * scaleFactorHeigth, 400 * scaleFactorWidth,
                           285 * scaleFactorHeigth)

    """
        Input: None
        Summary: Draws the rectangles to put the name of every song
        Output: None
        """
    def drawRect():
        pygame.draw.rect(window, (0, 128, 255), palette1, 0)
        pygame.draw.rect(window, (80, 128, 255), palette2, 0)
        pygame.draw.rect(window, (150, 128, 255), palette3, 0)
        pygame.draw.rect(window, (0, 128, 255), palette4, 0)
        pygame.draw.rect(window, (0, 128, 255), palette5, 0)


    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the colors configuration button is pressed

                    # Check which of the palettes is pressed
                if palette1.collidepoint(event.pos):
                    configColorPalet("Palette 1", user)
                    running = False
                    try:
                        startCustomSettings(user,language)
                    except():
                        print("error")

                if palette2.collidepoint(event.pos):
                    configColorPalet("Palette 2", user)
                    running = False
                    try:
                        startCustomSettings(user, language)
                    except():
                        print("error")

                if palette3.collidepoint(event.pos):
                    configColorPalet("Palette 3", user)
                    running = False
                    try:
                        startCustomSettings(user, language)
                    except():
                        print("error")

                if palette4.collidepoint(event.pos):
                    configColorPalet("Palette 4", user)
                    running = False
                    try:
                        startCustomSettings(user, language)
                    except():
                        print("error")

                if palette5.collidepoint(event.pos):
                    configColorPalet("Palette 5", user)
                    running = False
                    try:
                        startCustomSettings(user, language)
                    except():
                        print("error")

        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))
        #drawRect()

        pygame.display.flip()

        # Quit pygame
    pygame.quit()
    sys.exit()

def startCustomSettings(user, language):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    musicPath = personPath + "\Music"
    musicList = os.listdir(musicPath)
    songList = []
    for x in musicList:
        y = x.replace(".mp3", "")
        songList.append(y)
    pygame.init()

    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 30)

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeigth = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeigth))

    # Get the center of the screen
    centerX = screenWidth // 2
    centerY = screenHeigth // 2

    # Set the width and height for the input boxes
    input_box_width = 300
    input_box_height = 32

    # Load your image
    if language == "es":
        backgroundSettings = pygame.image.load('visuals/imágenesEspañol/8.png')
        backgroundColors = pygame.image.load('visuals/imágenesEspañol/9.png')
        backgroundMusic = pygame.image.load('visuals/imágenesEspañol/10.png')
    if language == "en":
        backgroundSettings = pygame.image.load('visuals/imágenesInglés/18.png')
        backgroundColors = pygame.image.load('visuals/imágenesInglés/19.png')
        backgroundMusic = pygame.image.load('visuals/imágenesInglés/20.png')

    # Get the image's original dimensions
    originalWidth, originalHeigth = backgroundSettings.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeigth = screenHeigth / originalHeigth

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))

    # Rectangles for every button in this window
    colorsRect = pygame.Rect(320 * scaleFactorWidth, 320 * scaleFactorHeigth, 440 * scaleFactorWidth,
                             250 * scaleFactorHeigth)
    effectsRect = pygame.Rect(1160 * scaleFactorWidth, 320 * scaleFactorHeigth, 440 * scaleFactorWidth,
                              250 * scaleFactorHeigth)
    musicRect = pygame.Rect(320 * scaleFactorWidth, 695 * scaleFactorHeigth, 440 * scaleFactorWidth,
                            250 * scaleFactorHeigth)
    textureRect = pygame.Rect(1160 * scaleFactorWidth, 695 * scaleFactorHeigth, 440 * scaleFactorWidth,
                              250 * scaleFactorHeigth)

    # Rectangles for every palette
    palette1 = pygame.Rect(260 * scaleFactorWidth, 555 * scaleFactorHeigth, 190 * scaleFactorWidth,
                           50 * scaleFactorHeigth)
    palette2 = pygame.Rect(855 * scaleFactorWidth, 555 * scaleFactorHeigth, 190 * scaleFactorWidth,
                           50 * scaleFactorHeigth)
    palette3 = pygame.Rect(1460 * scaleFactorWidth, 555 * scaleFactorHeigth, 190 * scaleFactorWidth,
                           50 * scaleFactorHeigth)
    palette4 = pygame.Rect(550 * scaleFactorWidth, 980 * scaleFactorHeigth, 190 * scaleFactorWidth,
                           50 * scaleFactorHeigth)
    palette5 = pygame.Rect(1160 * scaleFactorWidth, 980 * scaleFactorHeigth, 190 * scaleFactorWidth,
                           50 * scaleFactorHeigth)

    # Rectangles in the soundEffects selection, also the coordinates of the text for every song
    song1 = pygame.Rect(centerX - 205 * scaleFactorWidth, centerY - 75 * scaleFactorHeigth, 410 * scaleFactorWidth,
                        60 * scaleFactorHeigth)
    fill1 = pygame.Rect(centerX - 200 * scaleFactorWidth, centerY - 70 * scaleFactorHeigth, 400 * scaleFactorWidth,
                        50 * scaleFactorHeigth)
    song2 = pygame.Rect(centerX - 205 * scaleFactorWidth, centerY + 65 * scaleFactorHeigth, 410 * scaleFactorWidth,
                        60 * scaleFactorHeigth)
    fill2 = pygame.Rect(centerX - 200 * scaleFactorWidth, centerY + 70 * scaleFactorHeigth, 400 * scaleFactorWidth,
                        50 * scaleFactorHeigth)
    song3 = pygame.Rect(centerX - 205 * scaleFactorWidth, centerY + 205 * scaleFactorHeigth, 410 * scaleFactorWidth,
                        60 * scaleFactorHeigth)
    fill3 = pygame.Rect(centerX - 200 * scaleFactorWidth, centerY + 210 * scaleFactorHeigth, 400 * scaleFactorWidth,
                        50 * scaleFactorHeigth)

    readyButton = pygame.Rect(860 * scaleFactorWidth, 960 * scaleFactorHeigth, 200 * scaleFactorWidth,
                        80 * scaleFactorHeigth)

    """
    Input: None
    Summary: Draws the rectangles to put the name of every song
    Output: None
    """

    def drawRect():
        #pygame.draw.rect(window, (0, 128, 255), palette1, 0)
        #pygame.draw.rect(window, (80, 128, 255), palette2, 0)
        #pygame.draw.rect(window, (150, 128, 255), palette3, 0)
        #pygame.draw.rect(window, (0, 128, 255), palette4, 0)
        #pygame.draw.rect(window, (0, 128, 255), palette5, 0)

        pygame.draw.rect(window, (255, 255, 255), song1, 0)
        pygame.draw.rect(window, (0, 0, 0), fill1, 0)
        pygame.draw.rect(window, (255, 255, 255), song2, 0)
        pygame.draw.rect(window, (0, 0, 0), fill2, 0)
        pygame.draw.rect(window, (255, 255, 255), song3, 0)
        pygame.draw.rect(window, (0, 0, 0), fill3, 0)

        #pygame.draw.rect(window, (0, 128, 255), readyButton, 0)

    """
    input: text (str), x coord (int), y coord (int)
    summary: Renders and displays text on the screen
    outputs: None
    """

    def drawText(text, x, y):
        renderedText = font.render(text, True, (255, 255, 255))
        window.blit(renderedText, (x, y))

    clock = pygame.time.Clock()

    configurationsWindow = True
    musicWindow = False
    colorsWindow = False

    draw = False

    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the colors configuration button is pressed
                if configurationsWindow:


                    if colorsRect.collidepoint(event.pos):
                        startCustomSettingsSecond(user,language)
                        #scaledImage = pygame.transform.scale(backgroundColors, (newWidth, newHeigth))
                        #colorsWindow = True
                        #configurationsWindow = False

                    if effectsRect.collidepoint(event.pos):
                        pass
                    if musicRect.collidepoint(event.pos):
                        scaledImage = pygame.transform.scale(backgroundMusic, (newWidth, newHeigth))
                        musicWindow = True
                        configurationsWindow = False

                    if textureRect.collidepoint(event.pos):
                        pass
                    if readyButton.collidepoint(event.pos):
                        pass

                # It enters the if when the button of music settings is pressed
                if musicWindow:
                    draw = True
                    if song1.collidepoint(event.pos):
                        musicWindow = False
                        configurationsWindow = True
                        draw = False
                        configChangeSelectedSong(songList[0], user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))
                    if song2.collidepoint(event.pos):
                        musicWindow = False
                        configurationsWindow = True
                        draw = False
                        configChangeSelectedSong(songList[1], user)

                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))
                    if song3.collidepoint(event.pos):
                        musicWindow = False
                        configurationsWindow = True
                        draw = False
                        configChangeSelectedSong(songList[2], user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))

        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))

        if draw:
            drawRect()
            drawText(songList[0], centerX - 180, centerY - 55)
            drawText(songList[1], centerX - 180, centerY + 85)
            drawText(songList[2], centerX - 180, centerY + 225)

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()


#startCustomSettings("Felipe", "es")
