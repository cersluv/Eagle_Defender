import tkinter as tk
import tkinter.messagebox as tkMessageBox
from pytube import YouTube
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import tensorflow
import requests
from googletrans import Translator
from customSettings import startCustomSettings


# Replace 'YOUR_API_KEY' with your actual YouTube API key
apiKey = 'AIzaSyDj1am7jSbTOzU9VS6xqOMmVr1lqzpxGZs'

# Global variables for storing suggestions
suggestions = []

songCount = 0
boolImageRec = True

dirSong1 = ""
dirSong2 = ""
dirSong3 = ""


def searchYoutube(query):
    try:
        searchUrl = f"https://www.googleapis.com/youtube/v3/search?key={apiKey}&q={query}&maxResults=5&type=video"
        response = requests.get(searchUrl)
        response.raise_for_status()  # Raise an error if the request fails
        data = response.json()
        if 'items' in data:
            suggestions.clear()
            for item in data['items']:
                videoId = item['id']['videoId']
                videoUrl = f"https://www.youtube.com/watch?v={videoId}"
                suggestions.append(videoUrl)
            return suggestions
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


def saveInformation():
    with open("Data/tempUser.txt", "r") as tempFile:
        textUsername = tempFile.readline()
        cleanTextUsername = textUsername.rstrip('\n')

    mainDir = f"Data/{cleanTextUsername}/"
    os.makedirs(os.path.dirname(f"{mainDir}Images/"), exist_ok=True)
    filePath = "Data/" + cleanTextUsername + "/information.txt"
    with open(filePath, "r") as file1:
        first = file1.readline()
        second = file1.readline()
    with open(filePath, "w") as file:
        file.write(first)
        file.write(second)
        file.write(q1.get() + "\n")
        file.write(q2.get() + "\n")
        file.write(q3.get() + "\n")
        file.write(q4.get() + "\n")
        file.write(q5.get() + "\n")

    #os.remove("Data/tempUser.txt")

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


def onClick(event):
    global boolImageRec
    # Define the region coordinates and dimensions
    x1, y1, x2, y2 = 870, 970, 1066, 1039

    # Get the click coordinates
    clickX, clickY = event.x, event.y

    x11, y11, x22, y22 = 281, 835, 581, 863

    x111, y111, x222, y222 = 315, 937, 545, 964

    print(f"{clickX} / {clickY}")

    # Check if the click falls within the specified region
    if x1 <= clickX <= x2 and y1 <= clickY <= y2:
        if q1.get() and q2.get() and q3.get() and q4.get() and q5.get() != "":
            if song1.cget("text") and song2.cget("text") and song3.cget("text") != "":
                if not boolImageRec:
                    print("Click detected within the specified region!")
                    saveInformation()
                    with open("Data/tempUser.txt", "r") as tempFile1:
                        textUsername = tempFile1.readline()
                        language = tempFile1.readline()
                    targetLanguage1 = language.rstrip('\n')
                    cleanTextUsername = textUsername.rstrip('\n')
                    startCustomSettings(cleanTextUsername, targetLanguage1)
                else:
                    error_message = translateText("Es seleccionar una opción de biométrica", targetLanguage)
                    tkMessageBox.showerror("Error", error_message)
            else:
                error_message = translateText("Es necesario escoger 3 canciones", targetLanguage)
                tkMessageBox.showerror("Error", error_message)
        else:
            error_message = translateText("Es necesario que todas las preguntas seasn respondidas", targetLanguage)
            tkMessageBox.showerror("Error", error_message)

    if x11 <= clickX <= x22 and y11 <= clickY <= y22:
        facialRegister()

    if x111 <= clickX <= x222 and y111 <= clickY <= y222:
        boolImageRec = False


def update_suggestions():
    songaName = songEntry.get()
    if songaName:
        suggestions = searchYoutube(songaName)
        if suggestions:
            suggestionListbox.delete(0, tk.END)
            for url in suggestions:
                yt = YouTube(url)
                title = yt.title
                suggestionListbox.insert(tk.END, title)
        else:
            suggestionListbox.delete(0, tk.END)
            suggestionListbox.insert(tk.END, "No suggestions found.")


def download_audio():
    global songCount
    selectecIndex = suggestionListbox.curselection()
    if selectecIndex:
        selectedTitle = suggestionListbox.get(selectecIndex)
        for url in suggestions:
            yt = YouTube(url)
            if yt.title == selectedTitle:
                try:
                    print(songCount)
                    translator = Translator()
                    if songCount == 0:
                        songCount += 1
                        song1.config(text=selectedTitle)
                        downloadYtVideo(yt, selectedTitle)
                        translated = translator.translate("Primera canción descargada", dest=targetLanguage)
                        statusLabel.config(text=translated)

                    elif songCount == 1:
                        songCount += 1
                        song2.config(text=selectedTitle)
                        downloadYtVideo(yt, selectedTitle)
                        translated = translator.translate("Segunda canción descargada", dest=targetLanguage)
                        statusLabel.config(text=translated)

                    elif songCount == 2:
                        songCount += 1
                        song3.config(text=selectedTitle)
                        downloadYtVideo(yt, selectedTitle)
                        translated = translator.translate("Tercera canción descargada", dest=targetLanguage)
                        statusLabel.config(text=translated)
                        # os.remove("Data/tempUser.txt")

                    else:
                        translated = translator.translate("No se aceptan más canciones", dest=targetLanguage)
                        statusLabel.config(text=translated)

                except Exception as e:
                    statusLabel.config(text="Error: " + str(e))
                break
    else:
        statusLabel.config(text="Please select a suggestion.")


