import pygame
from player import *
from constantes import *
from auxiliar import *
from plataforma import *

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("JUEGO PRUEBA 1")

imagen_fondo = (pygame.image.load(r"Juego\assets\Maps background\Fondo uno.png"))
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

juego_ejecutandose = True

clock = pygame.time.Clock()

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

    pantalla.blit(imagen_fondo, imagen_fondo.get_rect())
    
    for bloque in objetos_lista:
        bloque.dibujar(pantalla)

    rana.actualizar(FPS,pantalla)

    pygame.display.flip()

pygame.quit()