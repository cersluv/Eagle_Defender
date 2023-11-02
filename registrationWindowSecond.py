import base64
import json
import tkinter as tk
import tkinter.messagebox as tkMessageBox

import spotipy
from PIL import Image, ImageTk
from pytube import YouTube
import os
import cv2
from googletrans import Translator
from requests import post, get
from spotipy import util

from loginConfig import registerConfiguration
from baseLogin import startGame2
from musicHandler import buttonSoundEffect, musicPlayer

global language

# Replace 'YOUR_API_KEY' with your actual YouTube API key
apiKey = 'AIzaSyDj1am7jSbTOzU9VS6xqOMmVr1lqzpxGZs'

# Global variables for storing suggestions
suggestions = []

songCount = 0
boolImageRec = True
boolImageTake = False
songSelected = None

dirSong1 = ""
dirSong2 = ""
dirSong3 = ""

statusLabel = None  # Initialize statusLabel as a global variable

clientID = '64ee53d497f64c5496151c40105f2413'
clientSecret = '33f3edb05f024c8b929cec2c15284d51'
redirectURI = 'http://localhost:8888/callback'
username = '12151711299'

scope = 'user-library-read user-modify-playback-state'
token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
sp = spotipy.Spotify(auth=token)

with open("Data/tempUser.txt", "r", encoding='utf-8') as tempFile1:
    textUsername = tempFile1.readline()
    language = tempFile1.readline()
targetLanguage1 = language.rstrip('\n')
cleanTextUsername = textUsername.rstrip('\n')



def saveInformation():
    with open("Data/tempUser.txt", "r", encoding='utf-8') as tempFile:
        textUsername = tempFile.readline()
        cleanTextUsername = textUsername.rstrip('\n')

    mainDir = f"Data/{cleanTextUsername}/"
    os.makedirs(os.path.dirname(f"{mainDir}Images/"), exist_ok=True)
    filePath = "Data/" + cleanTextUsername + "/information.txt"
    with open(filePath, "r", encoding='utf-8') as file1:
        first = file1.readline()
        second = file1.readline()
    with open(filePath, "w", encoding='utf-8') as file:
        file.write(first)
        file.write(second)
        file.write(q1.get() + "\n")
        file.write(q2.get() + "\n")
        file.write(q3.get() + "\n")
        file.write(q4.get() + "\n")
        file.write(q5.get() + "\n")

    os.remove("Data/tempUser.txt")
    window.destroy()


"""
Input: text, target language code
Summary: Function to translate a given text using Google Translate
Output: text translated
"""


def translateText(text, targetLanguage):
    global language
    language = targetLanguage
    translator = Translator()
    try:
        translated = translator.translate(text, dest=targetLanguage)
        return translated.text
    except AttributeError as e:
        print("Translation error:", e)
        return text


