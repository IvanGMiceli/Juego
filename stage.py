
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

    def dibujar(self, pantalla):
        pantalla.blit(self.fondo, self.fondo.get_rect())
        
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

    def actualizar(self, pantalla, jugador):
        for enemigo in self.lista_enemigos:
            enemigo.actualizar(pantalla, enemigo, self.lista_piso, jugador)