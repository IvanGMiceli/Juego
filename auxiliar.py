import pygame
# import os
from os import listdir
from os.path import isfile, join
import json
import sqlite3

json_de_config = "./configs/config.json"

class Auxiliar:
    """
    La función `flip` toma una lista de sprites y devuelve una nueva lista con cada sprite volteado
    horizontalmente usando la función `pygame.transform.flip()`.
    
    :param sprites: Se espera que el parámetro "sprites" sea una lista de objetos Surface de pygame.
    Estos objetos de Superficie representan cuadros o imágenes individuales que se pueden mostrar en la
    pantalla. La función "flip" toma esta lista de sprites y aplica la función pygame.transform.flip() a
    cada sprite. Esta función voltea el objeto horizontalmente
    """

    @staticmethod
    def cargar_sprite_sheets(dir1, dir2, width, height, direccion=False):
        ruta = join("Juego\\assets", dir1, dir2)
        imagenes = [f for f in listdir(ruta) if isfile(join(ruta, f))]

        all_sprites = {}

        for imagen in imagenes:
            sprite_sheet = pygame.image.load(join(ruta, imagen)).convert_alpha()

            lista_sprites = []
            for i in range(sprite_sheet.get_width() // width):
                superficie = pygame.Surface((width, height), pygame.SRCALPHA, 32)
                rect = pygame.Rect(i * width, 0, width, height)
                superficie.blit(sprite_sheet, (0, 0), rect)
                lista_sprites.append(pygame.transform.scale2x(superficie))

            if direccion:
                all_sprites[imagen.replace(".png", "") + "_derecha"] = lista_sprites
                all_sprites[imagen.replace(".png", "") + "_izquierda"] = flip(lista_sprites)
            else:
                all_sprites[imagen.replace(".png", "")] = lista_sprites

        return all_sprites
    
def flip(sprites):
    """
    La función "voltear" toma una lista de sprites y devuelve una nueva lista con cada sprite volteado
    horizontalmente.
    
    :param sprites: Se espera que el parámetro "sprites" sea una lista de objetos Surface de pygame.
    Estos objetos de Superficie representan cuadros o imágenes individuales que se pueden mostrar en la
    pantalla. La función "flip" toma esta lista de sprites y aplica la función pygame.transform.flip() a
    cada sprite. Esta función voltea el objeto horizontalmente
    :return: una lista de sprites que se han volteado horizontalmente usando la función
    pygame.transform.flip().
    """
    return [pygame.transform.flip(sprite, True, False) for sprite in sprites]

def open_configs() -> dict:
    """
    La función `open_configs()` lee y devuelve el contenido de un archivo JSON.
    :return: un diccionario.
    """
    with open(json_de_config, 'r', encoding='utf-8') as config:
        return json.load(config)
    
def crear_tabla_posiciones(nombre,jugador):
    """
    Esta función crea una tabla llamada "posiciones" en una base de datos SQLite e inserta nombre y puntaje del player
    """

    nombre = nombre
    puntaje = jugador.puntos

    with sqlite3.connect("Juego\posiciones.db") as conexion:
        try:
            sentencia = '''CREATE TABLE IF NOT EXISTS posiciones
                        (
                            nombre TEXT,
                            puntaje INTEGER
                        )
                        '''
            conexion.execute(sentencia)

            conexion.execute("INSERT INTO posiciones(nombre, puntaje) VALUES (?, ?)", (nombre, puntaje))

            conexion.commit()           
            print("Se creó o actualizó la tabla de posiciones")

        except sqlite3.OperationalError as e:
            print(f"Error al crear o actualizar la tabla de posiciones: {e}")
