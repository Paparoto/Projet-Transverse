import pygame
import sys
import os


def save_settings(volume):
    with open("settings.txt", "w") as file:
        file.write(f"volume={volume}\n")


def load_settings():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as file:
            for line in file:
                if line.startswith("volume="):
                    return float(line.strip().split("=")[1])
    return 0.5


def options_menu(screen):
    font = pygame.font.Font(None, 60)
    clock = pygame.time.Clock()

    back_text = font.render("BACK", True, (255, 255, 255))
    save_text = font.render("SAVE", True, (255, 255, 255))

    back_rect = pygame.Rect(860, 800, 200, 80)
    save_rect = pygame.Rect(860, 650, 200, 80)

    volume = load_settings()
    pygame.mixer.music.set_volume(volume)

    running = True
    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        # Titre
        options_title = font.render("OPTIONS", True, (255, 255, 255))
        screen.blit(options_title, (850, 100))

        # Affichage du texte du volume centré
        volume_text = font.render(f"VOLUME: {int(volume * 100)}%", True, (255, 255, 255))
        volume_rect = volume_text.get_rect(center=(960, 300))
        screen.blit(volume_text, volume_rect)

        # Position de base des flèches (80 pixels de chaque côté du texte)
        left_arrow_pos = (volume_rect.left - 80, volume_rect.centery)
        right_arrow_pos = (volume_rect.right + 80, volume_rect.centery)

        # Couleur par défaut des flèches
        left_arrow_color = (255, 255, 255)
        right_arrow_color = (255, 255, 255)

        # Création des surfaces et rectangles pour les flèches
        left_arrow_surface = font.render("<", True, left_arrow_color)
        right_arrow_surface = font.render(">", True, right_arrow_color)
        left_arrow_rect = left_arrow_surface.get_rect(center=left_arrow_pos)
        right_arrow_rect = right_arrow_surface.get_rect(center=right_arrow_pos)

        # Surbrillance en gris lorsque la souris survole les flèches
        if left_arrow_rect.collidepoint(mouse_pos):
            left_arrow_color = (150, 150, 150)
        if right_arrow_rect.collidepoint(mouse_pos):
            right_arrow_color = (150, 150, 150)

        # Recréation des surfaces avec la couleur de surbrillance si besoin
        left_arrow_surface = font.render("<", True, left_arrow_color)
        right_arrow_surface = font.render(">", True, right_arrow_color)
        left_arrow_rect = left_arrow_surface.get_rect(center=left_arrow_pos)
        right_arrow_rect = right_arrow_surface.get_rect(center=right_arrow_pos)

        # Variables pour l'effet de clic (offset)
        left_pressed = False
        right_pressed = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False
                elif save_rect.collidepoint(event.pos):
                    save_settings(volume)
                elif left_arrow_rect.collidepoint(event.pos):
                    left_pressed = True
                    volume = max(0.0, volume - 0.05)
                    pygame.mixer.music.set_volume(volume)
                elif right_arrow_rect.collidepoint(event.pos):
                    right_pressed = True
                    volume = min(1.0, volume + 0.05)
                    pygame.mixer.music.set_volume(volume)

        # Décalage vertical pour simuler l'effet de clic
        if left_pressed:
            left_arrow_rect = left_arrow_rect.move(0, 3)
        if right_pressed:
            right_arrow_rect = right_arrow_rect.move(0, 3)

        # Affichage des flèches
        screen.blit(left_arrow_surface, left_arrow_rect)
        screen.blit(right_arrow_surface, right_arrow_rect)

        # Bouton BACK
        back_color = (100, 100, 100) if back_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, back_color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Bouton SAVE
        save_color = (100, 100, 100) if save_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, save_color, save_rect, border_radius=10)
        save_text_rect = save_text.get_rect(center=save_rect.center)
        screen.blit(save_text, save_text_rect)

        pygame.display.flip()
        clock.tick(60)


def main_menu():
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Menu Principal")
    font = pygame.font.Font(None, 80)
    clock = pygame.time.Clock()

    background_image = pygame.image.load("Tileset/Pikache_resized.jpg")
    background_image = pygame.transform.scale(background_image, (1920, 1080))

    pygame.mixer.music.load("Tileset/Lavanville_Musique_trimmed.mp3")
    pygame.mixer.music.set_volume(0.5)
    pygame.mixer.music.play(-1)

    title_text = font.render("DESTRUCTION", True, (255, 255, 255))
    play_text = font.render("GAME", True, (255, 255, 255))
    options_text = font.render("OPTIONS", True, (255, 255, 255))
    quit_text = font.render("QUIT", True, (255, 255, 255))

    title_rect = title_text.get_rect(center=(960, 250))
    play_rect = pygame.Rect(810, 450, 300, 100)
    options_rect = pygame.Rect(810, 600, 300, 100)
    quit_rect = pygame.Rect(810, 750, 300, 100)

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        screen.blit(title_text, title_rect)

        mouse_pos = pygame.mouse.get_pos()

        for rect, text in [(play_rect, play_text), (options_rect, options_text), (quit_rect, quit_text)]:
            color = (100, 100, 100) if rect.collidepoint(mouse_pos) else (50, 50, 50)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    running = False
                elif options_rect.collidepoint(event.pos):
                    options_menu(screen)
                elif quit_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)