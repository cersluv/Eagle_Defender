import pygame
import sys
import os
from googletrans import Translator
#from customSettings import startCustomSettings, startCustomSettingsSecond
from loginConfig import configColorPalet, configSpecialEffect, configChangeSelectedSong
from musicHandler import buttonSoundEffect


def translateText(text, targetLanguage):
    translator = Translator()
    try:
        translated = translator.translate(text, dest=targetLanguage)
        return translated.text
    except AttributeError as e:
        print("Translation error:", e)
        return text


"""
input: user (str), language (str)
summary: It starts the custom color settings window
output: None
"""
def colorsWindow(user, language, palette):
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
                    buttonSoundEffect()
                    configColorPalet("Palette 1", user)
                    running = False
                    try:
                        customsSettingsWindow(user, language, "Palette 1")
                    except():
                        print("error")

                if palette2.collidepoint(event.pos):
                    buttonSoundEffect()
                    configColorPalet("Palette 2", user)
                    running = False
                    try:
                        customsSettingsWindow(user, language, "Palette 2")
                    except():
                        print("error")

                if palette3.collidepoint(event.pos):
                    buttonSoundEffect()
                    configColorPalet("Palette 3", user)
                    running = False
                    try:
                        customsSettingsWindow(user, language, "Palette 3")
                    except():
                        print("error")

                if palette4.collidepoint(event.pos):
                    buttonSoundEffect()
                    configColorPalet("Palette 4", user)
                    running = False
                    try:
                        customsSettingsWindow(user, language, "Palette 4")
                    except():
                        print("error")

                if palette5.collidepoint(event.pos):
                    buttonSoundEffect()
                    configColorPalet("Palette 5", user)
                    running = False
                    try:
                        customsSettingsWindow(user, language, "Palette 5")
                    except():
                        print("error")

        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))
        # drawRect()

        pygame.display.flip()

        # Quit pygame
    pygame.quit()
    sys.exit()

def songsWindow(user,language,palette):
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
        backgroundSongs = pygame.image.load('visuals/imágenesEspañol/10.png')
    if language == "en":
        backgroundSongs = pygame.image.load('visuals/imágenesInglés/20.png')

    # Get the image's original dimensions
    originalWidth, originalHeigth = backgroundSongs.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeigth = screenHeigth / originalHeigth

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(backgroundSongs, (newWidth, newHeigth))

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

    """
        Input: None
        Summary: Draws the rectangles to put the name of every song
        Output: None
        """
    def drawText(text, x, y):
        renderedText = font.render(text, True, (255, 255, 255))
        window.blit(renderedText, (x, y))

    clock = pygame.time.Clock()
    def drawRect():
        pygame.draw.rect(window, (255, 255, 255), song1, 0)
        pygame.draw.rect(window, (0, 0, 0), fill1, 0)
        pygame.draw.rect(window, (255, 255, 255), song2, 0)
        pygame.draw.rect(window, (0, 0, 0), fill2, 0)
        pygame.draw.rect(window, (255, 255, 255), song3, 0)
        pygame.draw.rect(window, (0, 0, 0), fill3, 0)

    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if song1.collidepoint(event.pos):
                    buttonSoundEffect()
                    configChangeSelectedSong(songList[0], user)
                    customsSettingsWindow(user, language, palette)

                if song2.collidepoint(event.pos):
                    buttonSoundEffect()
                    configChangeSelectedSong(songList[1], user)
                    customsSettingsWindow(user, language, palette)

                if song3.collidepoint(event.pos):
                    buttonSoundEffect()
                    configChangeSelectedSong(songList[2], user)
                    customsSettingsWindow(user, language, palette)


        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))


        drawRect()
        drawText(songList[0], centerX - 180, centerY - 55)
        drawText(songList[1], centerX - 180, centerY + 85)
        drawText(songList[2], centerX - 180, centerY + 225)

        pygame.display.flip()

        # Quit pygame
    pygame.quit()
    sys.exit()

