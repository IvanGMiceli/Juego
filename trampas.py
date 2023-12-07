import pygame
from auxiliar import *
from player import *
from plataforma import Objeto

class Sierra(Objeto):
    """
    La clase Sierra es una subclase de la clase Objeto y representa una trampa de sierra con atributos y
    métodos específicos.
    """
    def __init__(self, x, y, ancho, alto):
        super().__init__(x, y, ancho, alto,"saw")
        self.trampa = Auxiliar.cargar_sprite_sheets("Traps","Saw",ancho,alto)
        self.imagen = self.trampa["off"][0]
        self.mask = pygame.mask.from_surface(self.imagen)
        self.cont_animacion = 0
        self.nombre_animacion = "off"

    def on(self):
        """
        El metodo establece el valor de la variable "nombre_animacion" en "on".
        """
        self.nombre_animacion = "on"

    def off(self):
        """
        El metodo anterior establece el atributo "nombre_animacion" en "off".
        """
        self.nombre_animacion = "off"

    def loop_animacion(self):
        """
        El metodo `loop_animacion` actualiza la imagen y animación de un sprite en un bucle.
        """
        sprites = self.trampa[self.nombre_animacion]
        indice_sprite = (self.cont_animacion // ANIMACION_DELAY) % len(sprites)
        self.imagen = sprites[indice_sprite]
        self.cont_animacion += 1

        self.rect = self.imagen.get_rect(topleft=(self.rect.x, self.rect.y))
        self.mask = pygame.mask.from_surface(self.imagen)

        if self.cont_animacion // ANIMACION_DELAY > len(sprites):
            self.cont_animacion = 0

    def colision_trampa(self,trampa,player):
        """
        El metodo comprueba si hay una colisión entre una trampa y un objeto de jugador, y si hay una
        colisión y al jugador le quedan vidas, restablece la posición del jugador y disminuye su
        recuento de vidas.
        
        :param trampa: El parámetro "trampa" es un objeto sprite que representa una trampa en el juego.
        Se utiliza para comprobar si hay colisión con el jugador
        :param player: El parámetro del reproductor es una instancia de un objeto de reproductor. Se
        utiliza para acceder y modificar los atributos del jugador, como su posición y número de vidas
        """

        if pygame.sprite.collide_mask(trampa, player):
            if player.vidas > 0:
                player.rect.x = 500
                player.rect.y = 600
                player.vidas -= 1

    def actualizar(self,pantalla,trampa,player):
        """
        El metodo "actualizar" actualiza la pantalla, activa la animación y comprueba si hay colisión
        con una trampa y el jugador.
        
        :param pantalla: El parámetro "pantalla" representa la pantalla o display donde se está
        renderizando el juego
        :param trampa: Es probable que el parámetro "trampa" se refiera a un objeto o entidad trampa en
        el juego. Podría usarse para comprobar si hay colisiones entre el jugador y la trampa, o para
        actualizar el estado de la trampa durante el juego
        :param player: El parámetro "jugador" es un objeto que representa el personaje del jugador en el
        juego
        """
        self.dibujar(pantalla)
        self.on()
        self.loop_animacion()
        self.colision_trampa(trampa,player)

def crear_sierras(coordenadas):
    """
    La funcion "crear_sierras" toma una lista de coordenadas y crea una lista de objetos Sierra con esas
    coordenadas.
    
    :param coordenadas: El parámetro "coordenadas" es una lista de listas. Cada lista interna representa
    las coordenadas de una sierra (cordillera) y contiene cuatro elementos: coord[0] representa la
    coordenada x del punto inicial de la sierra, coord[1] representa la coordenada y del
    :return: una lista de objetos de Sierra.
    """
    sierras = []
    for coord in coordenadas:
        sierra = Sierra(coord[0], coord[1], coord[2], coord[3])
        sierras.append(sierra)
    return sierras