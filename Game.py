import pygame
import pytmx
import pyscroll
from player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption("Pygame")

        tmx_data = pytmx.util_pygame.load_pygame('Tileset/horror.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2

        player_position = tmx_data.get_object_by_name("Player")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []
        for obj in tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)

        enter_house = tmx_data.get_object_by_name("exit_room")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

    def handle_input(self):
        pressed = pygame.key.get_pressed()
        movement = {
            pygame.K_UP: self.player.move_up,
            pygame.K_DOWN: self.player.move_down,
            pygame.K_LEFT: self.player.move_left,
            pygame.K_RIGHT: self.player.move_right
        }
        for key, action in movement.items():
            if pressed[key]:
                self.player.save_location()
                action()

    def switch_house(self, new_map):
        tmx_data = pytmx.util_pygame.load_pygame(f'Tileset/{new_map}.tmx')
        map_data = pyscroll.data.TiledMapData(tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2

        self.walls = [pygame.Rect(obj.x, obj.y, obj.width, obj.height) for obj in tmx_data.objects if
                      obj.type == "collision"]

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)

        spawn = tmx_data.get_object_by_name("spawn")
        if spawn:
            self.player.position = (spawn.x, spawn.y)

    def update(self):
        self.player.update()

        if self.enter_house_rect and self.player.feet.colliderect(self.enter_house_rect):
            self.switch_house("couloir")
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

        self.group.center(self.player.rect.center)

    def run(self):
        clock = pygame.time.Clock()
        running = True

        while running:
            self.handle_input()
            self.update()

            self.screen.fill((0, 0, 0))
            self.group.draw(self.screen)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            clock.tick(60)

        pygame.quit()
