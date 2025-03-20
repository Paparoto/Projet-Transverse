import pygame
import pytmx
import pyscroll
from game_utils import display_screamer, options_menu
from player import Player

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1920, 1080))
        pygame.display.set_caption("Pygame Horror Game")

        self.load_map("horror")  # Start in the bedroom
        self.is_second_map = False

    def load_map(self, map_name):
        """Loads the map and initializes objects"""
        self.tmx_data = pytmx.util_pygame.load_pygame(f'Tileset/{map_name}.tmx')
        map_data = pyscroll.data.TiledMapData(self.tmx_data)
        self.map_layer = pyscroll.orthographic.BufferedRenderer(map_data, self.screen.get_size())
        self.map_layer.zoom = 2

        # Create wall collision rectangles
        self.walls = [pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                      for obj in self.tmx_data.objects if obj.type == "collision"]

        self.group = pyscroll.PyscrollGroup(map_layer=self.map_layer, default_layer=4)

        # Player spawn point
        spawn = self.tmx_data.get_object_by_name("spawn")
        if hasattr(self, 'player'):
            self.player.position = (spawn.x, spawn.y)
        else:
            self.player = Player(spawn.x, spawn.y)

        self.group.add(self.player)

        # Handle exit zones
        self.exits = {}  # Dictionary to store exits
        for obj in self.tmx_data.objects:
            if obj.type == "exit":
                self.exits[obj.name] = pygame.Rect(obj.x, obj.y, obj.width, obj.height)

        self.center_camera()

    def handle_input(self):
        """Handles player movement input"""
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
        """Switches to a new map"""
        print(f"Switching to: {new_map}")  # Debugging output
        self.load_map(new_map)

        # Display screamer when entering hallway
        if new_map == "couloir":
            display_screamer(self.screen)

    def center_camera(self):
        """Centers the camera on the player"""
        self.group.center(self.player.rect.center)

    def update(self):
        """Updates the game state"""
        self.player.update()

        # First, check if the player is touching an exit
        for exit_name, exit_rect in self.exits.items():
            if exit_rect.colliderect(self.player.rect):  # Using rect instead of feet
                print(f"Player touched exit: {exit_name}")  # Debugging print

                if exit_name == "exit_bedroom":  # Bedroom → Hallway
                    self.switch_house("couloir")
                elif exit_name == "exit_hallway":  # Hallway → Garden
                    self.switch_house("garden")
                elif exit_name == "exit_return_bedroom":  # Hallway → Bedroom
                    self.switch_house("horror")
                elif exit_name == "exit_return_hallway":  # Garden → Hallway
                    self.switch_house("couloir")

        # Then check for wall collision AFTER exit check
        if self.player.rect.collidelist(self.walls) > -1:
            self.player.move_back()

        # Update the camera position
        self.group.center(self.player.rect.center)

    def run(self):
        """Main game loop"""
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
                in_options_menu = False  # Return to game
            else:
                self.handle_input()
                self.update()
                self.screen.fill((0, 0, 0))
                self.group.draw(self.screen)
                pygame.display.flip()

            clock.tick(60)

        pygame.quit()


# Start the game
if __name__ == "__main__":
    Game().run()