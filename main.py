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
rana = Jugador(100,100,50,50,hoja_sprites)

#CREO EL PISO DEL NIVEL, INSTANCIO LA CLASE DENTRO DE UN FOR Y LAS AGREGO A LA LISTA
objetos_lista = []

for i in range(13):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen(TAMAÑO_BLOQUE,"Terrain","Terrain.png")
    objetos_lista.append(bloque)

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

    pantalla.blit(imagen_fondo, imagen_fondo.get_rect())
    pantalla.blit(tiempo_en_pantalla,(80,20))
    pantalla.blit(vidas_restantes,(580,20))
    
    for bloque in objetos_lista:
        bloque.dibujar(pantalla)

    rana.actualizar(FPS,pantalla)

    if tiempo_nivel == 0 or rana.vidas == 0:
        sys.exit()


    pygame.display.flip()

pygame.quit()