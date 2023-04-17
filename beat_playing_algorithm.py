from pydub import AudioSegment
import simpleaudio as sa
from pygame.time import get_ticks, Clock
import numpy as np
import wave

with wave.open("pasoori.wav", "rb") as wav_obj:
  # Getting metadata of wave audio
  sample_freq = wav_obj.getframerate()
  n_samples = wav_obj.getnframes()
  n_channels = wav_obj.getnchannels()
  signal_wave = wav_obj.readframes(n_samples)

for x in signal_wave:
    x += 1000

note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")

song_obj = sa.WaveObject.from_wave_file("pasoori.wav")
bonk_obj = sa.WaveObject.from_wave_file("bonk_sound.wav")

play_obj = song_obj.play()

while True:
    Clock().tick()
    print(f"get ticks is: {get_ticks()}")
    if get_ticks() in note_times*1000:
        bonk_obj.play()
        print("yeah", get_ticks())