import pygame
import sys
import os
from Game import Game

def save_settings(volume):
    with open("settings.txt", "w") as file:
        file.write(f"volume={volume}\n")

def load_settings():
    if os.path.exists("settings.txt"):
        with open("settings.txt", "r") as file:
            for line in file:
                if line.startswith("volume="):
                    return float(line.strip().split("=")[1])
    return 0.1  # Valeur par défaut si le fichier n'existe pas


# Fonction pour afficher le screamer
def display_screamer(screen):
    screamer_image = pygame.image.load("Tileset/hq720.jpg")  # Assure-toi d'avoir cette image
    screamer_sound = pygame.mixer.Sound("Tileset/Jumpscare-Sound-Trimmed-Final.wav")  # Assure-toi d'avoir ce son
    screamer_sound.play()  # Jouer le son du screamer

    screen.fill((0, 0, 0))  # Remplir l'écran de noir
    screamer_image = pygame.transform.scale(screamer_image, (screen.get_width(), screen.get_height()))
    screen.blit(screamer_image, (0, 0))
    pygame.display.flip()

    pygame.time.delay(2000)  # Laisser l'image afficher pendant 2 secondes (ajuste cette durée si nécessaire)

    # Après un délai, retourner au menu principal
    return False


def options_menu(screen):
    font = pygame.font.Font(None, 60)
    clock = pygame.time.Clock()

    back_text = font.render("BACK", True, (255, 255, 255))
    save_text = font.render("SAVE", True, (255, 255, 255))
    resolution_text = font.render("RESOLUTION", True, (255, 255, 255))

    back_rect = pygame.Rect(860, 800, 200, 80)
    save_rect = pygame.Rect(860, 650, 200, 80)
    resolution_rect = pygame.Rect(860, 500, 200, 80)

    volume = load_settings()  # Charger le volume depuis le fichier
    pygame.mixer.music.set_volume(volume)

    running = True
    while running:
        screen.fill((30, 30, 30))  # Fond sombre
        mouse_pos = pygame.mouse.get_pos()

        # Afficher "Options"
        options_title = font.render("OPTIONS", True, (255, 255, 255))
        screen.blit(options_title, (850, 100))

        # Afficher le volume
        volume_text = font.render(f"VOLUME: {int(volume * 100)}%", True, (255, 255, 255))
        screen.blit(volume_text, (850, 300))

        # Affichage des boutons
        color = (100, 100, 100) if back_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False  # Quitter le menu avec Échap
                elif event.key == pygame.K_LEFT:  # Réduire le volume
                    volume = max(0.0, volume - 0.1)
                    pygame.mixer.music.set_volume(volume)
                elif event.key == pygame.K_RIGHT:  # Augmenter le volume
                    volume = min(1.0, volume + 0.1)
                    pygame.mixer.music.set_volume(volume)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False
                elif save_rect.collidepoint(event.pos):
                    save_settings(volume)  # Sauvegarder le volume
                elif resolution_rect.collidepoint(event.pos):
                    running = display_screamer(screen)

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
    pygame.mixer.music.set_volume(0.1)
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
                    game = Game()
                    game.run()
                    running = False
                elif options_rect.collidepoint(event.pos):
                    options_menu(screen)  # Afficher le menu des options
                elif quit_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)