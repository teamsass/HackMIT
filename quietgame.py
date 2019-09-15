import pyaudio
import struct
import numpy as np
import time
import sys
import pygame
import wave

class Yell:
    def __init__(self):
        pygame.init()
        self.size = 800, 800
        self.black = 0, 0, 0
        self.white = 255, 255, 255
        self.red = 255, 0, 0
        self.blue = 0, 0, 255

        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption('The quiet game')
 
        self.level = 0
        self.leveldata = [[0, 0, 0, 0, 0, 0, 0],
                            [350, 525, 325, 400, 125, 200, 1], 
                            [275, 500, 425, 500, 150, 225, 2],
                            [200, 575, 375, 450, 550, 625, 4],
                            [175, 175, 575, 650, 575, 650, 3],
                            [375, 550, 350, 425, 175, 250, 2],
                            [175, 175, 550, 625, 550, 625, 3]]
        self.score = 0

        self.image = pygame.image.load("1.png")
        self.ballimg = pygame.image.load("ball.png")
        self.markerimg = pygame.image.load("marker.png")
        self.ballx = 0
        self.bally = 0
        self.markerx = 0
        self.markery = 0
        self.aim = False
        self.dir = (0, 1)
        self.xlow = 0
        self.xhigh = 0
        self.ylow = 0
        self.yhigh = 0
        self.totalc = 20
        self.par = 0

        self.FORMAT = pyaudio.paFloat32
        self.CHANNELS = 1
        self.RATE = 44100
        self.CHUNK = 1024
        self.RECORD_SECONDS = 3

        self.audio = pyaudio.PyAudio()

        self.power = 0

    def text_objects(self, text, font):
        textSurface = font.render(text, True, (200, 10, 10))
        return textSurface, textSurface.get_rect() 
    
    def text_objects2(self, text, font):
        textSurface = font.render(text, True, (0, 0, 0))
        return textSurface, textSurface.get_rect()

    def DrawBar(self, pos, size, borderC, barC, progress):

        pygame.draw.rect(self.screen, borderC, (*pos, *size), 1)
        innerPos  = (pos[0]+3, pos[1]+3)
        innerSize = ((size[0]-6) * progress, size[1]-6)
        pygame.draw.rect(self.screen, barC, (*innerPos, *innerSize))

    def find_power(self):
        self.stream = self.audio.open(format=self.FORMAT,
                channels = self.CHANNELS,
                rate = self.RATE, input=True, frames_per_buffer=self.CHUNK)
                    
        self.power = 0

        x = []

        for i in range(0, int(self.RATE/self.CHUNK*self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            decoded = struct.unpack(str(self.CHUNK)+'f',data)
            x.append(np.array(decoded))
        for i in range(len(x)):
            self.power+=(np.sqrt(np.mean(x[i]**2)))
        
        self.stream.stop_stream()
        self.stream.close()

    def set_dir(self):
        diffx = self.markerx-self.ballx
        diffy = self.markery-self.bally
        mag = (diffx**2+diffy**2)**0.5
        self.dir = ((diffx/mag, diffy/mag))
    def get_power(self):
        return self.power
    def ball(self, x, y):
        self.screen.blit(self.ballimg, (x, y))
    def marker(self, x, y):
        self.screen.blit(self.markerimg, (x-16, y-16))
    def levelup(self):
        if self.level == 6:
            start = time.time()
            largeText = pygame.font.Font("ComicSansMS3.ttf", 36)
            endTextSurf, endTextRect = self.text_objects("were you quiet???", largeText)
            scoreTextSurf, scoreTextRect = self.text_objects("real score: " + str(-self.totalc), 
                    largeText)
            endTextRect.center = (400, 300)
            scoreTextRect.center = (400, 450)
            self.screen.fill(self.white)
            while(time.time()-start < 5):
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                self.screen.blit(endTextSurf, endTextRect)
                self.screen.blit(scoreTextSurf, scoreTextRect)
                pygame.display.flip()
        self.level+=1
        self.ballx = self.leveldata[self.level][0]
        self.bally = self.leveldata[self.level][1]
        self.xlow = self.leveldata[self.level][2]
        self.xhigh = self.leveldata[self.level][3]
        self.ylow = self.leveldata[self.level][4]
        self.yhigh = self.leveldata[self.level][5]
        self.par = self.leveldata[self.level][6]
        string = str(self.level)+".png"
        self.image = pygame.image.load(string)
    def main_loop(self):
        while True:
            if self.level == 0:
                largeText = pygame.font.Font("ComicSansMS3.ttf", 36)
                self.screen.fill(self.white)
                titleTextSurf, titleTextRect = self.text_objects("the quiet game",
                        largeText)
                titleTextRect.center = ( 400, 400 )
                start = time.time()
                while(time.time()-start < 5):
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            sys.exit()
                    self.screen.fill(self.white)
                    self.screen.blit(titleTextSurf, titleTextRect)
                    pygame.display.flip()
                self.levelup()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit()
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        mouse = pygame.mouse.get_pos()
                        if self.aim:
                            self.markerx = mouse[0]
                            self.markery = mouse[1]
                            self.set_dir()
                            self.aim = False
                        else:
                            if 150 > mouse[0] > 50 and 750 > mouse[1] > 700:
                                self.totalc-=1
                                self.find_power()
                                red = False
                                shiftx = 0
                                shifty = 0
                                if self.dir[0] >= 0:
                                    for i in range(
                                            int(min(800-self.ballx,int(5*self.dir[0]*self.get_power())))):
                                        if self.screen.get_at((int(self.ballx+i+25), int(self.bally)))[0] > 10:
                                            if self.screen.get_at((int(self.ballx+i+25), int(self.bally)))[1] < 200:
                                                red = True
                                                break
                                        shiftx = i
                                else:
                                    for i in range(
                                            0, int(max(-self.ballx,int(5*self.dir[0]*self.get_power()))), -1):
                                        if self.screen.get_at((int(self.ballx+i), int(self.bally)))[0] > 10:
                                            if self.screen.get_at((int(self.ballx+i), int(self.bally)))[1] < 200:
                                                red = True
                                                break
                                        shiftx = i
                                if self.dir[1] >= 0:
                                    for i in range(
                                            int(min(800-self.bally,int(5*self.dir[1]*self.get_power())))):
                                        if self.screen.get_at((int(self.ballx), int(self.bally+i+25)))[0] > 10:
                                            if self.screen.get_at((int(self.ballx), int(self.bally+i+25)))[1] < 200:
                                                red = True
                                                break
                                        shifty = i
                                else:
                                    for i in range(
                                            0, int(max(-self.bally,int(5*self.dir[1]*self.get_power()))), -1):
                                        if self.screen.get_at((int(self.ballx), int(self.bally+i)))[0] > 10:
                                            if self.screen.get_at((int(self.ballx), int(self.bally+i)))[1] < 200:
                                                red = True
                                                break
                                        shifty = i
                                if not red:
                                    self.ballx+=(5*self.dir[0]*self.get_power())
                                    self.bally+=(5*self.dir[1]*self.get_power())
                                else:
                                    if abs(shiftx/self.dir[0]) < abs(shifty/self.dir[1]):
                                        self.ballx+=shiftx
                                        self.bally+=int(shiftx*self.dir[1]/self.dir[0])
                                    else:
                                        self.bally+=shifty
                                        self.ballx+=int(shifty*self.dir[0]/self.dir[1])
                                self.ball(self.ballx, self.bally)
                                if (self.xhigh-6 >= self.ballx >= self.xlow+6 and 
                                        self.yhigh-6 >= self.bally >= self.ylow+6):
                                    self.levelup()
                            elif 750 > mouse[0] > 650 and 750 > mouse[1] > 700:
                                self.aim = True
                self.screen.fill(self.white)
                self.screen.blit(self.image, (0, 0))
                self.ball(self.ballx, self.bally)
                mouse = pygame.mouse.get_pos()
                if self.aim:
                    self.marker(mouse[0], mouse[1])
                if 150 > mouse[0] > 50 and 750 > mouse[1] > 700:
                    pygame.draw.rect(self.screen, (200, 200, 200), (50, 700, 100, 50))
                else:
                    pygame.draw.rect(self.screen, (60, 60, 60), (50, 700, 100, 50))
                if 750 > mouse[0] > 650 and 750 > mouse[1] > 700:
                    pygame.draw.rect(self.screen, (200, 200, 200), (650, 700, 100, 50))
                else:
                    pygame.draw.rect(self.screen, (60, 60, 60), (650, 700, 100, 50))

                smallText = pygame.font.Font("freesansbold.ttf",20)
                powTextSurf, powTextRect = self.text_objects("POWER", smallText)
                powTextRect.center = ( 100, 725 )
                self.screen.blit(powTextSurf, powTextRect)
                aimTextSurf, aimTextRect = self.text_objects("AIM", smallText)
                aimTextRect.center = ( 700, 725 )
                self.screen.blit(aimTextSurf, aimTextRect)
                descTextSurf, descTextRect = self.text_objects("Your Power", smallText)
                descTextRect.center = ( 400, 700 )
                self.screen.blit(descTextSurf, descTextRect)
                scoreTextSurf, scoreTextRect = self.text_objects2("Score: " + str(self.totalc), smallText)
                scoreTextRect.center = (700, 50)
                self.screen.blit(scoreTextSurf, scoreTextRect)
                parTextSurf, parTextRect = self.text_objects2("Par " + str(self.par), smallText)
                parTextRect.center = (500, 50)
                self.screen.blit(parTextSurf, parTextRect)


                self.DrawBar((300, 750), (200, 20), (0, 0, 0), (0, 128, 0), self.get_power()/300)
                pygame.display.flip()

game = Yell()

game.main_loop()
