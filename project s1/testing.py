# this https://gitlab.com/avirzayev/medium-audio-visualizer-code program that doesnt work
import librosa
import numpy as np
import pygame


def clamp(min_value, max_value, value):

    if value < min_value:
        return min_value

    if value > max_value:
        return max_value

    return value


class AudioBar:

    def __init__(self, x, y, freq, color, width=50, min_height=10, max_height=100, min_decibel=-80, max_decibel=0):

        self.x, self.y, self.freq = x, y, freq

        self.color = color

        self.width, self.min_height, self.max_height = width, min_height, max_height

        self.height = min_height

        self.min_decibel, self.max_decibel = min_decibel, max_decibel

        self.__decibel_height_ratio = (self.max_height - self.min_height)/(self.max_decibel - self.min_decibel)

    def update(self, dt, decibel):

        desired_height = decibel * self.__decibel_height_ratio + self.max_height

        speed = (desired_height - self.height)/0.1

        self.height += speed * dt

        self.height = clamp(self.min_height, self.max_height, self.height)


    def render(self, screen):
        try:
            pygame.draw.rect(screen, self.color, pygame.Rect(
                self.x,
                self.y + self.max_height - self.height,
                self.width,
                self.height
            ))
        except:
            print(f"Skipping render for bar at {self.x}, {self.y} due to invalid dimensions")
            print(f"Width: {self.width} Height: {self.height}")
            return  # Fail quietly if rect is invalid



filename = "music/newgold.wav"

time_series, sample_rate = librosa.load(filename)  # getting information from the file

# getting a matrix which contains amplitude values according to frequency and time indexes
stft = np.abs(librosa.stft(time_series, hop_length=512, n_fft=2048*4))

spectrogram = librosa.amplitude_to_db(stft, ref=np.max)  # converting the matrix to decibel matrix

frequencies = librosa.core.fft_frequencies(n_fft=2048*4)  # getting an array of frequencies

# getting an array of time periodic
times = librosa.core.frames_to_time(np.arange(spectrogram.shape[1]), sr=sample_rate, hop_length=512, n_fft=2048*4)

time_index_ratio = len(times)/times[len(times) - 1]

frequencies_index_ratio = len(frequencies)/frequencies[len(frequencies)-1]


def get_decibel(target_time, freq):
    time_index = int(target_time * time_index_ratio)
    freq_index = int(freq * frequencies_index_ratio)

    # Clamp indices to array bounds
    time_index = min(max(time_index, 0), spectrogram.shape[1] - 1)
    freq_index = min(max(freq_index, 0), spectrogram.shape[0] - 1)

    return spectrogram[freq_index][time_index]


pygame.init()

infoObject = pygame.display.Info()

screen_w = int(infoObject.current_w/2.5)
screen_h = int(infoObject.current_w/2.5)

# Set up the drawing window
screen = pygame.display.set_mode([screen_w, screen_h])


bars = []


frequencies = np.arange(100, 8000, 100)

r = len(frequencies)


width = screen_w/r


x = (screen_w - width*r)/2

for c in frequencies:
    bars.append(AudioBar(x, 300, c, (255, 0, 0), max_height=400, width=width))
    x += width

t = pygame.time.get_ticks()
getTicksLastFrame = t

pygame.mixer.music.load(filename)
pygame.mixer.music.play(0)

# Run until the user asks to quit
running = True
while running:

    t = pygame.time.get_ticks()
    deltaTime = (t - getTicksLastFrame) / 1000.0
    getTicksLastFrame = t

    # Did the user click the window close button?
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Fill the background with white
    screen.fill((255, 255, 255))

    for b in bars:
        b.update(deltaTime, get_decibel(pygame.mixer.music.get_pos()/1000.0, b.freq))
        b.render(screen)

    # Flip the display
    pygame.display.flip()

# Done! Time to quit.
pygame.quit()
