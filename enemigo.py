import pygame
from constantes import *
from player import *

class Enemigo(pygame.sprite.Sprite):      
    def __init__(self,x,y,ancho,alto,sprites:dict):
        super().__init__()
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.vel_x = 3
        self.vel_y = 0
        self.mask = None
        self.direccion = "derecha"
        self.cont_animacion = 0
        self.contador_caida = 0
        self.contador = 0
        self.sprites = sprites

    def moverse(self, delta_x):
        if self.direccion == "izquierda":
            self.rect.x += delta_x
            self.contador += 1
            if self.contador == 150:
                self.direccion = "derecha"
                self.contador = 0
        elif self.direccion == "derecha":
            self.rect.x -= delta_x
            self.contador += 1
            if self.contador == 150:
                self.direccion = "izquierda"
                self.contador = 0

    def definir_limite_pantalla(self,delta_x):

        if self.vel_x > 0 and self.rect.right >= ANCHO_VENTANA:
            self.vel_x = -delta_x
            self.rect.right = ANCHO_VENTANA
            # self.direccion = "izquierda"
        elif self.vel_x < 0 and self.rect.left <= 0:
            self.vel_x = delta_x
            self.rect.left = 0
            # self.direccion = "derecha"

    def colision_piso(self,enemigo,objetos_colision:list):

        objetos_colisionados = []

        for obj in objetos_colision:
            if pygame.sprite.collide_rect(enemigo,obj):
                if self.rect.bottom >= obj.rect.top:
                    self.rect.bottom = obj.rect.top
                    self.vel_y = 0
                    self.contador_salto = 0
            objetos_colisionados.append(obj)
            
        return objetos_colisionados
    
    def colision_player(self,enemigo,player):

        self.golpes_enemigo = False

        if pygame.sprite.collide_mask(enemigo, player):
            if (self.rect.left <= player.rect.right) or (self.rect.right >= player.rect.left):
                if player.vidas > 0:
                    self.golpes_enemigo = True
                    player.vidas -= 1 

            if self.golpes_enemigo:
                self.golpes_enemigo = False


    def actualizar(self,pantalla:pygame.surface.Surface,enemigo,obj:list,player:Jugador):
        self.moverse(self.vel_x)
        self.actualizar_animacion()
        self.actualizar_rect()
        self.definir_limite_pantalla(self.vel_x)
        self.colision_piso(enemigo,obj)
        self.colision_player(enemigo,player)
        self.dibujar(pantalla)
        
    
    def actualizar_animacion(self):
        anim_actual = "idle"
        if self.vel_x != 0:
            anim_actual = "run"

        nombre_anim_actual = anim_actual + "_" + self.direccion
        sprites = self.sprites[nombre_anim_actual]
        indice_sprite = (self.cont_animacion // ANIMACION_DELAY) % len(sprites)
        self.sprite = sprites[indice_sprite]
        self.cont_animacion += 1
    
    def actualizar_rect(self):
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def dibujar(self, win):
        win.blit(self.sprite, (self.rect.x, self.rect.y))