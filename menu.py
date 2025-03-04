import pygame
import sys
from Game import Game

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
                    game = Game()
                    game.run()
                    running = False
                elif options_rect.collidepoint(event.pos):
                    print("Options cliqué")
                elif quit_rect.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)
