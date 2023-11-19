import pygame
from auxiliar import *
from player import *

class Objeto(pygame.sprite.Sprite):
    def __init__(self,x,y,ancho,alto,dict_sprites=None,dict_nombre = None):
        super().__init__()
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.imagen = pygame.Surface((ancho,alto), pygame.SRCALPHA)
        self.ancho = ancho
        self.alto = alto        
        self.cont_animacion = 0
        self.mask = None
        self.sprites = dict_sprites
        self.nombre = dict_nombre

    def cargar_bloque(self,size, dir_1, dir_2):
        ruta = join("Juego\\assets", dir_1, dir_2)
        imagen = pygame.image.load(ruta).convert_alpha()
        superficie = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        #Por defecto por cada 96 de X me muevo por cada bloque de la hoja.
        #Por cada 96 + 48 el bloque mas chico imcompleto, y por cada 63-65 de Y cambio de bloque arriba y abajo.
        rect = pygame.Rect(96,0,size,size) 
        superficie.blit(imagen, (0,0), rect)
        return pygame.transform.scale2x(superficie)
        
    def cargar_imagen(self,tamaño,dir_1,dir_2):
        bloque = self.cargar_bloque(tamaño,dir_1,dir_2)
        self.imagen.blit(bloque, (0,0))
        self.mask = pygame.mask.from_surface(self.imagen)

    def dibujar(self,pantalla:pygame.surface.Surface):
        pantalla.blit(self.imagen, (self.rect.x, self.rect.y))
