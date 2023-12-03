import pygame
from constantes import *
from auxiliar import *
from plataforma import *
from player import *
from enemigo import *
from config import *
from stage import *
from trampas import *

#INICIALIZAR PANTALLA Y TITULO
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("FROG GAIDEN III")

#LEO EL ARCHIVO DE CONFIGURACION DE NIVEL(PISO,PLATAFORMAS,FRUTAS)
stage_1_configs = configurar_nivel_uno(ANCHO_VENTANA, ALTO_VENTANA, TAMAÑO_BLOQUE)
stage_2_configs = configurar_nivel_dos(ANCHO_VENTANA, ALTO_VENTANA, TAMAÑO_BLOQUE)
stage_3_configs = configurar_nivel_tres(ANCHO_VENTANA, ALTO_VENTANA, TAMAÑO_BLOQUE)

#INSTANCIA Y CREACION DE NIVELES
nivel_1 = Stage(
    fondo=stage_1_configs["fondo"],
    lista_piso=stage_1_configs["lista_piso"],
    lista_plataformas=stage_1_configs["lista_plataformas"],
    lista_plataformas_dos=stage_1_configs["lista_plataformas_dos"],
    lista_plataformas_tres=stage_1_configs["lista_plataformas_tres"],
    lista_frutas=stage_1_configs["lista_manzanas"],
    lista_frutas_dos=stage_1_configs["lista_kiwis"],
    lista_enemigos=stage_1_configs["lista_enemigos"],
    cordenadas_trampas=stage_1_configs["coordenadas_sierras"]
)

nivel_2 = Stage(
    fondo=stage_2_configs["fondo"],
    lista_piso=stage_2_configs["lista_piso"],
    lista_plataformas=stage_2_configs["lista_plataformas"],
    lista_plataformas_dos=stage_2_configs["lista_plataformas_dos"],
    lista_plataformas_tres=stage_2_configs["lista_plataformas_tres"],
    lista_frutas=stage_2_configs["lista_bananas"],
    lista_frutas_dos=stage_2_configs["lista_cherries"],
    lista_enemigos=stage_2_configs["lista_enemigos"],
    cordenadas_trampas=stage_1_configs["coordenadas_sierras"]
)

nivel_3 = Stage(
    fondo=stage_3_configs["fondo"],
    lista_piso=stage_3_configs["lista_piso"],
    lista_plataformas=stage_3_configs["lista_plataformas"],
    lista_plataformas_dos=stage_3_configs["lista_plataformas_dos"],
    lista_plataformas_tres=stage_3_configs["lista_plataformas_tres"],
    lista_frutas=stage_3_configs["lista_bananas"],
    lista_frutas_dos=stage_3_configs["lista_cherries"],
    lista_enemigos=stage_3_configs["lista_enemigos"],
    cordenadas_trampas=stage_1_configs["coordenadas_sierras"]
)

#CONTROL DE NIVELES
niveles = [nivel_1,nivel_2,nivel_3]
nivel_actual = 1

juego_ejecutandose = True

#TIEMPO
clock = pygame.time.Clock()

#FUENTES Y MENSAJES
mensaje = input("Ingrese su nombre: ")

#CREO LA HOJA DE SPRITES DE MI PJ E INSTANCIO A MI PERSONAJE
hoja_sprites = Auxiliar.cargar_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
rana = Jugador(600,ALTURA_SUELO,50,50,hoja_sprites)

sierras = crear_sierras(niveles[nivel_actual].cordenadas_trampas)

while juego_ejecutandose:

    delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            juego_ejecutandose = False 
        if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and rana.contador_salto < 2:
                    rana.saltar()
                if evento.key == pygame.K_f:
                    rana.disparar_bala()

    #VARIABLES DE TIEMPO
    tiempo_nivel = 120
    tiempo_transcurrido = pygame.time.get_ticks() // 1000  
    tiempo_nivel -= tiempo_transcurrido

    #CAMBIO DE NIVEL SI SE CUMPLE CIERTA CONDICION
    # if condicion_cambio_nivel:
    #     nivel_actual += 1
    #     if nivel_actual >= len(niveles):
    #         juego_ejecutandose = False


    # for i in range(len(niveles[nivel_actual].lista_enemigos)):
    #     if len(niveles[nivel_actual].lista_enemigos) > 0:
    #         if niveles[nivel_actual].lista_enemigos[i].vidas == 0:
    #             niveles[nivel_actual].lista_enemigos.pop(i)
    #         else:
    #             print("Aún hay enemigos con vidas.")
    #     else:
    #         print("MATASTE A TODOS LOS ENEMIGOS. ¡FELICITACIONES!")
    #         condicion_cambio_nivel = True

    niveles[nivel_actual].dibujar(pantalla,tiempo_nivel,rana.vidas,rana.puntos,mensaje)
    niveles[nivel_actual].actualizar(pantalla, rana)

    rana.actualizar(FPS,pantalla,rana,niveles[nivel_actual].lista_piso,niveles[nivel_actual].lista_plataformas,
                    niveles[nivel_actual].lista_frutas,niveles[nivel_actual].lista_plataformas_dos,niveles[nivel_actual].lista_plataformas_tres,
                    niveles[nivel_actual].lista_frutas_dos,niveles[nivel_actual].lista_enemigos)
    
    for sierra in sierras:
        sierra.actualizar(pantalla,sierra,rana)

    if tiempo_nivel == 0:
        juego_ejecutandose = False
        pygame.quit()

    pygame.display.flip()

pygame.quit()