from auxiliar import *
from player import *

class Stage:
    def __init__(self, pantalla, jugador, fondo, ancho_vent, alto_vent, nombre, nivel_piso):
        self.pantalla = pantalla
        self.player_sprite = Auxiliar.cargar_sprite_sheets("MainCharacters", "NinjaFrog", 32, 32, True)
        self.jugador = Jugador(600,ALTURA_SUELO,50,50,self.player_sprite)
        self.fondo = fondo
        self.ancho_vent = ancho_vent
        self.alto_vent = alto_vent
        self.nombre = nombre
        self.nivel_piso = nivel_piso
        self.win = False

    def check_win(self):
        pass

    def update(self):
        pass

    def draw(self):
        pass

    def stage_passed(self):
        return self.win

current_stage = Stage(pantalla, jugador, fondo, ANCHO_VENTANA, ALTO_VENTANA, "stage_1", lista_piso)

while juego_ejecutandose:
    current_stage.update()
    current_stage.draw()

    if current_stage.stage_passed():
        pass