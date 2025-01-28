import pygame
import random
import sys

# Inicializace Pygame
pygame.init()

# Rozměry obrazovky
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Barvy
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Nastavení FPS
clock = pygame.time.Clock()
FPS = 60

# Loď hráče
player_width, player_height = 50, 20
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT - 60
player_speed = 7

# Střely hráče
bullet_width, bullet_height = 5, 15
bullets = []
bullet_speed = 10

# Nepřátelé
enemy_width, enemy_height = 40, 30
enemies = []
enemy_speed = 2
enemy_spawn_rate = 30  # Jak často se spawnují nepřátelé (v počtu snímků)

# Skóre
score = 0
font = pygame.font.Font(None, 36)

# Hlavní smyčka hry
def main():
    global player_x, player_y, bullets, enemies, score

    running = True
    frame_count = 0

    while running:
        screen.fill(BLACK)

        # Události
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Pohyb hráče
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
            player_x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:  # Maximálně 5 střel na obrazovce
                bullets.append(pygame.Rect(player_x + player_width // 2 - bullet_width // 2, player_y, bullet_width, bullet_height))

        # Pohyb střel
        for bullet in bullets[:]:
            bullet.y -= bullet_speed
            if bullet.y < 0:
                bullets.remove(bullet)

        # Spawn nepřátel
        if frame_count % enemy_spawn_rate == 0:
            enemy_x = random.randint(0, WIDTH - enemy_width)
            enemies.append(pygame.Rect(enemy_x, 0, enemy_width, enemy_height))

        # Pohyb nepřátel
        for enemy in enemies[:]:
            enemy.y += enemy_speed
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                score -= 1  # Ztráta bodu, pokud nepřítel projde

        # Kolize střel a nepřátel
        for bullet in bullets[:]:
            for enemy in enemies[:]:
                if bullet.colliderect(enemy):
                    bullets.remove(bullet)
                    enemies.remove(enemy)
                    score += 10  # Body za zničení nepřítele

        # Vykreslování hráče
        player_rect = pygame.Rect(player_x, player_y, player_width, player_height)
        pygame.draw.rect(screen, GREEN, player_rect)

        # Vykreslování střel
        for bullet in bullets:
            pygame.draw.rect(screen, YELLOW, bullet)

        # Vykreslování nepřátel
        for enemy in enemies:
            pygame.draw.rect(screen, RED, enemy)

        # Zobrazení skóre
        score_text = font.render(f"Skóre: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        # Kontrola prohry
        for enemy in enemies:
            if enemy.colliderect(player_rect):
                print("Prohráli jste!")
                running = False

        # Aktualizace snímků
        pygame.display.flip()
        clock.tick(FPS)
        frame_count += 1

if __name__ == "__main__":
    main()
    pygame.quit()