def customsSettingsWindow(user, language, palette):
    # Constants
    width, height = 800, 600
    white = (255, 255, 255)

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
    if palette == "Palette 1":
        backgroundSettings = pygame.image.load('visuals/menu/25.png')
    if palette == "Palette 2":
        backgroundSettings = pygame.image.load('visuals/menu/29.png')
    if palette == "Palette 3":
        backgroundSettings = pygame.image.load('visuals/menu/33.png')
    if palette == "Palette 4":
        backgroundSettings = pygame.image.load('visuals/menu/37.png')
    if palette == "Palette 5":
        backgroundSettings = pygame.image.load('visuals/menu/41.png')


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
    colorsRect = pygame.Rect(110 * scaleFactorWidth, 395 * scaleFactorHeigth, 590 * scaleFactorWidth,
                             145 * scaleFactorHeigth)
    effectsRect = pygame.Rect(880 * scaleFactorWidth, 395 * scaleFactorHeigth, 590 * scaleFactorWidth,
                              145 * scaleFactorHeigth)
    musicRect = pygame.Rect(110 * scaleFactorWidth, 570 * scaleFactorHeigth, 590 * scaleFactorWidth,
                            145 * scaleFactorHeigth)
    textureRect = pygame.Rect(880 * scaleFactorWidth, 570 * scaleFactorHeigth, 590 * scaleFactorWidth,
                              145 * scaleFactorHeigth)



    menuButton = pygame.Rect(100 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                             75 * scaleFactorHeigth)
    bestButton = pygame.Rect(640 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                          75 * scaleFactorHeigth)
    helpButton = pygame.Rect(910 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                                       75 * scaleFactorHeigth)


    """
    input: text (str), x coord (int), y coord (int)
    summary: Renders and displays text on the screen
    outputs: None
    """
    def drawText(text, x, y, size):
        font = pygame.font.Font("visuals/LEMONMILK-Bold.ttf", size)
        renderedText = font.render(text, True, (255, 255, 255))
        window.blit(renderedText, (x*scaleFactorWidth, y*scaleFactorHeigth))

    clock = pygame.time.Clock()

    configurationsWindow = True
    musicWindow = False

    def drawRect():
        pygame.draw.rect(window, (255, 255, 255), colorsRect, 0)
        pygame.draw.rect(window, (255, 255, 255), effectsRect, 0)
        pygame.draw.rect(window, (255, 255, 255), musicRect, 0)
        pygame.draw.rect(window, (255, 255, 255), textureRect, 0)
        pygame.draw.rect(window, (255, 255, 255), menuButton, 0)



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
                        buttonSoundEffect()
                        colorsWindow(user, language, palette)

                    if effectsRect.collidepoint(event.pos):
                        buttonSoundEffect()

                    if musicRect.collidepoint(event.pos):
                        buttonSoundEffect()
                        songsWindow(user,language,palette)

                    if textureRect.collidepoint(event.pos):
                        buttonSoundEffect()

                    if menuButton.collidepoint(event.pos):
                        buttonSoundEffect()
                        principalMenu(user,language)

                    if bestButton.collidepoint(event.pos):
                        buttonSoundEffect()
                        bestWindow(user,language,palette)

                    if helpButton.collidepoint(event.pos):
                        buttonSoundEffect()


        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))
        #drawRect()
        if language == "es":
            drawText("Jugar", 165, 245, 35)
            drawText("Configuración", 385, 235, 25)
            drawText("personalizada", 390, 270, 25)
            drawText("Mejores", 710, 235, 25)
            drawText("puntuaciones", 660, 270, 25)
            drawText("Ayuda", 970, 245, 35)

            drawText("Selección de colores", 135, 440, 40)
            drawText("Música", 300, 610, 40 )
            drawText("Efectos de sonido", 940, 440, 40)
            drawText("Texturas", 1065, 610, 40)

        if language == "en":
            drawText("Play", 180, 245, 35)
            drawText("Personalized", 400, 235, 25)
            drawText("configuration", 385, 270, 25)
            drawText("Best", 740, 235, 25)
            drawText("Scores", 715, 270, 25)
            drawText("Help", 1000, 245, 35)

            drawText("Color picker", 235, 440, 40)
            drawText("Music", 320, 610, 40)
            drawText("Sound effects", 1000, 440, 40)
            drawText("Textures", 1065, 610, 40)
        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

