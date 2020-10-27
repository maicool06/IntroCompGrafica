import pygame

from pygame.locals import *

class sound:
    
    soundObj = None
    
    def __init__(self):
        pygame.mixer.pre_init(44100, 16, 2, 4096) #frequency, size, channels, buffersize
        pygame.mixer.init()      

        self.hueteotl_run = pygame.mixer.Sound("./Music/hueteotl_run.ogg")
        self.hueteotl_jump = pygame.mixer.Sound("./Music/hueteotl_jump.ogg")
        self.hueteotl_crouch = pygame.mixer.Sound("./Music/hueteotl_crouch.ogg")
        self.hueteotl_stand = pygame.mixer.Sound("./Music/hueteotl_stand.ogg")
        
    def startSound(self, element):

        if element == "run":
            self.hueteotl_run.play(-1)
            self.hueteotl_run.set_volume(0.2)
        
        elif element == "jump":
            self.hueteotl_jump.play
        
        elif element == "crouch":
            self.hueteotl_crouch.play()

        elif element == "stand":
            self.hueteotl_stand.play(-1)
        
        elif element == "background":
            pygame.mixer.music.load("./Music/background.mp3")
            pygame.mixer.music.play(-1, 0.0)

        else:
            print("Default Start")

        
    def stopSound(self, element):
        
        if element == "run":
            self.hueteotl_run.stop()
    
        elif element == "jump":
            self.hueteotl_jump.stop()
        
        elif element == "crouch":
            self.hueteotl_crouch.stop()

        elif element == "stand":
            self.hueteotl_stand.stop()
        
        elif element == "background":
            pygame.mixer.music.stop()

        elif element == "all":
            self.hueteotl_run.stop()
            self.hueteotl_jump.stop()
            self.hueteotl_crouch.stop()
            self.hueteotl_stand.stop()
            #pygame.mixer.music.stop()