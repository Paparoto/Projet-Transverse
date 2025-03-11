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
    quit_text = font.render("QUIT", True, (255, 255, 255))

    back_rect = pygame.Rect(860, 800, 200, 80)
    save_rect = pygame.Rect(860, 650, 200, 80)
    quit_rect = pygame.Rect(860, 500, 200, 80)

    volume = load_settings()
    pygame.mixer.music.set_volume(volume)

    running = True
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
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
                elif left_arrow_rect.collidepoint(event.pos):
                    left_pressed = True
                    volume = max(0.0, volume - 0.05)
                    pygame.mixer.music.set_volume(volume)
                elif right_arrow_rect.collidepoint(event.pos):
                    right_pressed = True
                    volume = min(1.0, volume + 0.05)
                    pygame.mixer.music.set_volume(volume)

        if left_pressed:
            left_arrow_rect = left_arrow_rect.move(0, 3)
        if right_pressed:
            right_arrow_rect = right_arrow_rect.move(0, 3)

        screen.blit(left_arrow_surface, left_arrow_rect)
        screen.blit(right_arrow_surface, right_arrow_rect)

        for rect, text in [(back_rect, back_text), (save_rect, save_text), (quit_rect, quit_text)]:
            color = (100, 100, 100) if rect.collidepoint(mouse_pos) else (50, 50, 50)
            pygame.draw.rect(screen, color, rect, border_radius=10)
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(60)