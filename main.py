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

    # Instrucciones para levantar ventana grafica
    
    pygame.init()
    width = 875
    height = 654
    display_wh = (width,height)
    
    displayGame  = pygame.display.set_mode(display_wh, DOUBLEBUF|OPENGL|OPENGLBLIT)
    pygame.display.set_caption('Game Of Life')
    clock = pygame.time.Clock()

    glClearColor(0.1,0.6,0.8,0.5)               # Color de fondo.

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

    list_fondo_caverna = obj().objLoad(0,"./Animaciones/fondo/","fondo_")  
   
    list_fondo_game_over = obj().objLoad(0,"./Animaciones/fondo/","fondo_")  

    list_fondo = obj().objLoad(0,"./Animaciones/fondo/","fondo_")  
    #---------------------------------------------------------------------------------------

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
 
    lightZeroPosition = [10.,20.,10.,10.]
    lightZeroColor = [1.0,0,0,1.0]  # Red

    glEnable(GL_LIGHT0)
    
    glShadeModel(GL_SMOOTH)
    glEnable(GL_CULL_FACE)
    glEnable(GL_DEPTH_TEST)
  
    glLightfv(GL_LIGHT0, GL_DIFFUSE, lightZeroColor)
    glLightfv(GL_LIGHT0, GL_POSITION, lightZeroPosition)
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 0.2)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.05)
   

    #---------------------------------------------------------------------------------------

    glMatrixMode(GL_PROJECTION)          # Activo el stack de matrices para la proyeccion.
    glLoadIdentity()                     # Cargo una identidad para asegurarme que comience vacio.
    glViewport(0,0,width,height)            # Crea la matriz de escala, transforma de unidades arbitrarias a pixels.
    glFrustum(-1, 1, -1, 1, 1, 1000)     # Crea la matriz de Proyeccion. volumen de vista.

    glEnable(GL_DEPTH_TEST)                         # Comparaciones de profundidad y actualizar el bufer de profundidad.

    #---------------------------------------------------------------------------------------
 
    #Inicializar cosas de cositas para cosotes    
    
    obj_hueteotl = list_hueteotl_stand[0]

    obj_hueteotl_weapon = list_hueteotl_weapon_stand[0]

    obj_box = list_box[0]

    obj_fondo_caverna = list_fondo_caverna[0]

    obj_fondo_game_over = list_fondo_game_over[0]

    eventos = events_obj()

    eventos.startTimeEvents("stand")    
    sonido.startSound("stand")

    #---------------------------------------------------------------------------------------

    
    # Variables

    pos_box_1 = 15
    pos_box_2 = 30

    mode = GL_FILL
    zBuffer = True
    bfc = False
    bfcCW = True
    light = False
    mute = False

    c_hueteotl_run = 0
    c_hueteotl_jump = 0
    c_hueteotl_crouch = 0
    c_hueteotl_stand = 0 

    game_state = "Start"
    
    #---------------------------------------------------------------------------------------
   
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

                elif event.type == eventos.hueteotl_jump:
                    obj_hueteotl = list_hueteotl_jump[c_hueteotl_jump]
                    obj_hueteotl_weapon = list_hueteotl_weapon_jump[c_hueteotl_jump]
                    game_state = "Jump"

                    if c_hueteotl_jump >= ( len(list_hueteotl_jump) - 1 ):
                        c_hueteotl_jump = 0
                        eventos.stopTimeEvents("all")
                        eventos.startTimeEvents("run")       
                        sonido.stopSound("jump")
                        game_state = "Playing"             
                    else:
                        c_hueteotl_jump += 1

                elif event.type == eventos.hueteotl_crouch:
                    obj_hueteotl = list_hueteotl_crouch[c_hueteotl_crouch]
                    obj_hueteotl_weapon = list_hueteotl_weapon_crouch[c_hueteotl_crouch]
                    game_state = "Crouch"

                    if c_hueteotl_crouch >= ( len(list_hueteotl_crouch) - 1 ):
                        c_hueteotl_crouch = 0
                        eventos.stopTimeEvents("all")
                        eventos.startTimeEvents("run")    
                        sonido.stopSound("crouch")
                        game_state = "Playing"                         
                    else:
                        c_hueteotl_crouch += 1

                elif event.type == eventos.hueteotl_stand:
                    obj_hueteotl = list_hueteotl_stand[c_hueteotl_stand]
                    obj_hueteotl_weapon = list_hueteotl_weapon_stand[c_hueteotl_stand]

                    if c_hueteotl_stand >= ( len(list_hueteotl_stand) - 1 ):
                        c_hueteotl_stand = 0
                        game_state = "Playing"
                    else:
                        c_hueteotl_stand += 1

                elif event.type == eventos.box_1:
                    pos_box_1 -= 0.5
                    pos_box_2 -= 0.5

                    if pos_box_1 <= -15:
                        pos_box_1 = 15
                    if pos_box_2 <= -15:
                        pos_box_2 = 30
                    
            elif event.type == pygame.KEYDOWN:    # Evento tecla presionada.

                if event.key == pygame.K_w and game_state == "Playing":             # Saltar
                    eventos.stopTimeEvents("all")
                    eventos.startTimeEvents("jump")
                    sonido.startSound("jump")
 
                elif event.key == pygame.K_s and game_state == "Playing":             # Agacharse
                    eventos.stopTimeEvents("all")
                    eventos.startTimeEvents("crouch")
                    sonido.startSound("crouch")
                
                elif event.key == pygame.K_d and game_state == "Start":             # Start
                    eventos.stopTimeEvents("all")
                    eventos.startTimeEvents("run")
                    eventos.startTimeEvents("box_1")
                    
                    sonido.stopSound("all")
                    sonido.startSound("run")
                    game_state = "Playing"    

                elif event.key == pygame.K_p and game_state != "Start" and game_state != "Over":           # Pause
                    
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

                elif event.key == pygame.K_o:     # Con la letra o, muteo y desmuteo.

                    mute = not mute
                    
                    if mute:
                        sonido.stopSound("all")
                        pygame.mixer.music.pause()

                    else:
                        if game_state == "Playing":
                            sonido.startSound("run")   
                        
                        if game_state == "Start":
                            sonido.startSound("stand")  
                        
                        pygame.mixer.music.unpause()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                elif event.key == pygame.K_m:     # Con la letra m, lo deja en formato malla o no (con o sin fondo).
                    if mode == GL_LINE:
                        mode = GL_FILL
                    else:
                        mode = GL_LINE
                    glPolygonMode( GL_FRONT_AND_BACK, mode)

                elif event.key == pygame.K_z:     # Con la letra z, activa el z-buffer
                    zBuffer = not zBuffer
                    if(zBuffer):
                        glEnable(GL_DEPTH_TEST)
                    else:
                        glDisable(GL_DEPTH_TEST)

                elif event.key == pygame.K_b:     # Con la letra b, activo cullface
                    bfc = not bfc
                    if(bfc):
                        glEnable(GL_CULL_FACE)
                    else:
                        glDisable(GL_CULL_FACE)

                elif event.key == pygame.K_c:     # Con la letra c
                    bfcCW = not bfcCW
                    if(bfcCW):
                        glFrontFace(GL_CW)
                    else:
                        glFrontFace(GL_CCW)

                elif event.key == pygame.K_l:     # Con la letra L prendo y apago la iluminacion
                    light = not light
                    if(light):
                        glEnable(GL_LIGHTING)
                        glClearColor(0.,0.,0.,1.)   # Black

                    else:
                        glDisable(GL_LIGHTING)
                        glClearColor(0.1,0.6,0.8,0.5)               # Color de fondo.
  
            elif event.type == pygame.QUIT:       
                pygame.quit()
                quit()
      
        #---------------------------------------------------------------------------------------

        glMatrixMode(GL_MODELVIEW)                          # Activo el stack de matrices MODELVIEW.           
        glLoadIdentity()                                    # Limpio todas la transformaciones previas.
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)    # Limpio el buffer de colores y el ZBuffer donde voy a dibujar.
        
        # Habilito arrays.

        glEnableClientState(GL_VERTEX_ARRAY)                
        glEnableClientState(GL_NORMAL_ARRAY)               
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)        
        
        if  ( (-7 < pos_box_1) and (pos_box_1 < -3)  and game_state != "Jump" ) or ( (-7 < pos_box_2 ) and (pos_box_2 < -3) and game_state != "Crouch" ):
            sonido.stopSound("all")
            eventos.stopTimeEvents("all")
            eventos.stopTimeEvents("box_1")

            #---------------------------------------------------------------------------------------

            #  Fondo game_over

            glPushMatrix()

            glTranslatef(0, 0, -20)  # Traslacion. (derecha, arriba, profundida).
            escala = 20.5
            glScalef(escala,escala,escala)

            glVertexPointer(3, GL_FLOAT, 0, obj_fondo_game_over.vertFaces)         
            glNormalPointer(GL_FLOAT, 0, obj_fondo_game_over.normalFaces)           
            glTexCoordPointer(2, GL_FLOAT, 0, obj_fondo_game_over.texturesFaces)

            glBindTexture(GL_TEXTURE_2D, textura.fondo_game_over)
            glDrawArrays(GL_TRIANGLES, 0, len(obj_fondo_game_over.vertFaces)*3)  

            glPopMatrix()

            pygame.display.flip()       # Hago flip de los buffers, para que se refresque la imagen en pantalla

            pygame.time.wait(3000)


            pos_box_1 = 15
            pos_box_2 = 30

            c_hueteotl_run = 0
            c_hueteotl_jump = 0
            c_hueteotl_crouch = 0
            c_hueteotl_stand = 0 

            game_state = "Start"
            eventos.startTimeEvents("stand")    
            sonido.startSound("stand")

        else:

            #  Fondo caverna

            glPushMatrix()

            glTranslatef(0, 0, -20)  # Traslacion. (derecha, arriba, profundida).
            escala = 20.5
            glScalef(escala,escala,escala)

            glVertexPointer(3, GL_FLOAT, 0, obj_fondo_caverna.vertFaces)         
            glNormalPointer(GL_FLOAT, 0, obj_fondo_caverna.normalFaces)           
            glTexCoordPointer(2, GL_FLOAT, 0, obj_fondo_caverna.texturesFaces)

            glBindTexture(GL_TEXTURE_2D, textura.fondo_caverna)
            glDrawArrays(GL_TRIANGLES, 0, len(obj_fondo_caverna.vertFaces)*3)  

            glPopMatrix()

            #---------------------------------------------------------------------------------------
            
            #  BOX Down

            glPushMatrix()
    
            glTranslatef(pos_box_1, -5, -10)  # Traslacion. (derecha, arriba, profundida).
            #glRotatef(230, 0,0,1)
            glScalef(1.0,1.0,1.0)
        
            glVertexPointer(3, GL_FLOAT, 0, obj_box.vertFaces)         
            glNormalPointer(GL_FLOAT, 0, obj_box.normalFaces)           
            glTexCoordPointer(2, GL_FLOAT, 0, obj_box.texturesFaces)

            glBindTexture(GL_TEXTURE_2D, textura.box)                  
            glDrawArrays(GL_TRIANGLES, 0, len(obj_box.vertFaces)*3)     

            glPopMatrix()
        
            #---------------------------------------------------------------------------------------
            
            #  BOX Up

            glPushMatrix()
    
            glTranslatef(pos_box_2, 2, -10)  # Traslacion. (derecha, arriba, profundida).
            #glRotatef(230, 0,0,1)
            glScalef(1.6,1.6,1.6)
        
            glVertexPointer(3, GL_FLOAT, 0, obj_box.vertFaces)         
            glNormalPointer(GL_FLOAT, 0, obj_box.normalFaces)           
            glTexCoordPointer(2, GL_FLOAT, 0, obj_box.texturesFaces)

            glBindTexture(GL_TEXTURE_2D, textura.box)                  
            glDrawArrays(GL_TRIANGLES, 0, len(obj_box.vertFaces)*3)     

            glPopMatrix()

            #---------------------------------------------------------------------------------------

            #   HUETEOTL

            glPushMatrix()
    
#            glTranslatef(-1, -0.6, -2)  # Traslacion. (derecha, arriba, profundida).
            glTranslatef(-1, -0.4, -2)  # Traslacion. (derecha, arriba, profundida).
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
    
            glTranslatef(-1, -0.4, -2)  # Traslacion. (derecha, arriba, profundida).
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
