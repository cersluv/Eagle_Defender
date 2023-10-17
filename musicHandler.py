from pygame import mixer, time
import os
import vlc


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
    """datapath = os.getcwd() + "\Data"
    personPath = datapath + "\\" + user
    configurationFile = personPath + "\\configuration.txt"
    file = open(configurationFile, "r")
    text = file.read()
    configurationList = text.split("\n")
    song = configurationList[1]
    print("Data/" + user + "/Music/" + song + ".mp4")
    songPath = "Data/" + user + "/Music/" + song + ".mp4"""

    vlc_instance = vlc.Instance("--no-xlib")

    media_player = vlc_instance.media_player_new()


    input_file = "Data/Sebas/Music/Hola (Remix).mp4"
    media = vlc_instance.media_new(input_file)

    options = ":sout=#transcode{vcodec=none,acodec=mp3,ab=192,channels=2,samplerate=44100}:std{mux=mp3,dst=output_file.mp3}"


    media.add_option(options)

    media_player.set_media(media)

    media_player.play()
    while not media_player.get_state() == vlc.State.Ended:
        pass

    media_player.release()


playMusicUser("Sebas")