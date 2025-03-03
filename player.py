import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.sprite_sheet = pygame.image.load('Tileset/H5TPB4.png').convert_alpha()
        self.image = self.get_image(0, 0)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.position = [x, y]

        self.images = {
            'down': [self.get_image(0, 0), self.get_image(1, 0), self.get_image(2, 0)],
            'left': [self.get_image(0, 1), self.get_image(1, 1), self.get_image(2, 1)],
            'right': [self.get_image(0, 2), self.get_image(1, 2), self.get_image(2, 2)],
            'up': [self.get_image(0, 3), self.get_image(1, 3), self.get_image(2, 3)],
        }

        self.current_frame = 0
        self.animation_speed = 15
        self.animation_counter = 0
        self.direction = 'down'

        self.feet = pygame.Rect(0, 0, self.rect.width * 0.5, 15)
        self.old_position = self.position.copy()
        self.speed = 2

    def save_location(self):
        self.old_position = self.position.copy()

    def change_animation(self, direction):
        self.direction = direction
        self.animation_counter += 1

        if self.animation_counter >= self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.images[direction])
            self.animation_counter = 0

        self.image = self.images[direction][self.current_frame]

    def move_right(self):
        self.position[0] += self.speed
        self.change_animation("right")
        self.rect.topleft = self.position

    def move_left(self):
        self.position[0] -= self.speed
        self.change_animation("left")
        self.rect.topleft = self.position

    def move_up(self):
        self.position[1] -= self.speed
        self.change_animation("up")
        self.rect.topleft = self.position

    def move_down(self):
        self.position[1] += self.speed
        self.change_animation("down")
        self.rect.topleft = self.position

    def update(self):
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def move_back(self):
        self.position = self.old_position.copy()
        self.rect.topleft = self.position
        self.feet.midbottom = self.rect.midbottom

    def get_image(self, col, row):
        sprite_width, sprite_height = 32, 48
        x = col * sprite_width
        y = row * sprite_height
        image = pygame.Surface([sprite_width, sprite_height], pygame.SRCALPHA)
        image.blit(self.sprite_sheet, (0, 0), (x, y, sprite_width, sprite_height))
        return image.convert_alpha()
