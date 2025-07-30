# import pygame
import librosa
import math 
import tkinter as tk
from tkinter import filedialog
import numpy as np
import matplotlib.pyplot as plt


filename = 'sunny.wav'

y, sr = librosa.load(filename)

fig, ax = plt.subplots(nrows=2, ncols=1, sharex=True)
hop_length = 1024
D = librosa.amplitude_to_db(np.abs(librosa.stft(y, hop_length=hop_length)),
                            ref=np.max)
img = librosa.display.specshow(D, y_axis='linear', x_axis='time',
                               sr=sr, ax=ax[0])
                               
librosa.display.specshow(D, y_axis='log', sr=sr, hop_length=hop_length,
                         x_axis='time', ax=ax[1])
ax[1].set(title='Log-frequency power spectrogram')
ax[1].label_outer()
fig.colorbar(img, ax=ax, format="%+2.f dB")