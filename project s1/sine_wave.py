# scuffed first try manual syncing
import pygame
import math
import time
import librosa
# import sounddevice as sd

screen_width = 500
screen_height = 500
pygame.init()
pygame.mixer.init()

pygame.display.set_caption("Sine wave music visualiser")
screen = pygame.display.set_mode((screen_width, screen_height))

filename = 'music/battle.wav'
pygame.mixer.music.load(filename)

y, sr = librosa.load(filename)

rms = librosa.feature.rms(y=y, hop_length = 512)
print(len(rms[0]))
print(len(y))
def round_down(number, decimals):
    factor = 10 ** decimals
    return math.floor(number * factor) / factor

def draw_sine_wave(amplitude):
    screen.fill((0,0,0))
    # makes sure the background is black
    points = []
    if amplitude > 10: # adequate audio input
        for x in range(screen_width):
            y = screen_height/2 + int(amplitude * math.sin(x * 0.02)) # just maths
            points.append((x, y))
    else:
        points.append((0, screen_height/2)) # left most point in the middle
        points.append((screen_width, screen_height/2)) # right most point in the middle

    pygame.draw.lines(screen, (255, 255, 255), False, points, 2)
    # surface, colour of line, closed or not, relevant points, line width px
    pygame.display.flip()


seconds = round_down(len(y)/sr, 5)
delay = round_down(seconds/len(rms[0]), 2)

running = True
amplitude = 0
pygame.mixer.music.play(0)
# sd.play(y, sr)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    for r in rms[0]:
        amplitude = r*400
        # print(amplitude)
        draw_sine_wave(amplitude)
        time.sleep(delay)

    running = False

pygame.quit()