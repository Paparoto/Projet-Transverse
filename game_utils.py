import pygame
import sys
import os


def display_screamer(screen):
    screamer_image = pygame.image.load("Tileset/hq720.jpg")
    screamer_sound = pygame.mixer.Sound("Tileset/Jumpscare-Sound-Trimmed-Final.wav")
    screamer_sound.play()

    screen.fill((0, 0, 0))
    screamer_image = pygame.transform.scale(screamer_image, (screen.get_width(), screen.get_height()))
    screen.blit(screamer_image, (0, 0))
    pygame.display.flip()

    pygame.time.delay(2000)

    return False


def options_menu(screen):
    font = pygame.font.Font(None, 60)
    clock = pygame.time.Clock()

    back_text = font.render("BACK", True, (255, 255, 255))
    save_text = font.render("SAVE", True, (255, 255, 255))
    resolution_text = font.render("RESOLUTION", True, (255, 255, 255))
    quit_text = font.render("QUIT", True, (255, 255, 255))

    back_rect = pygame.Rect(860, 800, 200, 80)
    save_rect = pygame.Rect(860, 650, 200, 80)
    resolution_rect = pygame.Rect(860, 500, 200, 80)
    quit_rect = pygame.Rect(860, 350, 200, 80)

    volume = load_settings()
    pygame.mixer.music.set_volume(volume)

    running = True
    while running:
        screen.fill((30, 30, 30))
        mouse_pos = pygame.mouse.get_pos()

        options_title = font.render("OPTIONS", True, (255, 255, 255))
        screen.blit(options_title, (850, 100))

        buttons = [(back_rect, back_text), (save_rect, save_text), (resolution_rect, resolution_text),
                   (quit_rect, quit_text)]

        for rect, text in buttons:
            color = (100, 100, 100) if rect.collidepoint(mouse_pos) else (50, 50, 50)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False
                elif save_rect.collidepoint(event.pos):
                    save_settings(volume)
                elif resolution_rect.collidepoint(event.pos):
                    running = display_screamer(screen)
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)


# Fonction pour sauvegarder le volume dans un fichier
def save_settings(volume):
    with open("settings.txt", "w") as file:
        file.write(f"volume={volume}\n")


# Fonction pour charger le volume depuis un fichier
def load_settings():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as file:
            for line in file:
                if line.startswith("volume="):
                    return float(line.strip().split("=")[1])
    return 0.1  # Valeur par défaut si le fichier n'existe pas
