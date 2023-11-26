import pygame
from player import *
from constantes import *
from auxiliar import *
from plataforma import *
from enemigo import *


def configurar_nivel_uno(ancho_ventana, alto_ventana, tamaño_bloque):

    stage_1_configs = {"fondo": pygame.transform.scale(pygame.image.load(r"Juego\assets\Maps background\Fondo uno.png"), (ANCHO_VENTANA, ALTO_VENTANA)),
        "lista_piso" : [],
        "lista_plataformas" : [],
        "lista_plataformas_dos" : [],
        "lista_plataformas_tres" : [],
        "lista_manzanas" : [],
        "lista_kiwis" : [],
        "lista_enemigos" : []}

    for i in range(13):
        bloque = Objeto(i * tamaño_bloque,alto_ventana - tamaño_bloque,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,0)
        stage_1_configs["lista_piso"].append(bloque)

    for i in range(0,5):
        bloque = Objeto(i * tamaño_bloque,alto_ventana - tamaño_bloque * 3,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,0)
        stage_1_configs["lista_plataformas"].append(bloque)

    for i in range(0,6):
        bloque = Objeto(ancho_ventana - (tamaño_bloque * i),alto_ventana - tamaño_bloque * 4,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,0)
        stage_1_configs["lista_plataformas_dos"].append(bloque)

    for i in range(0,5):
        bloque = Objeto(i * tamaño_bloque,alto_ventana - tamaño_bloque * 6,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,0)
        stage_1_configs["lista_plataformas_tres"].append(bloque)


    for i in range(5):
        fruta = Objeto((i * tamaño_bloque) + 1, alto_ventana - tamaño_bloque * 4, 450 , 70)
        fruta.cargar_imagen_fruta(35,"Items/Fruits", "Apple.png")
        stage_1_configs["lista_manzanas"].append(fruta)

    for i in range(6):
        fruta = Objeto(ancho_ventana - (tamaño_bloque * i), alto_ventana - tamaño_bloque * 5, 450 , 70)
        fruta.cargar_imagen_fruta(35,"Items/Fruits", "Kiwi.png")
        stage_1_configs["lista_kiwis"].append(fruta)

    for i in range(3):
        stage_1_configs["lista_enemigos"].append(Enemigo((i * 2) + i * 100, ALTURA_SUELO, 50, 50, Auxiliar.cargar_sprite_sheets("Enemies", "Chicken", 32, 34, True)))

    coordenadas_sierras = [
        (672, ALTO_VENTANA - TAMAÑO_BLOQUE - 40, 38, 38),
        (750, ALTO_VENTANA - TAMAÑO_BLOQUE - 40, 38, 38),
        (830, ALTO_VENTANA - TAMAÑO_BLOQUE - 40, 38, 38),
    ]

    stage_1_configs["coordenadas_sierras"] = coordenadas_sierras

    return stage_1_configs


def configurar_nivel_dos(ancho_ventana, alto_ventana, tamaño_bloque):

    stage_2_configs = {"fondo": pygame.transform.scale(pygame.image.load(r"Juego\assets\Maps background\Fondo dos.png"), (ANCHO_VENTANA, ALTO_VENTANA)),
        "lista_piso" : [],
        "lista_plataformas" : [],
        "lista_plataformas_dos" : [],
        "lista_plataformas_tres" : [],
        "lista_bananas" : [],
        "lista_cherries" : [],
        "lista_enemigos" : []}

    for i in range(13):
        bloque = Objeto(i * tamaño_bloque,alto_ventana - tamaño_bloque,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,64)
        stage_2_configs["lista_piso"].append(bloque)

    for i in range(0,5):
        bloque = Objeto(i * tamaño_bloque,alto_ventana - tamaño_bloque * 3,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,64)
        stage_2_configs["lista_plataformas"].append(bloque)

    for i in range(0,6):
        bloque = Objeto(ancho_ventana - (tamaño_bloque * i),alto_ventana - tamaño_bloque * 4,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,64)
        stage_2_configs["lista_plataformas_dos"].append(bloque)

    for i in range(0,5):
        bloque = Objeto(i * tamaño_bloque,alto_ventana - tamaño_bloque * 6,tamaño_bloque,tamaño_bloque)
        bloque.cargar_imagen_bloque(tamaño_bloque,"Terrain","Terrain.png",96,64)
        stage_2_configs["lista_plataformas_tres"].append(bloque)


    for i in range(5):
        fruta = Objeto((i * tamaño_bloque) + 1, alto_ventana - tamaño_bloque * 4, 450 , 70)
        fruta.cargar_imagen_fruta(35,"Items/Fruits", "Bananas.png")
        stage_2_configs["lista_bananas"].append(fruta)

    for i in range(6):
        fruta = Objeto(ancho_ventana - (tamaño_bloque * i), alto_ventana - tamaño_bloque * 5, 450 , 70)
        fruta.cargar_imagen_fruta(35,"Items/Fruits", "Cherries.png")
        stage_2_configs["lista_cherries"].append(fruta)

    for i in range(3):
        stage_2_configs["lista_enemigos"].append(Enemigo((i * 2) + i * 100, ALTURA_SUELO, 50, 50, Auxiliar.cargar_sprite_sheets("Enemies", "AngryPig", 36, 30, True)))
        
    return stage_2_configs


