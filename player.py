from auxiliar import Auxiliar
import pygame
from constantes import *


class Jugador(pygame.sprite.Sprite):      
    def __init__(self,x,y,ancho,alto,sprites:dict):
        super().__init__()
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.vel_x = 0
        self.vel_y = 0
        self.mask = None
        self.direccion = "izquierda"
        self.cont_animacion = 0
        self.contador_caida = 0
        self.contador_salto = 0
        self.sprites = sprites
        self.puntos = 0
        self.vidas = 3

    def moverse(self, delta_x, delta_y):
        self.rect.x += delta_x
        self.rect.y += delta_y

    def moverse_izquierda(self, velocidad):
        self.vel_x = -velocidad
        if self.direccion != "izquierda":
            self.direccion = "izquierda"
            self.cont_animacion = 0

    def moverse_derecha(self, velocidad):
        self.vel_x = velocidad
        if self.direccion != "derecha":
            self.direccion = "derecha"
            self.cont_animacion = 0

    def definir_limite_pantalla(self):

        if self.vel_x > 0 and self.rect.right >= ANCHO_VENTANA:
            self.vel_x = 0
            self.rect.right = ANCHO_VENTANA
        elif self.vel_x < 0 and self.rect.left <= 0:
            self.vel_x = 0
            self.rect.left = 0
    
        if self.rect.bottom >= ALTO_VENTANA - TAMAÑO_BLOQUE:
            self.rect.bottom = ALTO_VENTANA - TAMAÑO_BLOQUE
            self.vel_y = 0
            self.contador_salto = 0
        elif self.rect.top <= 0:  
            self.rect.top = 0
            self.vel_y = 0

    def saltar(self):
        self.vel_y -= GRAVEDAD * 8
        self.cont_animacion = 0
        self.contador_salto += 1
        if self.contador_salto == 1:
            self.contador_caida = 0

    def aterrizar(self):
        self.vel_y = 0
        self.contador_salto = 0
        self.contador_caida = 0

    def mover_jugador(self):

        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.moverse_izquierda(VELOCIDAD)
        elif keys[pygame.K_RIGHT]:
            self.moverse_derecha(VELOCIDAD)

        if self.rect.y >= ALTURA_SUELO:
            self.aterrizar()

    def actualizar(self,fps,pantalla:pygame.surface.Surface):
        self.mover_jugador()
        self.vel_y += min(1, (self.contador_caida / fps) * GRAVEDAD)
        self.moverse(self.vel_x, self.vel_y)  

        self.contador_caida += 1
        self.actualizar_animacion()
        self.actualizar_rect()
        self.definir_limite_pantalla()
        self.dibujar(pantalla)

    def actualizar_animacion(self):
        anim_actual = "idle"

        if self.vel_y < 0:
            if self.contador_salto == 1:
                anim_actual = "jump"
            elif self.contador_salto == 2:
                anim_actual = "double_jump"
        elif self.vel_y > GRAVEDAD * 2:
            anim_actual = "fall"
        elif self.vel_x != 0:
            anim_actual = "run"

        nombre_anim_actual = anim_actual + "_" + self.direccion
        sprites = self.sprites[nombre_anim_actual]
        indice_sprite = (self.cont_animacion // ANIMACION_DELAY) % len(sprites)
        self.sprite = sprites[indice_sprite]
        self.cont_animacion += 1

    def actualizar_rect(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def dibujar(self, pantalla:pygame.surface.Surface):
        pantalla.blit(self.sprite, (self.rect.x, self.rect.y))