def downloadYtVideo(yt, selected_title):
    global dirSong1, dirSong2, dirSong3
    with open("Data/tempUser.txt", "r") as tempFile:
        textUsername = tempFile.readline()
        cleanTextUsername = textUsername.rstrip('\n')


    outputPath = f"Data/{cleanTextUsername}/Music/"
    os.makedirs(os.path.dirname(outputPath), exist_ok=True)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=outputPath, filename=f"{selected_title}.mp3")


def facialRegister():
    global boolImageRec
    with open("Data/tempUser.txt", "r") as tempFile:
        userReg = tempFile.readline()
        cleanTextUsername = textUsername.rstrip('\n')
        userReg = cleanTextUsername

    personPath = f"Data/{userReg}/Images"

    boolImageRec = False

    if not os.path.exists(personPath):
        print('FOLDER CREATED:', personPath)
        os.makedirs(personPath)

    # We capture de photo
    cap = cv2.VideoCapture(0)  # Choosing the camera
    while (True):
        ret, frame = cap.read()  # We read the video
        cv2.imshow('Facial Register', frame)  # Show the video on screen
        if cv2.waitKey(1) == 32:  # When we press 'space' key, we capture the last frame
            break
    print(personPath)
    cv2.imwrite(personPath + "\\" + "face.jpg", frame)  # we save the last frame in the user folder as "rostro.jpg"
    cap.release()  # We close the camera
    cv2.destroyAllWindows()

    def faceReg(img, lista_resultados):
        data = pyplot.imread(img)
        for i in range(len(lista_resultados)):
            x1, y1, ancho, alto = lista_resultados[i]['box']
            x2, y2 = x1 + ancho, y1 + alto
            pyplot.subplot(1, len(lista_resultados), i + 1)
            pyplot.axis('off')
            caraReg = data[y1:y2, x1:x2]
            caraReg = cv2.resize(caraReg, (150, 200),
                                  interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(userReg + ".jpg", caraReg)
            pyplot.imshow(data[y1:y2, x1:x2])
        pyplot.show()

    img = personPath + "\\" + "face.jpg"
    pixels = pyplot.imread(img)
    detector = MTCNN()
    faces = detector.detect_faces(pixels)
    faceReg(img, faces)


# Create the main window
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.attributes("-fullscreen", True)

with open("Data/tempUser.txt", "r") as tempFile:
    textUsername = tempFile.readline()
    targetLanguage = tempFile.readline()
    cleanTextUsername = targetLanguage.rstrip('\n')

if cleanTextUsername == "es":
    backgroundImage = tk.PhotoImage(file="visuals/imágenesEspañol/7.png")
else:
    backgroundImage = tk.PhotoImage(file="visuals/imágenesInglés/17.png")

backgroundLabel = tk.Label(window, image=backgroundImage)
backgroundLabel.place(relwidth=1, relheight=1)

window.bind("<Button-1>", onClick)

# Set the initial size of the window based on the screen resolution
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
window.geometry(f"{screen_width}x{screen_height}")

# Create and pack widgets
frame = tk.Frame(window)
frame.pack(padx=20, pady=20)
frame.place(relx=0.10, rely=0.42, anchor=tk.CENTER)  # Center the frame
frame.config(bg="#121212")

label = tk.Label(frame, text="Enter Song Name:", bg="#121212", fg="#FF6C69", font=("Arial", 20))
label.pack()

songEntry = tk.Entry(frame, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
songEntry.config(borderwidth=0)
songEntry.pack()

search_button = tk.Button(frame, text="Search", command=update_suggestions, bg="#121212", fg="#FF6C69",
                          font=("Arial", 15))
search_button.pack()
search_button.config(borderwidth=8)

suggestionListbox = tk.Listbox(frame, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
suggestionListbox.config(borderwidth=0)
suggestionListbox.pack()

download_button = tk.Button(frame, text="Download Audio", command=download_audio, bg="#121212", fg="#FF6C69",
                            font=("Arial", 15))
download_button.config(borderwidth=8)
download_button.pack()

statusLabel = tk.Label(frame, text="", bg="#121212", fg="#FF6C69", font=("Arial", 5))

statusLabel.pack()

song1 = tk.Label(window, text="", bg="black", fg="#FF6C69", font=("Arial", 15))
song1.place(x=370, y=300)

song2 = tk.Label(window, text="", bg="black", fg="#FF6C69", font=("Arial", 15))
song2.place(x=370, y=400)

song3 = tk.Label(window, text="", bg="black", fg="#FF6C69", font=("Arial", 15))
song3.place(x=370, y=500)

q1 = tk.Entry(window, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
q1.config(borderwidth=0)
q1.place(x=1350, y=320)

q2 = tk.Entry(window, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
q2.config(borderwidth=0)
q2.place(x=1350, y=470)

q3 = tk.Entry(window, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
q3.config(borderwidth=0)
q3.place(x=1350, y=630)

q4 = tk.Entry(window, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
q4.config(borderwidth=0)
q4.place(x=1350, y=780)

q5 = tk.Entry(window, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
q5.config(borderwidth=0)
q5.place(x=1350, y=930)

# Start the GUI main loop
window.mainloop()