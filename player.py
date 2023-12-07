import pygame
import random as random
from auxiliar import *
from constantes import *
from bullet import *



class Jugador(pygame.sprite.Sprite):
    """
    La clase "Jugador" representa un personaje jugador en un juego, con atributos como posición,
    velocidad, sprites, puntos, vidas y un grupo de balas.
    """    
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
        self.grupo_balas = pygame.sprite.Group()
    

    def moverse(self, delta_x, delta_y):
        """
        El metodo mueve un objeto una cantidad determinada en las direcciones xey.
        
        :param delta_x: La cantidad que el objeto debe moverse horizontalmente
        :param delta_y: El parámetro `delta_y` representa la cantidad que el objeto debe moverse
        verticalmente. Determina el cambio en la coordenada y de la posición del objeto
        """
        self.rect.x += delta_x
        self.rect.y += delta_y

    def moverse_izquierda(self, velocidad):
        """
        El metodo "moverse_izquierda" establece la velocidad horizontal en un valor negativo y
        actualiza las variables de dirección y animación si la dirección actual aún no es "izquierda".
        
        :param velocidad: El parámetro "velocidad" representa la velocidad a la que el objeto se moverá
        hacia la izquierda
        """
        self.vel_x = -velocidad
        if self.direccion != "izquierda":
            self.direccion = "izquierda"
            self.cont_animacion = 0

    def moverse_derecha(self, velocidad):
        """
        El metodo "moverse_derecha" establece la velocidad de un objeto para moverse hacia la derecha y
        actualiza la dirección y el contador de animación si es necesario.
        
        :param velocidad: El parámetro "velocidad" representa la velocidad a la que el objeto se moverá
        hacia la derecha
        """
        self.vel_x = velocidad
        if self.direccion != "derecha":
            self.direccion = "derecha"
            self.cont_animacion = 0

    def definir_limite_pantalla(self):
        """
        El metodo define los límites de la pantalla para un objeto en movimiento.
        """

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

    def crear_bala(self):
        """
        El metodo "crear_bala" crea un objeto de viñeta con una dirección específica basada en la
        dirección actual del objeto.
        :return: El código devuelve una instancia de la clase Bullet con parámetros específicos
        dependiendo del valor del atributo "direccion".
        """
        if self.direccion == "izquierda":
            return Bullet(self.rect.centerx, self.rect.centery, "derecha",True)
        else:
            return Bullet(self.rect.centerx, self.rect.centery, "izquierda",True)
        
    def disparar_bala(self):
        """
        El metodo "disparar_bala" crea un objeto viñeta y lo agrega a un grupo de viñetas.
        """
        bala = self.crear_bala()
        self.grupo_balas.add(bala)

    def colision_balas(self,lista_enemigos):
        """
        El metodo comprueba si hay colisiones entre balas y enemigos, resta una vida al enemigo y añade
        10 puntos a la puntuación del jugador.
        
        :param lista_enemigos: El parámetro "lista_enemigos" es una lista que contiene todos los objetos
        enemigos del juego
        """

        for enemigo in lista_enemigos:
            if pygame.sprite.spritecollide(enemigo, self.grupo_balas, True):
                enemigo.vidas -= 1
                self.puntos += 10

    def colision_piso(self,jugador,objetos_colision:list):
        """
        El metodo comprueba si hay colisiones entre el reproductor y una lista de objetos y devuelve
        una lista de los objetos con los que colisionaron.
        
        :param jugador: El parámetro "jugador" representa el objeto jugador que choca con otros objetos
        :param objetos_colision: El parámetro "objetos_colision" es una lista de objetos con los que el
        "jugador" puede potencialmente chocar
        :type objetos_colision: list
        :return: una lista de objetos con los que ha chocado el jugador.
        """

        objetos_colisionados = []

        for obj in objetos_colision:
            if pygame.sprite.collide_rect(jugador,obj):
                if self.rect.bottom >= obj.rect.top:
                    self.rect.bottom = obj.rect.top
                    self.vel_y = 0
                    self.contador_salto = 0
            objetos_colisionados.append(obj)
            
        return objetos_colisionados

    def colision_plataformas(self, jugador, objetos_colision: list):
        """
        El metodo comprueba si hay colisiones entre un jugador y una lista de objetos y actualiza la
        posición y velocidad del jugador en consecuencia.
        
        :param jugador: El parámetro "jugador" representa el objeto jugador o sprite que está chocando
        con las plataformas
        :param objetos_colision: El parámetro "objetos_colision" es una lista de objetos que
        potencialmente pueden colisionar con el objeto "jugador"
        :type objetos_colision: list
        :return: una lista de objetos con los que ha chocado el jugador.
        """

        objetos_colisionados = []

        for obj in objetos_colision:
            if pygame.sprite.collide_rect(jugador, obj):
                if jugador.rect.bottom > obj.rect.top and jugador.rect.top < obj.rect.top:
                    jugador.rect.bottom = obj.rect.top
                    jugador.vel_y = 0
                    self.contador_salto = 0
                    # print("colisión desde abajo")
                elif jugador.rect.top < obj.rect.bottom and jugador.rect.bottom > obj.rect.bottom:
                    jugador.rect.top = obj.rect.bottom
                    jugador.vel_y = 0
                    # print("colisión desde arriba")
                elif jugador.rect.right > obj.rect.left and jugador.rect.left < obj.rect.left:
                    jugador.rect.right = obj.rect.left
                    jugador.vel_x = 0
                    jugador.vel_y = 0
                    # print("colisión desde la derecha")
                elif jugador.rect.left < obj.rect.right and jugador.rect.right > obj.rect.right:
                    jugador.rect.left = obj.rect.right
                    jugador.vel_x = 0
                    jugador.vel_y = 0
                    # print("colisión desde la izquierda")

            objetos_colisionados.append(obj)

        return objetos_colisionados


    def colision_fruta(self,player,consumibles):
        """
        El metodo comprueba si hay colisiones entre un jugador y los consumibles y, si hay una
        colisión, elimina el consumible, aumenta los puntos del jugador en 100 y deja de comprobar si
        hay más colisiones.
        
        :param player: El parámetro "jugador" es un objeto que representa el personaje del jugador en el
        juego. Probablemente sea una instancia de una clase que tiene atributos y métodos relacionados
        con la posición, el movimiento y otras propiedades del jugador
        :param consumibles: El parámetro "consumibles" es una lista de objetos que representan elementos
        consumibles del juego
        """

        for i in range(len(consumibles)):
            obj = consumibles[i]
            if pygame.sprite.collide_mask(player, obj):
                consumibles.pop(i)
                player.puntos += 100
                break

    def saltar(self):
        """
        El metodo "saltar" disminuye la velocidad vertical de un objeto, restablece los contadores de
        animación y actualiza los contadores de saltos y caídas.
        """
        self.vel_y -= GRAVEDAD * 8
        self.cont_animacion = 0
        self.contador_salto += 1
        if self.contador_salto == 1:
            self.contador_caida = 0

    def aterrizar(self):
        """
        El metodo "aterrizar" pone a cero la velocidad vertical, el contador de saltos y el contador de
        caídas.
        """
        self.vel_y = 0
        self.contador_salto = 0
        self.contador_caida = 0

    def chocar_cabeza(self):
        """
        El metodo "chocar_cabeza" pone la variable "cont" a 0 e invierte el signo de la variable
        "vel_y".
        """
        self.cont = 0
        self.vel_y *= -1


    def mover_jugador(self):
        """
        El metodo "mover_jugador" mueve el personaje del jugador hacia la izquierda o hacia la derecha
        según la entrada del teclado y hace que el personaje aterrice en el suelo si está por debajo de
        cierta altura.
        """

        keys = pygame.key.get_pressed()
        self.vel_x = 0

        if keys[pygame.K_LEFT]:
            self.moverse_izquierda(VELOCIDAD)
        elif keys[pygame.K_RIGHT]:
            self.moverse_derecha(VELOCIDAD)

        if self.rect.y >= ALTURA_SUELO:
            self.aterrizar()


    def actualizar(self,fps,pantalla:pygame.surface.Surface,player,obj:list,obj_2:list,frutas:list,obj_3:list,obj_4:list,obj_5,lista_enemigos):
        """
        El metodo actualiza el estado del juego moviendo al jugador, actualizando animaciones,
        verificando colisiones con plataformas, balas y frutas, y dibujando el juego en la pantalla.
        
        :param fps: El parámetro "fps" representa los fotogramas por segundo del juego. Se utiliza para
        calcular la gravedad y la velocidad del jugador
        :param pantalla: El parámetro "pantalla" es un objeto pygame.surface.Surface, que representa la
        pantalla o ventana del juego donde se dibujarán los objetos del juego
        :type pantalla: pygame.surface.Surface
        :param player: El parámetro del jugador es una instancia del objeto del jugador en el juego.
        Representa el personaje principal controlado por el jugador
        :param obj: El parámetro "obj" es una lista que representa un grupo de objetos o entidades del
        juego. Se utiliza para la detección de colisiones y la interacción con el personaje del jugador
        :type obj: list
        :param obj_2: obj_2 es una lista de plataformas con las que el jugador puede chocar
        :type obj_2: list
        :param frutas: El parámetro "frutas" es una lista que contiene los objetos que representan
        frutas en el juego
        :type frutas: list
        :param obj_3: El parámetro "obj_3" es una lista que representa un grupo de plataformas u objetos
        con los que el jugador puede chocar
        :type obj_3: list
        :param obj_4: El parámetro "obj_4" parece ser una lista que representa un conjunto de
        plataformas u obstáculos con los que el jugador puede chocar
        :type obj_4: list
        :param obj_5: El parámetro "obj_5" parece representar una lista de objetos relacionados con
        frutas
        :param lista_enemigos: El parámetro "lista_enemigos" es una lista que contiene los enemigos del
        juego
        """
        self.mover_jugador()
        self.vel_y += min(1, (self.contador_caida / fps) * GRAVEDAD)
        self.moverse(self.vel_x, self.vel_y)  
        self.contador_caida += 1
        self.actualizar_animacion()
        self.actualizar_rect()
        self.grupo_balas.draw(pantalla)
        self.grupo_balas.update()
        self.definir_limite_pantalla()
        self.colision_piso(player,obj)
        self.colision_plataformas(player,obj_2)
        self.colision_plataformas(player,obj_3)
        self.colision_plataformas(player,obj_4)
        self.colision_balas(lista_enemigos)
        self.colision_fruta(player,frutas)
        self.colision_fruta(player,obj_5)
        self.dibujar(pantalla)

        

    def actualizar_animacion(self):
        """
        El metodo "actualizar_animacion" actualiza el cuadro de animación actual en función de la
        velocidad y el movimiento del jugador.
        """
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
        """
        El metodo actualiza la posición y la máscara del rectángulo de un objeto.
        """
        self.rect = self.sprite.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.sprite)

    def dibujar(self, pantalla:pygame.surface.Surface):
        """
        El metodo "dibujar" toma una superficie de pygame como entrada y envía el sprite a la
        superficie en las coordenadas especificadas.
        
        :param pantalla: El parámetro "pantalla" es un objeto pygame.surface.Surface, que representa la
        superficie donde se dibujará el sprite
        :type pantalla: pygame.surface.Surface
        """
        pantalla.blit(self.sprite, (self.rect.x, self.rect.y))
