from pygame import mixer

def musicPlayer():
    mixer.init()
    mixer.music.load("soundEffects/menuMusic.mp3")
    mixer.music.play(-1)
    mixer.music.set_volume(1)

def buttonSoundEffect():
    sound_effect = mixer.Sound("soundEffects/collideButtonSound.mp3")  # Replace with the path to your sound effect file
    sound_effect.play()