def onClick(event):
    global boolImageRec, boolImageTake, songSelected
    with open("Data/tempUser.txt", "r", encoding='utf-8') as tempFile1:
        textUsername = tempFile1.readline()
        language = tempFile1.readline()
    targetLanguage1 = language.rstrip('\n')
    cleanTextUsername = textUsername.rstrip('\n')

    # Define the region coordinates and dimensions
    x1, y1, x2, y2 = 870 * scaleFactorWidth, 970 * scaleFactorHeight, 1066 * scaleFactorWidth, 1039 * scaleFactorHeight

    x11, y11, x22, y22 = 302 * scaleFactorWidth, 664 * scaleFactorHeight, 531 * scaleFactorWidth, 700 * scaleFactorHeight

    x111, y111, x222, y222 = 295 * scaleFactorWidth, 1001 * scaleFactorHeight, 534 * scaleFactorWidth, 1033 * scaleFactorHeight

    # Get the click coordinates
    clickX, clickY = event.x, event.y

    print(f"{clickX} / {clickY}")

    # Check if the click falls within the specified region
    if x1 <= clickX <= x2 and y1 <= clickY <= y2:
        buttonSoundEffect()
        if q1.get() and q2.get() and q3.get() and q4.get() and q5.get() != "":
            if song1.cget("text") and song2.cget("text") and song3.cget("text") != "":
                if not boolImageRec:
                    print("Click detected within the specified region!")
                    saveInformation()
                    registerConfiguration(cleanTextUsername, songSelected)
                    startGame2(False, None)
                else:
                    error_message = translateText("Es necesario seleccionar una opción de biométrica", targetLanguage1)
                    tkMessageBox.showerror("Error", error_message)
            else:
                error_message = translateText("Es necesario escoger 3 canciones", targetLanguage1)
                tkMessageBox.showerror("Error", error_message)
        else:
            error_message = translateText("Es necesario que todas las preguntas seasn respondidas", targetLanguage1)
            tkMessageBox.showerror("Error", error_message)

    if x11 <= clickX <= x22 and y11 <= clickY <= y22:
        buttonSoundEffect()
        print("si")
        boolImageTake = True
        boolImageRec = False
        takePhoto()

    if x111 <= clickX <= x222 and y111 <= clickY <= y222:
        buttonSoundEffect()
        boolImageRec = False


def update_suggestions():
    global suggestions
    suggestions = []
    songName = songEntry.get()
    buttonSoundEffect()
    suggestionListbox.delete(0, tk.END)

    # Initialize lists to store original songs and other results
    original_songs = []

    if songName:
        results = sp.search(q=songName, type='track',
                            limit=10)  # You can adjust the limit as needed = sp.search(q=songName, type='track')
        # Iterate through the search results
        for track in results['tracks']['items']:
            if 'cover' not in track['name'].lower() and 'remix' not in track['name'].lower() and 'live' not in track[
                'name'].lower():
                original_songs.append(track)

        # Print the original songs followed by other results
        print("Original Songs:")
        for song in original_songs:
            print(song)

        if original_songs:
            for i, track in enumerate(original_songs):
                print(f"{i + 1}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")
                title = track['name']
                artist = track['artists'][0]['name']
                suggestionListbox.insert(tk.END, f"{title} by {artist}")
                suggestions.append(track['uri'])
        else:
            suggestionListbox.delete(0, tk.END)
            suggestionListbox.insert(tk.END, "No suggestions found.")
    else:
        suggestionListbox.delete(0, tk.END)


def downloadAudio():
    global songCount, suggestions, songSelected
    buttonSoundEffect()
    selectecIndex = suggestionListbox.curselection()


    if selectecIndex:
        selectedTitle = suggestionListbox.get(selectecIndex)
        songSelected = selectedTitle
        if songCount == 0:
            songCount += 1
            song1.config(text=selectedTitle)
            message = translateText("Primera canción descargada", targetLanguage1)

            selectecIndex = [int(index) for index in selectecIndex]
            index = 0
            for index in selectecIndex:
                print("Selected item:", suggestionListbox.get(index))

            uri = str(suggestions[index])

            filePath = "Data/" + cleanTextUsername + "/Music/" + str(suggestionListbox.get(index) )
            with open(filePath, "w", encoding='utf-8') as file:
                file.write(uri)

        elif songCount == 1:
            songCount += 1
            song2.config(text=selectedTitle)
            message = translateText("Segunda canción descargada", targetLanguage1)

            selectecIndex = [int(index) for index in selectecIndex]
            index = 0
            for index in selectecIndex:
                print("Selected item:", suggestionListbox.get(index))

            uri = str(suggestions[index])

            filePath = "Data/" + cleanTextUsername + "/Music/" + str(suggestionListbox.get(index) )
            with open(filePath, "w", encoding='utf-8') as file:
                file.write(uri)

        elif songCount == 2:
            songCount += 1
            song3.config(text=selectedTitle)
            message = translateText("Tercera canción descargada", targetLanguage1)
            # os.remove("Data/tempUser.txt")

            selectecIndex = [int(index) for index in selectecIndex]
            index = 0
            for index in selectecIndex:
                print("Selected item:", suggestionListbox.get(index))

            uri = str(suggestions[index])

            filePath = "Data/" + cleanTextUsername + "/Music/" + str(suggestionListbox.get(index) + ".txt")
            with open(filePath, "w", encoding='utf-8') as file:
                file.write(uri)

        else:
            message = translateText("No se aceptan más canciones", targetLanguage1)

        statusLabel.config(text=message)


