import random
import pygame
import sys
import tkinter.messagebox as tkMessageBox
from googletrans import Translator
from localMultiplayer import setVariables

import customSettings
import loginConfig
import menu
from musicHandler import buttonSoundEffect


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
                     "¿Cuál es su deporte favorito?", "¿Cuál es su color favorito?"]

    if language == "en":
        image = pygame.image.load('visuals/imágenesInglés/14.png')
        questions = ["In which country would you like to live?", "What is your favorite book?",
                     "What is your favorite animal?",
                     "What is your favorite sport?", "What is your favorite color?"]

    # Constants
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

    print(f'{scaleFactorWidth} / {scaleFactorHeigth}')

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(image, (newWidth, newHeigth))
    pygame.display.set_caption("Eagle Defender - Registration")

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
    nextButtonRect = pygame.Rect(int(220.0 * scaleFactorWidth), int(960 * scaleFactorHeigth), 300, 50)
    # pygame.draw.rect(window, (0, 128, 2), nextButtonRect, 0)
    print(f'{centerX - inputBoxWidth // 0.405} / {centerY + 420}')

    # Position the input boxes at the center
    inputQuestion1 = pygame.Rect(int(220.0 * scaleFactorWidth), int(740 * scaleFactorHeigth), inputBoxWidth,
                                 inputBoxHigth)
    print(f'{centerX - inputBoxWidth // 0.405} / {centerY + 200}')
    inputQuestion2 = pygame.Rect(int(220.0 * scaleFactorWidth), int(890 * scaleFactorHeigth), inputBoxWidth,
                                 inputBoxHigth)
    print(f'{centerX - inputBoxWidth // 0.405} / {centerY + 350}')

    colorActive = pygame.Color('#BD2927')
    inputQ1Color = inputQ2Color = colorInactive = pygame.Color('#FFD6D5')
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
                inputQ1Color = colorInactive
                inputQ2Color = colorInactive
                # Check if Q1 or Q2 input boxes were clicked
                if inputQuestion1.collidepoint(event.pos):
                    activeQuestion1 = not activeQuestion1
                    inputQ1Color = colorActive
                    inputQ2Color = colorInactive
                else:
                    activeQuestion1 = False

                if inputQuestion2.collidepoint(event.pos):
                    activeQuestion2 = not activeQuestion2
                    inputQ1Color = colorInactive
                    inputQ2Color = colorActive

                else:
                    activeQuestion2 = False

                # Check if the Next button was clicked
                if nextButtonRect.collidepoint(event.pos):
                    buttonSoundEffect()
                    try:
                        if not loginConfig.questionsLogin(textQuestion1, textQuestion2, user):
                            # Passwords do not match, display a pop-up error message
                            error_message = translateText("Respuestas Incorrectas", targetLanguage)
                            tkMessageBox.showerror("Error", error_message)
                        else:
                            menu.principalMenu(user, language)
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
        pygame.draw.rect(window, inputQ1Color, inputQuestion1, 2)
        pygame.draw.rect(window, inputQ2Color, inputQuestion2, 2)
        pygame.display.flip()
        clock.tick(30)

        for i, question in enumerate(randomQuestions):
            label = font.render(question, True, (255, 255, 255))
            label_rect = label.get_rect(center=(369 * scaleFactorWidth, (i + 5.6) * 125 * scaleFactorHeigth))
            print(f'{screenWidth // 5.2} / {(i + 5.6) * 125}')
            window.blit(label, label_rect)

        # Render the text input fields
        txtSurfaceQuestion1 = font.render(textQuestion1, True, colorInactive)
        txtSurfaceQuestion2 = font.render(textQuestion2, True, colorInactive)


        window.blit(txtSurfaceQuestion1, (225 * scaleFactorWidth, 745 * scaleFactorHeigth))

        window.blit(txtSurfaceQuestion2, (225 * scaleFactorWidth, 895 * scaleFactorHeigth))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

