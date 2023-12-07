import pygame
from constantes import *
from auxiliar import *
from plataforma import *
from player import *
from enemigo import *
from config import *
from stage import *
from trampas import *

class MenuOpciones:
    def __init__(self,opciones:list[str]):
        self.fondo = pygame.transform.scale(pygame.image.load(r"Juego\assets\Menu\fondo_menu.jpg"), (ANCHO_VENTANA, ALTO_VENTANA))
        self.opciones = opciones
        self.opcion_seleccionada = 0
        self.font = pygame.font.Font(None, 50)
        self.contorno_ancho = 2

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        for i, opcion in enumerate(self.opciones):
            texto = self.font.render(opcion, True, (0, 0, 0))
            x = ANCHO_VENTANA // 2 - texto.get_width() // 2
            y = ALTO_VENTANA // 3 - texto.get_height() + i * 70

            if i == self.opcion_seleccionada:
                pygame.draw.rect(pantalla, (255, 0, 0), (x - self.contorno_ancho, y - self.contorno_ancho,
                                texto.get_width() + 2 * self.contorno_ancho,
                                texto.get_height() + 2 * self.contorno_ancho),
                                self.contorno_ancho * 2)

            pantalla.blit(texto, (x, y))

    def manejar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP:
                    self.opcion_seleccionada = (self.opcion_seleccionada - 1) % len(self.opciones)
                elif evento.key == pygame.K_DOWN:
                    self.opcion_seleccionada = (self.opcion_seleccionada + 1) % len(self.opciones)
                elif evento.key == pygame.K_RETURN:
                    return self.opcion_seleccionada
        return None

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
menu_pausa = MenuOpciones(["Continuar", "Salir al Menú de Niveles", "Salir del Juego", "Salir al Menu Principal"])
menu_niveles = MenuOpciones(["Nivel 0", "Nivel 1", "Nivel 2"])
menu_principal = MenuOpciones(["Jugar", "Opciones", "Rankings","Salir"])
juego_pausado = False
seleccion_nivel = False
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
                    if not seleccion_nivel:
                        if not juego_pausado:
                            if evento.key == pygame.K_SPACE and rana.contador_salto < 2:
                                rana.saltar()
                                sonido_salto.play()
                            if evento.key == pygame.K_f:
                                rana.disparar_bala()
                                sonido_disparo.play()
                            if evento.key == pygame.K_q:
                                volumen_actual = min(1.0, pygame.mixer.music.get_volume() + 0.1)
                                pygame.mixer.music.set_volume(volumen_actual)
                            elif evento.key == pygame.K_e:
                                volumen_actual = max(0.0, pygame.mixer.music.get_volume() - 0.1)
                                pygame.mixer.music.set_volume(volumen_actual)
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
                        pygame.mixer.music.unpause()
                        resultado_menu_principal = menu_principal.manejar_eventos(lista_eventos)
                        if resultado_menu_principal is not None:
                            if resultado_menu_principal == 0:
                                seleccion_nivel = True
                                selec_menu_principal = False
                            elif resultado_menu_principal == 1:
                                pass
                                selec_menu_principal = False
                            elif resultado_menu_principal == 2:
                                pass
                                selec_menu_principal = False
                            elif resultado_menu_principal == 3:
                                juego_ejecutandose = False

    if not juego_pausado and not seleccion_nivel and not selec_menu_principal:

        #VARIABLES DE TIEMPO
        tiempo_nivel = 120
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
    else:
        menu_principal.dibujar(pantalla)
        pygame.display.flip()


pygame.quit()



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
