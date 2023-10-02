import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import os
from googletrans import Translator

"""
input: user (str), songList (list), language (str)
summary: It starts the custom settings window, with the user that has logged in before
output: None
"""
def startCustomSettings(user, songList, language):
    pygame.init()

    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 30)


    # Set screen resolution
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    window = pygame.display.set_mode((screen_width, screen_height))

    #Get the center of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2

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
    original_width, original_height = backgroundSettings.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scale_factor_width = screen_width / original_width
    scale_factor_height = screen_height / original_height

    # Choose the minimum scaling factor to maintain aspect ratio
    min_scale_factor = min(scale_factor_width, scale_factor_height)

    # Scale the image while maintaining aspect ratio
    new_width = int(original_width * min_scale_factor)
    new_height = int(original_height * min_scale_factor)
    scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))



    #Rectangles for every button in this window
    colorsRect = pygame.Rect(320, 320, 440, 250)
    effectsRect = pygame.Rect(1160, 320, 440, 250)
    musicRect = pygame.Rect(320, 695, 440, 250)
    textureRect = pygame.Rect(1160, 695, 440, 250)

    #Rectangles for every palette
    palette1 = pygame.Rect(260, 555, 190, 50)
    palette2 = pygame.Rect(855, 555, 190, 50)
    palette3 = pygame.Rect(1460, 555, 190, 50)
    palette4 = pygame.Rect(550, 980, 190, 50)
    palette5 = pygame.Rect(1160, 980, 190, 50)

    #Rectangles in the music selection, also the coordinates of the text for every song
    song1 = pygame.Rect(center_x - 205, center_y - 75, 410, 60)
    fill1 = pygame.Rect(center_x - 200, center_y - 70, 400, 50)
    song2 = pygame.Rect(center_x - 205, center_y + 65, 410, 60)
    fill2 = pygame.Rect(center_x - 200, center_y + 70, 400, 50)
    song3 = pygame.Rect(center_x - 205, center_y + 205, 410, 60)
    fill3 = pygame.Rect(center_x - 200, center_y + 210, 400, 50)

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
                        scaled_image = pygame.transform.scale(backgroundColors, (new_width, new_height))
                        colorsWindow = True
                        configurationsWindow = False

                    if effectsRect.collidepoint(event.pos):
                        pass
                    if musicRect.collidepoint(event.pos):
                        scaled_image = pygame.transform.scale(backgroundMusic, (new_width, new_height))
                        musicWindow = True
                        configurationsWindow = False

                    if textureRect.collidepoint(event.pos):
                        pass
            #It enters the if when the button of color settings is pressed
                if colorsWindow:
                    # Check which of the palettes is pressed
                    if palette1.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        print("Palette 1")
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))

                    if palette2.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        print("Palette 2")
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))

                    if palette3.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        print("Palette 3")
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))

                    if palette4.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        print("Palette 4")
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))

                    if palette5.collidepoint(event.pos):
                        colorsWindow = False
                        configurationsWindow = True
                        print("Palette 5")
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))
                if musicWindow:
                    draw = True
                    if song1.collidepoint(event.pos):
                        musicWindow = False
                        configurationsWindow = True
                        draw = False
                        print(songList[0])
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))
                    if song2.collidepoint(event.pos):
                        musicWindow = False
                        configurationsWindow = True
                        draw = False
                        print(songList[1])
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))
                    if song3.collidepoint(event.pos):
                        musicWindow = False
                        configurationsWindow = True
                        draw = False
                        print(songList[2])
                        scaled_image = pygame.transform.scale(backgroundSettings, (new_width, new_height))


        # Blit the scaled image onto the screen
        window.blit(scaled_image, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))

        if draw:
            drawRect()
            drawText(songList[0], center_x - 180, center_y - 55)
            drawText(songList[1], center_x - 180, center_y + 85)
            drawText(songList[2], center_x - 180, center_y + 225)

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

startCustomSettings("Felipe", ["7 Lágrimas", "Volando Remix", "Amapolas"], "es")