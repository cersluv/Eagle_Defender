import os
from tkinter import *

import cv2
import pygame
import sys
import tkinter.messagebox as tkMessageBox
from googletrans import Translator
from matplotlib import pyplot
from mtcnn import MTCNN

import loginConfig
from questionLogin import startQuestionLogin
from customSettings import startCustomSettings
from registrationWindow import startRegistrationWindow


def startBaseLogin(language):
    # Initialize pygame
    pygame.init()

    # Load your image
    if language == "es":
        image = pygame.image.load('visuals/imágenesEspañol/3.png')

    if language == "en":
        image = pygame.image.load('visuals/imágenesInglés/13.png')

    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    target_language = language

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
    pygame.display.set_caption("Eagle Defender - Login")

    questionCounter = 0

    """
    input: text, Language code
    summary: uses Google Translate to translate a given text
    outputs: translated language
    """

    def translate_text(text, target_language):
        translator = Translator()
        try:
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except AttributeError as e:
            print("Translation error:", e)
            return text  # Return the original text in case of an error

    # Define a Next button rectangle
    nextButtonRect = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 343, 300, 50)
    nextButtonText = ""

    backButtonRect = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 470, 300, 50)
    backButtonText = ""

    # Position the input boxes at the center
    inputBoxUsername = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 120, inputBoxWidth,
                                   inputBoxHeight)
    inputBoxPassword = pygame.Rect(centerX - inputBoxWidth // 0.405, centerY + 270, inputBoxWidth,
                                   inputBoxHeight)

    colorUsername = colorPassword = pygame.Color('#FFD6D5')
    font = pygame.font.Font(None, 32)
    textUsername = ''
    textPassword = ''
    textConfirmPassword = ''
    activeUsername = False
    activePassword = False

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if username or password input boxes were clicked
                if inputBoxUsername.collidepoint(event.pos):
                    activeUsername = not activeUsername
                else:
                    activeUsername = False
                if inputBoxPassword.collidepoint(event.pos):
                    activePassword = not activePassword
                else:
                    activePassword = False

                # Check if the Next button was clicked
                if nextButtonRect.collidepoint(event.pos):
                    try:
                        if questionCounter > 1:
                            startQuestionLogin(textUsername, language)

                        elif not loginConfig.baseLogin(textUsername, textPassword):
                            # Passwords do not match, display a pop-up error message
                            questionCounter += 1
                            errorMessage = translate_text("Contraseña Incorrecta", target_language)
                            tkMessageBox.showerror("Error", errorMessage)
                        else:
                            startCustomSettings(textUsername, language)
                    except(FileNotFoundError):
                        errorMessage = translate_text("Usuario no encontrado", target_language)
                        tkMessageBox.showerror("Error", errorMessage)
                    except():
                        errorMessage = translate_text("Error no reconocido, vuelva a intentarlo", target_language)
                        tkMessageBox.showerror("Error", errorMessage)

                if backButtonRect.collidepoint(event.pos):
                    try:
                        startGame2()
                    except():
                        errorMessage = translate_text("Error no reconocido, vuelva a intentarlo", target_language)
                        tkMessageBox.showerror("Error", errorMessage)

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

        # Clear the screen
        window.fill((0, 0, 0))

        # Blit the scaled image onto the screen
        window.blit(scaledImage, ((screenWidth - newWidth) // 2, (screenHeight - newHeight) // 2))

        # Draw the Next button
        # pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)
        # drawText(nextButtonText, nextButtonRect.x + 10, nextButtonRect.y + 5)

        # pygame.draw.rect(window, (0,128,255), backButtonRect, 0)

        # Draw the border around the input boxes
        pygame.draw.rect(window, '#FFD6D5', inputBoxUsername, 2)
        pygame.draw.rect(window, '#FFD6D5', inputBoxPassword, 2)
        pygame.display.flip()
        clock.tick(30)

        # Render the text input fields
        txtSurfaceUsername = font.render(textUsername, True, colorUsername)
        txtSurfacePassword = font.render("*" * len(textPassword), True, colorPassword)
        txtSurfaceConfirmPassword = font.render("*" * len(textConfirmPassword), True, colorPassword)

        window.blit(txtSurfaceUsername, (inputBoxUsername.x + 5, inputBoxUsername.y + 5))
        window.blit(txtSurfacePassword, (inputBoxPassword.x + 5, inputBoxPassword.y + 5))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()


def startGame2():
    pygame.init()

    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 30)

    # Globals
    global window2
    global passwordVerification
    global userEntry2
    global passwordEntry2

    userVerification = ""

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeight = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeight))

    # Load your image
    backgroundSpanish = pygame.image.load('visuals/imágenesEspañol/2.png')
    backgroundEnglish = pygame.image.load('visuals/imágenesInglés/12.png')
    backgroundFrench = pygame.image.load('visuals/imágenesFrancés/22.png')

    # Get the image's original dimensions
    originalWidth, originalHeigth = backgroundSpanish.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / originalWidth
    scaleFactorHeigth = screenHeight / originalHeigth

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)

    # Scale the image while maintaining aspect ratio
    newWidth = int(originalWidth * minScaleFactor)
    newHeigth = int(originalHeigth * minScaleFactor)

    scaledImage1 = pygame.transform.scale(backgroundSpanish, (newWidth, newHeigth))
    scaledImage2 = pygame.transform.scale(backgroundEnglish, (newWidth, newHeigth))
    scaledImage3 = pygame.transform.scale(backgroundFrench, (newWidth, newHeigth))
    scaledImage = [scaledImage1, scaledImage2, scaledImage3]

    # Rectangles for every button in this window
    faceRect = pygame.Rect(150, 690, 465, 40)
    userRect = pygame.Rect(155, 820, 460, 40)
    registerRect = pygame.Rect(150, 950, 465, 40)
    languageRect = pygame.Rect(1692, 935, 212, 113)

    clock = pygame.time.Clock()

    mainWindow = True

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

    def facialLogin():
        global window2, userVerification
        cap = cv2.VideoCapture(0)  # Choose the camera for face detection
        while (True):
            ret, frame = cap.read()  # Read the video
            cv2.imshow('Login Facial', frame)  # Display the video on screen
            if cv2.waitKey(1) == 32:  # Break the video when the "spaee" key is pressed
                break
        userLoginFace = userVerification  # Save the photo with a different name to avoid overwriting
        datapath = os.getcwd() + "\Data"
        personPath = datapath + "\\" + userLoginFace + "\\Images"
        rostroPath = datapath + "\\" + userLoginFace + "\\Images" + "\\face"
        # lista_archivos = os.listdir(personPath)
        cv2.imwrite(rostroPath + "LOG.jpg",
                    frame)  # Save the last video frame as an image and assign the username as the name
        cap.release()  # Close the video capture
        cv2.destroyAllWindows()

        # Input: an image and a list
        # Description: Function to save the face
        # Output: Data of the img and a confirmation that´s saved
        def logFace(img, result_list):
            data = pyplot.imread(img)
            for i in range(len(result_list)):
                x1, y1, width, heigth = result_list[i]['box']
                x2, y2 = x1 + width, y1 + heigth
                pyplot.subplot(1, len(result_list), i + 1)
                pyplot.axis('off')
                cara_reg = data[y1:y2, x1:x2]
                cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)  # Save the image as 150x200
                return pyplot.imshow(data[y1:y2, x1:x2])
            pyplot.show()

        img = rostroPath + "LOG.jpg"
        pixels = pyplot.imread(img)
        detector = MTCNN()
        faces = detector.detect_faces(pixels)
        logFace(img, faces)

        # Input: two different images
        # Description: Function to compare faces
        # Output: A percentage of how the two faces are alike
        def orbSim(img1, img2):
            global window2
            orb = cv2.ORB_create()  # Create the comparison object

            kpa, descrA = orb.detectAndCompute(img1, None)  # Create descriptor 1 and extract key points
            kpb, descrB = orb.detectAndCompute(img2, None)  # eate descriptor 2 and extract key points
            comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Create a brute force matcher

            matches = comp.match(descrA, descrB)  # Apply the matcher to the descriptors

            similarRegions = [i for i in matches if
                                  i.distance < 70]  # Extract similar regions based on key points
            if len(matches) == 0:
                return 0
            return len(similarRegions) / len(matches)  # Return the similarity percentage

        imFiles = os.listdir(personPath)  # Import the list of files using the os library
        print(os.listdir(personPath))

        if "face.jpg" in imFiles:  # Compare the files with the one we are interested in

            FaceImgReg = cv2.imread(rostroPath + ".jpg", 0)  # Import the registered face
            print(rostroPath)  # Import the registered face

            FaceImgLog = cv2.imread(rostroPath + "LOG.jpg", 0)  # Import the login face

            similitud = orbSim(FaceImgReg, FaceImgLog)
            if similitud >= 0.90:
                window2.destroy()
                print("Bienvenido al sistema usuario: ", userLoginFace)
                print("Compatibilidad con la foto del registro: ", similitud)
                startCustomSettings(userLoginFace, language[changeLanguage])
            else:
                print("Rostro incorrecto, Cerifique su usuario")
                print("Compatibilidad con la foto del registro: ", similitud)
                message = translateText("Incompatibilidad de rostros", language[changeLanguage])
                tkMessageBox.showerror("Error", message)
        else:
            window2.destroy()
            print("Foto no encontrada")
            errorMessage = translateText("Usuario no encontrado", language[changeLanguage])
            tkMessageBox.showerror("Error", errorMessage)

    def login():
        global userVerification, window2

        def getUsername():
            global userVerification
            userVerification = entry.get()
            print(userVerification)
            facialLogin()

        window2 = Tk()
        window2.title("Login")
        window2.config(bg="#1f1f1f")
        screenWidth = window2.winfo_screenwidth()
        screenHeight = window2.winfo_screenheight()
        x = (screenWidth - 300) // 2
        y = (screenHeight - 200) // 2
        window2.geometry(f"{300}x{200}+{x}+{y}")

        window2.overrideredirect(True)

        userVerification = StringVar()

        userText = ""
        cameraText = ""

        if language[changeLanguage] == "es":
            userText = "Usuario"
            cameraText = "Activar cámara"
            exitText = "Go back"

        if language[changeLanguage] == "en":
            userText = "Username"
            cameraText = "Enable camera"
            exitText = "Regresar"

        Label(window2, text="", bg="#1f1f1f").pack()
        Label(window2, text=userText, fg="#ff8280", bg="#1f1f1f", font=("Bauhaus 93", 14)).pack()
        Label(window2, text="", bg="#1f1f1f").pack()

        entry = Entry(window2, fg="#ff8280", bg="#1f1f1f", font=("Bauhaus 93", 14))
        entry.pack()
        Label(window2, text="\n", bg="#1f1f1f").pack()

        getUsernameButton = Button(window2, bg="#1f1f1f", fg="#ff8280", text=cameraText, font=("Bauhaus 93", 14),
                                   width=15, height=1, command=getUsername)
        getUsernameButton.pack()

        destroyButton = Button(window2, bg="#1f1f1f", fg="#ff8280", text=exitText, font=("Bauhaus 93", 14), width=15,
                               height=1, command=lambda: [window2.destroy()])
        destroyButton.pack()

        window2.mainloop()

    changeLanguage = 0
    language = ["es", "en", "fr"]

    running = True
    while running:
        window.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the colors configuration button is pressed
                if mainWindow:
                    if languageRect.collidepoint(event.pos):
                        if changeLanguage == 2:
                            changeLanguage = 0
                            print(language[changeLanguage])
                        else:
                            changeLanguage += 1
                            print(language[changeLanguage])

                    if changeLanguage != 2:
                        if faceRect.collidepoint(event.pos):
                            login()

                        if userRect.collidepoint(event.pos):
                            startBaseLogin(language[changeLanguage])

                        if registerRect.collidepoint(event.pos):
                            startRegistrationWindow(language[changeLanguage])

            # It enters the if when the button of color settings is pressed

        # Blit the scaled image onto the screen
        window.blit(scaledImage[changeLanguage], ((screenWidth - newWidth) // 2, (screenHeight - newHeigth) // 2))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

# startBaseLogin("en")
