import pygame
import random as random
import time
from constantes import *
from player import *
from bullet import *


class Enemigo(pygame.sprite.Sprite):
    """
    La clase Enemigo es una clase de sprite que representa a un enemigo en un juego, con atributos como
    posición, velocidad, dirección, animación, vidas y un grupo de balas.
    """     
    def __init__(self,x,y,ancho,alto,sprites:dict,direccion:str,vel_x = 0):
        super().__init__()
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.vel_x = vel_x
        self.vel_y = 0
        self.mask = None
        self.direccion = direccion
        self.cont_animacion = 0
        self.contador = 0
        self.sprites = sprites
        self.vidas = 1
        self.pos_inicial_enemiga = (1000,ALTURA_SUELO)
        self.grupo_balas = pygame.sprite.Group()

    def crear_bala(self):
        """
        El metodo "crear_bala" crea un objeto bala con una dirección específica basada en la
        dirección actual del objeto.
        :return: El código devuelve una instancia de la clase Bullet con los parámetros especificados.
        """
        if self.direccion == "derecha":
            return Bullet(self.rect.centerx, self.rect.centery, "derecha",True)
        else:
            return Bullet(self.rect.centerx, self.rect.centery, "izquierda",True)
        
    def disparar_bala(self):
        """
        El metodo "disparar_bala" agrega una nueva bala a un grupo de balas.
        """
        self.grupo_balas.add(self.crear_bala())

    def can_shoot(self) -> bool:
        """
        El metodo determina si un objeto puede disparar en función de una probabilidad, un número
        máximo de disparos y un intervalo de tiempo entre disparos.
        :return: un valor booleano. Devuelve Verdadero si se cumplen las condiciones para disparar (el
        número aleatorio generado es menor o igual que el porcentaje de disparo) y Falso en caso
        contrario.
        """
        self.porcentaje_disparo = 0.4
        self.contador_disparos = 0
        self.max_disparos = 1
        self.intervalo_disparo = 10

        if self.contador_disparos < self.max_disparos:
            if random.random() * 100 <= self.porcentaje_disparo:
                self.contador_disparos += 1
                return True
        else:
            time.sleep(self.intervalo_disparo)
            self.contador_disparos = 0
        return False
    
    def is_shooting(self) -> bool:
        """
        El metodo `is_shooting` devuelve un valor booleano que indica si el objeto puede disparar.
        :return: el resultado de la llamada al método `self.can_shoot()`.
        """
        return self.can_shoot()
    
    def definir_limite_pantalla(self):
        """
        El metodo define el límite de la pantalla para un objeto en movimiento según su dirección.
        """
        
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
        """
        El metodo busca colisiones entre un objeto enemigo y una lista de objetos, y si ocurre una
        colisión, ajusta la posición y velocidad del objeto enemigo.
        
        :param enemigo: El parámetro "enemigo" representa el objeto enemigo que choca con otros objetos
        :param objetos_colision: El parámetro "objetos_colision" es una lista de objetos que
        potencialmente pueden colisionar con el objeto "enemigo"
        :type objetos_colision: list
        :return: una lista de objetos con los que ha chocado el duende enemigo.
        """

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
        """
        El metodo comprueba la colisión entre un enemigo y un objeto de jugador en un juego y realiza
        diferentes acciones según la posición de la colisión.
        
        :param enemigo: El parámetro "enemigo" representa el objeto sprite enemigo en el juego. Se
        utiliza para comprobar si hay colisión con el objeto del jugador
        :param player: El parámetro "jugador" es un objeto que representa el personaje del jugador en el
        juego
        """

        if pygame.sprite.collide_rect(enemigo,player):
            if self.rect.top < player.rect.bottom and self.rect.bottom > player.rect.bottom:
                if player.vidas > 0 and self.vidas > 0:
                    self.rect.top = player.rect.bottom
                    self.rect.x = self.pos_inicial_enemiga[0]
                    self.rect.y = self.pos_inicial_enemiga[1]
                    self.vidas -= 1
                    player.puntos += 10                    
            elif self.rect.left < player.rect.right and self.rect.right > player.rect.right:
                if player.vidas > 0:
                    player.rect.x = player.pos_inicial[0]
                    player.rect.y = player.pos_inicial[1]
                    player.vidas -= 1
            elif self.rect.right > player.rect.left and self.rect.left < player.rect.left:
                if player.vidas > 0:
                    player.rect.x = player.pos_inicial[0]
                    player.rect.y = player.pos_inicial[1]
                    player.vidas -= 1
            elif self.rect.bottom > player.rect.top and self.rect.top < player.rect.top:
                if player.vidas > 0:
                    player.puntos = 0
    
    def colision_balas(self,player):
        """
        El metodo comprueba si hay colisiones entre el jugador y un grupo de balas, y si hay una
        colisión y al jugador le quedan vidas, restablece la posición del jugador y disminuye su
        recuento de vidas en 1.
        
        :param player: El parámetro "jugador" es una instancia de un objeto reproductor. Se utiliza para
        comprobar si hay colisión entre el jugador y las balas
        """
        if pygame.sprite.spritecollide(player, self.grupo_balas, True):
            if player.vidas > 0:
                player.rect.x = 500
                player.rect.y = 600
                player.vidas -= 1

    def actualizar(self,pantalla:pygame.surface.Surface,enemigo,obj:list,player:Jugador):
        """
        El metodo actualiza la animación, posición y colisiones de un personaje en un juego y luego lo
        dibuja en la pantalla junto con las balas disparadas.
        
        :param pantalla: El parámetro "pantalla" es de tipo pygame.surface.Surface y representa la
        superficie donde se está mostrando el juego
        :type pantalla: pygame.surface.Surface
        :param enemigo: Es probable que el parámetro "enemigo" se refiera a un objeto enemigo o a un
        grupo de objetos enemigos en el juego. Se utiliza para la detección de colisiones y la
        interacción con el jugador
        :param obj: El parámetro "obj" es una lista que contiene objetos con los que el jugador puede
        chocar
        :type obj: list
        :param player: El parámetro "jugador" es una instancia de la clase "Jugador"
        :type player: Jugador
        """
        self.actualizar_animacion()
        self.actualizar_rect()
        self.definir_limite_pantalla()
        self.colision_piso(enemigo,obj)
        self.colision_player(enemigo,player)
        self.colision_balas(player)
        self.dibujar(pantalla)
        self.grupo_balas.draw(pantalla)
        self.grupo_balas.update()
        if self.is_shooting():
            self.disparar_bala()
    
    def actualizar_animacion(self):
        """
        El metodo "actualizar_animacion" actualiza la animación de un sprite en función de su velocidad
        y dirección actuales.
        """
        anim_actual = "idle"
        if self.vel_x != 0:
            anim_actual = "run"

        nombre_anim_actual = anim_actual + "_" + self.direccion
        sprites = self.sprites[nombre_anim_actual]
        indice_sprite = (self.cont_animacion // ANIMACION_DELAY) % len(sprites)
        self.sprite = sprites[indice_sprite]
        self.cont_animacion += 1
    
    def actualizar_rect(self):
        """
        El metodo actualiza la posición y la máscara del rectángulo de un objeto.
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def dibujar(self, win):
        """
        El metodo "dibujar" toma una ventana como argumento y dibuja el sprite en la posición
        especificada en la ventana.
        
        :param win: El parámetro "win" es la superficie o ventana donde se dibujará el sprite
        """
        win.blit(self.sprite, (self.rect.x, self.rect.y))