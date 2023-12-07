import pygame
from auxiliar import *
from player import *

class Objeto(pygame.sprite.Sprite):
    def __init__(self,x,y,ancho,alto,dict_sprites=None,dict_nombre = None):
        """
        Es un constructor de una clase objeto(bloque) que inicializa varios atributos y variables.
        
        :param x: La coordenada x de la esquina superior izquierda del rectángulo del objeto
        :param y: El parámetro "y" representa la coordenada y de la esquina superior izquierda del
        rectángulo que define la posición del objeto
        :param ancho: El parámetro "ancho" representa el ancho del objeto o sprite
        :param alto: El parámetro "alto" representa la altura del objeto
        :param dict_sprites: El parámetro `dict_sprites` es un diccionario que contiene diferentes
        sprites para el objeto. Cada objeto está asociado con una clave específica en el diccionario
        :param dict_nombre: El parámetro `dict_nombre` es un diccionario que contiene los nombres de los
        sprites. Se utiliza para asociar un nombre con cada sprite en el diccionario `dict_sprites`
        """
        super().__init__()
        self.rect = pygame.Rect(x,y,ancho,alto)
        self.imagen = pygame.Surface((ancho,alto), pygame.SRCALPHA)
        self.ancho = ancho
        self.alto = alto        
        self.cont_animacion = 0
        self.mask = None
        self.sprites = dict_sprites
        self.nombre = dict_nombre

    def cargar_bloque(self,size, dir_1, dir_2,bloque_x,bloque_y):
        """
        El metodo `cargar_bloque` carga una imagen, crea una superficie y devuelve una versión escalada
        de la superficie.
        
        :param size: El parámetro de tamaño representa el ancho y alto de la superficie que se creará
        para contener la imagen. Determina el tamaño de la superficie y el tamaño del rectángulo que se
        utilizará para aplicar la imagen a la superficie
        :param dir_1: El parámetro `dir_1` es una cadena que representa el primer directorio en la ruta
        del archivo donde se encuentra la imagen
        :param dir_2: El parámetro "dir_2" es una cadena que representa el directorio o carpeta donde se
        encuentra el archivo de imagen. Se utiliza para construir la ruta del archivo para cargar la
        imagen
        :param bloque_x: El parámetro "bloque_x" representa la coordenada x de la esquina superior
        izquierda del bloque en la superficie
        :param bloque_y: El parámetro "bloque_y" representa la coordenada y de la esquina superior
        izquierda del bloque en la superficie
        :return: una versión ampliada de la superficie que se creó.
        """
        ruta = join("Juego\\assets", dir_1, dir_2)
        imagen = pygame.image.load(ruta).convert_alpha()
        superficie = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        rect = pygame.Rect(bloque_x,bloque_y,size,size) 
        superficie.blit(imagen, (0,0), rect)
        return pygame.transform.scale2x(superficie)
    
    def cargar_imagen_bloque(self,tamaño,dir_1,dir_2,bloque_x,bloque_y):
        """
        El metodo carga un bloque de imagen y establece su máscara.
        
        :param tama: El parámetro "tamaño" representa el tamaño de la imagen del bloque
        :param dir_1: Es probable que el parámetro "dir_1" sea una cadena que represente el directorio o
        la ruta al primer archivo de imagen del bloque
        :param dir_2: Es probable que el parámetro "dir_2" sea un directorio o ruta al segundo archivo
        de imagen que se utiliza para crear el bloque. Se utiliza en El metodo "cargar_bloque" para
        cargar el segundo archivo de imagen y crear el bloque
        :param bloque_x: El parámetro "bloque_x" representa la coordenada x de la posición del bloque en
        la pantalla
        :param bloque_y: El parámetro "bloque_y" representa la coordenada y del bloque en la imagen
        """
        bloque = self.cargar_bloque(tamaño,dir_1,dir_2,bloque_x,bloque_y)
        self.imagen.blit(bloque, (0,0))
        self.mask = pygame.mask.from_surface(self.imagen)
    
    def cargar_bloque_fruta(self,size, dir_1, dir_2):
        """
        El metodo carga una imagen, la recorta a un tamaño específico y luego la amplía en un factor de
        2.
        
        :param size: El parámetro de tamaño representa el tamaño deseado (ancho y alto) de la imagen
        cargada
        :param dir_1: El parámetro "dir_1" es una cadena que representa el primer directorio en la ruta
        del archivo donde se encuentra la imagen
        :param dir_2: El parámetro "dir_2" es una cadena que representa el directorio o carpeta donde se
        encuentra la imagen de la fruta. Se utiliza para construir la ruta del archivo para cargar la
        imagen
        :return: una versión ampliada de la imagen que se ha cargado y recortado.
        """
        ruta = join("Juego\\assets", dir_1, dir_2)
        imagen = pygame.image.load(ruta).convert_alpha()
        imagen_recortada = pygame.Surface((size, size), pygame.SRCALPHA, 32)
        imagen_recortada.blit(imagen, (0, 0))
        return pygame.transform.scale2x(imagen_recortada)
        
    def cargar_imagen_fruta(self,tamaño,dir_1,dir_2):
        """
        El metodo "cargar_imagen_fruta" carga una imagen de una fruta y le aplica una máscara.
        
        :param tama: El parámetro "tamaño" representa el tamaño de la imagen de la fruta
        :param dir_1: El parámetro "dir_1" es el directorio o ruta al primer archivo de imagen de la
        fruta
        :param dir_2: Es probable que el parámetro "dir_2" sea un directorio o ruta al archivo de imagen
        de la fruta. Se utiliza para cargar la imagen de la fruta y mostrarla en pantalla
        """
        fruta = self.cargar_bloque_fruta(tamaño,dir_1,dir_2)
        self.imagen.blit(fruta, (0,0))
        self.mask = pygame.mask.from_surface(self.imagen)

    def dibujar(self,pantalla:pygame.surface.Surface):
        """
        El metodo "dibujar" toma una superficie de pygame como entrada y transfiere la imagen a la
        superficie en las coordenadas especificadas.
        
        :param pantalla: El parámetro "pantalla" es un objeto de superficie de pygame que representa la
        pantalla o ventana donde se dibujará la imagen
        :type pantalla: pygame.surface.Surface
        """
        pantalla.blit(self.imagen, (self.rect.x, self.rect.y))
