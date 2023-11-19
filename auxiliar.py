import pygame
import os
from os import listdir
from os.path import isfile, join

class Auxiliar:

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
        return [pygame.transform.flip(sprite, True, False) for sprite in sprites]