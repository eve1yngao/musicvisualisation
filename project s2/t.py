import librosa
import numpy as np
import statistics
import pygame

pygame.init()
pygame.mixer.init()

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

filename = 'battle.wav'

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

# current_time = 1

# running = True
# amplitude = 100
# pygame.mixer.music.play(0)

# while running:
#     position = 0
#     while position >= 0: # while the song is playing

#         position = pygame.mixer.music.get_pos() / 1000
#         frame = (f.index(min(f, key=lambda x:abs(x-position))))

#         print(section_2[frame])

#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 running = False
#                 pygame.mixer.music.stop()
    
#     running = False 

# pygame.quit()