import pygame
import pytmx
import pyscroll
from player import Player

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1920, 1080))  # Même résolution que le menu
        pygame.display.set_caption("Pygame")

        self.tmx_data = pytmx.util_pygame.load_pygame('Tileset/horror.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2

        player_position = self.tmx_data.get_object_by_name("Player")
        self.player = Player(player_position.x, player_position.y)

        self.walls = []
        for obj in self.tmx_data.objects:
            if obj.type == "collision":
                self.walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)
        self.group.add(self.player)

        enter_house = self.tmx_data.get_object_by_name("exit_room")
        self.enter_house_rect = pygame.Rect(enter_house.x, enter_house.y, enter_house.width, enter_house.height)

        self.is_second_map = False  # On commence sur la première carte

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

        # Si nous sommes dans la deuxième carte, activer le suivi de la caméra
        if new_map == "couloir":
            self.is_second_map = True
        else:
            self.is_second_map = False

    def update(self):
        self.player.update()

        # Si nous entrons dans la zone de sortie, on change de carte
        if self.enter_house_rect.colliderect(self.player.feet):
            self.switch_house("couloir")

        # Vérifier les collisions avec les murs
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

        # Si la carte est la deuxième, suivre le joueur
        if self.is_second_map:
            self.center_camera()

        # Centrer la caméra sur le joueur
        self.group.center(self.player.rect.center)

    def center_camera(self):
        """ Déplace la caméra pour centrer le joueur """
        camera_width, camera_height = self.screen.get_size()
        player_rect = self.player.rect

        # Calculer les nouvelles coordonnées de la caméra
        camera_x = player_rect.centerx - camera_width // 2
        camera_y = player_rect.centery - camera_height // 2

        # Empêcher la caméra de sortir des bords de la carte
        map_width = self.tmx_data.width * self.tmx_data.tilewidth  # Largeur de la carte en pixels
        map_height = self.tmx_data.height * self.tmx_data.tileheight  # Hauteur de la carte en pixels

        camera_x = max(0, min(camera_x, map_width - camera_width))  # Limiter à la largeur de la carte
        camera_y = max(0, min(camera_y, map_height - camera_height))  # Limiter à la hauteur de la carte

        # Appliquer le décalage de la caméra
        self.map_layer.camera = pygame.Rect(camera_x, camera_y, camera_width, camera_height)

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