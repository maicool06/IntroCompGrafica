import numpy
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

class texture:
    
    hueteotl = None
    hueteotl_weapon = None
    box = None
    fondo_caverna = None
    fondo_game_over = None

    def __init__(self):
        
         # Activo las texturas ( 8 disponibles).
        glEnable(GL_TEXTURE_2D)                         
        glActiveTexture(GL_TEXTURE0)       
        
        # Levanta las texturas a memoria de video            
        self.hueteotl = self.__loadTexture("./Animaciones/hueteotl_animado/hueteotl.png")
        self.hueteotl_weapon = self.__loadTexture("./Animaciones/weapon_hueteotl_animada/weapon.png")
        self.box = self.__loadTexture("./Animaciones/box/box.jpg")
        self.fondo_caverna = self.__loadTexture("./Animaciones/fondo/fondo_pasto.jpg")
        self.fondo_game_over = self.__loadTexture("./Animaciones/fondo/fondo_game_over.jpg")
 
    def __loadTexture(self,path):

        surf = pygame.image.load(path)                  # Cargo imagen en memoria
        surf = pygame.transform.flip(surf, False, True) # Espejo la imagen

        image = pygame.image.tostring(surf, 'RGBA', 1)  # Obtengo la matriz de colores de la imagen.
        
        ix, iy = surf.get_rect().size       # Obentego las dimensiones de la imagen
        texid = glGenTextures(1)            # Textura vacia en memoria de video
        glBindTexture(GL_TEXTURE_2D, texid) # Activo textura

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
        
        glBindTexture(GL_TEXTURE_2D, 0)
        
        return texid
