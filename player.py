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
        self.max_vidas = 3
        self.pos_inicial = (100,ALTURA_SUELO)

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

        if self.vel_y > 0 and self.rect.bottom >= ALTO_VENTANA:
            self.vel_y = 0
            self.rect.bottom = ALTO_VENTANA
        elif self.vel_y < 0 and self.rect.top <= 0:
            self.vel_y = 0
            self.rect.top = 0

    def colision_piso(self,jugador,objetos_colision:list):

        objetos_colisionados = []

        for obj in objetos_colision:
            if pygame.sprite.collide_rect(jugador,obj):
                if self.rect.bottom >= obj.rect.top:
                    self.rect.bottom = obj.rect.top
                    self.vel_y = 0
                    self.contador_salto = 0
                    print("Estoy en el if de colision_piso")
            objetos_colisionados.append(obj)
            
        return objetos_colisionados

    def colision_plataformas(self, jugador, objetos_colision: list):

        objetos_colisionados = []

        for obj in objetos_colision:
            if pygame.sprite.collide_rect(jugador, obj):
                # Colisión desde abajo
                if jugador.rect.bottom > obj.rect.top and jugador.rect.top < obj.rect.top:
                    jugador.rect.bottom = obj.rect.top
                    jugador.vel_y = 0
                    self.contador_salto = 0
                    print("Estoy en el if de colision_plataformas (colisión desde arriba)")
                # Colisión desde arriba
                elif jugador.rect.top < obj.rect.bottom and jugador.rect.bottom > obj.rect.bottom:
                    jugador.rect.top = obj.rect.bottom
                    jugador.vel_y = 0
                    print("Estoy en el if de colision_plataformas (colisión desde abajo)")
                # Colisión desde la derecha
                elif jugador.rect.right > obj.rect.left and jugador.rect.left < obj.rect.left:
                    jugador.rect.right = obj.rect.left
                    jugador.vel_x = 0
                    jugador.vel_y = 0
                    print("Estoy en el if de colision_plataformas (colisión desde la derecha)")
                # Colisión desde la izquierda
                elif jugador.rect.left < obj.rect.right and jugador.rect.right > obj.rect.right:
                    jugador.rect.left = obj.rect.right
                    jugador.vel_x = 0
                    jugador.vel_y = 0
                    print("Estoy en el if de colision_plataformas (colisión desde la izquierda)")

            objetos_colisionados.append(obj)

        return objetos_colisionados


    def colision_fruta(self,player,consumibles):

        for i in range(len(consumibles)):
            obj = consumibles[i]
            if pygame.sprite.collide_mask(player, obj):
                consumibles.pop(i)
                player.puntos += 100
                break

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

    def chocar_cabeza(self):
        self.cont = 0
        self.vel_y *= -1


    def mover_jugador(self):

        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.moverse_izquierda(VELOCIDAD)
        elif keys[pygame.K_RIGHT]:
            self.moverse_derecha(VELOCIDAD)

        if self.rect.y >= ALTURA_SUELO:
            self.aterrizar()

        # def actualizar(self,fps,pantalla:pygame.surface.Surface,player,obj:list):


    def actualizar(self,fps,pantalla:pygame.surface.Surface,player,obj:list,obj_2:list,frutas:list,obj_3:list,obj_4:list,obj_5):
        self.mover_jugador()
        self.vel_y += min(1, (self.contador_caida / fps) * GRAVEDAD)
        self.moverse(self.vel_x, self.vel_y)  

        self.contador_caida += 1
        self.actualizar_animacion()
        self.actualizar_rect()
        self.definir_limite_pantalla()
        self.colision_piso(player,obj)
        self.colision_plataformas(player,obj_2)
        self.colision_plataformas(player,obj_3)
        self.colision_plataformas(player,obj_4)
        self.colision_fruta(player,frutas)
        self.colision_fruta(player,obj_5)
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
