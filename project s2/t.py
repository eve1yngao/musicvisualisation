import librosa
import numpy as np
import statistics
import pygame
import math

pygame.init()
pygame.mixer.init()

screen_width = 500
screen_height = 500

def draw_sine_wave(amplitudes, sections):
# function from https://www.youtube.com/watch?v=675teI6-_-g&ab_channel=AndingAnalytics


# for i in range sections
# get the amplitude list of that section
# screen width/sections = the division of each section
# determine the screen interval x in range (i*division:(i+1)*division)
# for that range calculate the y with the amplitude in the according section
    screen.fill((0, 0, 0))
    points = []
    chunk = screen_width/sections
    for i in range(sections):
        current = amplitudes[i]
        if i < (sections - 1):
            for x in range(int(i*chunk), int((i+1)*chunk)):
                y = screen_height/2 + int(current*5 * math.sin(x * 0.02)) # sin function
                print(y)
                points.append((x, y))
        else:
            for x in range(int(i*chunk), int(screen_width)):
                y = screen_height/2 + int(current*5 * math.sin(x * 0.02)) # sin function
                points.append((x, y))

    # if amplitude > 10:
    #     for x in range(screen_width):
    #         y = screen_height/2 + int(amplitude * math.sin(x * 0.02)) # sin function
    #         points.append((x, y))
    
    # else:
    #     points.append((0, screen_height/2)) 
    #     points.append((screen_width, screen_height/2)) 
    #     # two edge points halfway up the screen

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2) 
    pygame.display.flip()

filename = 'red_instrumental.wav'

screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

y, sr = librosa.load(filename)
pygame.mixer.music.load(filename)

stft = np.abs(librosa.stft(y))
D = librosa.amplitude_to_db(stft)
# i = librosa.samples_to_times(hop_length = hop_length)

print(D[40, 2000]) # freq, frame
frequencies = librosa.fft_frequencies(n_fft=2048)
print(len(y)/sr)

frames = len(D[0]) # number of frames

f = list(librosa.frames_to_time(np.arange(0, frames)))
# f = list(librosa.frames_to_time(D[0]))

print(f[-1])
print(len(f))
print(max(f))



# create a dict with the key being the time and the value being a dictionary 
# with frequency as the key and amplitude as the value


# or get the time, get the frame from that time, then for each frequency 
# get the amplitude and display that


# use a for loop or something to get the amplitudes from a particular range 
# of frequencies

# create an avg by adding them together and dividing by length (split into 
# 5 sections for the frequencies)

# square these values? *test*
# use that as some section of the line to be displayed

section_1 = []
section_2 = []
section_3 = []
section_4 = []
section_5 = []

for i in range(frames):
    sec1 = D[:206, i]
    section_1.append(statistics.mean(sec1)+31.77744)

    sec2 = D[206:411, i]
    section_2.append(statistics.mean(sec2)+31.77744)

    sec3 = D[411:616, i]
    section_3.append(statistics.mean(sec3)+31.77744)

    sec4 = D[616:821, i]
    section_4.append(statistics.mean(sec4)+31.77744)

    sec5 = D[821:1026, i]
    section_5.append(statistics.mean(sec5)+31.77744)

all_amplitudes = [section_1, section_2, section_3, section_4, section_5]
print(all_amplitudes)

running = True
amplitude = 100
pygame.mixer.music.play(0)

while running:
    position = 0
    while position >= 0: # while the song is playing

        position = pygame.mixer.music.get_pos() / 1000
        frame = (f.index(min(f, key=lambda x:abs(x-position))))

        # for section in all_amplitudes:
        #     print(section[frame])
            # make a function that takes the entire all_amplitudes and the given frame to produce an image

        current_amps = [section[frame] for section in all_amplitudes] # this should do what i want to work w the function
        print(current_amps)
        draw_sine_wave(current_amps, 5)
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.mixer.music.stop()
    
    running = False 

pygame.quit()