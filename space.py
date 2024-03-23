import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Attack")

# Load images
player_img = pygame.image.load("p.png")
player_img = pygame.transform.scale(player_img, (40, 40))
enemy_img = pygame.image.load("e.png")
enemy_img = pygame.transform.scale(enemy_img, (40, 40))
bullet_img = pygame.Surface((4, 12))  # Create a simple bullet image
bullet_img.fill((255, 0, 0))  # Fill bullet image with red color

# Load background image
background_img = pygame.image.load("s1.jpg")
background_img = pygame.transform.scale(background_img, (screen_width, screen_height))

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Define player attributes
player_rect = player_img.get_rect()
player_rect.x = 380
player_rect.y = 540
player_speed = 5

# Define enemy attributes
enemies = []
enemy_speed = 3
enemy_speed_increase = 0.05  # Speed increase per frame

# Define bullet attributes
bullets = []
bullet_speed = 8

# Define level
level = [
    "PPPPPPPPPPPPPPPPPPPP",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P                  P",
    "P    E          E  P",
    "P                  P",
    "P                  P",
    "P    E          E  P",
    "PPPPPPPPPPPPPPPPPPPP",
]

# Create enemies based on level
for y, row in enumerate(level):
    for x, char in enumerate(row):
        if char == "E":
            enemy_rect = enemy_img.get_rect()
            enemy_rect.x = x * 40
            enemy_rect.y = y * 40
            enemies.append(enemy_rect)

# Game loop
running = True
clock = pygame.time.Clock()
score = 0
font = pygame.font.Font(None, 36)

while running:
    screen.blit(background_img, (0, 0))  # Blit background image
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet_rect = bullet_img.get_rect()
                bullet_rect.centerx = player_rect.centerx
                bullet_rect.centery = player_rect.top
                bullets.append(bullet_rect)

    # Player movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT]:
        player_rect.x += player_speed

    # Ensure player stays within screen boundaries
    if player_rect.x < 0:
        player_rect.x = 0
    elif player_rect.x > screen_width - player_rect.width:
        player_rect.x = screen_width - player_rect.width

    # Enemy movement
    for enemy in enemies:
        enemy.y += enemy_speed
        if enemy.y > screen_height:
            enemy.y = 0
            enemy.x = random.randint(0, screen_width - enemy.width)
            score += 10

    # Increase enemy speed over time
    enemy_speed += enemy_speed_increase

    # Bullet movement
    for bullet in bullets:
        bullet.y -= bullet_speed
        if bullet.y < 0:
            bullets.remove(bullet)

    # Collision detection
    for enemy in enemies:
        for bullet in bullets:
            if enemy.colliderect(bullet):
                enemies.remove(enemy)
                bullets.remove(bullet)
                score += 50
        if player_rect.colliderect(enemy):
            print("Game Over")
            running = False

    # Draw level
    for y, row in enumerate(level):
        for x, char in enumerate(row):
            if char == "P":
                pygame.draw.rect(screen, BLACK, (x * 40, y * 40, 40, 40))

    # Draw player, enemies, and bullets
    screen.blit(player_img, player_rect)
    for enemy in enemies:
        screen.blit(enemy_img, enemy)
    for bullet in bullets:
        screen.blit(bullet_img, bullet)

    # Display score
    score_text = font.render("Score: " + str(score), True, (255, 255, 255))
    screen.blit(score_text, (50, 50))  # Adjusted position

    pygame.display.update()
    clock.tick(30)

pygame.quit()
