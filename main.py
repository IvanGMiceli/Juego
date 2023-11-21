import pygame
import sys
from player import *
from constantes import *
from auxiliar import *
from plataforma import *

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("FROG GAIDEN III")

imagen_fondo = (pygame.image.load(r"Juego\assets\Maps background\Fondo uno.png"))
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

juego_ejecutandose = True

clock = pygame.time.Clock()

#SE AGREGA FUENTE PARA PROBAR GIT
fuente = pygame.font.SysFont("consolas",35)

#CREO LA HOJA DE SPRITES DE MI PJ, E INSTANCIO A MI PERSONAJE
hoja_sprites = Auxiliar.cargar_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
rana = Jugador(600,ALTURA_SUELO,50,50,hoja_sprites)

#CREO EL PISO DEL NIVEL, INSTANCIO LA CLASE DENTRO DE UN FOR Y LAS AGREGO A LA LISTA
lista_piso = []
lista_plataformas = []
lista_plataformas_dos = []
lista_plataformas_tres = []
lista_manzanas = []
lista_kiwis = []

for i in range(13):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen(TAMAÑO_BLOQUE,"Terrain","Terrain.png")
    lista_piso.append(bloque)

for i in range(0,5):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE * 3,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen(TAMAÑO_BLOQUE,"Terrain","Terrain.png")
    lista_plataformas.append(bloque)

for i in range(0,6):
    bloque = Objeto(ANCHO_VENTANA - (TAMAÑO_BLOQUE * i),ALTO_VENTANA - TAMAÑO_BLOQUE * 4,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen(TAMAÑO_BLOQUE,"Terrain","Terrain.png")
    lista_plataformas_dos.append(bloque)

for i in range(0,5):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE * 6,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen(TAMAÑO_BLOQUE,"Terrain","Terrain.png")
    lista_plataformas_tres.append(bloque)


for i in range(5):
    fruta = Objeto((i * TAMAÑO_BLOQUE) + 1, ALTO_VENTANA - TAMAÑO_BLOQUE * 4, 450 , 70)
    fruta.cargar_imagen(35,"Items/Fruits", "Apple.png")
    lista_manzanas.append(fruta)

for i in range(6):
    fruta = Objeto(ANCHO_VENTANA - (TAMAÑO_BLOQUE * i), ALTO_VENTANA - TAMAÑO_BLOQUE * 5, 450 , 70)
    fruta.cargar_imagen(35,"Items/Fruits", "Kiwi.png")
    lista_manzanas.append(fruta)


while juego_ejecutandose:
    delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            juego_ejecutandose = False 

        if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and rana.contador_salto < 2:
                    rana.saltar()
                elif evento.key == pygame.K_h:
                    rana.vidas -= 1    


    tiempo_nivel = 120
    tiempo_transcurrido = pygame.time.get_ticks() // 1000  
    tiempo_nivel -= tiempo_transcurrido

    tiempo_en_pantalla = pygame.font.Font.render(fuente,"Tiempo: {}".format(tiempo_nivel),True,(0,0,0))
    vidas_restantes = pygame.font.Font.render(fuente,"Vidas: {}".format(rana.vidas),True,(0,0,0))
    puntaje = pygame.font.Font.render(fuente,"Puntos: {}".format(rana.puntos),True,(0,0,0))

    pantalla.blit(imagen_fondo, imagen_fondo.get_rect())
    pantalla.blit(tiempo_en_pantalla,(200,20))
    pantalla.blit(vidas_restantes,(520,20))
    pantalla.blit(puntaje,(770,20))
    
    for bloque in lista_piso:
        bloque.dibujar(pantalla)
    for plat in lista_plataformas:
        plat.dibujar(pantalla)
    for fruta in lista_manzanas:
        fruta.dibujar(pantalla)
    for block in lista_plataformas_dos:
        block.dibujar(pantalla)
    for platform in lista_plataformas_tres:
        platform.dibujar(pantalla)
    for fruit in lista_kiwis:
        fruit.dibujar(pantalla)


    rana.actualizar(FPS,pantalla,rana,lista_piso,lista_plataformas,lista_manzanas,lista_plataformas_dos,lista_plataformas_tres,lista_kiwis)

    if tiempo_nivel == 0:
        sys.exit()


    pygame.display.flip()

pygame.quit()