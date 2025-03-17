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
    save_message_time = None  # Temps de début de l'affichage du message
    fade_alpha = 0  # Opacité du message "SETTING SAVE"

    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        options_title = font.render("OPTIONS", True, (255, 255, 255))
        screen.blit(options_title, (850, 100))

        volume_text = font.render(f"VOLUME: {int(volume * 100)}%", True, (255, 255, 255))
        volume_rect = volume_text.get_rect(center=(960, 300))
        screen.blit(volume_text, volume_rect)

        left_arrow_pos = (volume_rect.left - 80, volume_rect.centery)
        right_arrow_pos = (volume_rect.right + 80, volume_rect.centery)

        left_arrow_surface = font.render("<", True, (255, 255, 255))
        right_arrow_surface = font.render(">", True, (255, 255, 255))
        left_arrow_rect = left_arrow_surface.get_rect(center=left_arrow_pos)
        right_arrow_rect = right_arrow_surface.get_rect(center=right_arrow_pos)

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

                    # Déclencher l'affichage du message "SETTING SAVE"
                    save_message_time = pygame.time.get_ticks()
                    fade_alpha = 255  # Opacité maximale au début
                elif left_arrow_rect.collidepoint(event.pos):
                    left_pressed = True
                    volume = round(max(0.0, volume - 0.05), 2)
                    pygame.mixer.music.set_volume(volume)
                elif right_arrow_rect.collidepoint(event.pos):
                    right_pressed = True
                    volume = round(min(1.0, volume + 0.05), 2)
                    pygame.mixer.music.set_volume(volume)

        if left_pressed:
            left_arrow_rect = left_arrow_rect.move(0, 3)
        if right_pressed:
            right_arrow_rect = right_arrow_rect.move(0, 3)

        screen.blit(left_arrow_surface, left_arrow_rect)
        screen.blit(right_arrow_surface, right_arrow_rect)

        back_color = (100, 100, 100) if back_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, back_color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        save_color = (100, 100, 100) if save_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, save_color, save_rect, border_radius=10)
        save_text_rect = save_text.get_rect(center=save_rect.center)
        screen.blit(save_text, save_text_rect)

        # Affichage de "SETTING SAVE" avec un effet de fondu
        if save_message_time is not None:
            elapsed_time = pygame.time.get_ticks() - save_message_time
            if elapsed_time < 2000:  # Affiche le message pendant 2 secondes
                save_message = font.render("SETTING SAVE", True, (255, 255, 255))
                fade_alpha = max(0, 255 - (255 * elapsed_time // 2000))  # Réduction progressive de l'opacité
                save_message.set_alpha(fade_alpha)  # Appliquer l'opacité
                save_message_rect = save_message.get_rect(center=(960, 500))
                screen.blit(save_message, save_message_rect)
            else:
                save_message_time = None  # Supprime le message après 2 secondes

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