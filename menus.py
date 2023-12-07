import pygame
from constantes import *
from auxiliar import *

class MenuOpciones:
    def __init__(self,opciones:list[str]):
        self.fondo = pygame.transform.scale(pygame.image.load(r"Juego\assets\Menu\fondo_menu.jpg"), (ANCHO_VENTANA, ALTO_VENTANA))
        self.opciones = opciones
        self.opcion_seleccionada = 0
        self.fuente = pygame.font.Font(r'Archivos Juego\recursos\fonts\Halimount.otf', 60)
        self.fuente_titulo = pygame.font.Font(r'Archivos Juego\recursos\fonts\Halimount.otf', 100)
        self.contorno_ancho = 2

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, (0, 0))
        titulo = self.fuente_titulo.render("FROG GAIDEN III", True, (0, 0, 0))
        for i, opcion in enumerate(self.opciones):
            texto = self.fuente.render(opcion, True, (255, 255, 255))
            x = ANCHO_VENTANA // 2 - texto.get_width() // 2
            y = ALTO_VENTANA // 2 - texto.get_height() + i * 70

            if i == self.opcion_seleccionada:
                pygame.draw.rect(pantalla, (255, 0, 0), (x - self.contorno_ancho, y - self.contorno_ancho,
                                texto.get_width() + 2 * self.contorno_ancho,
                                texto.get_height() + 2 * self.contorno_ancho),
                                self.contorno_ancho * 2)

            pantalla.blit(titulo,(350,50))
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