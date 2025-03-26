import pygame
import random
import os

# TAMAÑO DEL LIENZO
WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

ROOT_DIR = os.path.dirname(__file__)
IMAGE_DIR = os.path.join(ROOT_DIR, '..', 'assets')

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('GALAGA')
clock = pygame.time.Clock()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar imagen del jugador
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'player_rotated.png')).convert()
        self.image = pygame.transform.scale(self.image, (85, 90))
        self.image.set_colorkey(BLACK)  # Hace que el fondo negro sea transparente
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2  # Posicionar en el centro de la pantalla
        self.rect.bottom = HEIGHT - 10  # Posicionar en la parte inferior
        self.speed_x = 0  # Velocidad inicial

    def update(self):
        """Mueve al jugador a la izquierda o derecha"""
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x

        # Evitar que salga de los bordes
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self, all_sprites, bullet_group):
        """Dispara una bala desde la nave"""
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)  # Agregar la bala a los sprites generales
        bullet_group.add(bullet)  # Agregar la bala al grupo de balas

class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Cargar imagen del meteorito
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'meteorGrey_big1.png')).convert()
        self.image.set_colorkey(BLACK)  # Hace el fondo negro transparente
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH - self.rect.width)  # Posición aleatoria
        self.rect.y = random.randint(-100, -40)  # Aparece fuera de la pantalla
        self.speedy = random.randint(2, 5)  # Velocidad de caída más lenta

    def update(self):
        """Mueve el meteorito hacia abajo y lo reinicia si sale de la pantalla"""
        self.rect.y += self.speedy

        # Si el meteorito sale de la pantalla, reaparece arriba con nueva posición
        if self.rect.top > HEIGHT:
            self.rect.x = random.randint(0, WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speedy = random.randint(2, 5)
            
        

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        # Cargar imagen de la bala
        self.image = pygame.image.load(os.path.join(IMAGE_DIR, 'laser.png')).convert()
        self.image = pygame.transform.scale(self.image, (10, 10))
        self.image.set_colorkey(WHITE)  # Hace el fondo blanco transparente
        self.rect = self.image.get_rect()
        self.rect.centerx = x  # Posición inicial en X
        self.rect.top = y  # Posición inicial en Y
        self.speedy = -8  # Velocidad más lenta para que se vea mejor

    def update(self):
        """Mueve la bala hacia arriba y la elimina si sale de la pantalla"""
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()  # Eliminar la bala si sale de la pantalla

# Cargar fondo
background = pygame.image.load(os.path.join(IMAGE_DIR, 'background.png')).convert()

# Crear los grupos de sprites
all_sprites = pygame.sprite.Group()
bullet_group = pygame.sprite.Group()  # Crear un grupo para las balas
meteor_list = pygame.sprite.Group()

# Crear el jugador y añadirlo al grupo de sprites
player = Player()
all_sprites.add(player)

# Crear meteoritos y añadirlos a los grupos
for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)
    
hits = pygame.sprite.groupcollide(meteor_list,bullet_group, True, True)
for hit in hits:
    score +=1
    new_meteor = Meteor()
    all_sprites.add(new_meteor)
    meteor_list.add(new_meteor)

running = True
while running:
    clock.tick(60)
    
    # Procesar eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Disparo cuando se presiona la barra espaciadora
                player.shoot(all_sprites, bullet_group)  # Disparar una bala

    # Actualizar los sprites
    all_sprites.update()

    # Dibujar el fondo
    screen.blit(background, [0, 0])

    # Dibujar todos los sprites en la pantalla
    all_sprites.draw(screen)

    # Actualizar la pantalla
    pygame.display.flip()

pygame.quit()

