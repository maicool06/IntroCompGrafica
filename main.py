import numpy
import pygame

from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GL.shaders import *


from obj import *
from events_obj import *
from texture import *
from sound import *


def main():

    game_state = "Start"

    #--------------------------------------------------------------------------------------- 

    # Instrucciones para levantar ventana grafica
    
    pygame.init()
    width = 1024
    height = 720
    display = (width,height)
    
    gameDisplay  = pygame.display.set_mode(display, DOUBLEBUF|OPENGL|OPENGLBLIT)
    pygame.display.set_caption('Game Of Life')
    clock = pygame.time.Clock()

    #---------------------------------------------------------------------------------------  

    # Cargar archivos .obj.

    list_hueteotl_run = obj().objLoad(5,"./Animaciones/hueteotl_animado/","hueteotl_run_")    
    list_hueteotl_weapon_run = obj().objLoad(5,"./Animaciones/weapon_hueteotl_animada/","weapon_run_")  

    list_hueteotl_jump = obj().objLoad(5,"./Animaciones/hueteotl_animado/","hueteotl_jump_")  
    list_hueteotl_weapon_jump = obj().objLoad(5,"./Animaciones/weapon_hueteotl_animada/","weapon_jump_")  

    list_hueteotl_crouch = obj().objLoad(5,"./Animaciones/hueteotl_animado/","hueteotl_crouch_walk_")  
    list_hueteotl_weapon_crouch = obj().objLoad(5,"./Animaciones/weapon_hueteotl_animada/","weapon_crouch_walk_")  

    list_hueteotl_stand= obj().objLoad(39,"./Animaciones/hueteotl_animado/","hueteotl_stand_")  
    list_hueteotl_weapon_stand = obj().objLoad(39,"./Animaciones/weapon_hueteotl_animada/","weapon_stand_")


    list_box = obj().objLoad(0,"./Animaciones/box/","box_")  
   
    #---------------------------------------------------------------------------------------

    # Activo las texturas ( 8 disponibles).

    glEnable(GL_TEXTURE_2D)                         
    glActiveTexture(GL_TEXTURE0)       

    # Cargar texturas.
    
    textura = texture()

    #---------------------------------------------------------------------------------------

    # Cargar musica.
    
    sonido = sound()

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
    glViewport(0,0,width,height)            # Crea la matriz de escala, transforma de unidades arbitrarias a pixels.
    glFrustum(-1, 1, -1, 1, 1, 1000)     # Crea la matriz de Proyeccion. volumen de vista.

    glEnable(GL_DEPTH_TEST)                         # Comparaciones de profundidad y actualizar el bufer de profundidad.

    glClearColor(0.1,0.6,0.8,0.5)               # Color de fondo.

    
    #---------------------------------------------------------------------------------------

    # Variables
    ang = 20
    vel = 1
    pos_box_1 = 15
    pos_box_2 = 30

    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
    light = False


    #---------------------------------------------------------------------------------------
    
   
    #Inicializar cosas de cositas para cosotes    
    
    obj_hueteotl = list_hueteotl_stand[0]

    obj_hueteotl_weapon = list_hueteotl_weapon_stand[0]

    obj_box = list_box[0]

    eventos = events_obj()

    eventos.startTimeEvents("stand")    
    sonido.startSound("stand")

    #---------------------------------------------------------------------------------------

    c_hueteotl_run = 0
    c_hueteotl_jump = 0
    c_hueteotl_crouch = 0
    c_hueteotl_stand = 0 

    while True:

        for event in pygame.event.get():        

            if event.type >= pygame.USEREVENT and event.type <= pygame.USEREVENT + 4:     # Evento Obj 

                if event.type == eventos.hueteotl_run:
                    obj_hueteotl = list_hueteotl_run[c_hueteotl_run]
                    obj_hueteotl_weapon = list_hueteotl_weapon_run[c_hueteotl_run]
                
                    if c_hueteotl_run >= ( len(list_hueteotl_run) - 1 ):
                        c_hueteotl_run = 0
                    else:
                        c_hueteotl_run += 1

                if event.type == eventos.hueteotl_jump:
                    obj_hueteotl = list_hueteotl_jump[c_hueteotl_jump]
                    obj_hueteotl_weapon = list_hueteotl_weapon_jump[c_hueteotl_jump]

                    if c_hueteotl_jump >= ( len(list_hueteotl_jump) - 1 ):
                        c_hueteotl_jump = 0
                        eventos.stopTimeEvents("all")
                        eventos.startTimeEvents("run")       
                        sonido.stopSound("jump")             
                    else:
                        c_hueteotl_jump += 1

                if event.type == eventos.hueteotl_crouch:
                    obj_hueteotl = list_hueteotl_crouch[c_hueteotl_crouch]
                    obj_hueteotl_weapon = list_hueteotl_weapon_crouch[c_hueteotl_crouch]

                    if c_hueteotl_crouch >= ( len(list_hueteotl_crouch) - 1 ):
                        c_hueteotl_crouch = 0
                        eventos.stopTimeEvents("all")
                        eventos.startTimeEvents("run")    
                        sonido.stopSound("crouch")                         
                    else:
                        c_hueteotl_crouch += 1

                if event.type == eventos.hueteotl_stand:
                    obj_hueteotl = list_hueteotl_stand[c_hueteotl_stand]
                    obj_hueteotl_weapon = list_hueteotl_weapon_stand[c_hueteotl_stand]

                    if c_hueteotl_stand >= ( len(list_hueteotl_stand) - 1 ):
                        c_hueteotl_stand = 0
                    else:
                        c_hueteotl_stand += 1

                if event.type == eventos.box_1:
                    pos_box_1 -= 1
                    pos_box_2 -= 1

                    if pos_box_1 <= -15:
                        pos_box_1 = 15
                    if pos_box_2 <= -15:
                        pos_box_2 = 15
                    
            elif event.type == pygame.KEYDOWN:    # Evento tecla presionada.

                if event.key == pygame.K_w and game_state == "Playing":             # Saltar
                    eventos.stopTimeEvents("all")
                    eventos.startTimeEvents("jump")
                    sonido.startSound("jump")
 
                if event.key == pygame.K_s and game_state == "Playing":             # Agacharse
                    eventos.stopTimeEvents("all")
                    eventos.startTimeEvents("crouch")
                    sonido.startSound("crouch")
                
                if event.key == pygame.K_d and game_state == "Start":             # Start
                    eventos.stopTimeEvents("all")
                    eventos.startTimeEvents("run")
                    eventos.startTimeEvents("box_1")
                    
                    sonido.stopSound("all")
                    sonido.startSound("run")
                    game_state = "Playing"    

                if event.key == pygame.K_p and ( game_state == "Playing" or  game_state == "Pause"):           # Pause
                    
                    if  game_state != "Pause":  
                        
                        game_state = "Pause"
                        sonido.stopSound("all")
                        pygame.mixer.music.pause()
                        eventos.stopTimeEvents("all")
                        eventos.stopTimeEvents("box_1")
                        
                    else:
                        
                        game_state = "Playing"  
                        pygame.mixer.music.unpause()
                        eventos.startTimeEvents("run")
                        eventos.startTimeEvents("box_1")
                        sonido.startSound("run")
                        
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

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

                if event.key == pygame.K_l:     # Con la letra L prendo y apago la iluminacion
                    light = not light
                    if(light):
                        #glEnable(GL_LIGHTING)

                        '''
                         #hago push matrix para salvar el estado, y luego ingreso las transfromaciones para mover la luz
                        #glPushMatrix()
                        glRotatef(ang, 0,0,1)
                        glTranslatef(10,15,0)


                        #Dibujo un punto para mostrar donde está la fuente de luz
                        glDisable(GL_LIGHTING)
                        glBegin(GL_POINTS)
                        glVertex3fv([10,15,0])
                        glEnd()
                        glEnable(GL_LIGHTING)

                        #Al setear la posción de la luz, esta se multiplica por el contenido de la matrix MODELVIEW, haciendo que la fuente de luz se mueva
                        glLightfv(GL_LIGHT4, GL_POSITION, [0,0,0,1])
                        '''

                        #glClearColor(0.,0.,0.,1.)
                        glShadeModel(GL_SMOOTH)
                        glEnable(GL_CULL_FACE)
                        glEnable(GL_DEPTH_TEST)
                        glEnable(GL_LIGHTING)
                        lightZeroPosition = [10.,20.,10.,10.]
                        #lightZeroColor = [0.8,1.0,0.8,1.0] #green tinged
                        lightZeroColor = [1.0,0,0,1.0] #green tinged

                        glEnable(GL_LIGHTING)   #Prueba
                        glLightfv(GL_LIGHT0, GL_AMBIENT, (GLfloat*4)(1,1,1,1))
                        glLightfv(GL_LIGHT0, GL_DIFFUSE, (GLfloat*4)(1,1,1,1))
                        glEnable(GL_LIGHT0)


                        glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
                        glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
                        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.1)
                        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
                        glEnable(GL_LIGHT0)


                        #Vuelvo al estado anterior de la matriz, para dibujar el modelo
                        #glPopMatrix()

                    else:
                        glDisable(GL_LIGHTING)
                        glClearColor(0.1,0.6,0.8,0.5)               # Color de fondo.
  
            elif event.type == pygame.QUIT:       
                pygame.quit()
                quit()

        
     #---------------------------------------------------------------------------------------
    
        glMatrixMode(GL_MODELVIEW)                          # Activo el stack de matrices MODELVIEW.           
        glLoadIdentity()                                    # Limpio todas la transformaciones previas.
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    # Limpio el buffer de colores donde voy a dibujar.
        
        # Habilito arrays.

        glEnableClientState(GL_VERTEX_ARRAY)                
        glEnableClientState(GL_NORMAL_ARRAY)               
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)        


    #---------------------------------------------------------------------------------------

        #  BOX 1

        glPushMatrix()
   
        glTranslatef(pos_box_1, -5, -15)  # Traslacion. (derecha, arriba, profundida).
        glScalef(0.5,0.5,0.5)
      
        glRotatef(0, 0, 0, 0)   # Rotacion.  (angulo, eje x, eje y, eje z).
    
        #glRotatef(270, 180,0,0)   # Rotacion.  (angulo, eje x, eje y, eje z).

        #glRotatef(230, 0,0,1)

        glVertexPointer(3, GL_FLOAT, 0, obj_box.vertFaces)         
        glNormalPointer(GL_FLOAT, 0, obj_box.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, obj_box.texturesFaces)

        glBindTexture(GL_TEXTURE_2D, textura.box_1)                  
        glDrawArrays(GL_TRIANGLES, 0, len(obj_box.vertFaces)*3)     

        glPopMatrix()

    #---------------------------------------------------------------------------------------

        #  BOX 2

        glPushMatrix()
   
        glTranslatef(pos_box_2, 5, -15)  # Traslacion. (derecha, arriba, profundida).
        glScalef(0.5,0.5,0.5)
      
        glRotatef(0, 0, 0, 0)   # Rotacion.  (angulo, eje x, eje y, eje z).
    
        #glRotatef(270, 180,0,0)   # Rotacion.  (angulo, eje x, eje y, eje z).

        #glRotatef(230, 0,0,1)

        glVertexPointer(3, GL_FLOAT, 0, obj_box.vertFaces)         
        glNormalPointer(GL_FLOAT, 0, obj_box.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, obj_box.texturesFaces)

        glBindTexture(GL_TEXTURE_2D, textura.box_2)                  
        glDrawArrays(GL_TRIANGLES, 0, len(obj_box.vertFaces)*3)     

        glPopMatrix()

   #---------------------------------------------------------------------------------------

        #   HUETEOTL

        glPushMatrix()
   
        glTranslatef(0, 0, -2)  # Traslacion. (derecha, arriba, profundida).
        #glScalef(0.02,0.02,0.02)
        glScalef(0.03,0.03,0.03)
        
        #glTranslatef(-20,-10,-80) # Traslacion. (derecha, arriba, profundida).
        
        #glRotatef(0, 0, 0, 0)   # Rotacion.  (angulo, eje x, eje y, eje z).
    
        glRotatef(270, 180,0,0)   # Rotacion.  (angulo, eje x, eje y, eje z).

        #glRotatef(230, 0,0,1)

        glVertexPointer(3, GL_FLOAT, 0, obj_hueteotl.vertFaces)         
        glNormalPointer(GL_FLOAT, 0, obj_hueteotl.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, obj_hueteotl.texturesFaces)

        glBindTexture(GL_TEXTURE_2D, textura.hueteotl)                  
        glDrawArrays(GL_TRIANGLES, 0, len(obj_hueteotl.vertFaces)*3)     

        glPopMatrix()

    #---------------------------------------------------------------------------------------
 
        #   HUETEOTL WEAPON

        glPushMatrix()
   
        glTranslatef(0, 0, -2)  # Traslacion. (derecha, arriba, profundida).
        glScalef(0.02,0.02,0.02)
        
        #glTranslatef(-20,-10,-80) # Traslacion. (derecha, arriba, profundida).
        
        #glRotatef(0, 0, 0, 0)   # Rotacion.  (angulo, eje x, eje y, eje z).
    
        glRotatef(270, 180,0,0)   # Rotacion.  (angulo, eje x, eje y, eje z).

        #glRotatef(230, 0,0,1)

        glVertexPointer(3, GL_FLOAT, 0, obj_hueteotl_weapon.vertFaces)         
        glNormalPointer(GL_FLOAT, 0, obj_hueteotl_weapon.normalFaces)           
        glTexCoordPointer(2, GL_FLOAT, 0, obj_hueteotl_weapon.texturesFaces)

        glBindTexture(GL_TEXTURE_2D, textura.hueteotl_weapon)                  
        glDrawArrays(GL_TRIANGLES, 0, len(obj_hueteotl_weapon.vertFaces)*3)     

        glPopMatrix()
    
        
    #---------------------------------------------------------------------------------------


        # Luego de dibujar, desactivo todo.

        glBindTexture(GL_TEXTURE_2D, 0)                     

        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_NORMAL_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)
        
        pygame.display.flip()       # Hago flip de los buffers, para que se refresque la imagen en pantalla

        
    #glDeleteTextures([text])
    pygame.quit()
    quit()

main()  
