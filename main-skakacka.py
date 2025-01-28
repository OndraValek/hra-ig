import pygame
import random
import sys

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Skákací plošinovka")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# FPS
clock = pygame.time.Clock()
FPS = 60

# Hráč
player_width, player_height = 30, 30
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - player_height - 60
player_speed_x = 5
player_velocity_y = 0
gravity = 0.5
jump_strength = -10

# Plošiny
platform_width, platform_height = 80, 10
platforms = [
    pygame.Rect(WIDTH // 2 - platform_width // 2, HEIGHT - 50, platform_width, platform_height)
]
for _ in range(5):
    platforms.append(
        pygame.Rect(random.randint(0, WIDTH - platform_width),
                    random.randint(0, HEIGHT - platform_height),
                    platform_width, platform_height)
    )

# Skóre
score = 0
font = pygame.font.Font(None, 36)

def reset_player():
    """Resetuje pozici hráče na startovní plošinu."""
    global player_x, player_y, player_velocity_y
    player_x = WIDTH // 2 - player_width // 2
    player_y = HEIGHT - player_height - 60
    player_velocity_y = 0

# Hlavní smyčka hry
def main():
    global player_x, player_y, player_velocity_y, platforms, score

    reset_player()  # Reset hráče na začátku
    running = True

    while running:
        screen.fill(WHITE)

        # Události
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pohyb hráče
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed_x
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed_x

        # Gravitace a pohyb
        player_velocity_y += gravity
        player_y += player_velocity_y

        # Kolize s plošinami
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        for platform in platforms:
            if player_rect.colliderect(platform) and player_velocity_y > 0:
                player_velocity_y = jump_strength

        # Posun plošin a generování nových
        if player_y < HEIGHT // 2:
            player_y = HEIGHT // 2
            for platform in platforms:
                platform.y += abs(player_velocity_y)
                if platform.y > HEIGHT:
                    platform.x = random.randint(0, WIDTH - platform_width)
                    platform.y = random.randint(-50, -10)
                    score += 10

        # Prohra (pád dolů)
        if player_y > HEIGHT:
            print(f"Konec hry! Skóre: {score}")
            running = False

        # Vykreslení hráče
        pygame.draw.rect(screen, GREEN, player_rect)

        # Vykreslení plošin
        for platform in platforms:
            pygame.draw.rect(screen, BLUE, platform)

        # Zobrazení skóre
        score_text = font.render(f"Skóre: {score}", True, BLACK)
        screen.blit(score_text, (10, 10))

        # Aktualizace snímků
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
    pygame.quit()
