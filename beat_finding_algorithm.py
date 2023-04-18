import wave
import scipy
import numpy as np
import matplotlib.pyplot as plt

wav_file_name = "pasoori"

# Opening wave file as object
with wave.open(wav_file_name + ".wav", "rb") as wav_obj:
  # Getting metadata of wave audio
  sample_freq = wav_obj.getframerate()
  n_samples = wav_obj.getnframes()
  n_channels = wav_obj.getnchannels()
  signal_wave = wav_obj.readframes(n_samples)

# Converts a buffer(byte) object to an Int16 numpy array
signal_array = abs(np.frombuffer(signal_wave, dtype=np.int16))
signal_length = n_samples/sample_freq # In seconds

# Smoothes the wave signal to allow for easier data analysis
filt_num = sample_freq
filt = np.ones(filt_num)/filt_num # Creates an array of length filt num, with values of 1/filt num
# Calculates a moving average over filt_num values
signal_smoothed = scipy.signal.fftconvolve(signal_array, filt, mode="same")

# Creates an array corresponding to the time of each audio sample
# Creates array of length n_samples, with values going from 0 to signal_length
times = np.linspace(0, signal_length, num=n_samples)

# Creates a Fast Fourier Transform of the smoothed signal array
signal_fft = np.fft.fft(signal_smoothed)

# Keeps only some of the coefficients
coeff_keep = 100 # Increasing this increases the level of detail in the smoothed signal
signal_stripped_fft = signal_fft
signal_stripped_fft[100:] = 0

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
turning_points = np.where(np.round(smoothed_gradient, 1) == 0)[0]
turning_points_seconds = turning_points/sample_freq # Calculating signal length

# rounding all numbers to 1 decimal place, any duplicates will automatically be deleted when converting to a set
# Conversion back to list allows for sorting the values
# Conversion back to array allows for easier writing to file
distinct_tps = np.asarray(sorted(list(set(np.round(turning_points_seconds, 1)))))

# Writing all values to a file, separated by ", "
with open("turning_points.txt", 'w') as tps:
  distinct_tps.tofile(tps, sep=', ')

# Plotting graphs for debugging
plt.figure(figsize=(20,5))
plt.plot(times, fft_smoothed)
# Creating a dotted graph with dots at zero, and x coordinates at the turing points
plt.plot(distinct_tps, np.zeros(len(distinct_tps)), '.')
plt.plot(times, smoothed_gradient, color="r")
plt.show()

# Prints the times(in seconds) of distinct turning points - for debugging
print("Turning points: ", distinct_tps)
