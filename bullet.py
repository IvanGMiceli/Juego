from constantes import *
from auxiliar import *


class Bullet(pygame.sprite.Sprite):
    """
    La clase Bullet representa un objeto bala en un juego, con atributos de posición, dirección e imagen.
    """
    def __init__(self, pos_x, pos_y, direction, img_path = False):
        super().__init__()
        self.__load_img(img_path)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction

    def __load_img(self, img_path: bool):
        """
        El metodo carga una imagen desde una ruta determinada y la escala, o crea una superficie blanca
        si no se proporciona ninguna ruta.
        
        :param img_path: El parámetro `img_path` es un valor booleano que indica si se proporciona o no
        una ruta de imagen. Si `img_path` es `True`, significa que se proporciona una ruta de imagen y
        el código cargará la imagen desde la ruta especificada. Si `img_path` es `False`,
        :type img_path: bool
        """
        if img_path:
            self.image = pygame.image.load(r'Juego\assets\Enemies\Plant\bullet.png')
            self.image = pygame.transform.scale2x(self.image)
        else: 
            self.image = pygame.Surface((4, 20))
            self.image.fill('white')

    def update(self):
        """
        El metodo actualiza la posición de un objeto según su dirección y lo elimina si va más allá de
        los límites de la ventana.
        """
        
        match self.direction:
            case 'izquierda':
                self.rect.x += 10
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case 'derecha':
                self.rect.x -= 10
                if self.rect.x <= 0:
                    self.kill()