def playSpotifySong(selected_title, selected_uri):
    buttonSoundEffect()
    if selected_uri:
        sp.start_playback(uris=[selected_uri])
        print(f"Playing: {selected_title}")
    else:
        print("No URI found for the selected song")


def takePhoto():
    global boolImageTake
    camera = cv2.VideoCapture(0)
    while boolImageTake:
        # Retrieve the camera frame
        ret, frame = camera.read()
        if not ret:
            break

        # Process and display the camera frame as needed
        faceImage = None
        # Detect and display faces
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            with open("Data/tempUser.txt", "r", encoding='utf-8') as tempFile:
                textUsername = tempFile.readline()
                cleanTextUsername = textUsername.rstrip('\n')

            # Extract and save the detected face as 'faceReference.jpg'
            faceImage = frame[y:y + h, x:x + w]
            cv2.imwrite(f'Data/{cleanTextUsername}/Images/face.jpg', faceImage)
            boolImageTake = False
            camera.release()

        # Convert the frame to RGB format for tkinter
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_pil = Image.fromarray(frame_rgb)
        frame_tk = ImageTk.PhotoImage(image=frame_pil)

        # Update the tkinter label with the current frame
        cameraLabel = tk.Label(window)
        cameraLabel.place(x=int(250 * scaleFactorWidth), y=int(735 * scaleFactorHeight))
        cameraLabel.config(width=int(330 * scaleFactorWidth), height=int(250 * scaleFactorHeight),
                           bg="SystemButtonFace")

        cameraLabel.config(image=frame_tk)
        cameraLabel.image = frame_tk

        window.update()


# Create the main window
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.attributes("-fullscreen", True)

musicPlayer()

with open("Data/tempUser.txt", "r", encoding='utf-8') as tempFile:
    textUsername = tempFile.readline()
    targetLanguage = tempFile.readline()
    cleanTextUsername = targetLanguage.rstrip('\n')
    time = tempFile.readline().rstrip('\n')

if cleanTextUsername == "es":
    backgroundImage = Image.open("visuals/imágenesEspañol/7.png")
else:
    backgroundImage = Image.open("visuals/imágenesInglés/17.png")

# Set screen resolution
screenWidth = window.winfo_screenwidth()
screenHeight = window.winfo_screenheight()

# Calculate the scaling factors to fit the image to the screen
scaleFactorWidth = screenWidth / backgroundImage.width
scaleFactorHeight = screenHeight / backgroundImage.height

newWidth = int(backgroundImage.width * scaleFactorWidth)
newHeight = int(backgroundImage.height * scaleFactorHeight)
resizedImage = backgroundImage.resize((newWidth, newHeight))

backgroundPhoto = ImageTk.PhotoImage(resizedImage)
# Create a Label widget with the resized image and display it
background_label = tk.Label(window, image=backgroundPhoto)
background_label.place(x=0, y=0, relwidth=1, relheight=1)
window.backgroundPhoto = backgroundPhoto

face_cascade = cv2.CascadeClassifier('visuals/faceRecognition/haarcascade_frontalface_default.xml')

print(f'{scaleFactorWidth} / {scaleFactorHeight}')

window.bind("<Button-1>", onClick)

