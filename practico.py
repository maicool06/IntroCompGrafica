import numpy
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *

from obj import *
from events_obj import *

def main():

    #--------------------------------------------------------------------------------------- 

    # Instrucciones para levantar ventana grafica
    
    pygame.init()
    cw = 800
    ch = 600
    display = (cw,ch)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    pygame.display.set_caption('Game Of Life')



    #---------------------------------------------------------------------------------------  

    # Cargar archivos .obj.

    list_hueteotl = obj().objLoad(39,"./Animaciones/hueteotl_animado/","hueteotl_stand_")  
    hueteotl = list_hueteotl[0]

    list_hueteotl_weapon = obj().objLoad(39,"./Animaciones/weapon_hueteotl_animada/","weapon_stand_")  
    hueteotl_weapon = list_hueteotl_weapon[0]
    
    #---------------------------------------------------------------------------------------

    # Activo las texturas ( 8 disponibles).

    glEnable(GL_TEXTURE_2D)                         
    glActiveTexture(GL_TEXTURE0)       

    # Funcion que levanta la textura a memoria de video            

    text1 = loadTexture("./Animaciones/hueteotl_animado/hueteotl.png")

    text2 = loadTexture("./Animaciones/weapon_hueteotl_animada/weapon.png")

    #---------------------------------------------------------------------------------------
    
    #glShadeModel(GL_SMOOTH) # El pipeline estatico use Gouraud Shading (sombreado suave).

    # Seteao los parametros del material del objeto a dibujar.
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, [1,1,1,1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, [0.2,0.2,0.2,1])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [1,1,1,1])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 128)           


    # Activo las luces ( 0 a 7 )

    glEnable(GL_LIGHT0)   
    glLight(GL_LIGHT0, GL_DIFFUSE, [1.0,0.0,0.0,1])      
    glLight(GL_LIGHT0, GL_AMBIENT, [1,1,1,1])       
    glLight(GL_LIGHT0, GL_POSITION, [0,100,-50,0])      # [0,0,0,1] es luz puntual, [0,0,0,0] es luz direccional
    glLight(GL_LIGHT0, GL_SPECULAR, [1,0,0,1])

    #---------------------------------------------------------------------------------------

    glMatrixMode(GL_PROJECTION)          # Activo el stack de matrices para la proyeccion.
    glLoadIdentity()                     # Cargo una identidad para asegurarme que comience vacio.
    glViewport(0,0,cw,ch)            # Crea la matriz de escala, transforma de unidades arbitrarias a pixels.
    glFrustum(-1, 1, -1, 1, 1, 1000)     # Crea la matriz de Proyeccion. volumen de vista.

    glEnable(GL_DEPTH_TEST)                         # Comparaciones de profundidad y actualizar el bufer de profundidad.

    glClearColor(0,1,1,1)               # Color de fondo.

    
    #---------------------------------------------------------------------------------------

    # Variables
    ang = 0.0
    vel = 0.0

    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
    light = False


    #---------------------------------------------------------------------------------------
    
    eventos = events_obj()

    eventos.setTimeEvents()


    #---------------------------------------------------------------------------------------

    
    c_hueteotl = 0
    c_hueteotl_weapon = 0

    while True:
        for event in pygame.event.get():        
            if event.type == pygame.QUIT:       
                pygame.quit()
                quit()
        
            
            
            if event.type == pygame.KEYDOWN:    # Evento tecla presionada.

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                if event.key == pygame.K_l:     # Con la letra L prendo y apago la iluminacion
                    light = not light
                    if(light):
                        glEnable(GL_LIGHTING)
                    else:
                        glDisable(GL_LIGHTING)

                if event.key == pygame.K_m:     # Con la letra m, lo deja en formato malla o no (con o sin fondo).
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode( GL_FRONT_AND_BACK, mode)

                if event.key == pygame.K_z:     # Con la letra z, activa el z-buffer
                    zBuffer = not zBuffer
                    if(zBuffer):
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)

                if event.key == pygame.K_b:     # Con la letra b, activo cullface
                    bfc = not bfc
                    if(bfc):
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)

                if event.key == pygame.K_c:     # Con la letra c
                    bfcCW = not bfcCW
                    if(bfcCW):
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)

            if event.type == eventos.hueteotl:
                hueteotl = list_hueteotl[c_hueteotl]

                if c_hueteotl >= ( len(list_hueteotl) - 1 ):
                    c_hueteotl = 0
                else:
                    c_hueteotl += 1
            
            if event.type == eventos.hueteotl_weapon:
                hueteotl_weapon = list_hueteotl_weapon[c_hueteotl_weapon]

                if c_hueteotl_weapon >= ( len(list_hueteotl_weapon) - 1 ):
                    c_hueteotl_weapon = 0
                else:
                    c_hueteotl_weapon += 1

    #---------------------------------------------------------------------------------------
    
        glMatrixMode(GL_MODELVIEW)                          # Activo el stack de matrices MODELVIEW.           
        glLoadIdentity()                                    # Limpio todas la transformaciones previas.
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    # Limpio el buffer de colores donde voy a dibujar.
        
        # Habilito arrays.

        glEnableClientState(GL_VERTEX_ARRAY)                
        glEnableClientState(GL_NORMAL_ARRAY)               
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)        


    #---------------------------------------------------------------------------------------

        glPushMatrix()


        glTranslatef(-30,0,-60) # Traslacion. (derecha, arriba, hacia adentro).
        glRotatef(-90, 1,0,0)   # Rotacion. (angulo, eje x, eje y, eje z).

        
        #glRotatef(230, 0,0,1)
        

        glVertexPointer(3, GL_FLOAT, 0, hueteotl.vertFaces)         
        glNormalPointer(GL_FLOAT, 0, hueteotl.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, hueteotl.texturesFaces)    

        glBindTexture(GL_TEXTURE_2D, text1)                  
        glDrawArrays(GL_TRIANGLES, 0, len(hueteotl.vertFaces)*3)     

        glPopMatrix()
        

    #---------------------------------------------------------------------------------------

        glPushMatrix()

        glTranslatef(-30,0,-60) # Traslacion. (derecha, arriba, hacia adentro).
        glRotatef(-90, 1,0,0)   # Rotacion. (angulo, eje x, eje y, eje z).
       
        #glRotatef(243, 0,0,1)
        

        glVertexPointer(3, GL_FLOAT, 0, hueteotl_weapon.vertFaces)          
        glNormalPointer(GL_FLOAT, 0, hueteotl_weapon.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, hueteotl_weapon.texturesFaces)    

        glBindTexture(GL_TEXTURE_2D, text2)                  
        glDrawArrays(GL_TRIANGLES, 0, len(hueteotl_weapon.vertFaces)*3)     

        glPopMatrix()

    #---------------------------------------------------------------------------------------
    
        # Luego de dibujar, desactivo todo.

        glBindTexture(GL_TEXTURE_2D, 0)                     

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        
        pygame.display.flip()       # Hago flip de los buffers, para que se refresque la imagen en pantalla

    glDeleteTextures([text])
    pygame.quit()
    quit()

def loadTexture(path):

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

main()  
