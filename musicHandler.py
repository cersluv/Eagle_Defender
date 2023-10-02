import tkinter as tk
from pytube import YouTube
import os
import cv2
from matplotlib import pyplot
from mtcnn.mtcnn import MTCNN
import numpy as np
import tensorflow
import requests
from googletrans import Translator

# Replace 'YOUR_API_KEY' with your actual YouTube API key
API_KEY = 'AIzaSyDj1am7jSbTOzU9VS6xqOMmVr1lqzpxGZs'

# Global variables for storing suggestions
suggestions = []

songCount = 0
targetLanguage = 'es'
boolImage = True


def search_youtube(query):
    try:
        search_url = f"https://www.googleapis.com/youtube/v3/search?key={API_KEY}&q={query}&maxResults=5&type=video"
        response = requests.get(search_url)
        response.raise_for_status()  # Raise an error if the request fails
        data = response.json()
        if 'items' in data:
            suggestions.clear()
            for item in data['items']:
                video_id = item['id']['videoId']
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                suggestions.append(video_url)
            return suggestions
        else:
            return None
    except Exception as e:
        print("Error:", e)
        return None


def saveInformation():
    with open("Data/tempUser.txt", "r") as tempFile:
        textUsername = tempFile.readline()

    mainDir = f"Data/{textUsername}/"
    os.makedirs(os.path.dirname(f"{mainDir}Images/"), exist_ok=True)
    file_path = "Data/" + textUsername + "/information.txt"
    with open(file_path, "r") as file1:
        first = file1.readline()
        second = file1.readline()
    with open(file_path, "w") as file:
        file.write(first)
        file.write(second)
        file.write(q1.get() + "\n")
        file.write(q2.get() + "\n")
        file.write(q3.get() + "\n")
        file.write(q4.get() + "\n")
        file.write(q5.get() + "\n")


def on_click(event):
    # Define the region coordinates and dimensions
    x1, y1, x2, y2 = 870, 970, 1066, 1039

    # Get the click coordinates
    click_x, click_y = event.x, event.y

    x11, y11, x22, y22 = 281, 835, 581, 863

    # Check if the click falls within the specified region
    if x1 <= click_x <= x2 and y1 <= click_y <= y2:
        if q1.get() and q2.get() and q3.get() and q4.get() and q5.get() != "":
            saveInformation()
            if song1.cget("text") and song2.cget("text") and song3.cget("text") != "":
                if boolImage:
                    print("Click detected within the specified region!")

    if x11 <= click_x <= x22 and y11 <= click_y <= y22:
        facialRegister()


def update_suggestions():
    song_name = song_entry.get()
    if song_name:
        suggestions = search_youtube(song_name)
        if suggestions:
            suggestion_listbox.delete(0, tk.END)
            for url in suggestions:
                yt = YouTube(url)
                title = yt.title
                suggestion_listbox.insert(tk.END, title)
        else:
            suggestion_listbox.delete(0, tk.END)
            suggestion_listbox.insert(tk.END, "No suggestions found.")


def download_audio():
    global songCount
    selected_index = suggestion_listbox.curselection()
    if selected_index:
        selected_title = suggestion_listbox.get(selected_index)
        for url in suggestions:
            yt = YouTube(url)
            if yt.title == selected_title:
                try:
                    print(songCount)
                    translator = Translator()
                    if songCount == 0:
                        songCount += 1
                        song1.config(text=selected_title)
                        downloadYtVideo(yt, selected_title)
                        translated = translator.translate("Primera canción descargada", dest=targetLanguage)
                        status_label.config(text=translated)

                    elif songCount == 1:
                        songCount += 1
                        song2.config(text=selected_title)
                        downloadYtVideo(yt, selected_title)
                        translated = translator.translate("Segunda canción descargada", dest=targetLanguage)
                        status_label.config(text=translated)

                    elif songCount == 2:
                        songCount += 1
                        song3.config(text=selected_title)
                        downloadYtVideo(yt, selected_title)
                        translated = translator.translate("Tercera canción descargada", dest=targetLanguage)
                        status_label.config(text=translated)
                        # os.remove("Data/tempUser.txt")

                    else:
                        translated = translator.translate("No se aceptan más canciones", dest=targetLanguage)
                        status_label.config(text=translated)

                except Exception as e:
                    status_label.config(text="Error: " + str(e))
                break
    else:
        status_label.config(text="Please select a suggestion.")


def downloadYtVideo(yt, selected_title):
    with open("Data/tempUser.txt", "r") as tempFile:
        textUsername = tempFile.readline()

    output_path = f"Data/{textUsername}/Music/"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    audio_stream = yt.streams.filter(only_audio=True).first()
    audio_stream.download(output_path=output_path, filename=f"{selected_title}.mp3")


def facialRegister():
    with open("Data/tempUser.txt", "r") as tempFile:
        userReg = tempFile.readline()
    personPath = f"Data/{userReg}/Images"

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
            cara_reg = data[y1:y2, x1:x2]
            cara_reg = cv2.resize(cara_reg, (150, 200),
                                  interpolation=cv2.INTER_CUBIC)  # Guardamos la imagen con un tamaño de 150x200
            cv2.imwrite(userReg + ".jpg", cara_reg)
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

backgroundImage = tk.PhotoImage(file="visuals/imágenesEspañol/7.png")

backgroundLabel = tk.Label(window, image=backgroundImage)
backgroundLabel.place(relwidth=1, relheight=1)

window.bind("<Button-1>", on_click)

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

song_entry = tk.Entry(frame, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
song_entry.config(borderwidth=0)
song_entry.pack()

search_button = tk.Button(frame, text="Search", command=update_suggestions, bg="#121212", fg="#FF6C69",
                          font=("Arial", 15))
search_button.pack()
search_button.config(borderwidth=8)

suggestion_listbox = tk.Listbox(frame, width=40, bg="#1f1f1f", font=("Arial", 10), fg="white")
suggestion_listbox.config(borderwidth=0)
suggestion_listbox.pack()

download_button = tk.Button(frame, text="Download Audio", command=download_audio, bg="#121212", fg="#FF6C69",
                            font=("Arial", 15))
download_button.config(borderwidth=8)
download_button.pack()

status_label = tk.Label(frame, text="", bg="#121212", fg="#FF6C69", font=("Arial", 5))

status_label.pack()

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