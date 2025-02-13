import pygame
import pytmx
import pyscroll

from player import Player




class Game:
    def __init__(self):

        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pygame")

        tmx_data = pytmx.util_pygame.load_pygame('Tileset/pokemonn.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        map_layer.zoom=1

        player_postion=tmx_data.get_object_by_name("Player")
        self.player=Player(player_postion.x, player_postion.y)

        self.group = pyscroll.PyscrollGroup(map_layer=map_layer, default_layer=3)
        self.group.add(self.player)

    def run(self):
        running = True
        while running:
            self.group.update()
            self.group.center(self.player.rect)
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
