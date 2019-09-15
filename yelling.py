import pyaudio
import struct
import numpy as np
import pygame
import time

pygame.init()

FORMAT = pyaudio.paFloat32
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "file.wav"
width = 800
height = 600

audio = pyaudio.PyAudio()

screen = pygame.display.set_mode((width, height))

screen.fill((255, 255, 255))

end = False

def DrawBar(pos, size, borderC, barC, progress):

    pygame.draw.rect(screen, borderC, (*pos, *size), 1)
    innerPos  = (pos[0]+3, pos[1]+3)
    innerSize = ((size[0]-6) * progress, size[1]-6)
    pygame.draw.rect(screen, barC, (*innerPos, *innerSize))

def get_power():

	stream = audio.open(format=FORMAT,
		channels = CHANNELS,
		rate = RATE, input=True, frames_per_buffer=CHUNK)
	print("recording...")

	power = 0

	x = []

	for i in range(0, int(RATE/CHUNK*RECORD_SECONDS)):
		data = stream.read(CHUNK)
		decoded = struct.unpack(str(CHUNK)+'f',data)
		x.append(np.array(decoded))
	for i in range(len(x)):
		power+=(np.sqrt(np.mean(x[i]**2)))
		time.sleep(0.1)
		DrawBar((300, 250), (200, 20), (0, 0, 0), (0, 128, 0), power/300)
		pygame.display.flip()
	print("finished recording")
	
	stream.stop_stream()
	stream.close()
	audio.terminate()

get_power()
while not end:
	pygame.display.update()

