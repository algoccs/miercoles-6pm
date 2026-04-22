from pygame import *
from random import *
from config import * # IMPORTAR MODULO DE CONFIGURACION
init()
font.init()
# mixer.init()

# PARAMETROS INICIALES
points = 0
fallos = 0
vidas = 3

# TRABAJO CON FUENTE
font_1 = font.Font(FONT_FILE, 20)

# GUI
screen = display.set_mode((WIDTH, HEIGHT))
display.set_caption(TITLE)

background = transform.scale(image.load(BACK_IMG), (WIDTH, HEIGHT))

class GameSprite(sprite.Sprite):
    def __init__(self, img, cord_x, cord_y, width, height, speed=0):
        super().__init__()
        self.width = width
        self.height = height
        self.image = transform.scale(image.load(img), (self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = cord_x
        self.rect.y = cord_y
        self.speed = speed

    def reset(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_d] and self.rect.x <= WIDTH -self.rect.width:
            self.rect.x += self.speed
        elif keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        
    def shoot(self):
        bullet =  Bullet(ENEMY_IMG, self.rect.centerx, self.rect.top, 10, 15, 5)
        balas.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global fallos
        self.rect.y += self.speed
        if self.rect.y >= HEIGHT:
            self.rect.y = -self.height
            self.rect.x = randint(0, WIDTH - 60)
            self.speed = randint(1, 5)
            fallos += 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill() # remueve el sprite del grupo

# OBJETOS
player = Player(PLAYER_IMG, (WIDTH - 60) // 2, HEIGHT - 60, 60, 60, 5)

# Grupo de objetos
aliens = sprite.Group()
for i in range(5):
    enemy = Enemy(ENEMY_IMG, randint(0, WIDTH - 60), -60, 60, 60, randint(1, 5))
    aliens.add(enemy)

balas = sprite.Group()

# CICLO DE JUEGO
run = True # ESTADO INICIAL
finish = False
clock = time.Clock()

while run:
    # EVENTS
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_r:
                finish = False
            if e.key == K_SPACE:
                player.shoot()

    if not finish:
        screen.blit(background, (0, 0))
        points_text = font_1.render(f'POINTS: {points}', 1, WHITE)
        screen.blit(points_text, (20, 20))
        misses_text = font_1.render(f'MISSES: {fallos}', 1, WHITE)
        screen.blit(misses_text, (20, 50))
        vidas_text = font_1.render(f'VIDAS: {vidas}', 1, WHITE)
        screen.blit(vidas_text, (550, 20))

        player.reset()
        player.update()

        # enemy.reset() # Solo para objetos individuales
        aliens.draw(screen) # renderizar sprites de un grupo
        aliens.update()
        balas.draw(screen)
        balas.update()

    # LOGICA DE COLISION ENTRE GRUPOS DE SPRITES
        if sprite.groupcollide(aliens, balas, True, True):
            points += 1
            enemy = Enemy(ENEMY_IMG, randint(0, WIDTH - 60), -60, 60, 60, randint(1, 5))
            aliens.add(enemy)
    # COLISION ENTRE SPRITE Y GRUPO
        if sprite.spritecollide(player, aliens, True):
            vidas -= 1
            enemy = Enemy(ENEMY_IMG, randint(0, WIDTH - 60), -60, 60, 60, randint(1, 5))
            aliens.add(enemy)

    # condicion de derrota
        if fallos == 10 or vidas == 0:
            finish = True
            screen.fill(BLACK)
            gameover = transform.scale(image.load(GAMEOVER_IMG), (WIDTH, HEIGHT))
            screen.blit(gameover, (0, 0))

    # condicion de victoria
        if points >= 20:
            finish = True
            screen.fill(BLACK)
            # ... renderizar la pantalla de victoria



    # NO SE TOCA!!!
    display.update()
    clock.tick(FPS)

quit()
