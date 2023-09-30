import tkinter as tk
from pytube import YouTube
import os
import requests

# Replace 'YOUR_API_KEY' with your actual YouTube API key
API_KEY = 'AIzaSyDj1am7jSbTOzU9VS6xqOMmVr1lqzpxGZs'

# Global variables for storing suggestions
suggestions = []

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
    selected_index = suggestion_listbox.curselection()
    if selected_index:
        selected_title = suggestion_listbox.get(selected_index)
        for url in suggestions:
            yt = YouTube(url)
            if yt.title == selected_title:
                try:
                    # Sanitize the video title to remove invalid characters
                    sanitized_title = "".join(c for c in yt.title if c.isalnum() or c.isspace())
                    output_path = os.path.join("music", sanitized_title)
                    os.makedirs(output_path, exist_ok=True)
                    audio_stream = yt.streams.filter(only_audio=True).first()
                    audio_stream.download(output_path=output_path)

                    status_label.config(text="Download completed!")
                except Exception as e:
                    status_label.config(text="Error: " + str(e))
                break
    else:
        status_label.config(text="Please select a suggestion.")


# Create the main window
window = tk.Tk()
window.title("YouTube Audio Downloader")
window.geometry("600x400")

# Create and pack widgets
frame = tk.Frame(window)
frame.pack(padx=20, pady=20)

label = tk.Label(frame, text="Enter Song Name:")
label.pack()

song_entry = tk.Entry(frame, width=40)
song_entry.pack()

search_button = tk.Button(frame, text="Search", command=update_suggestions)
search_button.pack()

suggestion_listbox = tk.Listbox(frame, width=60)
suggestion_listbox.pack()

refresh_button = tk.Button(frame, text="Refresh Suggestions", command=update_suggestions)
refresh_button.pack()

download_button = tk.Button(frame, text="Download Audio", command=download_audio)
download_button.pack()

status_label = tk.Label(frame, text="")
status_label.pack()

# Start the GUI main loop
window.mainloop()
