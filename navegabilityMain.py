import pygame
import sys
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import os
from googletrans import Translator
from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import tensorflow
from baseLogin import startBaseLogin
from registrationWindow import startRegistrationWindow


pygame.init()

# Constants
width, height = 800, 600
white = (255, 255, 255)
font = pygame.font.Font(None, 30)

#Globals
global window2
global userVerification
global passwordVerification
global userEntry2
global passwordEntry2


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
backgroundSpanish = pygame.image.load('visuals/imágenesEspañol/2.png')
backgroundEnglish = pygame.image.load('visuals/imágenesInglés/12.png')
backgroundFrench = pygame.image.load('visuals/imágenesFrancés/22.png')


# Get the image's original dimensions
original_width, original_height = backgroundSpanish.get_size()

# Calculate the scaling factors to fit the image to the screen
scale_factor_width = screen_width / original_width
scale_factor_height = screen_height / original_height

# Choose the minimum scaling factor to maintain aspect ratio
min_scale_factor = min(scale_factor_width, scale_factor_height)

# Scale the image while maintaining aspect ratio
new_width = int(original_width * min_scale_factor)
new_height = int(original_height * min_scale_factor)

scaled_image1 = pygame.transform.scale(backgroundSpanish, (new_width, new_height))
scaled_image2 = pygame.transform.scale(backgroundEnglish, (new_width, new_height))
scaled_image3 = pygame.transform.scale(backgroundFrench, (new_width, new_height))
scaled_image = [scaled_image1, scaled_image2, scaled_image3]


#Rectangles for every button in this window
faceRect = pygame.Rect(150, 690, 465, 40)
userRect = pygame.Rect(155, 820, 460, 40)
registerRect = pygame.Rect(150, 950, 465, 40)
languageRect = pygame.Rect(1692, 935, 212, 113)


clock = pygame.time.Clock()

mainWindow = True


def facialLogin():
    cap = cv2.VideoCapture(0)  # Choose the camera for face detection
    while (True):
        ret, frame = cap.read()  # Read the video
        cv2.imshow('Login Facial', frame)  # Display the video on screen
        if cv2.waitKey(1) == 32:  # Break the video when the "spaee" key is pressed
            break
    usuario_loginFac = userVerification.get()  # Save the photo with a different name to avoid overwriting
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + usuario_loginFac + "\\Images"
    rostroPath = datapath + "\\" + usuario_loginFac + "\\Images" + "\\rostro"
    # lista_archivos = os.listdir(personPath)
    cv2.imwrite(rostroPath + "LOG.jpg",
                frame)  # Save the last video frame as an image and assign the username as the name
    cap.release()  # Close the video capture
    cv2.destroyAllWindows()

    userEntry2.delete(0, END)  # Clear the text variables
    passwordEntry2.delete(0, END)

    # Input: an image and a list
    # Description: Function to save the face
    # Output: Data of the img and a confirmation that´s saved
    def log_rostro(img, result_list):
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
    log_rostro(img, faces)

    # Input: two different images
    # Description: Function to compare faces
    # Output: A percentage of how the two faces are alike
    def orb_sim(img1, img2):
        orb = cv2.ORB_create()  # Create the comparison object

        kpa, descr_a = orb.detectAndCompute(img1, None)  # Create descriptor 1 and extract key points
        kpb, descr_b = orb.detectAndCompute(img2, None)  # eate descriptor 2 and extract key points
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)  # Create a brute force matcher

        matches = comp.match(descr_a, descr_b)  # Apply the matcher to the descriptors

        regiones_similares = [i for i in matches if
                              i.distance < 70]  # Extract similar regions based on key points
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)  # Return the similarity percentage

    im_archivos = os.listdir(personPath)  # Import the list of files using the os library
    print(os.listdir(personPath))

    if "rostro.jpg" in im_archivos:  # Compare the files with the one we are interested in

        FaceImgReg = cv2.imread(rostroPath + ".jpg", 0)  # Import the registered face
        print(rostroPath)  # Import the registered face

        FaceImgLog = cv2.imread(rostroPath + "LOG.jpg", 0)  # Import the login face

        similitud = orb_sim(FaceImgReg, FaceImgLog)
        if similitud >= 0.90:
            Label(window2, text="Inicio de Sesion Exitoso", fg="green", font=("Calibri", 11)).pack()
            print("Bienvenido al sistema usuario: ", usuario_loginFac)
            print("Compatibilidad con la foto del registro: ", similitud)
        else:
            print("Rostro incorrecto, Cerifique su usuario")
            print("Compatibilidad con la foto del registro: ", similitud)
            Label(window2, text="Incompatibilidad de rostros", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Foto no encontrada")
        Label(window2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


def login():
    window2 = Tk()
    window2.title("Login")
    window2.config(bg = "#1f1f1f")
    screen_width = window2.winfo_screenwidth()
    screen_height = window2.winfo_screenheight()
    x = (screen_width - 300) // 2
    y = (screen_height - 200) // 2
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

    Label(window2, text="", bg = "#1f1f1f").pack()
    Label(window2, text = userText,fg = "#ff8280",  bg = "#1f1f1f",font=("Bauhaus 93",14)).pack()
    Label(window2, text="", bg = "#1f1f1f").pack()
    userEntry = Entry(window2, textvariable=userVerification,fg = "#ff8280",  bg = "#1f1f1f",font=("Bauhaus 93",14)).pack()
    Label(window2, text = "\n", bg = "#1f1f1f").pack()

    btnFaceRecognition = Button(window2,bg = "#1f1f1f", fg = "#ff8280",text=cameraText, font=("Bauhaus 93",14), width=15, height=1, command= facialLogin).pack()

    exitButton = Button(window2,bg = "#1f1f1f", fg = "#ff8280",text=exitText, font=("Bauhaus 93",14), width=15, height=1, command= lambda:[window2.destroy()]).pack()

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



        #It enters the if when the button of color settings is pressed


    # Blit the scaled image onto the screen
    window.blit(scaled_image[changeLanguage], ((screen_width - new_width) // 2, (screen_height - new_height) // 2))




    pygame.display.flip()
    clock.tick(30)

# Quit pygame
pygame.quit()
sys.exit()
