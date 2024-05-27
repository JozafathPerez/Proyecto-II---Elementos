import pygame
import random
import os

# Inicializar pygame
pygame.init()

# Definir constantes
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

class Player(pygame.sprite.Sprite):
    def __init__(self, control_keys):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'player.png')).convert()
        self.image.set_colorkey((0, 0, 0))  # Color transparente
        self.rect = self.image.get_rect()
        self.rect.centerx = SCREEN_WIDTH // 2
        self.rect.bottom = SCREEN_HEIGHT - 10
        self.speed_x = 0
        self.control_keys = control_keys

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[self.control_keys['left']]:
            self.rect.x -= 5
        if keys[self.control_keys['right']]:
            self.rect.x += 5
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'enemy.png')).convert()
        self.image.set_colorkey((0, 0, 0))  # Color transparente
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > SCREEN_HEIGHT + 10:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load(os.path.join('assets', 'bullet.png')).convert()
        self.image.set_colorkey((0, 0, 0))  # Color transparente
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed_y = -10

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.bottom < 0:
            self.kill()

def load_images():
    player_image = pygame.image.load(os.path.join('assets', 'player.png')).convert()
    player_image.set_colorkey((0, 0, 0))  # Color transparente
    enemy_image = pygame.image.load(os.path.join('assets', 'enemy.png')).convert()
    enemy_image.set_colorkey((0, 0, 0))  # Color transparente
    bullet_image = pygame.image.load(os.path.join('assets', 'bullet.png')).convert()
    bullet_image.set_colorkey((0, 0, 0))  # Color transparente
    return player_image, enemy_image, bullet_image

def load_sounds():
    shoot_sound = pygame.mixer.Sound(os.path.join('assets', 'shoot.wav'))
    explosion_sound = pygame.mixer.Sound(os.path.join('assets', 'explosion.wav'))
    return shoot_sound, explosion_sound

def show_menu():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space Invaders - Menú Principal')

    font = pygame.font.Font(None, 36)
    menu_items = ['Jugar Individual', 'Jugar Multijugador', 'Highscores', 'Ayuda', 'Salir']
    menu_y = SCREEN_HEIGHT // 2 - len(menu_items) * 20

    selected_item = 0

    while True:
        screen.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected_item = (selected_item - 1) % len(menu_items)
                elif event.key == pygame.K_DOWN:
                    selected_item = (selected_item + 1) % len(menu_items)
                elif event.key == pygame.K_RETURN:
                    if selected_item == 0:
                        main('individual')
                    elif selected_item == 1:
                        main('multijugador')
                    elif selected_item == 2:
                        show_highscores()
                    elif selected_item == 3:
                        show_help()
                    elif selected_item == 4:
                        pygame.quit()
                        quit()

        for i, item in enumerate(menu_items):
            color = (255, 255, 255) if i == selected_item else (128, 128, 128)
            text_surface = font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, menu_y + i * 40))
            screen.blit(text_surface, text_rect)

        pygame.display.flip()

def show_highscores():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Highscores')

    font = pygame.font.Font(None, 36)

    # Leer highscores desde archivo
    with open('highscores.txt', 'r') as file:
        highscores = file.read()

    highscores_text = font.render(highscores, True, (255, 255, 255))
    text_rect = highscores_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(highscores_text, text_rect)

    pygame.display.flip()
    pygame.time.wait(3000)  # Mostrar highscores durante 3 segundos
    show_menu()  # Volver al menú principal después de mostrar highscores

def show_help():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Ayuda')

    font = pygame.font.Font(None, 36)
    help_text = [
        'Controles:',
        'Modo Individual:',
        '   - Flecha Izquierda: Mover a la izquierda',
        '   - Flecha Derecha: Mover a la derecha',
        '   - CTRL derecho para disparar',
        'Modo Multijugador:',
        '   - Jugador 1: Flecha Izquierda y Derecha',
        '   - Dispara con CTRL derecho',
        '   - Jugador 2: A y D',
        '   - Dispara con el espacio',
        '',
        'Objetivo: Eliminar a todos los enemigos sin ser golpeado.',
        '',
        'Presiona cualquier tecla para volver al menú principal.'
    ]

    screen.fill((0, 0, 0))

    for i, line in enumerate(help_text):
        text_surface = font.render(line, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 50 + i * 30))
        screen.blit(text_surface, text_rect)

    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                show_menu()  # Volver al menú principal al presionar cualquier tecla


def main(mode):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Space Invaders')

    clock = pygame.time.Clock()
    all_sprites = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()

    player_image, enemy_image, bullet_image = load_images()
    shoot_sound, explosion_sound = load_sounds()

    if mode == 'individual':
        player1 = Player({'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_RCTRL})
        all_sprites.add(player1)
    elif mode == 'multijugador':
        player1 = Player({'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'shoot': pygame.K_RCTRL})
        player2 = Player({'left': pygame.K_a, 'right': pygame.K_d, 'shoot': pygame.K_SPACE})  # Tecla de espacio para disparar
        all_sprites.add(player1, player2)
    else:
        raise ValueError("Modo de juego no válido")

    for _ in range(8):
        enemy = Enemy()
        all_sprites.add(enemy)
        enemies.add(enemy)

    running = True
    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RCTRL:  # Disparo jugador 1 (tecla de espacio)
                    bullet = Bullet(player1.rect.centerx, player1.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()
                elif event.key == pygame.K_SPACE:  # Disparo jugador 2 (tecla de espacio)
                    bullet = Bullet(player2.rect.centerx, player2.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    shoot_sound.play()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for hit in hits:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
            explosion_sound.play()

        hits = pygame.sprite.spritecollide(player1, enemies, False)
        if hits:
            running = False  # Game Over

        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    show_menu()


if __name__ == '__main__':
    show_menu()