def bestWindow(user,language, palette):
    # Constants
    width, height = 800, 600
    white = (255, 255, 255)

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
    if palette == "Palette 1":
        backgroundSettings = pygame.image.load('visuals/menu/26.png')
    if palette == "Palette 2":
        backgroundSettings = pygame.image.load('visuals/menu/30.png')
    if palette == "Palette 3":
        backgroundSettings = pygame.image.load('visuals/menu/34.png')
    if palette == "Palette 4":
        backgroundSettings = pygame.image.load('visuals/menu/38.png')
    if palette == "Palette 5":
        backgroundSettings = pygame.image.load('visuals/menu/42.png')

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

    menuButton = pygame.Rect(100 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                             75 * scaleFactorHeigth)
    configurationsButton = pygame.Rect(370 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                                       75 * scaleFactorHeigth)
    bestButton = pygame.Rect(640 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                          75 * scaleFactorHeigth)
    helpButton = pygame.Rect(910 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                             75 * scaleFactorHeigth)

    """
    input: text (str), x coord (int), y coord (int)
    summary: Renders and displays text on the screen
    outputs: None
    """

    def drawText(text, x, y, size):
        font = pygame.font.Font("visuals/LEMONMILK-Bold.ttf", size)
        renderedText = font.render(text, True, (255, 255, 255))
        window.blit(renderedText, (x*scaleFactorWidth, y*scaleFactorHeigth))

    clock = pygame.time.Clock()

    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the colors configuration button is pressed
                if menuButton.collidepoint(event.pos):
                    buttonSoundEffect()
                    principalMenu(user, language)
                if configurationsButton.collidepoint(event.pos):
                    buttonSoundEffect()
                    customsSettingsWindow(user,language,palette)
                if helpButton.collidepoint(event.pos):
                    buttonSoundEffect()

        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))
        if language == "es":
            drawText("Jugar", 165, 245, 35)
            drawText("Configuración", 385, 235, 25)
            drawText("personalizada", 390, 270, 25)
            drawText("Mejores", 710, 235, 25)
            drawText("puntuaciones", 660, 270, 25)
            drawText("Ayuda", 970, 245, 35)

        if language == "en":
            drawText("Play", 180, 245, 35)
            drawText("Personalized", 400, 235, 25)
            drawText("configuration", 385, 270, 25)
            drawText("Best", 740, 235, 25)
            drawText("Scores", 715, 270, 25)
            drawText("Help", 1000, 245, 35)
        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

def principalMenu(user, language):
    pygame.init()
