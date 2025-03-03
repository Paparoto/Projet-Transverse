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
    play_text = font.render("Jouer", True, (255, 255, 255))
    quit_text = font.render("Quitter", True, (255, 255, 255))

    play_rect = play_text.get_rect(center=(400, 350))
    quit_rect = quit_text.get_rect(center=(400, 450))
    title_rect = title_text.get_rect(center=(400, 150))

    running = True
    while running:
        screen.fill((0, 0, 0))
        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_rect.collidepoint(event.pos):
                    game = Game()
                    game.run()
                    running = False
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main_menu()