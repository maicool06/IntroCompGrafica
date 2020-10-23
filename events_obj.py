import pygame

class events_obj():
    def __init__(self):
        self.hueteotl = pygame.USEREVENT + 1
        self.hueteotl_weapon = pygame.USEREVENT + 2
        self.hueteotl_jump = pygame.USEREVENT + 3
        self.hueteotl_jump_weapon = pygame.USEREVENT + 4
        
        self.velocidad_caminar = 500
        self.velocidad_correr = 500
        

    def startTimeEvents(self, element):

        if element == 1:
            pygame.time.set_timer(self.hueteotl, self.velocidad_caminar)
            pygame.time.set_timer(self.hueteotl_weapon, self.velocidad_caminar)
            return
            
        if element == 2:
            pygame.time.set_timer(self.hueteotl_jump, self.velocidad_correr)
            pygame.time.set_timer(self.hueteotl_jump_weapon, self.velocidad_correr)
            return

        else:
            print("Default Start")

    def stopTimeEvents(self, element):

        if element == 1:
            pygame.time.set_timer(self.hueteotl, 0)
            pygame.time.set_timer(self.hueteotl_weapon, 0)
            return
            
        if element == 2:
            pygame.time.set_timer(self.hueteotl_jump, 0)
            pygame.time.set_timer(self.hueteotl_jump_weapon, 0)
            return
        
        else:
            print("Default Stop")

        
        
       
    
