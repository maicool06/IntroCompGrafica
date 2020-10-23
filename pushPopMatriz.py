import numpy
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *


class pushPopMatriz:

    @staticmethod
    def load( obj, texture):
        glPushMatrix()

   
        glTranslatef(-20,-10,-80) # Traslacion. (derecha, arriba, profundida).
        glRotatef(270, 180,0,0)   # Rotacion.  (angulo, eje x, eje y, eje z).

        #glRotatef(230, 0,0,1)

        glVertexPointer(3, GL_FLOAT, 0, obj.vertFaces)         
        glNormalPointer(GL_FLOAT, 0, obj.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, obj.texturesFaces)

        glBindTexture(GL_TEXTURE_2D, texture)                  
        glDrawArrays(GL_TRIANGLES, 0, len(obj.vertFaces)*3)     

        glPopMatrix()


  