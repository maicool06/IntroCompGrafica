import pygame

class events_obj():
    def __init__(self):
        self.hueteotl = pygame.USEREVENT + 1
        self.hueteotl_weapon = pygame.USEREVENT + 2
        

    def setTimeEvents(self):
        pygame.time.set_timer(self.hueteotl, 50)
        pygame.time.set_timer(self.hueteotl_weapon, 50)

    
