import pygame
from constantes import *
from auxiliar import *
from plataforma import *
from auxiliar import *
from player import *
from enemigo import *
from config import *
from stage import *

#INICIALIZAR PANTALLA Y TITULO
pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("FROG GAIDEN III")

#LEO EL ARCHIVO DE CONFIGURACION DE NIVEL(PISO,PLATAFORMAS,FRUTAS)
stage_1_configs = configurar_nivel_uno(ANCHO_VENTANA, ALTO_VENTANA, TAMAÑO_BLOQUE)
stage_2_configs = configurar_nivel_dos(ANCHO_VENTANA, ALTO_VENTANA, TAMAÑO_BLOQUE)

#INSTANCIA Y CREACION DE NIVELES
nivel_1 = Stage(
    fondo=stage_1_configs["fondo"],
    lista_piso=stage_1_configs["lista_piso"],
    lista_plataformas=stage_1_configs["lista_plataformas"],
    lista_plataformas_dos=stage_1_configs["lista_plataformas_dos"],
    lista_plataformas_tres=stage_1_configs["lista_plataformas_tres"],
    lista_frutas=stage_1_configs["lista_manzanas"],
    lista_frutas_dos=stage_1_configs["lista_kiwis"],
    lista_enemigos=[Enemigo(1000, ALTURA_SUELO, 50, 50, Auxiliar.cargar_sprite_sheets("Enemies", "AngryPig", 36, 30, True))]
)

nivel_2 = Stage(
    fondo=stage_2_configs["fondo"],
    lista_piso=stage_2_configs["lista_piso"],
    lista_plataformas=stage_2_configs["lista_plataformas"],
    lista_plataformas_dos=stage_2_configs["lista_plataformas_dos"],
    lista_plataformas_tres=stage_2_configs["lista_plataformas_tres"],
    lista_frutas=stage_2_configs["lista_bananas"],
    lista_frutas_dos=stage_2_configs["lista_cherries"],
    lista_enemigos=[Enemigo(1000, ALTURA_SUELO, 50, 50, Auxiliar.cargar_sprite_sheets("Enemies", "Chicken", 32, 34, True))]
)


#CONTROL DE NIVELES
niveles = [nivel_1,nivel_2]
nivel_actual = 0
condicion_cambio_nivel = False

juego_ejecutandose = True

#TIEMPO
clock = pygame.time.Clock()

#FUENTES Y MENSAJES
fuente = pygame.font.SysFont("consolas",35)
fuente_nivel = pygame.font.SysFont("consolas",90)
mensaje = input("Ingrese su nombre: ")

#CREO LA HOJA DE SPRITES DE MI PJ E INSTANCIO A MI PERSONAJE
hoja_sprites = Auxiliar.cargar_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
rana = Jugador(600,ALTURA_SUELO,50,50,hoja_sprites)

while juego_ejecutandose:

    delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            juego_ejecutandose = False 

        if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE and rana.contador_salto < 2:
                    rana.saltar()
                if evento.key == pygame.K_h:
                    rana.vidas += 1

    #VARIABLES DE TIEMPO
    tiempo_nivel = 120
    tiempo_transcurrido = pygame.time.get_ticks() // 1000  
    tiempo_nivel -= tiempo_transcurrido

    #VARIABLES DE SUPERFICIE EN PANTALLA
    tiempo_en_pantalla = pygame.font.Font.render(fuente,"Tiempo: {}".format(tiempo_nivel),True,(0,0,0))
    vidas_restantes = pygame.font.Font.render(fuente,"Vidas: {}".format(rana.vidas),True,(0,0,0))
    puntaje = pygame.font.Font.render(fuente,"Puntos: {}".format(rana.puntos),True,(0,0,0))
    mensaje_derrota = pygame.font.Font.render(fuente_nivel,"GAME OVER",True,(0,0,0))
    mensaje_victoria = pygame.font.Font.render(fuente_nivel,"NIVEL COMPLETADO!",True,(0,0,0))
    puntuacion_final = pygame.font.Font.render(fuente,"Nombre: {0} | Puntuacion: {1}".format(mensaje,rana.puntos),True,(0,0,0))


    #CAMBIO DE NIVEL SI SE CUMPLE CIERTA CONDICION
    if condicion_cambio_nivel:
        nivel_actual += 1
        if nivel_actual >= len(niveles):
            juego_ejecutandose = False

    niveles[nivel_actual].dibujar(pantalla)
    niveles[nivel_actual].actualizar(pantalla, rana)

    pantalla.blit(tiempo_en_pantalla,(200,20))
    pantalla.blit(vidas_restantes,(520,20)) 
    pantalla.blit(puntaje,(770,20))

    rana.actualizar(FPS,pantalla,rana,niveles[nivel_actual].lista_piso,niveles[nivel_actual].lista_plataformas,
                    niveles[nivel_actual].lista_frutas,niveles[nivel_actual].lista_plataformas_dos,niveles[nivel_actual].lista_plataformas_tres,
                    niveles[nivel_actual].lista_frutas_dos)

    if tiempo_nivel == 0:
        juego_ejecutandose = False
        pygame.quit()

    pygame.display.flip()

pygame.quit()