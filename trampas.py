import pygame
from auxiliar import *
from player import *
from plataforma import Objeto

class Sierra(Objeto):
    def __init__(self, x, y, ancho, alto):
        super().__init__(x, y, ancho, alto,"saw")
        self.trampa = Auxiliar.cargar_sprite_sheets("Traps","Saw",ancho,alto)
        self.imagen = self.trampa["off"][0]
        self.mask = pygame.mask.from_surface(self.imagen)
        self.cont_animacion = 0
        self.nombre_animacion = "off"

    def on(self):
        self.nombre_animacion = "on"

    def off(self):
        self.nombre_animacion = "off"

    def loop_animacion(self):
        sprites = self.trampa[self.nombre_animacion]
        indice_sprite = (self.cont_animacion // ANIMACION_DELAY) % len(sprites)
        self.imagen = sprites[indice_sprite]
        self.cont_animacion += 1

        self.rect = self.imagen.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.imagen)

        if self.cont_animacion // ANIMACION_DELAY > len(sprites):
            self.cont_animacion = 0

    def colision_trampa(self,trampa,player):

        if pygame.sprite.collide_mask(trampa, player):
            if player.vidas > 0:
                player.rect.x = 500
                player.rect.y = 600
                player.vidas -= 1

    def actualizar(self,pantalla,trampa,player):
        self.dibujar(pantalla)
        self.on()
        self.loop_animacion()
        self.colision_trampa(trampa,player)

def crear_sierras(coordenadas):
        sierras = []
        for coord in coordenadas:
            sierra = Sierra(coord[0], coord[1], coord[2], coord[3])
            sierras.append(sierra)
        return sierras