# final
import pygame
import librosa
import math 
import tkinter as tk
from tkinter import filedialog

def draw_sine_wave(amplitude):
# function from https://www.youtube.com/watch?v=675teI6-_-g&ab_channel=AndingAnalytics
    screen.fill((0, 0, 0))
    points = []
    if amplitude > 10:
        for x in range(screen_width):
            y = screen_height/2 + int(amplitude * math.sin(x * 0.02)) # sin function
            points.append((x, y))
    
    else:
        points.append((0, screen_height/2)) 
        points.append((screen_width, screen_height/2)) 
        # two edge points halfway up the screen

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2) 
    pygame.display.flip()

def import_file():
# function from https://stackoverflow.com/questions/66116411/is-there-a-way-to-upload-files-with-tkinter-in-python-3-7
# and https://www.geeksforgeeks.org/create-an-import-file-button-with-tkinter/
    root=tk.Tk()
    root.withdraw()

    filePath=filedialog.askopenfilename(title = 'Select Song', filetypes = [("Wav Files", "*.wav")])

    print('File selected',filePath)
    return filePath

filename = import_file()

pygame.display.set_caption('Sine Wave Music Visualiser')

screen_width = 500
screen_height = 500
pygame.init()
pygame.mixer.init()


screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

y, sr = librosa.load(filename)
# loads the wav file with the time series and sample rate

pygame.mixer.music.load(filename)

rms = librosa.feature.rms(y=y) # returns a np array with the rms value for each frame

time_matrix = librosa.times_like(rms) # the times that correspond to the frames in the rms array

time_rms = dict(zip(time_matrix, rms[0])) # create a dictionary with the time stamps aligning with rms

running = True
amplitude = 100
pygame.mixer.music.play(0)

while running:
    position = 0
    while position >= 0: # while the song is playing

        position = pygame.mixer.music.get_pos() / 1000
        amplitude = (time_rms.get(position) or time_rms[ min(time_rms.keys(), key = lambda key: abs(key-position))]) * 300
        # get amplitude from the closest time in the dictionary to the current position
        # from https://www.geeksforgeeks.org/python-find-the-closest-key-in-dictionary/

        draw_sine_wave(amplitude)
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
    
    running = False 

pygame.quit()