import pygame
pygame.init()

from Game import Game

if __name__ == '__main__':
    pygame.init()
    Game=Game()
    Game.run()


pygame.quit()