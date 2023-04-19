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


# Converting byte buffer array to numpy array of int16
signal_wave = abs(np.frombuffer(signal_wave, dtype=np.int16))
# Increasing volume
signal_wave = signal_wave * 100

# Generating array of times from the text file
note_times = np.genfromtxt("turning_points.txt", delimiter = ", ")

# Initialising sound objects
song_obj = sa.WaveObject.from_wave_file("pasoori.wav")
# Creating a playable function to play the bonk sound
bonk_obj = lambda: sa.play_buffer(signal_wave, n_channels, sample_width, sample_freq)

def run():
    # Starting playback of song
    song_obj.play()

    while True:
        # Initialising clock and ticks
        Clock().tick()
        
        # Checking if the time(in ms) is a time in the note times
        if get_ticks() in note_times*1000:
            bonk_obj()
            print("yeah", get_ticks()) # debug statement
        
        if get_ticks() == 60*1000:
            break

if __name__ == "__main__":
  run()
