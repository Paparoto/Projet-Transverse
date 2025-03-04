import pygame
from menu import main_menu

pygame.init()

from Game import Game

if __name__ == '__main__':
    pygame.init()
    main_menu()
    Game=Game()
    Game.run()

pygame.quit()