import os

questions = ["¿En cuál país le gustaria vivir?", "¿Cuál es su libro favorito?", "¿Cuál es su animal favorito?",
                     "¿Cuál es su deporte favorito?", "¿Cuál es su color favorito?"]

"""
   input: text, Language code
   summary: uses Google Translate to translate a given text
   outputs: translated language
   """

# Input      : The Username and the password
# Description: Login funtion, using the password.
# Output     : True, if the passwords match. False, if there´s no registered username, or if the password it´s wrong
def baseLogin(userInfo, passwordInfo):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + userInfo
    infoPath = personPath + "\\information.txt"
    lista_archivos = os.listdir(personPath)
    if 'information.txt' in lista_archivos:
        archivo2 = open(infoPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        print(verification)
        print(passwordInfo)
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
    if 'information.txt' in lista_archivos:
        archivo2 = open(infoPath, "r", encoding='utf-8')
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
def registerConfiguration(user, Music):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    archivo = open(configPath, "w", encoding='utf-8')
    archivo.write("Palette 3" + "\n")
    archivo.write(str(Music) + ".txt" + "\n")
    archivo.write("1" + "\n")
    archivo.write("eagle1" + "\n")
    archivo.write("goblin1" + "\n")
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
        archivo2 = open(configPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        verification[0] = colorPalet
        archivo2.close()
        archivo = open(configPath, "w", encoding='utf-8')
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
        archivo2 = open(configPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        verification[1] = selectedSong
        archivo2.close()
        archivo = open(configPath, "w", encoding='utf-8')
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")


# Input      : The selected effect and the user
# Description: The funtion to update the special effect
# Output     : The updated file
def configSpecialEffectProjectile(specialEffect, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        verification[2] = specialEffect
        archivo2.close()
        archivo = open(configPath, "w", encoding='utf-8')
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")


# Input      : The selected effect and the user
# Description: The funtion to update the special effect
# Output     : The updated file
def configSpecialEffectEagleSkin(specialEffect, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        verification[3] = specialEffect
        archivo2.close()
        archivo = open(configPath, "w", encoding='utf-8')
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")

def configSpecialEffectGoblinSkin(specialEffect, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        verification[4] = specialEffect
        archivo2.close()
        archivo = open(configPath, "w", encoding='utf-8')
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")

def configSpecialEffectSounds(specialEffect, user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configPath = personPath + "\\configuration.txt"
    lista_archivos = os.listdir(personPath)
    if 'configuration.txt' in lista_archivos:
        archivo2 = open(configPath, "r", encoding='utf-8')
        verification = archivo2.read().splitlines()
        verification[5] = specialEffect
        archivo2.close()
        archivo = open(configPath, "w", encoding='utf-8')
        for x in verification:
            archivo.write(x+"\n")
        archivo.close()
    else:
        print("user not found")