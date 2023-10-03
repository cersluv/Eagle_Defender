import pygame
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import os
from googletrans import Translator
import re
import subprocess


def startRegistrationWindow(targetLanguage):
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Eagle Defender - Registration")

    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)

    boolSub = False

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeight = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeight))

    # Calculate the center of the screen
    centerX = screenWidth // 2
    centerY = screenHeight // 2

    # Set the width and height for the input boxes
    inputBoxWidth = 300
    inputBoxHeight = 32

    # Load your image
    if targetLanguage == "es":
        image = pygame.image.load('visuals/imágenesEspañol/6.png')
    else:
        image = pygame.image.load('visuals/imágenesInglés/16.png')

    # Get the image's original dimensions
    originalWidth, originalHeight = image.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeight = screenHeight / originalHeight

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeight)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeight = int(originalHeight * minScaleFactor)
    scaledImage = pygame.transform.scale(image, (newWidth, newHeight))

    # Image upload
    uploadedImage = ""
    imagePreviewRect = pygame.Rect(centerX + 1175 // 2, centerY, 1000, 500)
    uploadButtonRect = pygame.Rect(centerX - 500 // 2, centerY + 280, inputBoxWidth + 200, inputBoxHeight)
    uploadButtonText = ""
    maxImageSizeBytes = 300 * 1024 * 1024  # 300MB limit

    # Define a Next button rectangle
    nextButtonRect = pygame.Rect(centerX - 150, centerY + 440, 300, 50)
    nextButtonText = "Next"

    # Define a Subscription button rectangle
    subButtonRect = pygame.Rect(centerX + 565, centerY + 400, 350, 50)
    subButtonText = "Sub"

    # Position the input boxes at the center
    inputBoxUsername = pygame.Rect(centerX - inputBoxWidth // 2, centerY - 115, inputBoxWidth, inputBoxHeight)
    inputBoxPassword = pygame.Rect(centerX - inputBoxWidth // 2, centerY + 50, inputBoxWidth, inputBoxHeight)
    inputConfirmPassword = pygame.Rect(centerX - inputBoxWidth // 2, centerY + 200, inputBoxWidth, inputBoxHeight)

    colorActive = pygame.Color('#BD2927')
    colorUsername = colorPassword = colorInactive = pygame.Color('#FFD6D5')
    boxUsernameColor = pygame.Color('#FFD6D5')
    boxPasswordColor = pygame.Color('#FFD6D5')
    boxConfirmPasswordColor = pygame.Color('#FFD6D5')
    textUsername = ''
    textPassword = ''
    textConfirmPassword = ''
    fileExtension = ''
    activeUsername = False
    activePassword = False
    activeConfirmPassword = False

    """
    Input: text, x coords, y coords
    Summary: draws a text on given coords
    Output: None
    """

    def drawText(text, x, y):
        renderedText = font.render(text, True, (0, 0, 0))
        window.blit(renderedText, (x, y))

    """
    Input: None
    Summary: Function to update and display the uploaded image preview on the screen
    Output: None
    """

    def updateImagePreview():
        if uploadedImage:
            window.blit(uploadedImage, imagePreviewRect)

    """
    Input: text
    Summary: Function to check if the given text completes all regulations for username
    Output: Str with answer
    """

    def usernameVerification(text):
        if len(text) < 5:
            return str("Nombre de usuario tiene que ser de al menos 5 caracteres de largo")

        hasLetters = False
        hasNumbers = False

        for char in text:
            if char.isalpha():
                hasLetters = True
            elif char.isdigit():
                hasNumbers = True

            if hasLetters and hasNumbers:
                return ""

        return str("Nombre de usuario tiene que contener al menos 1 letra y 1 número")

    """
    Input: text
    Summary: Function to check if the given text completes all regulations for password
    Output: Str with answer
    """

    def passwordVerification(password):
        if len(password) < 8:
            return str("Contraseña tiene que ser de al menos 8 caracteres de largo")

        if not re.search(r'[A-Z]', password):
            return str("Contraseña tiene contener al menos 1 letra mayúscula")

        if not re.search(r'[a-z]', password):
            return str("Contraseña tiene contener al menos 1 letra minúscula")

        if not re.search(r'[^a-zA-Z0-9]', password):
            return str("Contraseña tiene contener al menos 1 número y 1 letra especial: [!¡@#$%^&*?¿]")

        if textUsername in password:
            return str("Contraseña NO puede contener el nombre de usuario")

        if textPassword != textConfirmPassword:
            return str("Passwords do not match. Please re-enter.")

        return ""

    """
    Input: text, target language code
    Summary: Function to translate a given text using Google Translate
    Output: text translated
    """

    def translateText(text, targetLanguage):
        translator = Translator()
        try:
            translated = translator.translate(text, dest=targetLanguage)
            return translated.text
        except AttributeError as e:
            print("Translation error:", e)
            return text

    """
    Input: None
    Summary: Function to save information for future logins
    Output: None
    """

    def saveInformation():
        mainDir = f"Data/{textUsername}/"
        os.makedirs(os.path.dirname(f"{mainDir}Images/"), exist_ok=True)
        filePath = "Data/" + textUsername + "/information.txt"
        with open(filePath, "w") as file:
            file.write(textPassword + "\n")
            file.write(str(boolSub) + "\n")
        with open("Data/tempUser.txt", "w") as tempFile:
            tempFile.write(f"{textUsername}\n")
            tempFile.write(f"{targetLanguage}\n")

        pygame.image.save(uploadedImage, f"{mainDir}Images/icon{fileExtension}")

    """
    Input: None
    Summary: Function to save information for future logins
    Output: None
    """

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if inputBoxUsername.collidepoint(event.pos):
                    activeUsername = not activeUsername
                    boxUsernameColor = colorActive
                else:
                    activeUsername = False
                    boxUsernameColor = colorInactive
                if inputBoxPassword.collidepoint(event.pos):
                    activePassword = not activePassword
                    boxPasswordColor = colorActive
                else:
                    activePassword = False
                    boxPasswordColor = colorInactive
                if inputConfirmPassword.collidepoint(event.pos):
                    activeConfirmPassword = not activeConfirmPassword
                    boxConfirmPasswordColor = colorActive
                else:
                    activeConfirmPassword = False
                    boxConfirmPasswordColor = colorInactive
                if uploadButtonRect.collidepoint(event.pos):
                    root = tk.Tk()
                    root.withdraw()
                    fileDialog = filedialog.askopenfilename(
                        filetypes=[
                            ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                            ("All files", "*.*")
                        ]
                    )
                    root.destroy()
                    if fileDialog:
                        fileExtension = os.path.splitext(fileDialog)[1]
                        if os.path.getsize(fileDialog) <= maxImageSizeBytes:
                            uploadedImage = pygame.image.load(fileDialog)
                            uploadedImage = pygame.transform.scale(uploadedImage, (300, 300))
                        else:
                            errorMessage = translateText(
                                "Image size exceeds the limit (300MB). Please select a smaller image.", targetLanguage)
                            tkMessageBox.showerror("Error", errorMessage)
                if nextButtonRect.collidepoint(event.pos):
                    if passwordVerification(textPassword) != "":
                        errorMessage = translateText(passwordVerification(textPassword), targetLanguage)
                        tkMessageBox.showerror("Error", errorMessage)

                    elif usernameVerification(textUsername) != "":
                        errorMessage = translateText(usernameVerification(textUsername), targetLanguage)
                        tkMessageBox.showerror("Error", errorMessage)

                    elif uploadedImage == "":
                        errorMessage = translateText("Es necesario cargar una imagen para continuar", targetLanguage)
                        tkMessageBox.showerror("Error", errorMessage)

                    else:
                        saveInformation()
                        running = False

                if subButtonRect.collidepoint(event.pos):
                    if boolSub:
                        boolSub = False
                        print(boolSub)
                    else:
                        boolSub = True
                        print(boolSub)

            if event.type == pygame.KEYDOWN:
                if activeUsername:
                    if event.key == pygame.K_RETURN:
                        username = textUsername
                        textUsername = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textUsername = textUsername[:-1]
                    else:
                        textUsername += event.unicode
                if activePassword:
                    if event.key == pygame.K_RETURN:
                        password = textPassword
                        textPassword = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textPassword = textPassword[:-1]
                    else:
                        textPassword += event.unicode
                if activeConfirmPassword:
                    if event.key == pygame.K_RETURN:
                        password = textConfirmPassword
                        textConfirmPassword = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textConfirmPassword = textConfirmPassword[:-1]
                    else:
                        textConfirmPassword += event.unicode

        window.fill((0, 0, 0))
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeight - newHeight) // 2))

        # drawUploadButton()

        # pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)
        # drawText(nextButtonText, nextButtonRect.x + 10, nextButtonRect.y + 5)

        # pygame.draw.rect(window, (0, 128, 255), subButtonRect, 0)
        # drawText(subButtonText, subButtonRect.x + 10, subButtonRect.y + 5)

        updateImagePreview()

        pygame.draw.rect(window, boxUsernameColor, inputBoxUsername, 2)
        pygame.draw.rect(window, boxPasswordColor, inputBoxPassword, 2)
        pygame.draw.rect(window, boxConfirmPasswordColor, inputConfirmPassword, 2)

        txtSurfaceUsername = font.render(textUsername, True, colorUsername)
        txtSurfacePassword = font.render("*" * len(textPassword), True, colorPassword)
        txtSurfaceConfirmPassword = font.render("*" * len(textConfirmPassword), True, colorPassword)

        window.blit(txtSurfaceUsername, (inputBoxUsername.x + 5, inputBoxUsername.y + 5))
        window.blit(txtSurfacePassword, (inputBoxPassword.x + 5, inputBoxPassword.y + 5))
        window.blit(txtSurfaceConfirmPassword, (inputConfirmPassword.x + 5, inputConfirmPassword.y + 5))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    subprocess.run(["python", "registrationWindowSecond.py"])


#startRegistrationWindow("en")
