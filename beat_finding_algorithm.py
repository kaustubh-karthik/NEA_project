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
print(n_samples, sample_freq)

# Converts a buffer(byte) object to an Int16 array
signal_array = abs(np.frombuffer(signal_wave, dtype=np.int16))
signal_length = n_samples/sample_freq # In seconds

# Smoothes the wave signal to allow for easier data analysis
filt_num = sample_freq
filt = np.ones(filt_num)/filt_num
signal_smoothed = scipy.signal.fftconvolve(signal_array, filt, mode="same")

# Creates an array corresponding to the time of each audio sample
times = np.linspace(0, signal_length, num=n_samples)

# Creates a Fast Fourier Transform of the smoothed signal array
signal_fft = np.fft.fft(signal_smoothed)

signal_stripped_fft = signal_fft
signal_stripped_fft[100:] = 0

fft_smoothed = np.fft.ifft(signal_stripped_fft)
conv_smoothed = scipy.signal.fftconvolve(fft_smoothed, filt, mode="same") # secondary smoothing

times_len = len(times)
wave_len = len(conv_smoothed)
half_diff = (times_len - wave_len)//2

# Calculating gradients and turning points
smoothed_gradient = np.gradient(conv_smoothed, times[half_diff: -half_diff]).real
turning_points = np.where(np.round(smoothed_gradient, 2) == 0)[0]
with open("turning_points.txt", 'w') as tps:
  turning_points_seconds = turning_points/sample_freq
  turning_points_seconds.tofile(tps, sep=', ')

plt.figure(figsize=(20,5))
plt.plot(times[half_diff: -half_diff], fft_smoothed)
plt.plot(turning_points/sample_freq, np.zeros(len(turning_points)), '.')
plt.plot(times[half_diff: -half_diff], smoothed_gradient, color="r")
plt.show()
# Prints the times(in seconds) of turning points
print("Turning points: ", turning_points/sample_freq)
