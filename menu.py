import pygame
import sys
from Game import Game


def main_menu():
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Menu Principal")
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    title_text = font.render("m̶̌̿l̶̾͝n̵̊͗1̵͂͝g̸̎̐4̴̒̄m̶̂3s", True, (255, 255, 255))
    play_text = font.render("Jouer", True, (0, 0, 0))
    quit_text = font.render("Quitter", True, (0, 0, 0))

    title_rect = title_text.get_rect(center=(400, 150))
    play_rect = pygame.Rect(300, 320, 200, 60)  # Création d'un bouton rectangulaire
    quit_rect = pygame.Rect(300, 420, 200, 60)

    running = True
    while running:
        screen.fill((0, 0, 0))

        # Vérifie si la souris est sur un bouton
        mouse_pos = pygame.mouse.get_pos()
        play_color = (200, 200, 200) if play_rect.collidepoint(mouse_pos) else (255, 255, 255)
        quit_color = (200, 200, 200) if quit_rect.collidepoint(mouse_pos) else (255, 255, 255)

        # Affichage du titre
        screen.blit(title_text, title_rect)

        # Dessine les boutons avec fond et texte
        pygame.draw.rect(screen, play_color, play_rect, border_radius=10)
        pygame.draw.rect(screen, quit_color, quit_rect, border_radius=10)

        play_text_surface = font.render("Jouer", True, (0, 0, 0))
        quit_text_surface = font.render("Quitter", True, (0, 0, 0))

        screen.blit(play_text_surface, play_text_surface.get_rect(center=play_rect.center))
        screen.blit(quit_text_surface, quit_text_surface.get_rect(center=quit_rect.center))

        # Gestion des événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game = Game()
                    game.run()
                    pygame.quit()
                    sys.exit()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()
