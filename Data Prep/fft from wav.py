# from pydub import AudioSegment
import numpy as np
import scipy.io.wavfile as wav
import matplotlib.pyplot as plt

# Load WAV file
rate, data = wav.read("วงวน - SERIOUS BACON ( ORIGINAL by ONEONE ).wav")

# # Load mp3 file
# audio = AudioSegment.from_file("file.mp3", format="mp3")

# # Convert to numpy array
# data = np.array(audio.get_array_of_samples())

# # Get sample rate
# rate = audio.frame_rate

# Perform FFT
fft_out = np.fft.fft(data)

# Plot spectrum
plt.plot(np.abs(fft_out))
plt.show()
