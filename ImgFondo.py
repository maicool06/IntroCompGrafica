#importamos librerias
import pygame
from pygame.locals import *

#iniciamos pygame
pygame.init()

#definimos constantes
pantalla = pygame.display.set_mode((640, 480))
pygame.display.set_caption('Titulo de ventana')

reloj = pygame.time.Clock()

#definimos funciones
def cargar_imagen(nombre,transparente=False):
    imagen = pygame.image.load("./Animaciones/Fondo.png")

    imagen = imagen.convert()
    if transparente:
        color = imagen.get_at((0,0))
        imagen.set_colorkey(color, RLEACCEL)
    return imagen

#Aqui es donde colocamos el fondo a la pantalla
fondo = cargar_imagen('datos/fondo.jpg')
pantalla.blit(fondo, (0, 0)) #es para esto que nos sirvio poner en una 
                             #variable los datos de la pantalla
pygame.display.flip()

#Bucle principal del juego
while 1:
 for event in pygame.event.get():
  if event.type == QUIT:
   pygame.quit()
   sys.exit()
  elif event.type == KEYDOWN:
   if event.type == K_ESCAPE:
    pygame.quit()
    sys.exit()

 pygame.display.update()
 reloj.tick(10)