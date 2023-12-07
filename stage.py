import pygame


class Stage:
    """
    La clase Stage representa una etapa de un juego, con varios atributos como fondo, plataformas,
    frutas, enemigos y trampas.
    """
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
        self.sonido_victoria = pygame.mixer.Sound(r"Juego\assets\Sounds\sonido_victoria.wav")
        self.sonido_victoria_reproducido = False
        self.win = (True,False)

    def dibujar(self, pantalla,tiempo_nivel,vidas):
        """
        El metodo "dibujar" toma parámetros para la pantalla, tiempo de nivel y vidas restantes, y
        luego dibuja varios elementos en la pantalla como fondo, tiempo, vidas, puntuación, plataformas
        y frutas.
        
        :param pantalla: El parámetro "pantalla" es el objeto de superficie que representa la pantalla
        de juego donde se dibujarán los elementos
        :param tiempo_nivel: La variable "tiempo_nivel" representa el tiempo restante en el nivel. Se
        utiliza para mostrar el tiempo restante en la pantalla
        :param vidas: El parámetro "vidas" representa el número de vidas que quedan en el juego
        """

        pantalla.blit(self.fondo, self.fondo.get_rect())
        
        fuente = pygame.font.SysFont("consolas",35)
        tiempo_en_pantalla = pygame.font.Font.render(fuente,"Tiempo: {}".format(tiempo_nivel),True,(0,0,0))
        vidas_restantes = pygame.font.Font.render(fuente,"Vidas: {}".format(vidas),True,(0,0,0))
        puntaje = pygame.font.Font.render(fuente,"Puntos: {}".format(self.puntaje_final),True,(0,0,0))

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


    def actualizar(self, pantalla, jugador,nombre,nivel_actual):
        """
        El metodo "actualizar" actualiza el estado del juego según el nivel actual y las acciones del
        jugador, y muestra mensajes de victoria o derrota en consecuencia.
        
        :param pantalla: El parámetro "pantalla" es la superficie donde se está mostrando el juego. Se
        utiliza para actualizar y dibujar los elementos del juego en la pantalla
        :param jugador: El parámetro "jugador" representa el objeto jugador. Se utiliza para acceder y
        actualizar los atributos del jugador como vidas, puntos, etc
        :param nombre: El parámetro "nombre" es una cadena que representa el nombre del jugador
        :param nivel_actual: La variable "nivel_actual" representa el nivel actual del juego. Se utiliza
        para determinar las condiciones de victoria o derrota en cada nivel
        """

        for enemigo in self.lista_enemigos:
            enemigo.actualizar(pantalla, enemigo, self.lista_piso, jugador)
            if enemigo.vidas <= 0:
                self.lista_enemigos.remove(enemigo)

        match nivel_actual:
            case 0:
                if jugador.vidas > 0:
                    self.puntaje_final = jugador.puntos
                    if jugador.puntos >= 1000 and self.win:
                        self.mostrar_mensaje(pantalla,nombre,"victoria")
                else:
                    self.mostrar_mensaje(pantalla,nombre,"derrota")
                    
            case 1:
                if jugador.vidas > 0:
                    self.puntaje_final = jugador.puntos
                    if len(self.lista_enemigos) == 0 and self.win:
                        self.mostrar_mensaje(pantalla,nombre,"victoria")
                else:
                    self.mostrar_mensaje(pantalla,nombre,"derrota")

            case 2:
                if jugador.vidas > 0:
                    self.puntaje_final = jugador.puntos
                    if jugador.puntos >= 2000 and (len(self.lista_frutas) == 0 or len(self.lista_frutas_dos) == 0) and len(self.lista_enemigos) == 0 and self.win:
                        self.mostrar_mensaje(pantalla,nombre,"victoria")
                else:
                    self.mostrar_mensaje(pantalla,nombre,"derrota")

    def reproducir_victoria(self, loops=0):
        """
        El metodo `reproducir_victoria` reproduce un sonido de victoria si no se ha reproducido antes.
        
        :param loops: El parámetro de bucles determina cuántas veces se reproducirá el sonido. De forma
        predeterminada, está configurado en 0, lo que significa que el sonido sólo se reproducirá una
        vez. Si desea que el sonido se reproduzca continuamente, puede establecer los bucles en un valor
        negativo, como -1, defaults to 0 (optional)
        """

        if not self.sonido_victoria_reproducido:
            self.sonido_victoria.play(loops=loops)
            self.sonido_victoria_reproducido = True
            

    def mostrar_mensaje(self,pantalla,nombre,estado):
        """
        El metodo "mostrar_mensaje" muestra en pantalla un mensaje de victoria o derrota junto con el
        resultado final.
        
        :param pantalla: El parámetro "pantalla" representa la pantalla o superficie donde se mostrarán
        los mensajes
        :param nombre: El parámetro "nombre" es una cadena que representa el nombre del jugador
        :param estado: El parámetro "estado" representa el estado del juego, ya sea "victoria"
        (victoria) o "derrota" (derrota)
        """

        fuente = pygame.font.SysFont("consolas",35)
        fuente_nivel = pygame.font.SysFont("consolas",90) 
        mensaje_derrota = pygame.font.Font.render(fuente_nivel,"GAME OVER",True,(0,0,0))
        mensaje_victoria = pygame.font.Font.render(fuente_nivel,"NIVEL COMPLETADO!",True,(0,0,0))
        puntuacion_final = pygame.font.Font.render(fuente,"Nombre: {0} | Puntuacion: {1}".format(nombre,self.puntaje_final),True,(0,0,0))

        if estado == "victoria":
                pantalla.blit(mensaje_victoria,(200,210))
                pantalla.blit(puntuacion_final,(310,300))
                self.reproducir_victoria()
        elif estado == "derrota":
            pantalla.blit(mensaje_derrota,(380,210))
            pantalla.blit(puntuacion_final,(310,300))
