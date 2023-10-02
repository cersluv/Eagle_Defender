import os

questions = ["¿En cuál país le gustaria vivir?", "¿Cuál es su libro favorito?", "¿Cuál es su animal favorito?", "¿Cuál es su juego de mesa favorito?", "¿Cuál es su pelicula favorita?"]

# Input      : The User Name and the password
# Description: Login funtion, using the password.
# Output     : True, if the passwords match. False, if there´s no registered username, or if the password it´s wrong
def baseLogin(userInfo, passwordInfo):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + userInfo
    infoPath = personPath + "\\information.txt"
    lista_archivos = os.listdir(personPath)
    if 'Information.txt' in lista_archivos:
        archivo2 = open(infoPath, "r")
        verification = archivo2.read().splitlines()
        if passwordInfo in verification:
            print("Inicio de sesion exitoso")
            return True # everything´s fine
        else:
            print("Contraseña incorrecta, ingrese de nuevo")
            return False  #this changes for an error message
    else:
        print("Usuario no encontrado")
        return False #this changes for an error message

# Input      : Two answers for the questions and the username
# Description: Login funtion, using the security questions.
# Output     : True, if the asnwers of the quetions match. False, if there´s no registered username, or if the answers are wrong.

def questionsLogin(Q1, Q2, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    infoPath = personPath + "\\information.txt"
    lista_archivos = os.listdir(personPath)
    if 'Information.txt' in lista_archivos:
        archivo2 = open(infoPath, "r")
        verification = archivo2.read().splitlines()
        if Q1 in verification and Q2 in verification:
            print("Change your password")
            return True # u login
        else:
            print("Those are not the correct answers")
            return False  # error message
    else:
        print("User not found")
        return False # error message


# Input      : The color palet, the selected song, special effect and the user
# Description: The funtion to register and create the configuration file
# Output     : The created and updated file
def registerConfiguration(colorPalet, selectedSong, specialEffect, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    archivo = open(configPath, "w")
    archivo.write("Palette1" + "\n")
    archivo.write("." + "\n")
    archivo.write("." + "\n")
    archivo.close()


# Input      : The color palet and the user
# Description: The funtion to update the color palet
# Output     : The updated file
def configColorPalet(colorPalet, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r")
        verification = archivo2.read().splitlines()
        verification[0] = colorPalet
        archivo2.close()
        archivo = open(configPath, "w")
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")

# Input      : The selected song and the user
# Description: The funtion to update the selected song
# Output     : The updated file
def configChangeSelectedSong(selectedSong, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r")
        verification = archivo2.read().splitlines()
        verification[1] = selectedSong
        archivo2.close()
        archivo = open(configPath, "w")
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")


# Input      : The selected song and the user
# Description: The funtion to update the special effect
# Output     : The updated file
def configSpecialEffect(specialEffect, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r")
        verification = archivo2.read().splitlines()
        verification[2] = specialEffect
        archivo2.close()
        archivo = open(configPath, "w")
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")