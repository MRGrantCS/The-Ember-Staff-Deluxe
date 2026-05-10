import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH = 900
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Strategy Game")

# Colors
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BLUE = (50, 100, 255)
RED = (200, 50, 50)
DARK_GREEN = (20, 120, 20)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Map settings
TILE_SIZE = 40
MAP_WIDTH = WIDTH // TILE_SIZE
MAP_HEIGHT = HEIGHT // TILE_SIZE

# Unit settings
unit_size = 24
unit_speed = 2

# Font
font = pygame.font.SysFont(None, 32)


class Unit:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.selected = False
        self.target_x = x
        self.target_y = y
        self.health = 100

    def update(self):
        dx = self.target_x - self.x
        dy = self.target_y - self.y
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance > 1:
            self.x += (dx / distance) * unit_speed
            self.y += (dy / distance) * unit_speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color,
                         (self.x - unit_size // 2,
                          self.y - unit_size // 2,
                          unit_size,
                          unit_size))

        # Selection outline
        if self.selected:
            pygame.draw.rect(surface, WHITE,
                             (self.x - unit_size // 2 - 2,
                              self.y - unit_size // 2 - 2,
                              unit_size + 4,
                              unit_size + 4), 2)

        # Health bar
        pygame.draw.rect(surface, RED,
                         (self.x - 15, self.y - 24, 30, 5))
        pygame.draw.rect(surface, GREEN,
                         (self.x - 15, self.y - 24,
                          30 * (self.health / 100), 5))

    def contains_point(self, pos):
        rect = pygame.Rect(
            self.x - unit_size // 2,
            self.y - unit_size // 2,
            unit_size,
            unit_size
        )
        return rect.collidepoint(pos)


# Create player units
player_units = [
    Unit(100, 100, BLUE),
    Unit(160, 100, BLUE),
    Unit(220, 100, BLUE)
]

# Create enemy units
enemy_units = []
for i in range(5):
    enemy_units.append(
        Unit(random.randint(500, 850),
             random.randint(100, 500),
             RED)
    )

selected_unit = None

# Main game loop
running = True
while running:
    clock.tick(FPS)

    # Events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Mouse controls
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Left click selects units
            if event.button == 1:
                selected_unit = None

                for unit in player_units:
                    unit.selected = False

                    if unit.contains_point(mouse_pos):
                        unit.selected = True
                        selected_unit = unit

            # Right click moves selected unit
            if event.button == 3 and selected_unit:
                selected_unit.target_x = mouse_pos[0]
                selected_unit.target_y = mouse_pos[1]

    # Update units
    for unit in player_units:
        unit.update()

    # Simple enemy movement
    for enemy in enemy_units:
        if random.randint(0, 100) < 2:
            enemy.target_x = random.randint(0, WIDTH)
            enemy.target_y = random.randint(0, HEIGHT)

        enemy.update()

    # Combat system
    for player in player_units:
        for enemy in enemy_units:
            distance = ((player.x - enemy.x) ** 2 +
                        (player.y - enemy.y) ** 2) ** 0.5

            if distance < 40:
                player.health -= 0.1
                enemy.health -= 0.1

    # Remove defeated units
    player_units = [u for u in player_units if u.health > 0]
    enemy_units = [u for u in enemy_units if u.health > 0]

    # Draw background grid
    screen.fill(DARK_GREEN)

    for x in range(0, WIDTH, TILE_SIZE):
        pygame.draw.line(screen, BLACK, (x, 0), (x, HEIGHT), 1)

    for y in range(0, HEIGHT, TILE_SIZE):
        pygame.draw.line(screen, BLACK, (0, y), (WIDTH, y), 1)

    # Draw units
    for unit in player_units:
        unit.draw(screen)

    for enemy in enemy_units:
        enemy.draw(screen)

    # UI text
    controls_text = font.render(
        "Left Click: Select Unit | Right Click: Move Unit",
        True,
        WHITE
    )
    screen.blit(controls_text, (10, 10))

    # Win/Lose conditions
    if len(enemy_units) == 0:
        win_text = font.render("Victory!", True, WHITE)
        screen.blit(win_text, (WIDTH // 2 - 60, HEIGHT // 2))

    if len(player_units) == 0:
        lose_text = font.render("Defeat!", True, WHITE)
        screen.blit(lose_text, (WIDTH // 2 - 60, HEIGHT // 2))

    pygame.display.flip()

pygame.quit()
sys.exit()
