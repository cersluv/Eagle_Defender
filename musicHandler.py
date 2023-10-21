import json

from pygame import mixer
import spotipy.util as util
import spotipy

from dotenv import load_dotenv
import os
from requests import post, get
import base64

clientID = '64ee53d497f64c5496151c40105f2413'
clientSecret = '33f3edb05f024c8b929cec2c15284d51'
redirectURI = 'http://localhost:8888/callback'
username = '12151711299'

scope = 'user-library-read user-modify-playback-state'
token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)
sp = spotipy.Spotify(auth=token)

def musicPlayer():
    mixer.init()
    mixer.music.load("soundEffects/menuMusic.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(1)

def buttonSoundEffect():
    sound_effect = mixer.Sound("soundEffects/collideButtonSound.mp3")  # Replace with the path to your sound effect file
    sound_effect.set_volume(1)
    sound_effect.play()


def playMusicUser(user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configurationFile = personPath + "\\configuration.txt"
    file = open(configurationFile, "r")
    text = file.read()
    configurationList = text.split("\n")
    song = configurationList[1]
    songPath = "Data/" + user + "/Music/" + song
    print(songPath)
    mixer.music.stop()
    with open(songPath, "r", encoding="utf-8") as songFile:
        uriSelectedSong = songFile.readline()
        print(f'Canción con URI; {uriSelectedSong} reproducida')

    sp.start_playback(uris = [uriSelectedSong])

def getMusicFeatures(user):
    datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configurationFile = personPath + "\\configuration.txt"
    file = open(configurationFile, "r")
    text = file.read()
    configurationList = text.split("\n")
    song = configurationList[1]
    songPath = "Data/" + user + "/Music/" + song
    print(songPath)
    with open(songPath, "r", encoding="utf-8") as songFile:
        uriSelectedSong = songFile.readline()
        print(f'Canción con URI; {uriSelectedSong} reproducida')


    trackInfo = sp.track(uriSelectedSong)
    popularity = trackInfo['popularity']
    audioFeatures = sp.audio_features(uriSelectedSong)
    danceability = audioFeatures[0]['danceability']
    acoustics = audioFeatures[0]['acousticness']
    tempo = audioFeatures[0]['tempo']

    popularity = round(popularity, 2)
    danceability = round(danceability * 100, 2)
    acoustics = round(acoustics * 100, 2)
    tempo = round(tempo, 2)

    return popularity, danceability, acoustics, tempo


def otros():
    clientID = '64ee53d497f64c5496151c40105f2413'
    clientSecret = '33f3edb05f024c8b929cec2c15284d51'
    redirectURI = 'http://localhost:8888/callback'

    load_dotenv()

    def getToken():
        authString = clientID + ":" + clientSecret
        authBytes = authString.encode("utf-8")
        authBase64 = str(base64.b64encode(authBytes), "utf-8")

        url = "https://accounts.spotify.com/api/token"
        headers = {
            "Authorization": "Basic " + authBase64,
            "Content-Type": "application/x-www-form-urlencoded"
        }

        data = {"grant_type": "client_credentials"}
        result = post(url, headers=headers, data=data)
        jsonResult = json.loads(result.content)
        token = jsonResult["access_token"]
        return token

    def getAuthHeader(token):
        return {"Authorization": "Bearer " + token}

    def searchArtist(token, artistName):
        url = "https://api.spotify.com/v1/search"
        headers = getAuthHeader(token)
        query = f"?q={artistName}&type=artist&limit=1"

        queryURL = url + query
        result = get(queryURL, headers=headers)
        jsonResult = json.loads(result.content)["artists"]["items"]
        if len(jsonResult) == 0:
            print("No hay artistas con ese nombre")
            return None

        return jsonResult[0]

    def getSongsArtists(token, artistID):
        url = f"https://api.spotify.com/v1/artists/{artistID}/top-tracks?country=US"
        headers = getAuthHeader(token)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["tracks"]
        return jsonResult

    def getSong(token, songID):
        url = f"https://api.spotify.com/v1/tracks/{artistID}/top-tracks?country=US"
        headers = getAuthHeader(token)
        result = get(url, headers=headers)
        jsonResult = json.loads(result.content)["tracks"]
        print(f'{json.loads(result.content)["track"]["artists"][0]["name"]}')
        return jsonResult

    token = getToken()
    artist = "Metallica"
    result = searchArtist(token, artist)
    artistID = result["id"]
    songs = getSongsArtists(token, artistID)

    print(f"Canciones famosas de: {artist}")
    for idx, song in enumerate(songs):
        print(f"{idx + 1}. {song['name']}")

    '''
    Para buscar, escoger y sacar info:
    '''

    # Authenticate with Spotify
    username = '12151711299'

    scope = 'user-library-read user-modify-playback-state'
    token = util.prompt_for_user_token(username, scope, clientID, clientSecret, redirectURI)

    sp = spotipy.Spotify(auth=token)

    # Prompt the user for an artist or song name
    search_query = input("Enter an artist or song name: ")
    results = sp.search(q=search_query, type='track', limit=10)  # Adjust the limit as needed

    if results['tracks']['items']:
        # Let the user choose a song from the suggestions
        for i, track in enumerate(results['tracks']['items']):
            print(f"{i + 1}. {track['name']} by {', '.join(artist['name'] for artist in track['artists'])}")

        selection = int(input("Enter the number of the song you want to play: ")) - 1
        if 0 <= selection < len(results['tracks']['items']):
            trackURI = results['tracks']['items'][selection]['uri']
            track = results['tracks']['items'][0]
        else:
            print(f'Invalid selection')
            exit()
    else:
        print(f'No songs found for: {search_query}')
        exit()

    song_features = sp.audio_features([trackURI])

    if song_features:
        song = song_features[0]
        popularity = track['popularity']
        danceability = song['danceability']
        acoustics = song['acousticness']
        tempo = song['tempo']
        print(f"Popularity: {popularity}")
        print(f"Danceability: {danceability}")
        print(f"Acousticness: {acoustics}")
        print(f"Tempo: {tempo}")
    else:
        print('Failed to retrieve song features')
        exit()

    while True:
        sp.start_playback(uris=[trackURI])
        input("Press Enter to play the song again, or Ctrl+C to exit...")

    '''
    Para reproducir la canción seleccionada:
    '''

    '''
    songName = 'Hardwired'
    results = sp.search(q=songName, type='track', limit=1)

    if results['tracks']['items']:
        trackURI = results['tracks']['items'][0]['uri']
    else:
        print(f'No se encontró la canción: {songName}')
        exit()

    sp.start_playback(uris=[trackURI])
    '''


#playMusicUser("DryGoz")
#popularity, danceability, acoustics, tempo = getMusicFeatures("Sebas")
#print(f'Popularidad: {popularity} \nBaleabilidad: {danceability} \nAcusticos: {acoustics} \nTempo: {tempo}')