def startQuestionLoginSecond(firstUser,firstLanguage, user, language):
    # Initialize pygame
    print(user, language)
    pygame.init()
    questions = []
    # Load your image
    if language == "es":
        image = pygame.image.load('visuals/imágenesEspañol/4.png')
        questions = ["¿En cuál país le gustaria vivir?", "¿Cuál es su libro favorito?", "¿Cuál es su animal favorito?",
                     "¿Cuál es su deporte favorito?", "¿Cuál es su color favorito?"]

    if language == "en":
        image = pygame.image.load('visuals/imágenesInglés/14.png')
        questions = ["In which country would you like to live?", "What is your favorite book?",
                     "What is your favorite animal?",
                     "What is your favorite sport?", "What is your favorite color?"]

    # Constants
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

    print(f'{scaleFactorWidth} / {scaleFactorHeigth}')

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)
    scaledImage = pygame.transform.scale(image, (newWidth, newHeigth))
    pygame.display.set_caption("Eagle Defender - Registration")

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
    nextButtonRect = pygame.Rect(int(220.0 * scaleFactorWidth), int(960 * scaleFactorHeigth), 300, 50)
    # pygame.draw.rect(window, (0, 128, 2), nextButtonRect, 0)
    print(f'{centerX - inputBoxWidth // 0.405} / {centerY + 420}')

    # Position the input boxes at the center
    inputQuestion1 = pygame.Rect(int(220.0 * scaleFactorWidth), int(740 * scaleFactorHeigth), inputBoxWidth,
                                 inputBoxHigth)
    print(f'{centerX - inputBoxWidth // 0.405} / {centerY + 200}')
    inputQuestion2 = pygame.Rect(int(220.0 * scaleFactorWidth), int(890 * scaleFactorHeigth), inputBoxWidth,
                                 inputBoxHigth)
    print(f'{centerX - inputBoxWidth // 0.405} / {centerY + 350}')

    colorActive = pygame.Color('#BD2927')
    inputQ1Color = inputQ2Color = colorInactive = pygame.Color('#FFD6D5')
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
                inputQ1Color = colorInactive
                inputQ2Color = colorInactive
                # Check if Q1 or Q2 input boxes were clicked
                if inputQuestion1.collidepoint(event.pos):
                    activeQuestion1 = not activeQuestion1
                    inputQ1Color = colorActive
                    inputQ2Color = colorInactive
                else:
                    activeQuestion1 = False

                if inputQuestion2.collidepoint(event.pos):
                    activeQuestion2 = not activeQuestion2
                    inputQ1Color = colorInactive
                    inputQ2Color = colorActive

                else:
                    activeQuestion2 = False

                # Check if the Next button was clicked
                if nextButtonRect.collidepoint(event.pos):
                    buttonSoundEffect()
                    try:
                        if not loginConfig.questionsLogin(textQuestion1, textQuestion2, user):
                            # Passwords do not match, display a pop-up error message
                            error_message = translateText("Respuestas Incorrectas", targetLanguage)
                            tkMessageBox.showerror("Error", error_message)
                        else:
                            setVariables(firstUser,firstLanguage,user,1)
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
        pygame.draw.rect(window, inputQ1Color, inputQuestion1, 2)
        pygame.draw.rect(window, inputQ2Color, inputQuestion2, 2)
        pygame.display.flip()
        clock.tick(30)

        for i, question in enumerate(randomQuestions):
            label = font.render(question, True, (255, 255, 255))
            label_rect = label.get_rect(center=(369 * scaleFactorWidth, (i + 5.6) * 125 * scaleFactorHeigth))
            print(f'{screenWidth // 5.2} / {(i + 5.6) * 125}')
            window.blit(label, label_rect)

        # Render the text input fields
        txtSurfaceQuestion1 = font.render(textQuestion1, True, colorInactive)
        txtSurfaceQuestion2 = font.render(textQuestion2, True, colorInactive)

        window.blit(txtSurfaceQuestion1, (225 * scaleFactorWidth, 745 * scaleFactorHeigth))

        window.blit(txtSurfaceQuestion2, (225 * scaleFactorWidth, 895 * scaleFactorHeigth))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

#startQuestionLogin("carlos", "en")
