import pygame
import random
from pygame import Rect


pygame.init()


WIDTH, HEIGHT = 800, 600
PLAYER_COLOR = (205, 92, 92)
ENEMY_COLOR = (139, 0, 0)
BULLET_COLOR = (255, 215, 0)
WALL_COLOR = (128, 128, 128)
BACKGROUND_COLOR = (0, 0, 0)
EXIT_COLOR = (0, 255, 0)


window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('game for 0iq kids...')


walls = [
    Rect(50, 100, 600, 20),
    Rect(100, 100, 20, 400),
    Rect(100, 500, 600, 20),
    Rect(700, 100, 20, 400),
    Rect(300, 200, 20, 200),
    Rect(200, 300, 100, 20),
    Rect(300, 300, 20, 100),
    Rect(400, 300, 20, 100),
    Rect(500, 300, 100, 20),
]


class Player:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 30, 30)  
        self.speed = 5
        self.x_speed = 0
        self.y_speed = 0

    def move(self):
        new_rect = self.rect.move(self.x_speed, self.y_speed)
        
        
        collide = False
        for wall in walls:
            if new_rect.colliderect(wall):
                collide = True
                break
                
        if not collide and 0 <= new_rect.x <= WIDTH - self.rect.width and 0 <= new_rect.y <= HEIGHT - self.rect.height:
            self.rect = new_rect

    def fire(self):
        bullet = Bullet(self.rect.right, self.rect.centery, 10)
        bullets.append(bullet)


class Enemy:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 40, 40)  
        self.speed = random.choice([-2, -1, 1, 2])

    def move(self):
        self.rect.x += self.speed
        
        if self.rect.x < 0 or self.rect.x > WIDTH - self.rect.width:
            self.speed = -self.speed
        for wall in walls:
            if self.rect.colliderect(wall):
                self.speed = -self.speed
                break


class Bullet:
    def __init__(self, x, y, dx):
        self.rect = Rect(x, y, 10, 5)  
        self.dx = dx

    def move(self):
        self.rect.x += self.dx
        
        return self.rect.x > WIDTH


player = Player(50, 50)
enemies = [Enemy(random.randint(150, WIDTH-150), random.randint(150, HEIGHT-150)) for _ in range(5)]
bullets = []
exit_rect = Rect(WIDTH - 70, HEIGHT - 70, 50, 50)  


clock = pygame.time.Clock()
running = True
game_over = False
win = False

while running:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            elif event.key == pygame.K_LEFT:
                player.x_speed = -player.speed
            elif event.key == pygame.K_RIGHT:
                player.x_speed = player.speed
            elif event.key == pygame.K_UP:
                player.y_speed = -player.speed
            elif event.key == pygame.K_DOWN:
                player.y_speed = player.speed
            elif event.key == pygame.K_SPACE:
                player.fire()
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player.x_speed = 0
            elif event.key in (pygame.K_UP, pygame.K_DOWN):
                player.y_speed = 0

    if not game_over and not win:
        
        player.move()
        for enemy in enemies:
            enemy.move()
        
        
        bullets = [bullet for bullet in bullets if not bullet.move()]
        
        
        for enemy in enemies[:]:
            if player.rect.colliderect(enemy.rect):
                game_over = True
        
        
        if player.rect.colliderect(exit_rect):
            win = True

    
    window.fill(BACKGROUND_COLOR)
    
    
    for wall in walls:
        pygame.draw.rect(window, WALL_COLOR, wall)
    
    
    pygame.draw.rect(window, EXIT_COLOR, exit_rect)
    
    pygame.draw.rect(window, PLAYER_COLOR, player.rect)
    
    for enemy in enemies:
        pygame.draw.rect(window, ENEMY_COLOR, enemy.rect)
    
    for bullet in bullets:
        pygame.draw.rect(window, BULLET_COLOR, bullet.rect)
    
    if game_over:
        font = pygame.font.SysFont(None, 72)
        text = font.render("GAME OVER", True, (255, 0, 0))
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    
    if win:
        font = pygame.font.SysFont(None, 72)
        text = font.render("YOU WIN!", True, (0, 255, 0))
        window.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
font = font.SysFont('Arial', 40)