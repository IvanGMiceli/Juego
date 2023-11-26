import pygame
from constantes import *
from player import *

class Enemigo(pygame.sprite.Sprite):      
    def __init__(self,x,y,ancho,alto,sprites:dict):
        super().__init__()
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.vel_x = 2
        self.vel_y = 0
        self.mask = None
        self.direccion = "derecha"
        self.cont_animacion = 0
        self.contador_caida = 0
        self.contador = 0
        self.sprites = sprites
        self.vidas = 3
        self.pos_inicial_enemiga = (1000,ALTURA_SUELO)

    def definir_limite_pantalla(self):
        
        if self.direccion == "izquierda":
            if (self.rect.right + self.vel_x ) < ANCHO_VENTANA:
                self.rect.x += self.vel_x
            else:
                if self.rect.bottom + self.vel_x * 2 < ALTO_VENTANA:
                    self.rect.y += self.vel_x * 2
                    self.direccion = "derecha"
        else:
            if self.rect.left - self.vel_x > 0:
                self.rect.x -= self.vel_x
            else:
                if (self.rect.bottom + self.vel_x * 2) < ALTO_VENTANA:
                    self.rect.y += self.vel_x * 2
                    self.direccion = "izquierda"

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

        if pygame.sprite.collide_rect(enemigo,player):
            if self.rect.top < player.rect.bottom and self.rect.bottom > player.rect.bottom:
                if player.vidas > 0 and self.vidas > 0:
                    self.rect.top = player.rect.bottom
                    self.rect.x = self.pos_inicial_enemiga[0]
                    self.rect.y = self.pos_inicial_enemiga[1]
                    self.vidas -= 1
                    player.puntos += 1000                    
                    # print("Estoy pisando al sprite")
            elif self.rect.left < player.rect.right and self.rect.right > player.rect.right:
                if player.vidas > 0:
                    player.rect.x = player.pos_inicial[0]
                    player.rect.y = player.pos_inicial[1]
                    player.puntos = 0
                    # print("Estoy chocando a la izquierda del sprite")
            elif self.rect.right > player.rect.left and self.rect.left < player.rect.left:
                if player.vidas > 0:
                    # player.rect.x = player.pos_inicial[0]
                    # player.rect.y = player.pos_inicial[1]
                    player.puntos = 0
                    # print("Estoy chocando a la derecha del sprite")
            elif self.rect.bottom > player.rect.top and self.rect.top < player.rect.top:
                if player.vidas > 0:
                    player.puntos = 0
                    # print("Estoy pegando de abajo al sprite")

    def actualizar(self,pantalla:pygame.surface.Surface,enemigo,obj:list,player:Jugador):
        self.actualizar_animacion()
        self.actualizar_rect()
        self.definir_limite_pantalla()
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