import beat_finding_algorithm as bfa
import main_game as bpa
import time

bfa.filt_num = bfa.sample_freq # Higher value increases smoothing
bfa.coeff_keep = 350 # Increasing this increases the level of detail in the smoothed signal
bfa.decimal_places = 1 # Higher value reduces amount of zeroes
bfa.rounding_diff = 1 # Higher values increase the amount of duplicates

bfa.run()
print("Playing song in 1 second")
time.sleep(1)
bpa.run()
