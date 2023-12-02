from constantes import *
from auxiliar import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, direction, img_path = False):
        super().__init__()
        # self.image = pygame.Surface((50, 10))
        # self.image.fill((255, 0, 0))
        self.__load_img(img_path)
        self.rect = self.image.get_rect(center=(pos_x, pos_y))
        self.direction = direction

    def __load_img(self, img_path: bool):
        if img_path:
            self.image = pygame.image.load(r'Juego\assets\Enemies\Plant\bullet.png')
            self.image = pygame.transform.scale2x(self.image)
        else: 
            self.image = pygame.Surface((4, 20))
            self.image.fill('white')

    def update(self):
        
        match self.direction:
            case 'izquierda':
                self.rect.x += 10
                if self.rect.x >= ANCHO_VENTANA:
                    self.kill()
            case 'derecha':
                self.rect.x -= 10
                if self.rect.x <= 0:
                    self.kill()