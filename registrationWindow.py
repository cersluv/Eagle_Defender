import cv2
import pygame
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import os
from googletrans import Translator
import re
import subprocess

from musicHandler import buttonSoundEffect


def startRegistrationWindow(targetLanguage):
    # Initialize pygame
    pygame.init()
    pygame.display.set_caption("Eagle Defender - Registration")

    # Constants
    font = pygame.font.Font(None, 36)

    boolSub = False

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeight = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeight))

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

    print(f'{scaleFactorWidth} / {scaleFactorHeight}')

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeight)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeight = int(originalHeight * minScaleFactor)
    scaledImage = pygame.transform.scale(image, (newWidth, newHeight))

    # Image upload
    uploadedImage = ""
    imagePreviewRect = pygame.Rect(1547 * scaleFactorWidth, 540 * scaleFactorHeight,
                                   1000 * scaleFactorWidth, 500 * scaleFactorHeight)

    uploadButtonRect = pygame.Rect(710 * scaleFactorWidth, 820 * scaleFactorHeight,
                                   (inputBoxWidth + 200) * scaleFactorWidth, inputBoxHeight * scaleFactorHeight)

    uploadImageRect = pygame.Rect(1500 * scaleFactorWidth, 400 * scaleFactorHeight,
                                  (inputBoxWidth + 200) * scaleFactorWidth, inputBoxHeight * scaleFactorHeight)

    maxImageSizeBytes = 300 * 1024 * 1024  # 300MB limit

    # Define a Next button rectangle
    nextButtonRect = pygame.Rect(810 * scaleFactorWidth, 980 * scaleFactorHeight,
                                 300 * scaleFactorWidth, 50 * scaleFactorHeight)

    # Define a Subscription button rectangle
    subButtonRect = pygame.Rect(1525 * scaleFactorWidth, 940 * scaleFactorHeight,
                                350 * scaleFactorWidth, 50 * scaleFactorHeight)

    # Position the input boxes at the center
    inputBoxUsername = pygame.Rect(810 * scaleFactorWidth,
                                   425 * scaleFactorHeight, inputBoxWidth * scaleFactorWidth,
                                   inputBoxHeight * scaleFactorHeight)

    inputBoxPassword = pygame.Rect(810 * scaleFactorWidth,
                                   590 * scaleFactorHeight, inputBoxWidth * scaleFactorWidth,
                                   inputBoxHeight * scaleFactorHeight)

    inputConfirmPassword = pygame.Rect(810 * scaleFactorWidth,
                                       740 * scaleFactorHeight, inputBoxWidth * scaleFactorWidth,
                                       inputBoxHeight * scaleFactorHeight)

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
    Input: None
    Summary: Function to update and display the uploaded image preview on the screen
    Output: None
    """

    def updateImagePreview():
        if uploadedImage:
            scaledImage = pygame.transform.scale(uploadedImage,
                                                 (int(300 * scaleFactorWidth), int(300 * scaleFactorHeight)))
            window.blit(scaledImage, imagePreviewRect)

    """
    Input: text
    Summary: Function to check if the given text completes all regulations for username
    Output: Str with answer
    """

    def usernameVerification(text):
        if len(text) < 5:
            return str("Nombre de usuario tiene que ser de al menos 5 caracteres de largo")

        hasLetters = False
        for char in text:
            if char.isalpha():
                hasLetters = True

            if hasLetters:
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

    def saveInformation(currentPosition):
        mainDir = f"Data/{textUsername}/"
        os.makedirs(os.path.dirname(f"{mainDir}Images/"), exist_ok=True)
        filePath = "Data/" + textUsername + "/information.txt"
        with open(filePath, "w", encoding='utf-8') as file:
            file.write(textPassword + "\n")
            file.write(str(boolSub) + "\n")
        with open("Data/tempUser.txt", "w", encoding='utf-8') as tempFile:
            tempFile.write(f"{textUsername}\n")
            tempFile.write(f"{targetLanguage}\n")
            tempFile.write(f"{currentPosition}\n")

        pygame.image.save(uploadedImage, f"{mainDir}Images/icon.png")

        if os.path.exists('icon.png'):
            os.remove('icon.png')
        else:
            pass


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
                if uploadImageRect.collidepoint(event.pos):
                    buttonSoundEffect()
                    camera = cv2.VideoCapture(0)
                    face_cascade = cv2.CascadeClassifier('visuals/faceRecognition/haarcascade_frontalface_default.xml')
                    boolImageTake = True
                    while boolImageTake:
                        # Retrieve the camera frame
                        print("Toma de foto")
                        ret, frame = camera.read()
                        if not ret:
                            boolImageTake = False

                        if not camera.isOpened():
                            boolImageTake = False
                            camera.release()

                        faceImage = None
                        # Detect and display faces
                        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

                        for (x, y, w, h) in faces:
                            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                            # Extract and save the detected face as 'faceReference.jpg'
                            faceImage = frame[y:y + h, x:x + w]
                            cv2.imwrite('icon.png', faceImage)
                            boolImageTake = False
                            camera.release()
                            uploadedImage = pygame.image.load('icon.png')

                        # Display the frame in the Pygame window
                        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        pygame_frame = pygame.surfarray.make_surface(frame)
                        pygame_frame = pygame.transform.scale(pygame_frame,
                                                              (300 * scaleFactorWidth,
                                                               300 * scaleFactorHeight))  # Resize frame
                        angle = 270  # Angle in degrees, adjust as needed
                        rotated_frame = pygame.transform.rotate(pygame_frame, angle)
                        window.blit(rotated_frame,
                                    (1547 * scaleFactorWidth, 540 * scaleFactorHeight))  # Set the desired position

                        pygame.display.update()

                if uploadButtonRect.collidepoint(event.pos):
                    buttonSoundEffect()
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
                    buttonSoundEffect()
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
                        currentPosition = pygame.mixer.music.get_pos()
                        saveInformation(currentPosition)
                        running = False

                if subButtonRect.collidepoint(event.pos):
                    buttonSoundEffect()
                    if boolSub:
                        boolSub = False
                        print(boolSub)
                    else:
                        boolSub = True
                        print(boolSub)

            if event.type == pygame.KEYDOWN:
                if activeUsername:
                    if event.key == pygame.K_RETURN:
                        textUsername = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textUsername = textUsername[:-1]
                    else:
                        textUsername += event.unicode
                if activePassword:
                    if event.key == pygame.K_RETURN:
                        textPassword = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textPassword = textPassword[:-1]
                    else:
                        textPassword += event.unicode
                if activeConfirmPassword:
                    if event.key == pygame.K_RETURN:
                        textConfirmPassword = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textConfirmPassword = textConfirmPassword[:-1]
                    else:
                        textConfirmPassword += event.unicode

        window.fill((0, 0, 0))
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeight - newHeight) // 2))

        #pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)

        #pygame.draw.rect(window, (0, 128, 255), subButtonRect, 0)

        #pygame.draw.rect(window, (0, 128, 255), uploadImageRect, 0)

        updateImagePreview()

        pygame.draw.rect(window, boxUsernameColor, inputBoxUsername, 2)
        pygame.draw.rect(window, boxPasswordColor, inputBoxPassword, 2)
        pygame.draw.rect(window, boxConfirmPasswordColor, inputConfirmPassword, 2)


        txtSurfaceUsername = font.render(textUsername, True, colorUsername)
        txtSurfacePassword = font.render("*" * len(textPassword), True, colorPassword)
        txtSurfaceConfirmPassword = font.render("*" * len(textConfirmPassword), True, colorPassword)

        window.blit(txtSurfaceUsername, (815 * scaleFactorWidth, 430 * scaleFactorHeight))

        window.blit(txtSurfacePassword, (815 * scaleFactorWidth, 595 * scaleFactorHeight))

        window.blit(txtSurfaceConfirmPassword, (815 * scaleFactorWidth, 745 * scaleFactorHeight))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
    subprocess.run(["python", "registrationWindowSecond.py"])

# startRegistrationWindow("en")
