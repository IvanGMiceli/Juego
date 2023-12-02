import pygame
import sys
from player import *
from constantes import *
from auxiliar import *
from plataforma import *
from enemigo import *

pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
pygame.display.set_caption("FROG GAIDEN III")


#CARGO FONDOS DE CADA NIVEL
imagen_fondo = (pygame.image.load(r"Juego\assets\Maps background\Fondo uno.png"))
imagen_fondo = pygame.transform.scale(imagen_fondo,(ANCHO_VENTANA,ALTO_VENTANA))

fondo_lvl_2 = (pygame.image.load(r"Juego\assets\Maps background\Fondo dos.png"))
fondo_lvl_2 = pygame.transform.scale(fondo_lvl_2,(ANCHO_VENTANA,ALTO_VENTANA))

fondo_lvl_3 = (pygame.image.load(r"Juego\assets\Maps background\Fondo tres.png"))
fondo_lvl_3 = pygame.transform.scale(fondo_lvl_3,(ANCHO_VENTANA,ALTO_VENTANA))


juego_ejecutandose = True

clock = pygame.time.Clock()

#SE AGREGA FUENTE PARA PROBAR GIT
fuente = pygame.font.SysFont("consolas",35)
fuente_nivel = pygame.font.SysFont("consolas",90)
# mensaje = input("Ingrese su nombre: ")

#CREO LA HOJA DE SPRITES DE MI PJ, E INSTANCIO A MI PERSONAJE
hoja_sprites = Auxiliar.cargar_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
rana = Jugador(600,ALTURA_SUELO,50,50,hoja_sprites)

#CREO ENEMIGO
hoja_sprites_dos = Auxiliar.cargar_sprite_sheets("Enemies","Plant", 44, 42, True)
gallina = Enemigo(1000,ALTURA_SUELO,50,50,hoja_sprites_dos)
gallina2 = Enemigo(1000,334,50,50,hoja_sprites_dos)
gallina3 = Enemigo(10,430,50,50,hoja_sprites_dos)
print(hoja_sprites_dos)

#CREO EL PISO DEL NIVEL, INSTANCIO LA CLASE DENTRO DE UN FOR Y LAS AGREGO A LA LISTA
lista_piso = []
lista_plataformas = []
lista_plataformas_dos = []
lista_plataformas_tres = []
lista_manzanas = []
lista_kiwis = []

for i in range(13):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen_bloque(TAMAÑO_BLOQUE,"Terrain","Terrain.png",96,0)
    lista_piso.append(bloque)
    print(i * TAMAÑO_BLOQUE)

for i in range(0,5):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE * 3,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen_bloque(TAMAÑO_BLOQUE,"Terrain","Terrain.png",96,0)
    lista_plataformas.append(bloque)

for i in range(0,6):
    bloque = Objeto(ANCHO_VENTANA - (TAMAÑO_BLOQUE * i),ALTO_VENTANA - TAMAÑO_BLOQUE * 4,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen_bloque(TAMAÑO_BLOQUE,"Terrain","Terrain.png",96,0)
    lista_plataformas_dos.append(bloque)

for i in range(0,5):
    bloque = Objeto(i * TAMAÑO_BLOQUE,ALTO_VENTANA - TAMAÑO_BLOQUE * 6,TAMAÑO_BLOQUE,TAMAÑO_BLOQUE)
    bloque.cargar_imagen_bloque(TAMAÑO_BLOQUE,"Terrain","Terrain.png",96,0)
    lista_plataformas_tres.append(bloque)


for i in range(5):
    fruta = Objeto((i * TAMAÑO_BLOQUE) + 1, ALTO_VENTANA - TAMAÑO_BLOQUE * 4, 450 , 70)
    fruta.cargar_imagen_fruta(35,"Items/Fruits", "Apple.png")
    lista_manzanas.append(fruta)

for i in range(6):
    fruta = Objeto(ANCHO_VENTANA - (TAMAÑO_BLOQUE * i), ALTO_VENTANA - TAMAÑO_BLOQUE * 5, 450 , 70)
    fruta.cargar_imagen_fruta(35,"Items/Fruits", "Kiwi.png")
    lista_kiwis.append(fruta)


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
    # puntuacion_final = pygame.font.Font.render(fuente,"Nombre: {0} | Puntuacion: {1}".format(mensaje,rana.puntos),True,(0,0,0))

    #IMPRIMO EN PANTALLA
    pantalla.blit(fondo_lvl_2, fondo_lvl_2.get_rect())
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


    #IMPRIMIR UN TEXTO EN PANTALLA POR SI GANA O SE PIERDE
    # if rana.vidas == 0:
    #     pantalla.blit(mensaje_derrota,(380,210))
    #     pantalla.blit(puntuacion_final,(310,300))
    # elif rana.puntos == 1000:
    #     pantalla.blit(mensaje_victoria,(200,210))
    #     pantalla.blit(puntuacion_final,(310,300))

    rana.actualizar(FPS,pantalla,rana,lista_piso,lista_plataformas,lista_manzanas,lista_plataformas_dos,lista_plataformas_tres,lista_kiwis)
    # rana.actualizar(FPS,pantalla,rana,lista_piso)
    gallina.actualizar(pantalla,gallina,lista_piso,rana)
    gallina2.actualizar(pantalla,gallina2,lista_plataformas_dos,rana)
    gallina3.actualizar(pantalla,gallina3,lista_plataformas_tres,rana)

    

    if tiempo_nivel == 0:
        sys.exit()


    pygame.display.flip()

pygame.quit()




"""

stage_1 = False
stage_2 = False

img_nivel_1 = poner imagen
img_nivel_1 = poner imagen

y se lo paso a stage al instanciarlo

while juego_ejecutandose:

    if not stage:
        stage = Instacion el stage Stage(pantalla,jugador,fondo,ancho_vent_,alto_vent, nombre del stage, nivel del piso )
    
    if not stage_1_win:
        stage_1_win = stage.stage_passed()
    elif stage_1_win and not stage_2_win:
        stage = Instacion el stage 2
    elif stage_2_win and not stage_3_win:
        stage = Instacion el stage 3


def check_win(self) -> bool

    match self.stage_name:
    case 'stage_1':
        self.win = condicion para ganar (juntar todas las frutas)
    case 'stage_2':
        self.win = condicion para ganar (juntar todas las frutas) and cantidad de enemigos == 0
    case 'stage_3':
        self.win = condicion para ganar

def stage_passed(self) -> bool
    return self.win

"""