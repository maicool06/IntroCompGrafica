import pygame

class events_obj():
    def __init__(self):
        self.hueteotl_run = pygame.USEREVENT + 0
        self.hueteotl_jump = pygame.USEREVENT + 1
        self.hueteotl_crouch = pygame.USEREVENT + 2
        self.hueteotl_stand = pygame.USEREVENT + 3
        self.box_1 = pygame.USEREVENT + 4

        self.v_hueteotl_run = 250
        self.v_hueteotl_jump = 300
        self.v_hueteotl_crouch = 250
        self.v_hueteotl_stand = 250
        self.v_box_1 = 300 

    def startTimeEvents(self, element):

        if element == "run":
            pygame.time.set_timer(self.hueteotl_run, self.v_hueteotl_run)
        
        elif element == "jump":
            pygame.time.set_timer(self.hueteotl_jump, self.v_hueteotl_jump)
        
        elif element == "crouch":
            pygame.time.set_timer(self.hueteotl_crouch, self.v_hueteotl_crouch)
        
        elif element == "stand":
            pygame.time.set_timer(self.hueteotl_stand, self.v_hueteotl_stand)

        elif element == "box_1":
            pygame.time.set_timer(self.box_1, self.v_box_1)

        else:
            print("Default Start")

    def stopTimeEvents(self, element):
        if element == "run":
            pygame.time.set_timer(self.hueteotl_run, 0)

        elif element == "jump":
            pygame.time.set_timer(self.hueteotl_jump, 0)

        elif element == "crouch":
            pygame.time.set_timer(self.hueteotl_crouch, 0)

        elif element == "stand":
            pygame.time.set_timer(self.hueteotl_stand, 0)

        elif element == "box_1":
            pygame.time.set_timer(self.box_1, 0)

        elif element == "all":                                #Solo los del Hueteotl
            pygame.time.set_timer(self.hueteotl_run, 0)
            pygame.time.set_timer(self.hueteotl_jump, 0)
            pygame.time.set_timer(self.hueteotl_crouch, 0)
            pygame.time.set_timer(self.hueteotl_stand, 0)
            
        else:
            print("Default Stop")  
        
        
       
    
