from pygame import mixer

def musicPlayer():
    mixer.init()
    mixer.music.load("music/menuMusic.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(1)