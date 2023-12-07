import pygame
import sqlite3
from constantes import *
from auxiliar import *
from plataforma import *
from player import *
from enemigo import *
from config import *
from stage import *
from trampas import *
from menus import *

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
    cordenadas_trampas=stage_2_configs["coordenadas_sierras"]
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

#CARGAR Y REPRODUCIR MUSICA Y EFECTOS
pygame.mixer.music.load(r"Juego\assets\Sounds\Overworld_Day.mp3")

volumen_inicial = 0.3
pygame.mixer.music.set_volume(volumen_inicial)

pygame.mixer.music.play(-1)

sonido_disparo = pygame.mixer.Sound(r"Juego\assets\Sounds\player_fire.wav")
sonido_salto = pygame.mixer.Sound(r"Juego\assets\Sounds\player jump.wav")


#CONTROL DE NIVELES
niveles = [nivel_1,nivel_2,nivel_3]
nivel_actual = 0

#CONTROL JUEGO
juego_ejecutandose = True
menu_pausa = MenuOpciones(["Continuar", "Elegir Nivel", "Salir del Juego", "Ir al Menu Principal"])
menu_niveles = MenuOpciones(["Nivel 0", "Nivel 1", "Nivel 2"])
menu_principal = MenuOpciones(["Jugar", "Opciones", "Rankings","Salir"])
menu_settings = MenuOpciones(["Activar Musica","Desactivar Musica","Subir Volumen","Bajar Volumen","Salir"])
musica_activa = True
juego_pausado = False
seleccion_nivel = False
seleccion_menu_settings = False
selec_menu_principal = True


#TIEMPO
clock = pygame.time.Clock()

#FUENTES Y MENSAJES
mensaje = input("Ingrese su nombre: ")

#CREO LA HOJA DE SPRITES DE MI PJ E INSTANCIO A MI PERSONAJE
hoja_sprites = Auxiliar.cargar_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
rana = Jugador(600,ALTURA_SUELO,50,50,hoja_sprites)

#TRAMPAS
sierras = crear_sierras(niveles[nivel_actual].cordenadas_trampas)

while juego_ejecutandose:

    delta_ms = clock.tick(FPS)
    lista_eventos = pygame.event.get()

    for evento in lista_eventos:
        if evento.type == pygame.QUIT:
            juego_ejecutandose = False 
        if evento.type == pygame.KEYDOWN:
                if not selec_menu_principal:
                    if not seleccion_menu_settings:
                        if not seleccion_nivel:
                            if not juego_pausado:
                                if evento.key == pygame.K_SPACE and rana.contador_salto < 2:
                                    rana.saltar()
                                    sonido_salto.play()
                                if evento.key == pygame.K_f:
                                    rana.disparar_bala()
                                    sonido_disparo.play()
                                if evento.key == pygame.K_p:
                                    juego_pausado = not juego_pausado
                                    if juego_pausado:
                                        pygame.mixer.music.pause()
                                    else:
                                        pygame.mixer.music.unpause()
                            else:
                                resultado_menu_pausa = menu_pausa.manejar_eventos(lista_eventos)
                                if resultado_menu_pausa is not None:
                                    if resultado_menu_pausa == 0:
                                        juego_pausado = False
                                        pygame.mixer.music.unpause()
                                    elif resultado_menu_pausa == 1:
                                        seleccion_nivel = True
                                    elif resultado_menu_pausa == 2:
                                        juego_ejecutandose = False
                                    elif resultado_menu_pausa == 3:
                                        juego_pausado = False
                                        selec_menu_principal = True
                        else:
                            resultado_menu_nivel = menu_niveles.manejar_eventos(lista_eventos)
                            if resultado_menu_nivel is not None:
                                nivel_actual = resultado_menu_nivel
                                seleccion_nivel = False
                    else:
                        resultado_menu_settings = menu_settings.manejar_eventos(lista_eventos)
                        if resultado_menu_settings is not None:
                            if resultado_menu_settings == 0:
                                musica_activa = True
                                pygame.mixer.music.unpause()
                            elif resultado_menu_settings == 1:
                                musica_activa = False
                                pygame.mixer.music.pause()
                            elif resultado_menu_settings == 2:
                                volumen_actual = min(1.0, pygame.mixer.music.get_volume() + 0.1)
                                pygame.mixer.music.set_volume(volumen_actual)
                            elif resultado_menu_settings == 3:
                                volumen_actual = max(0.0, pygame.mixer.music.get_volume() - 0.1)
                                pygame.mixer.music.set_volume(volumen_actual)
                            elif resultado_menu_settings == 4:
                                seleccion_menu_settings = False
                                selec_menu_principal = True
                else:   
                        if musica_activa:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                        resultado_menu_principal = menu_principal.manejar_eventos(lista_eventos)
                        if resultado_menu_principal is not None:
                            if resultado_menu_principal == 0:
                                seleccion_nivel = True
                                selec_menu_principal = False
                            elif resultado_menu_principal == 1:
                                seleccion_menu_settings = True
                                selec_menu_principal = False
                            elif resultado_menu_principal == 2:
                                crear_tabla_posiciones(mensaje,rana)
                            elif resultado_menu_principal == 3:
                                juego_ejecutandose = False

    if not juego_pausado and not seleccion_nivel and not selec_menu_principal and not seleccion_menu_settings:

        #VARIABLES DE TIEMPO
        tiempo_nivel = 200
        tiempo_transcurrido = pygame.time.get_ticks() // 1000  
        tiempo_nivel -= tiempo_transcurrido

        niveles[nivel_actual].dibujar(pantalla,tiempo_nivel,rana.vidas)
        niveles[nivel_actual].actualizar(pantalla, rana,mensaje,nivel_actual)

        rana.actualizar(FPS,pantalla,rana,niveles[nivel_actual].lista_piso,niveles[nivel_actual].lista_plataformas,
                        niveles[nivel_actual].lista_frutas,niveles[nivel_actual].lista_plataformas_dos,niveles[nivel_actual].lista_plataformas_tres,
                        niveles[nivel_actual].lista_frutas_dos,niveles[nivel_actual].lista_enemigos)
        
        for sierra in sierras:
            sierra.actualizar(pantalla,sierra,rana)

        if tiempo_nivel == 0:
            juego_ejecutandose = False
            pygame.quit()

        pygame.display.flip()

    elif seleccion_nivel:
        menu_niveles.dibujar(pantalla)
        pygame.display.flip()
    elif juego_pausado:
        menu_pausa.dibujar(pantalla)
        pygame.display.flip()
    elif seleccion_menu_settings:
        menu_settings.dibujar(pantalla)
        pygame.display.flip()
    else:
        menu_principal.dibujar(pantalla)
        pygame.display.flip()


pygame.quit()
