import sys
from deepface import DeepFace
from googletrans import Translator
import os
import cv2
from pygame import mixer
import menu
from registrationWindow import startRegistrationWindow
from musicHandler import musicPlayer, buttonSoundEffect
from localMultiplayer import setVariables
from baseLoginSeconUser import startBaseLoginSecond

import pygame.transform


global window2
global passwordVerification
global userEntry2
global passwordEntry2

def newLogin(firstUser, firstLanguage):
    pygame.init()

    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 30)

    # Globals


    userVerification = ""

    # Set screen resolution
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeigth = screenInfo.current_h
    window = pygame.display.set_mode((screenWidth, screenHeigth))

    # Load your image
    backgroundSpanish = pygame.image.load('visuals/imágenesEspañol/2.png')
    backgroundEnglish = pygame.image.load('visuals/imágenesInglés/12.png')
    backgroundFrench = pygame.image.load('visuals/imágenesFrancés/22.png')

    # Get the image's original dimensions
    original_width, original_height = backgroundSpanish.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scaleFactorWidth = screenWidth / original_width
    scaleFactorHeight = screenHeigth / original_height

    print(f'{scaleFactorWidth} / {scaleFactorHeight}')

    # Choose the minimum scaling factor to maintain aspect ratio
    minScaleFactor = min(scaleFactorWidth, scaleFactorHeight)

    # Scale the image while maintaining aspect ratio
    newWidth = int(original_width * minScaleFactor)
    newHeigth = int(original_height * minScaleFactor)

    scaledImage1 = pygame.transform.scale(backgroundSpanish, (newWidth, newHeigth))
    scaledImage2 = pygame.transform.scale(backgroundEnglish, (newWidth, newHeigth))
    scaledImage3 = pygame.transform.scale(backgroundFrench, (newWidth, newHeigth))
    scaledImage = [scaledImage1, scaledImage2, scaledImage3]

    # Rectangles for every button in this window
    # Update the positions and sizes of pygame.Rect objects
    #                               x                      y                         ancho                    largo
    faceRect = pygame.Rect(150 * scaleFactorWidth, 690 * scaleFactorHeight, 465 * scaleFactorWidth, 40 * scaleFactorHeight)
    userRect = pygame.Rect(155 * scaleFactorWidth, 820 * scaleFactorHeight, 460 * scaleFactorWidth, 40 * scaleFactorHeight)

    registerRect = pygame.Rect(150 * scaleFactorWidth, 950 * scaleFactorHeight, 465 * scaleFactorWidth,
                               40 * scaleFactorHeight)
    languageRect = pygame.Rect(1692 * scaleFactorWidth, 935 * scaleFactorHeight, 212 * scaleFactorWidth,
                               113 * scaleFactorHeight)

    print(f'{150 * scaleFactorWidth} / {690 * scaleFactorHeight} / {465 * scaleFactorWidth} / {40 * scaleFactorHeight}')

    clock = pygame.time.Clock()

    #musicPlayer()

    mainWindow = True

    camera = cv2.VideoCapture(0)
    face_cascade = cv2.CascadeClassifier('visuals/faceRecognition/haarcascade_frontalface_default.xml')

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


    changeLanguage = 0
    language = ["es", "en", "fr"]

    running = True
    detecting_face = True  # Flag to enable face detection

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if the colors configuration button is pressed
                if mainWindow:
                    if languageRect.collidepoint(event.pos):
                        buttonSoundEffect()
                        if changeLanguage == 2:
                            changeLanguage = 0
                            print(language[changeLanguage])
                        else:
                            changeLanguage += 1
                            print(language[changeLanguage])

                    if changeLanguage != 2:

                        if userRect.collidepoint(event.pos):
                            buttonSoundEffect()

                            camera.release()
                            startBaseLoginSecond(firstUser, firstLanguage, language[changeLanguage])

                        if registerRect.collidepoint(event.pos):
                            buttonSoundEffect()

                            camera.release()
                            startRegistrationWindow(language[changeLanguage])

                        detecting_face = True

            # It enters the if when the button of color settings is pressed

        # Blit the scaled image onto the screen
        window.blit(scaledImage[changeLanguage], ((screenWidth - newWidth) // 2, (screenHeigth - newHeigth) // 2))



        # pygame.draw.rect(window, (0, 128, 255), faceRect, 0)
        # pygame.draw.rect(window, (0, 128, 255), userRect, 0)
        # pygame.draw.rect(window, (0, 128, 255), registerRect, 0)
        # pygame.draw.rect(window, (0, 128, 255), languageRect, 0)


        def find_matching_user(detected_face, reference_dir, distance_threshold=0.3):
            min_distance = float("inf")
            matching_user = None
            matching_image_path = None
            models = [
                "VGG-Face",
                "Facenet",
                "Facenet512",
                "OpenFace",
                "DeepFace",
                "DeepID",
                "ArcFace",
                "Dlib",
                "SFace",
            ]

            for root, dirs, files in os.walk(reference_dir):
                for filename in files:
                    if filename.endswith('.jpg'):
                        reference_image_path = os.path.join(root, filename)
                        print(f'Intento: - - - - - -')
                        print(f'Processando: {reference_image_path}')

                        try:
                            result = DeepFace.verify(img1_path=detected_face, img2_path=reference_image_path, model_name = models[0], enforce_detection=False)
                            distance = result['distance']
                            print(
                                f'Distancia: {distance} // Distancia Minima: {min_distance} // ThreshHold: {distance_threshold} // Confidence: {1 - min_distance}')

                            if distance < min_distance and distance < distance_threshold:
                                min_distance = distance
                                matching_user = os.path.basename(os.path.dirname(reference_image_path))
                                matching_image_path = reference_image_path

                        except Exception as e:
                            print(f"An error occurred: {e}")

            return matching_user, matching_image_path, min_distance


        # Specify the root directory where user directories are located
        root_directory = 'Data'

        # Iterate through all user directories
        for username in os.listdir(root_directory):
            user_directory = os.path.join(root_directory, username, 'Images')

            # Check if the user directory exists and contains image files
            if os.path.exists(user_directory) and os.path.isdir(user_directory):
                for image_filename in os.listdir(user_directory):
                    if image_filename.endswith('.jpg'):
                        image_path = os.path.join(user_directory, image_filename)
                        # Load the user's image
                        user_image = cv2.imread(image_path)

        # Retrieve the camera frame
        ret, frame = camera.read()
        pygame.display.update()
        if not ret:
            break

        # Process and display the camera frame as needed
        faceImage = None
        if detecting_face:
            # Detect and display faces
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Extract and save the detected face as 'faceReference.jpg'
                faceImage = frame[y:y + h, x:x + w]
                cv2.imwrite('visuals/faceRecognition/faceReference.jpg', faceImage)

                # Compare the detected face to reference images
                detected_face = 'visuals/faceRecognition/faceReference.jpg'  # The path to the detected face image
                matching_user, matching_image_path, min_distance = find_matching_user(detected_face, root_directory)
                confidence = 1 - min_distance

                if min_distance != float("inf") and confidence >= 0.88:
                    print("--------------------------------------------------------------------------------")
                    print(f"Matching user: {matching_image_path}")
                    print(f"Minimum Distance: {min_distance}")
                    print(f"Confidence: {confidence:.2f}")

                    cv2.putText(frame, f"User: {matching_user}", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    correctUser = matching_image_path.split("\\")
                    print(f'{correctUser[1]}')
                    menu.principalMenu(correctUser[1], language[changeLanguage])
                    setVariables(firstUser,firstLanguage,correctUser[1], 1)

                else:
                    cv2.putText(frame, "Unknown", (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)

            # Display the frame in the Pygame window
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            pygame_frame = pygame.surfarray.make_surface(frame)
            pygame_frame = pygame.transform.scale(pygame_frame,
                                                  (300 * scaleFactorWidth, 300 * scaleFactorHeight))  # Resize frame
            angle = 270  # Angle in degrees, adjust as needed
            rotated_frame = pygame.transform.rotate(pygame_frame, angle)
            window.blit(rotated_frame, (1500 * scaleFactorWidth, 300 * scaleFactorHeight))  # Set the desired position

        pygame.display.update()

        pygame.display.flip()
        clock.tick(30)

    # After the loop, release camera resources and quit pygame
    camera.release()
    cv2.destroyAllWindows()
    pygame.quit()
