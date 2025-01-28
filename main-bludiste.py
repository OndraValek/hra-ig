import pygame
import random
import sys

# Inicializace Pygame
pygame.init()

# Nastavení obrazovky
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Bludiště s časem")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Časovač
FONT = pygame.font.Font(None, 36)
time_limit = 30  # Sekundy
clock = pygame.time.Clock()

# Hráč
player_size = 20
player_x, player_y = 50, 50
player_speed = 5

# Cíl
goal_size = 30
goal_x, goal_y = WIDTH - 50, HEIGHT - 50

# Power-upy
power_ups = []
for _ in range(5):
    power_ups.append((random.randint(50, WIDTH - 50), random.randint(50, HEIGHT - 50)))

# Překážky
walls = [
    pygame.Rect(200, 100, 400, 20),
    pygame.Rect(200, 200, 20, 200),
    pygame.Rect(400, 300, 20, 200),
    pygame.Rect(100, 400, 200, 20),
]

# Hlavní smyčka hry
def main():
    global time_limit
    player_rect = pygame.Rect(player_x, player_y, player_size, player_size)
    goal_rect = pygame.Rect(goal_x, goal_y, goal_size, goal_size)

    running = True
    start_ticks = pygame.time.get_ticks()

    while running:
        screen.fill(WHITE)

        # Vykreslení cílů, překážek a hráče
        pygame.draw.rect(screen, GREEN, goal_rect)
        for wall in walls:
            pygame.draw.rect(screen, BLACK, wall)
        for power_up in power_ups:
            pygame.draw.circle(screen, BLUE, power_up, 10)
        pygame.draw.rect(screen, RED, player_rect)

        # Aktualizace času
        seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        remaining_time = max(0, int(time_limit - seconds))
        time_text = FONT.render(f"Čas: {remaining_time}s", True, BLACK)
        screen.blit(time_text, (10, 10))

        if remaining_time <= 0:
            print("Prohráli jste!")
            running = False

        # Události
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pohyb hráče
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player_rect.y -= player_speed
        if keys[pygame.K_DOWN]:
            player_rect.y += player_speed
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        # Kolize s překážkami
        for wall in walls:
            if player_rect.colliderect(wall):
                if keys[pygame.K_UP]:
                    player_rect.y += player_speed
                if keys[pygame.K_DOWN]:
                    player_rect.y -= player_speed
                if keys[pygame.K_LEFT]:
                    player_rect.x += player_speed
                if keys[pygame.K_RIGHT]:
                    player_rect.x -= player_speed

        # Kolize s power-upy
        for power_up in power_ups[:]:
            if player_rect.colliderect(pygame.Rect(power_up[0] - 10, power_up[1] - 10, 20, 20)):
                power_ups.remove(power_up)
                time_limit += 5  # Přidá 5 sekund

        # Kontrola vítězství
        if player_rect.colliderect(goal_rect):
            print("Vyhráli jste!")
            running = False

        pygame.display.flip()
        clock.tick(30)

if __name__ == "__main__":
    main()
    pygame.quit()
