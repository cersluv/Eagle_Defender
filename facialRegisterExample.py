# --------------------------------------Imports --------------------------------------------------------------

from tkinter import *
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import tensorflow

if not os.path.exists(os.getcwd() + "\Data"):
    print('FOLDER CREATED:', os.getcwd() + "\Data")
    os.makedirs(os.getcwd() + "\Data")

# ------------------------ We create a funtion for register the user -------------------------------------------

# Input: A string (username and password)
# Description: Registers a user, creating a folder with a text file named "info" that contains their username and password.
# Output: A folder with a text file
def registrar_usuario():
    userInfo = usuario.get()
    passwordInfo = contra.get()
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\"+ userInfo
    if not os.path.exists(personPath):
        print('Carpeta creada:' ,personPath)
        os.makedirs(personPath)
    print(personPath)
    archivo = open(personPath+"\\info", "w")
    archivo.write(userInfo + "\n")
    archivo.write(passwordInfo)
    archivo.close()

    # Limpiaremos los text variable
    usuario_entrada.delete(0, END)
    contra_entrada.delete(0, END)

    # Ahora le diremos al usuario que su registro ha sido exitoso
    Label(pantalla1, text="Registro Convencional Exitoso", fg="green", font=("Calibri", 11)).pack()



# Input: A string (username and password)
# Description: Registers a user, creating a folder with a text file named "info" that contains their username and password.
# Output: A folder with a jpg file
def facialRegister():
    userReg = usuario.get()
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\"+ userReg + "\\Images"

    if not os.path.exists(personPath):
        print('FOLDER CREATED:' ,personPath)
        os.makedirs(personPath)

    # We capture de photo
    cap = cv2.VideoCapture(0)  # Choosing the camera
    while (True):
        ret, frame = cap.read()  # We read the video
        cv2.imshow('Facial Register', frame)  # Show the video on screen
        if cv2.waitKey(1) == 32:  # When we press 'space' key, we capture the last frame
            break
    print(personPath)
    cv2.imwrite(personPath+ "\\"+"rostro.jpg", frame)  # we save the last frame in the user folder as "rostro.jpg"
    cap.release()  # We close the camera
    cv2.destroyAllWindows()

    usuario_entrada.delete(0, END)  # We vlean the text variables
    contra_entrada.delete(0, END)
    Label(pantalla1, text="Facial Register Succesfull", fg="green", font=("Calibri", 11)).pack()

    # ----------------- Detectamos el rostro y exportamos los pixels --------------------------

    def faceReg(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200),
                                  interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(userReg + ".jpg", cara_reg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = personPath+ "\\"+"rostro.jpg"
    pixels = pyplot.imread(img)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    faceReg(img, faces)


# ------------------------Crearemos una funcion para asignar al boton registro --------------------------------
def register():
    global usuario
    global contra
    global usuario_entrada
    global contra_entrada
    global pantalla1
    pantalla1 = Toplevel(screen)
    pantalla1.title("Registro")
    pantalla1.geometry("300x250")

    # --------- Empezaremos a crear las entradas ----------------------------------------

    usuario = StringVar()
    contra = StringVar()

    Label(pantalla1, text="Registro facial: debe de asignar un usuario:").pack()
    Label(pantalla1, text="Registro tradicional: debe asignar usuario y contraseña:").pack()
    Label(pantalla1, text="").pack()
    Label(pantalla1, text="Usuario * ").pack()
    usuario_entrada = Entry(pantalla1,
                            textvariable=usuario)
    usuario_entrada.pack()
    Label(pantalla1, text="Contraseña * ").pack()
    contra_entrada = Entry(pantalla1,
                           textvariable=contra)
    contra_entrada.pack()
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro Tradicional", width=15, height=1,
           command=registrar_usuario).pack()

    # ------------ Vamos a crear el boton para hacer el registro facial --------------------
    Label(pantalla1, text="").pack()
    Button(pantalla1, text="Registro Facial", width=15, height=1, command=facialRegister).pack()