# Create and pack widgets
frame = tk.Frame(window)
frame.pack(padx=10 * scaleFactorWidth, pady=20 * scaleFactorHeight)
frame.place(relx=0.10, rely=0.40, anchor=tk.CENTER)  # Center the frame
frame.config(bg="#121212")
frame.config(width=5 * scaleFactorWidth, height=5 * scaleFactorHeight)

texto1 = "Ingrese la canción:"
texto2 = "Buscar"
texto3 = "Cargar canción"
if targetLanguage1 == "es":
    texto1 = "Ingrese la canción:"
    texto2 = "Buscar"
    texto3 = "Cargar canción"
if targetLanguage1 == "en":
    texto1 = "Enter song name::"
    texto2 = "Search"
    texto3 = "Load song"

label = tk.Label(frame, text=texto1, bg="#121212", fg="#FF6C69", font=("Arial", 15))
label.pack()

songEntry = tk.Entry(frame, width=int(40 * scaleFactorWidth), bg="#1f1f1f", font=("Arial", 10), fg="white")
songEntry.config(borderwidth=0)
songEntry.pack()

search_button = tk.Button(frame, text=texto2, command=update_suggestions, bg="#121212", fg="#FF6C69",
                          font=("Arial", 15))
search_button.pack()
search_button.config(borderwidth=int(8 * scaleFactorWidth))

suggestionListbox = tk.Listbox(frame, width=int(40 * scaleFactorWidth), height=int(8 * scaleFactorHeight), bg="#1f1f1f",
                               font=("Arial", 10), fg="white")
suggestionListbox.config(borderwidth=0)
suggestionListbox.pack()

download_button = tk.Button(frame, text=texto3, command=downloadAudio, bg="#121212", fg="#FF6C69",
                            font=("Arial", 15))
download_button.config(borderwidth=int(8 * scaleFactorWidth))
download_button.pack()

statusLabel = tk.Label(frame, text="", bg="#121212", fg="#FF6C69", font=("Arial", 10))
statusLabel.pack()

song1 = tk.Label(window, text="", bg="black", fg="#FF6C69", font=("Arial", 15))
song1.place(x=int(370 * scaleFactorWidth), y=int(300 * scaleFactorHeight))

song2 = tk.Label(window, text="", bg="black", fg="#FF6C69", font=("Arial", 15))
song2.place(x=int(370 * scaleFactorWidth), y=int(400 * scaleFactorHeight))

song3 = tk.Label(window, text="", bg="black", fg="#FF6C69", font=("Arial", 15))
song3.place(x=int(370 * scaleFactorWidth), y=int(500 * scaleFactorHeight))

q1 = tk.Entry(window, width=int(40 * scaleFactorWidth), bg="#1f1f1f", font=("Arial", 10), fg="white")
q1.config(borderwidth=0)
q1.place(x=int(1350 * scaleFactorWidth), y=int(320 * scaleFactorHeight))

q2 = tk.Entry(window, width=int(40 * scaleFactorWidth), bg="#1f1f1f", font=("Arial", 10), fg="white")
q2.config(borderwidth=0)
q2.place(x=int(1350 * scaleFactorWidth), y=int(470 * scaleFactorHeight))

q3 = tk.Entry(window, width=int(40 * scaleFactorWidth), bg="#1f1f1f", font=("Arial", 10), fg="white")
q3.config(borderwidth=0)
q3.place(x=int(1350 * scaleFactorWidth), y=int(630 * scaleFactorHeight))

q4 = tk.Entry(window, width=int(40 * scaleFactorWidth), bg="#1f1f1f", font=("Arial", 10), fg="white")
q4.config(borderwidth=0)
q4.place(x=int(1350 * scaleFactorWidth), y=int(780 * scaleFactorHeight))

q5 = tk.Entry(window, width=int(40 * scaleFactorWidth), bg="#1f1f1f", font=("Arial", 10), fg="white")
q5.config(borderwidth=0)
q5.place(x=int(1350 * scaleFactorWidth), y=int(930 * scaleFactorHeight))

# Start the GUI main loop
window.mainloop()
