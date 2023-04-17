from pydub import AudioSegment
import simpleaudio as sa
from pygame.time import get_ticks, Clock
import numpy as np

note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")

print(note_times*1000)

song_obj = sa.WaveObject.from_wave_file("pasoori.wav")
bonk_obj = sa.WaveObject.from_wave_file("bonk_sound.wav")


play_obj = song_obj.play()

while True:
    Clock().tick()
    print(f"get ticks is: {get_ticks()}")
    if get_ticks() in note_times*1000:
        bonk_obj.play()
        print("yeah", get_ticks())