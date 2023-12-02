import pygame
from constantes import *

class Crosshair(pygame.sprite.Sprite):
    def __init__(self, picture_path):
        super().__init__()
        self.image = pygame.image.load(picture_path)
        self.rect = self.image.get_rect()

    def verificar_si_clickeo(self,crosshair,boton):

        if pygame.sprite.spritecollide(crosshair, boton, False):
            for bot in boton:
                if bot.opcion == 1:
                    print("APRETE ICONO 1")
                elif bot.opcion == 2:
                    print("APRETE ICONO 2")
                elif bot.opcion == 3:
                    print("APRETE ICONO 3")
                elif bot.opcion == 4:
                    print("APRETE ICONO 4")
                elif bot.opcion == 5:
                    print("APRETE ICONO 5")
                elif bot.opcion == 6:
                    print("APRETE ICONO 6")


    def update(self):
        self.rect.center = pygame.mouse.get_pos()

class Boton(pygame.sprite.Sprite):
    def __init__(self, picture_path,pos_x, pos_y,opcion):
        super().__init__()
        self.image = pygame.transform.scale2x(pygame.image.load(picture_path))
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.opcion = opcion
        print(f"Nuevo Boton creado: opcion={opcion}, rect={self.rect}")




pygame.init()
pantalla = pygame.display.set_mode((ANCHO_VENTANA,ALTO_VENTANA))
clock = pygame.time.Clock()

pygame.mouse.set_visible(True)

background = pygame.image.load(r'C:\Users\usuario\Desktop\Archivos Progra y Labo I\Tiro al blanco\BG.png')

cursor = Crosshair(r'C:\Users\usuario\Desktop\Archivos Progra y Labo I\Tiro al blanco\crosshair.png')

nivel_1 = Boton(r'Juego\assets\Menu\Levels\01.png',100,200,1)
nivel_2 = Boton(r'Juego\assets\Menu\Levels\02.png',600,200,2)
nivel_3 = Boton(r'Juego\assets\Menu\Levels\03.png',1100,200,3)
boton_play = Boton(r'Juego\assets\Menu\Buttons\Play.png',100,400,4)
boton_back = Boton(r'Juego\assets\Menu\Buttons\Back.png',600,400,5)
boton_close = Boton(r'Juego\assets\Menu\Buttons\Close.png',1100,400,6)

grupo_botones = pygame.sprite.Group()

grupo_botones.add(boton_back)
grupo_botones.add(boton_play)
grupo_botones.add(boton_close)
grupo_botones.add(nivel_1)
grupo_botones.add(nivel_2)
grupo_botones.add(nivel_3)



# def update():
#     rect.center = pygame.mouse.get_pos()

while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
        if evento.type == pygame.MOUSEBUTTONDOWN:
            cursor.verificar_si_clickeo(cursor,grupo_botones)
    

    pantalla.blit(background,(0,0))

    # pantalla.blit(boton_play,(100,400))
    # pantalla.blit(boton_back,(600,400))
    # pantalla.blit(boton_close,(1100,400))

    cursor.update()

    grupo_botones.draw(pantalla)
    grupo_botones.update()

            
    pygame.display.flip()

def seleccion_de_nivel(nivel):
    match nivel:
        case 0:
            pass
        case 1:
            pass
        case 2:
            pass