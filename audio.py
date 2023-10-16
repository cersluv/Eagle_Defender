import librosa
import time

#input      : A song
#description: This funtion gives the bpm of a song
#output     : An integer that gives the bpm of a song
def getTempo(song):
    y, sr = librosa.load(song, sr=11025, duration=60)
    hop_length = 256
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr, hop_length=hop_length)
    print(tempo)
    return tempo
    # Print the estimated tempo


# inicio = time.time()
# getTempo(r'C:\Users\crseg\OneDrive\Escritorio\Chayanne - Torero (Vídeo Oficial).mp3') #usage example : "Data\user\configuration\indice respectivo de la canción"
# fin = time.time()
# duracion = fin - inicio #aprox. 2s cada canción
# print(duracion)