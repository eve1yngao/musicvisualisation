# plays a created data file with sd 
import numpy as np
import sounddevice as sd

sample_rate = 44100  # Standard audio sample rate
duration = 3  # Duration in seconds
frequency = 440  # Hz (A4 note)

time = np.linspace(0, duration, int(sample_rate * duration), False)
audio_data = 0.5 * np.sin(2 * np.pi * frequency * time)

sd.play(audio_data, sample_rate)
sd.wait()