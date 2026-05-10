import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Platformer")

# Colors
WHITE = (255, 255, 255)
BLUE = (100, 149, 237)
GREEN = (34, 177, 76)
RED = (200, 50, 50)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player settings
player_width = 40
player_height = 60
player_x = 100
player_y = HEIGHT - 200
player_speed = 5
jump_strength = -15
gravity = 0.8
velocity_y = 0
on_ground = False

# Platforms
platforms = [
    pygame.Rect(0, HEIGHT - 40, WIDTH, 40),
    pygame.Rect(200, 450, 150, 20),
    pygame.Rect(450, 350, 150, 20),
    pygame.Rect(650, 250, 100, 20),
]

# Goal
goal = pygame.Rect(720, 190, 40, 60)

# Font
font = pygame.font.SysFont(None, 48)

# Game loop
running = True
won = False

while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if not won:
        # Movement input
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            player_x -= player_speed

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            player_x += player_speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
            velocity_y = jump_strength
            on_ground = False

        # Apply gravity
        velocity_y += gravity
        player_y += velocity_y

        # Player rectangle
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

        # Collision detection
        on_ground = False

        for platform in platforms:
            if player_rect.colliderect(platform) and velocity_y >= 0:
                if player_rect.bottom <= platform.bottom:
                    player_y = platform.top - player_height
                    velocity_y = 0
                    on_ground = True
                    player_rect.y = player_y

        # Prevent falling off screen
        if player_y > HEIGHT:
            player_x = 100
            player_y = HEIGHT - 200
            velocity_y = 0

        # Keep player inside screen
        player_x = max(0, min(WIDTH - player_width, player_x))

        # Check win condition
        if player_rect.colliderect(goal):
            won = True

    # Draw everything
    screen.fill(BLUE)

    # Draw platforms
    for platform in platforms:
        pygame.draw.rect(screen, GREEN, platform)

    # Draw goal
    pygame.draw.rect(screen, RED, goal)

    # Draw player
    pygame.draw.rect(screen, BLACK, (player_x, player_y, player_width, player_height))

    # Win message
    if won:
        text = font.render("You Win!", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 100, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
