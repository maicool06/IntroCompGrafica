
import pygame

class sound:
    
    def __init__(self):
        pygame.mixer.init()      


    def startSount(self, element):

        #sonidoRecolección = pygame.mixer.Sound('recolección.wav')

        if element == "run":
            pygame.mixer.music.load("./Music/hueteotl_run.mp3")
            pygame.mixer.music.play(-1, 0.0)
            return
        if element == "jump":
            pygame.mixer.music.sound("./Music/hueteotl_jump.wav")
            pygame.mixer.music.play(-1, 0.0)
            return
        if element == "crouch":
            pygame.mixer.music.sound("./Music/hueteotl_crouch.wav")
            pygame.mixer.music.play(-1, 0.0)
            return
        if element == "stand":
            pygame.mixer.music.load("./Music/hueteotl_stand.mp3")
            pygame.mixer.music.play(-1, 0.0)
            return
        else:
            print("Default Start")

        
        def stopSount(self):
            pygame.mixer.music.stop()