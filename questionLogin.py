import random
import pygame
import sys
import tkinter.messagebox as tkMessageBox
from googletrans import Translator

import customSettings
import loginConfig


def getRandomQuestions(questions, numQuestions=2):
    if numQuestions > len(questions):
        numQuestions = len(questions)
    randomQuestions = random.sample(questions, numQuestions)
    return randomQuestions


def startQuestionLogin(user, language):
    # Initialize pygame
    print(user, language)
    pygame.init()
    questions = []
    # Load your image
    if language == "es":
        image = pygame.image.load('visuals/imágenesEspañol/4.png')
        questions = ["¿En cuál país le gustaria vivir?", "¿Cuál es su libro favorito?", "¿Cuál es su animal favorito?",
                     "¿Cuál es su juego de mesa favorito?", "¿Cuál es su pelicula favorita?"]

    if language == "en":
        image = pygame.image.load('visuals/imágenesInglés/14.png')
        questions = ["In which country would you like to live?", "What is your favorite book?",
                     "What is your favorite animal?",
                     "What is your favorite board game?", "What is your favorite movie?"]

    # Constants
    font = pygame.font.Font(None, 36)
    targetLanguage = language
    randomQuestions = getRandomQuestions(questions, numQuestions=2)

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeigth = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeigth))

    # Calculate the center of the screen
    centerX = screenWidth // 2
    centerY = screenHeigth // 2

    # Set the width and height for the input boxes
    inputBoxWidth = 300
    inputBoxHigth = 32

    # Get the image's original dimensions
    originalWidth, originalHeigth = image.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeigth = screenHeigth / originalHeigth

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(image, (newWidth, newHeigth))
    pygame.display.set_caption("Eagle Defender - Registration")

    """
    input: text (str), x coord (int), y coord (int)
    summary: Renders and displays text on the screen
    outputs: None
    """

    def drawText(text, x, y):
        renderedText = font.render(text, True, (0, 0, 0))
        window.blit(renderedText, (x, y))

    """
    input: text, Language code
    summary: uses Google Translate to translate a given text
    outputs: translated language
    """

    def translateText(text, targetLanguage):
        translator = Translator()
        try:
            translated = translator.translate(text, dest=targetLanguage)
            return translated.text
        except AttributeError as e:
            print("Translation error:", e)
            return text  # Return the original text in case of an error

    # Define a Next button rectangle
    nextButtonRect = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 420, 300, 50)
    nextButtonText = ""

    # Position the input boxes at the center
    inputQuestion1 = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 200, inputBoxWidth, inputBoxHigth)
    inputQuestion2 = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 350, inputBoxWidth, inputBoxHigth)

    colorUsername = colorPassword = pygame.Color('#FFD6D5')
    font = pygame.font.Font(None, 32)
    textQuestion1 = ''
    textQuestion2 = ''

    activeQuestion1 = False
    activeQuestion2 = False

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Q1 or Q2 input boxes were clicked
                if inputQuestion1.collidepoint(event.pos):
                    activeQuestion1 = not activeQuestion1
                else:
                    activeQuestion1 = False
                if inputQuestion2.collidepoint(event.pos):
                    activeQuestion2 = not activeQuestion2
                else:
                    activeQuestion2 = False

                # Check if the Next button was clicked
                if nextButtonRect.collidepoint(event.pos):
                    try:
                        if not loginConfig.questionsLogin(textQuestion1, textQuestion2, user):
                            # Passwords do not match, display a pop-up error message
                            error_message = translateText("Respuestas Incorrectas", targetLanguage)
                            tkMessageBox.showerror("Error", error_message)
                        else:
                            customSettings.startCustomSettings(user, language)
                    except():
                        error_message = translateText("Error no reconocido, vuelva a intentarlo", targetLanguage)
                        tkMessageBox.showerror("Error", error_message)

            if event.type == pygame.KEYDOWN:
                if activeQuestion1:
                    if event.key == pygame.K_RETURN:
                        username = textQuestion1
                        textQuestion1 = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textQuestion1 = textQuestion1[:-1]
                    else:
                        textQuestion1 += event.unicode
                if activeQuestion2:
                    if event.key == pygame.K_RETURN:
                        password = textQuestion2
                        textQuestion2 = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textQuestion2 = textQuestion2[:-1]
                    else:
                        textQuestion2 += event.unicode

        # Clear the screen
        window.fill((0, 0, 0))

        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))

        # Draw the border around the input boxes
        pygame.draw.rect(window, '#FFD6D5', inputQuestion1, 2)
        pygame.draw.rect(window, '#FFD6D5', inputQuestion2, 2)
        pygame.display.flip()
        clock.tick(30)

        for i, question in enumerate(randomQuestions):
            label = font.render(question, True, (255, 255, 255))
            label_rect = label.get_rect(center=(screenWidth // 5.2, (i + 5.6) * 125))
            window.blit(label, label_rect)

        # Render the text input fields
        txtSurfaceQuestion1 = font.render(textQuestion1, True, colorUsername)
        txtSurfaceQuestion2 = font.render(textQuestion2, True, colorUsername)

        window.blit(txtSurfaceQuestion1, (inputQuestion1.x + 5, inputQuestion1.y + 5))
        window.blit(txtSurfaceQuestion2, (inputQuestion2.x + 5, inputQuestion2.y + 5))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

# startQuestionLogin("carlos", "en")