# Constants
    width, height = 800, 600
    white = (255, 255, 255)


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
    try:
        datapath = os.getcwd() + "\Data"
        personPath = datapath + "\\" + user
        configurationFile = personPath + "\\configuration.txt"
        file = open(configurationFile, "r")
        text = file.read()
        configurationList = text.split("\n")
        palette = configurationList[0]

        if palette == "Palette 1":
            backgroundMainMenu = pygame.image.load('visuals/menu/24.png')
        if palette == "Palette 2":
            backgroundMainMenu = pygame.image.load('visuals/menu/28.png')
        if palette == "Palette 3":
            backgroundMainMenu = pygame.image.load('visuals/menu/32.png')
        if palette == "Palette 4":
            backgroundMainMenu = pygame.image.load('visuals/menu/36.png')
        if palette == "Palette 5":
            backgroundMainMenu = pygame.image.load('visuals/menu/40.png')


    except:
        backgroundMainMenu = pygame.image.load('visuals/menu/28.png')

    pygame.init()
    # Get the image's original dimensions
    originalWidth, originalHeigth = backgroundMainMenu.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeigth = screenHeigth / originalHeigth

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(backgroundMainMenu, (newWidth, newHeigth))

    menuButton = pygame.Rect(100 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                           75 * scaleFactorHeigth)
    configurationsButton = pygame.Rect(370 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                          75 * scaleFactorHeigth)
    bestButton = pygame.Rect(640 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                          75 * scaleFactorHeigth)
    helpButton = pygame.Rect(910 * scaleFactorWidth, 230 * scaleFactorHeigth, 270 * scaleFactorWidth,
                          75 * scaleFactorHeigth)
    button5 = pygame.Rect(105 * scaleFactorWidth, 395 * scaleFactorHeigth, 620 * scaleFactorWidth,
                          580 * scaleFactorHeigth)
    button6 = pygame.Rect(740 * scaleFactorWidth, 398 * scaleFactorHeigth, 620 * scaleFactorWidth,
                          275 * scaleFactorHeigth)
    button7 = pygame.Rect(740 * scaleFactorWidth, 690 * scaleFactorHeigth, 620 * scaleFactorWidth,
                          275 * scaleFactorHeigth)

    """
        Input: None
        Summary: Draws the rectangles to put the name of every song
        Output: None
        """
    def drawRect():
        pass
        #pygame.draw.rect(window, (0, 128, 255), colorsButton, 0)
        #pygame.draw.rect(window, (0, 100, 255), button2, 0)
        #pygame.draw.rect(window, (0, 174, 255), button3, 0)
        #pygame.draw.rect(window, (0, 233, 255), button4, 0)
        #pygame.draw.rect(window, (0, 63, 255), button5, 0)
        #pygame.draw.rect(window, (0, 128, 255), button6, 0)
        #pygame.draw.rect(window, (0, 128, 255), button7, 0)

    def drawText(text, x, y, size):
        font = pygame.font.Font("visuals/LEMONMILK-Bold.ttf", size)
        renderedText = font.render(text, True, (255, 255, 255))
        window.blit(renderedText, (x*scaleFactorWidth, y*scaleFactorHeigth))

    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the colors configuration button is pressed
                if menuButton.collidepoint(event.pos):
                    buttonSoundEffect()
                    principalMenu(user,language)
                # Check which of the palettes is pressed
                if configurationsButton.collidepoint(event.pos):
                    buttonSoundEffect()
                    customsSettingsWindow(user, language, palette)
                if bestButton.collidepoint(event.pos):
                    buttonSoundEffect()
                    bestWindow(user,language,palette)
                if helpButton.collidepoint(event.pos):
                    buttonSoundEffect()


        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))
        #drawRect()
        if language == "es":
            drawText("Jugar", 165, 245, 35)
            drawText("Configuración", 385, 235, 25)
            drawText("personalizada", 390, 270, 25)
            drawText("Mejores", 710, 235, 25)
            drawText("puntuaciones", 660, 270, 25)
            drawText("Ayuda", 970, 245, 35)

            drawText("Modo", 500, 840, 60)
            drawText("solitario", 355, 895, 60)

            drawText("Multijugador", 755, 400, 40)
            drawText("local", 755, 440, 40)

            drawText("En línea", 755, 700, 40)

        if language == "en":
            drawText("Play", 180, 245, 35)
            drawText("Personalized", 400, 235, 25)
            drawText("configuration", 385, 270, 25)
            drawText("Best", 740, 235, 25)
            drawText("Scores", 715, 270, 25)
            drawText("Help", 1000, 245, 35)

            drawText("Solo", 530, 840, 60)
            drawText("mode", 515, 895, 60)

            drawText("Local", 755, 400, 40)
            drawText("multiplayer", 755, 440, 40)

            drawText("Online", 755, 700, 40)
        pygame.display.flip()

        # Quit pygame
    pygame.quit()
    sys.exit()


#principalMenu("Felipe", "en")