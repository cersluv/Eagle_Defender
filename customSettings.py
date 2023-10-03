import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import os
from googletrans import Translator
from loginConfig import configColorPalet, configSpecialEffect, configChangeSelectedSong
"""
input: user (str), songList (list), language (str)
summary: It starts the custom settings window, with the user that has logged in before
output: None
"""


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
    colorsRect = pygame.Rect(320, 320, 440, 250)
    effectsRect = pygame.Rect(1160, 320, 440, 250)
    musicRect = pygame.Rect(320, 695, 440, 250)
    textureRect = pygame.Rect(1160, 695, 440, 250)

    # Rectangles for every palette
    palette1 = pygame.Rect(260, 555, 190, 50)
    palette2 = pygame.Rect(855, 555, 190, 50)
    palette3 = pygame.Rect(1460, 555, 190, 50)
    palette4 = pygame.Rect(550, 980, 190, 50)
    palette5 = pygame.Rect(1160, 980, 190, 50)

    # Rectangles in the music selection, also the coordinates of the text for every song
    song1 = pygame.Rect(centerX - 205, centerY - 75, 410, 60)
    fill1 = pygame.Rect(centerX - 200, centerY - 70, 400, 50)
    song2 = pygame.Rect(centerX - 205, centerY + 65, 410, 60)
    fill2 = pygame.Rect(centerX - 200, centerY + 70, 400, 50)
    song3 = pygame.Rect(centerX - 205, centerY + 205, 410, 60)
    fill3 = pygame.Rect(centerX - 200, centerY + 210, 400, 50)

    """
    Input: None
    Summary: Draws the rectangles to put the name of every song
    Output: None
    """

    def drawRect():
        # pygame.draw.rect(window, (0, 128, 255), palette1, 0)
        # pygame.draw.rect(window, (80, 128, 255), palette2, 0)
        # pygame.draw.rect(window, (150, 128, 255), palette3, 0)
        # pygame.draw.rect(window, (0, 128, 255), palette4, 0)
        # pygame.draw.rect(window, (0, 128, 255), palette5, 0)

        pygame.draw.rect(window, (255, 255, 255), song1, 0)
        pygame.draw.rect(window, (0, 0, 0), fill1, 0)
        pygame.draw.rect(window, (255, 255, 255), song2, 0)
        pygame.draw.rect(window, (0, 0, 0), fill2, 0)
        pygame.draw.rect(window, (255, 255, 255), song3, 0)
        pygame.draw.rect(window, (0, 0, 0), fill3, 0)

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
                        scaledImage = pygame.transform.scale(backgroundColors, (newWidth, newHeigth))
                        colorsWindow = True
                        configurationsWindow = False

                    if effectsRect.collidepoint(event.pos):
                        pass
                    if musicRect.collidepoint(event.pos):
                        scaledImage = pygame.transform.scale(backgroundMusic, (newWidth, newHeigth))
                        musicWindow = True
                        configurationsWindow = False

                    if textureRect.collidepoint(event.pos):
                        pass
                # It enters the if when the button of color settings is pressed
                if colorsWindow:
                    # Check which of the palettes is pressed
                    if palette1.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        configColorPalet("Palette 1", user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))

                    if palette2.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        configColorPalet("Palette 2", user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))

                    if palette3.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        configColorPalet("Palette 3", user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))

                    if palette4.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        configColorPalet("Palette 4", user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))

                    if palette5.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        configColorPalet("Palette 5", user)
                        scaledImage = pygame.transform.scale(backgroundSettings, (newWidth, newHeigth))
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