# Input: A string (username and password)
# Description: Logins a user using the text file
# Output: A String that confirms if the user is logged or not
def normalLogin():
    userLog = userVerification.get()
    passwordLog = passwordVerification.get()

    userEntry2.delete(0, END)
    passwordEntry2.delete(0, END)

    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\"+ userLog
    infoPath = datapath + "\\"+ userLog + "\\info"

    lista_archivos = os.listdir(personPath)
    if 'info' in lista_archivos:
        archivo2 = open(infoPath, "r")
        verificacion = archivo2.read().splitlines()
        if passwordLog in verificacion:
            print("Inicio de sesion exitoso")
            Label(window2, text="Inicio de Sesion Exitoso", fg="green", font=("Calibri", 11)).pack()
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            Label(window2, text="Contraseña Incorrecta", fg="red", font=("Calibri", 11)).pack()
    else:
        print("Usuario no encontrado")
        Label(window2, text="Usuario no encontrado", fg="red", font=("Calibri", 11)).pack()


# Input: A string (username and password)
# Description: Logins a user using the facial recognizor
# Output: A String that confirms if the user is logged or not
def facialLogin():
    cap = cv2.VideoCapture(0)  # Choose the camera for face detection
    while (True):
        ret, frame = cap.read()  # Read the video
        cv2.imshow('Login Facial', frame)  # Display the video on screen
        if cv2.waitKey(1) == 32:  # Break the video when the "spaee" key is pressed
            break
    usuario_loginFac = userVerification.get()   # Save the photo with a different name to avoid overwriting
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + usuario_loginFac + "\\Images"
    rostroPath = datapath + "\\" + usuario_loginFac +"\\Images" + "\\rostro"
    #lista_archivos = os.listdir(personPath)
    cv2.imwrite(rostroPath + "LOG.jpg", frame)   # Save the last video frame as an image and assign the username as the name
    cap.release()   # Close the video capture
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
            cara_reg = cv2.resize(cara_reg, (150, 200), interpolation=cv2.INTER_CUBIC)   # Save the image as 150x200
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
        comp = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)   # Create a brute force matcher

        matches = comp.match(descr_a, descr_b)   # Apply the matcher to the descriptors

        regiones_similares = [i for i in matches if
                              i.distance < 70]  # Extract similar regions based on key points
        if len(matches) == 0:
            return 0
        return len(regiones_similares) / len(matches)  # Return the similarity percentage

    im_archivos = os.listdir(personPath) # Import the list of files using the os library
    print(os.listdir(personPath))

    if "rostro.jpg" in im_archivos:   # Compare the files with the one we are interested in

        FaceImgReg = cv2.imread(rostroPath + ".jpg", 0) # Import the registered face
        print(rostroPath)# Import the registered face

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

# Input: a button
# Description: The login screen :D
# Output: a login screen
def login():
    global window2
    global userVerification
    global passwordVerification
    global userEntry2
    global passwordEntry2

    window2 = Toplevel(screen)
    window2.title("Login")
    window2.geometry("300x250")
    Label(window2, text="Login facial: debe de asignar un usuario:").pack()
    Label(window2, text="Login tradicional: debe asignar usuario y contraseña:").pack()
    Label(window2, text="").pack()

    userVerification = StringVar()
    passwordVerification = StringVar()


    Label(window2, text="Usuario * ").pack()
    userEntry2 = Entry(window2, textvariable=userVerification)
    userEntry2.pack()
    Label(window2, text="Contraseña * ").pack()
    passwordEntry2 = Entry(window2, textvariable=passwordVerification)
    passwordEntry2.pack()
    Label(window2, text="").pack()
    Button(window2, text="Inicio de Sesion Tradicional", width=20, height=1, command=normalLogin).pack()


    Label(window2, text="").pack()
    Button(window2, text="Inicio de Sesion Facial", width=20, height=1, command=facialLogin).pack()

# Input: -
# Description: The main screen :D
# Output: The main screen
def mainWindow():
    global screen
    screen = Tk()
    screen.geometry("300x250")
    screen.title("Aprende e Ingenia")
    Label(text="Login Inteligente", bg="gray", width="300", height="2",
          font=("Verdana", 13)).pack()
    Label(text="").pack()  # Creamos el espacio entre el titulo y el primer boton
    Button(text="Iniciar Sesion", height="2", width="30", command=login).pack()
    Label(text="").pack()  # Creamos el espacio entre el primer boton y el segundo boton
    Button(text="Registro", height="2", width="30", command=register).pack()
    screen.mainloop()
mainWindow()
