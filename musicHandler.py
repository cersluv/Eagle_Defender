import tkinter as tk
from pytube import YouTube
import os
import requests
from googletrans import Translator

# Replace 'YOUR_API_KEY' with your actual YouTube API key
API_KEY = 'AIzaSyDj1am7jSbTOzU9VS6xqOMmVr1lqzpxGZs'

# Global variables for storing suggestions
suggestions = []

songCount = 0
targetLanguage = 'es'


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


# Create the main window
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.geometry("600x400")

backgroundImage = tk.PhotoImage(file="visuals/imágenesEspañol/7.png")

backgroundLabel = tk.Label(window, image=backgroundImage)
backgroundLabel.place(relwidth=1, relheight=1)

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

song1 = tk.Label(window, text="1", bg="black", fg="#FF6C69", font=("Arial", 15))
song1.place(x=370, y=300)

song2 = tk.Label(window, text="2", bg="black", fg="#FF6C69", font=("Arial", 15))
song2.place(x=370, y=400)

song3 = tk.Label(window, text="3", bg="black", fg="#FF6C69", font=("Arial", 15))
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
