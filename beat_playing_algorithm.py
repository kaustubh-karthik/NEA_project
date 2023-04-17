from pydub import AudioSegment
import simpleaudio as sa
from pygame.time import get_ticks, Clock
import numpy as np
import wave

with wave.open("bonk_sound.wav", "rb") as wav_obj:
  # Getting metadata of wave audio
  sample_freq = wav_obj.getframerate()
  n_samples = wav_obj.getnframes()
  n_channels = wav_obj.getnchannels()
  sample_width = wav_obj.getsampwidth()
  signal_wave = wav_obj.readframes(n_samples)

signal_wave = abs(np.frombuffer(signal_wave, dtype=np.int16))
print(signal_wave)
signal_wave = signal_wave * 100
print(signal_wave)

note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")

song_obj = sa.WaveObject.from_wave_file("pasoori.wav")
bonk_obj = lambda: sa.play_buffer(signal_wave, n_channels, sample_width, sample_freq)

play_obj = song_obj.play()

while True:
    Clock().tick()
    #print(f"get ticks is: {get_ticks()}")
    if get_ticks() in note_times*1000:
        bonk_obj()
        print("yeah", get_ticks())