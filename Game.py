import pygame
import pytmx
import pyscroll
import os  # Pour vérifier les fichiers
from game_utils import display_screamer, options_menu
from player import Player


class Game:
    def __init__(self):
        self.exit_rect = None
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pygame Horror Game")

        # Vérifier si les fichiers sont bien là
        print("📂 Liste des fichiers dans Tileset/:", os.listdir("Tileset"))

        # Chargement de la première carte
        self.load_map("horror")
        self.is_second_map = False

    def load_map(self, map_name):
        """Charge une carte et initialise ses composants."""
        print(f"🔄 Chargement de la carte: {map_name}.tmx...")

        # Charger la carte avec gestion alpha
        self.tmx_data = pytmx.util_pygame.load_pygame(f'Tileset/{map_name}.tmx', pixelalpha=True)

        # Afficher tous les objets présents dans la carte
        object_names = [obj.name for obj in self.tmx_data.objects]
        print(f"📌 Objets trouvés dans {map_name}.tmx: {object_names}")

        # Zone de transition (débogage)
        exit_zone = self.tmx_data.get_object_by_name("exit_room")
        if exit_zone:
            print(f"✅ Exit_room trouvé à x={exit_zone.x}, y={exit_zone.y}")
            self.exit_rect = pygame.Rect(exit_zone.x, exit_zone.y, exit_zone.width, exit_zone.height)
        else:
            print("❌ Erreur: 'exit_room' n'a pas été trouvé dans la carte !")
            self.exit_rect = None  # Empêche le crash

        # Chargement des collisions
        self.walls = [pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                      for obj in self.tmx_data.objects if obj.type == "collision"]

        # Création du groupe de rendu
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2
        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

        # Placement du joueur
        spawn = self.tmx_data.get_object_by_name("spawn")
        if hasattr(self, 'player'):
            self.player.position = (spawn.x, spawn.y)
        else:
            self.player = Player(spawn.x, spawn.y)

        self.group.add(self.player)
        self.center_camera()

    def handle_input(self):
        """Gère les déplacements du joueur."""
        keys = pygame.key.get_pressed()
        movements = {
            pygame.K_UP: self.player.move_up,
            pygame.K_DOWN: self.player.move_down,
            pygame.K_LEFT: self.player.move_left,
            pygame.K_RIGHT: self.player.move_right
        }
        for key, action in movements.items():
            if keys[key]:
                self.player.save_location()
                action()

    def switch_house(self, new_map):
        """Change de carte et affiche un screamer si nécessaire."""
        print(f"🚪 Changement de carte vers {new_map}...")
        self.load_map(new_map)
        self.is_second_map = (new_map == "couloir")

        if self.is_second_map:
            display_screamer(self.screen)

    def center_camera(self):
        """Centre la caméra sur le joueur."""
        self.group.center(self.player.rect.center)

    def update(self):
        """Met à jour le jeu."""
        self.player.update()

        # Vérifier si exit_room est bien défini avant d’essayer de l’utiliser
        if self.exit_rect and self.exit_rect.colliderect(self.player.feet):
            print("🔄 Le joueur entre dans exit_room, changement de carte...")
            self.switch_house("couloir")

        # Empêche le joueur de traverser les murs
        if self.player.feet.collidelist(self.walls) > -1:
            self.player.move_back()

        # Mise à jour de la caméra
        self.group.center(self.player.rect.center)

    def run(self):
        """Boucle principale du jeu."""
        clock = pygame.time.Clock()
        running = True
        in_options_menu = False

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    in_options_menu = True

            if in_options_menu:
                options_menu(self.screen)
                in_options_menu = False  # Retour au jeu
            else:
                self.handle_input()
                self.update()
                self.screen.fill((0, 0, 0))
                self.group.draw(self.screen)
                pygame.display.flip()

            clock.tick(60)

        pygame.quit()


# Lancement du jeu
if __name__ == "__main__":
    Game().run()