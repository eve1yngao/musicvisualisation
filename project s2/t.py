import librosa
import numpy as np
import statistics
import pygame
import math
import tkinter as tk
from tkinter import filedialog

def draw_sine_wave(amplitudes, sections):

    period = screen_width/sections
    b = (math.pi * 2)/period
    screen.fill((0, 0, 0))
    points = []
    chunk = screen_width/sections
    for i in range(sections):
        current = amplitudes[i]
        for x in range(int(i*chunk), int((i+1)*chunk)):
            y = screen_height/2 + int(current*sections * math.sin(x * b)) # sin function
            # print(y)
            points.append((x, y))

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2) 
    pygame.display.flip()

def import_file():
    root=tk.Tk()
    root.withdraw()

    filePath=filedialog.askopenfilename(title = 'Select Song', filetypes = [("Wav Files", "*.wav")])

    print('File selected',filePath)
    return filePath

filename = import_file()

if not filename:
    quit()

pygame.init()
pygame.mixer.init()

screen_width = 500
screen_height = 500

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

y, sr = librosa.load(filename)
pygame.mixer.music.load(filename)

stft = np.abs(librosa.stft(y))
D = librosa.amplitude_to_db(stft)

frequencies = librosa.fft_frequencies()

frames = len(D[0]) # number of frames

f = list(librosa.frames_to_time(np.arange(0, frames))) # timestamps of frames
min_amp = abs(min(D[0])) # so the negative amplitudes arent negative

section_1 = []
section_2 = []
section_3 = []
section_4 = []
section_5 = []

sections = 5

for i in range(frames): # make an actual function to do this
    sec1 = D[:206, i]
    section_1.append(statistics.mean(sec1) + min_amp)

    sec2 = D[206:411, i]
    section_2.append(statistics.mean(sec2) + min_amp)

    sec3 = D[411:616, i]
    section_3.append(statistics.mean(sec3) + min_amp)

    sec4 = D[616:821, i]
    section_4.append(statistics.mean(sec4) + min_amp)

    sec5 = D[821:1026, i]
    section_5.append(statistics.mean(sec5) + min_amp)

all_amplitudes = [section_1, section_2, section_3, section_4, section_5]

running = True
pygame.mixer.music.play(0)

while running:
    position = 0 
    while position >= 0: # while the song is playing

        position = pygame.mixer.music.get_pos() / 1000
        frame = (f.index(min(f, key=lambda x:abs(x-position))))

        current_amps = [section[frame] for section in all_amplitudes] 
        draw_sine_wave(current_amps, 5)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
    
    running = False 

pygame.quit()