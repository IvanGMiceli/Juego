import pygame

class Stage:
    def __init__(self, fondo, lista_piso, lista_plataformas,lista_plataformas_dos,lista_plataformas_tres, lista_frutas, lista_frutas_dos, lista_enemigos,cordenadas_trampas):
        self.fondo = fondo
        self.lista_piso = lista_piso
        self.lista_plataformas = lista_plataformas
        self.lista_plataformas_dos = lista_plataformas_dos
        self.lista_plataformas_tres = lista_plataformas_tres
        self.lista_frutas = lista_frutas
        self.lista_frutas_dos = lista_frutas_dos
        self.lista_enemigos = lista_enemigos
        self.cordenadas_trampas = cordenadas_trampas
        self.puntaje_final = 0

    def dibujar(self, pantalla,tiempo_nivel,vidas,puntos,nombre):
        
        pantalla.blit(self.fondo, self.fondo.get_rect())
        
        fuente = pygame.font.SysFont("consolas",35)
        fuente_nivel = pygame.font.SysFont("consolas",90)       

        tiempo_en_pantalla = pygame.font.Font.render(fuente,"Tiempo: {}".format(tiempo_nivel),True,(0,0,0))
        vidas_restantes = pygame.font.Font.render(fuente,"Vidas: {}".format(vidas),True,(0,0,0))
        puntaje = pygame.font.Font.render(fuente,"Puntos: {}".format(self.puntaje_final),True,(0,0,0))
        mensaje_derrota = pygame.font.Font.render(fuente_nivel,"GAME OVER",True,(0,0,0))
        mensaje_victoria = pygame.font.Font.render(fuente_nivel,"NIVEL COMPLETADO!",True,(0,0,0))
        puntuacion_final = pygame.font.Font.render(fuente,"Nombre: {0} | Puntuacion: {1}".format(nombre,self.puntaje_final),True,(0,0,0))

        pantalla.blit(tiempo_en_pantalla,(200,20))
        pantalla.blit(vidas_restantes,(520,20)) 
        pantalla.blit(puntaje,(770,20))
        
        for bloque in self.lista_piso:
            bloque.dibujar(pantalla)

        for plat in self.lista_plataformas:
            plat.dibujar(pantalla)
        for fruta in self.lista_frutas:
            fruta.dibujar(pantalla)
        for block in self.lista_plataformas_dos:
            block.dibujar(pantalla)
        for platform in self.lista_plataformas_tres:
            platform.dibujar(pantalla)
        for fruit in self.lista_frutas_dos:
            fruit.dibujar(pantalla)

        if vidas > 0:
            self.puntaje_final = puntos 
            if puntos == 1000:
                pantalla.blit(mensaje_victoria,(200,210))
                pantalla.blit(puntuacion_final,(310,300))
        else:
            pantalla.blit(mensaje_derrota,(380,210))
            pantalla.blit(puntuacion_final,(310,300))

    def actualizar(self, pantalla, jugador):

        for enemigo in self.lista_enemigos:
            enemigo.actualizar(pantalla, enemigo, self.lista_piso, jugador)
            if enemigo.vidas <= 0:
                self.lista_enemigos.remove(enemigo)