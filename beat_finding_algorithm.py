import wave
import scipy
import numpy as np
import matplotlib.pyplot as plt
import os

wav_file_name = "losing_my_religion"
song_bpm = 125

# Opening wave file as object
with wave.open(wav_file_name + ".wav", "rb") as wav_obj:
  # Getting metadata of wave audio
  sample_freq = wav_obj.getframerate()
  n_samples = wav_obj.getnframes()
  n_channels = wav_obj.getnchannels()
  signal_wave = wav_obj.readframes(n_samples)

filt_num = sample_freq # Higher value increases smoothing
coeff_keep = 50 # Increasing this increases the level of detail in the smoothed signal
decimal_places = 1 # Higher value reduces amount of zeroes
rounding_diff = 1 # Higher values increase the amount of duplicates

def run():
  # Converts a buffer(byte) object to an Int16 numpy array
  signal_array = abs(np.frombuffer(signal_wave, dtype=np.int16))
  signal_length = n_samples/sample_freq # In seconds

  # Smoothes the wave signal to allow for easier data analysis
  filt = np.ones(filt_num)/filt_num # Creates an array of length filt num, with values of 1/filt num
  # Calculates a moving average over filt_num values
  signal_smoothed = scipy.signal.fftconvolve(signal_array, filt, mode="same")

  # Creates an array corresponding to the time of each audio sample
  # Creates array of length n_samples, with values going from 0 to signal_length
  times = np.linspace(0, signal_length, num=n_samples)

  # Creates a Fast Fourier Transform of the smoothed signal array
  signal_fft = np.fft.fft(signal_smoothed)

  # Keeps only some of the coefficients
  signal_stripped_fft = signal_fft
  signal_stripped_fft[coeff_keep:] = 0

  fft_smoothed = np.fft.ifft(signal_stripped_fft) # Converts the array of coefficients back to an array of y coordinates
  conv_smoothed = scipy.signal.fftconvolve(fft_smoothed, filt, mode="same") # secondary smoothing

  # Calculating difference in length caused by moving average calculation
  times_len = len(times)
  wave_len = len(conv_smoothed)
  half_diff = (times_len - wave_len)//2

  # Calculating gradients and turning points
  smoothed_gradient = np.gradient(conv_smoothed, times).real
  # Turning points are where gradient is equal to 0
  # Need to round as computer will never be accurate enough to know when it is exactly equal to 0
  turning_points = np.where(np.round(smoothed_gradient, decimal_places) == 0)[0]
  turning_points_seconds = turning_points/sample_freq # Calculating turning points in seconds

  # rounding all numbers to 1 decimal place, any duplicates will automatically be deleted when converting to a set
  # Conversion back to list allows for sorting the values
  bpm_beats = np.array([(60/song_bpm)*count for count in range(2, int(song_bpm*(signal_length/60)))])
  print(bpm_beats)
  distinct_tps = np.asarray(sorted(list(set(np.round(np.concatenate((turning_points_seconds, bpm_beats)), rounding_diff)))))

  # Writing all values to a file, separated by ", "
  with open("turning_points.txt", 'w') as tps:
    distinct_tps.tofile(tps, sep=', ')

  # Writing to a separate folder holding the log of testing
  try:
    os.mkdir(f"C:/Users/Kaustubh Karthik/Documents/Computer_Science/Python_Projects/NEA_project/beat_finding_graphs_txts/{wav_file_name}")
  except OSError:
    print(f"{wav_file_name} folder already exists")
    
  with open(f"beat_finding_graphs_txts/{wav_file_name}/{str(filt_num)}-{str(coeff_keep)}-{str(decimal_places)}-{str(rounding_diff)}-{str(len(distinct_tps))}-bpm{song_bpm}.txt", "w") as tps:
    distinct_tps.tofile(tps, sep=', ')

  print(f"Num Turning points: {len(distinct_tps)}")
  '''# Plotting graphs for debugging
  plt.figure(figsize=(20,5))
  plt.plot(times, fft_smoothed)
  # Creating a dotted graph with dots at zero, and x coordinates at the turing points
  plt.plot(distinct_tps, np.zeros(len(distinct_tps)), '.')
  plt.plot(times, smoothed_gradient, color="r")
  plt.savefig(f"beat_finding_graphs_txts/{wav_file_name}/{str(filt_num)}-{str(coeff_keep)}-{str(decimal_places)}-{str(rounding_diff)}-{str(len(distinct_tps))}-bpm{song_bpm}.png", format="png")'''
  # Prints the times(in seconds) of distinct turning points - for debugging
  '''print("Turning points: ", distinct_tps)'''

  
if __name__ == "__main__":
  run()
