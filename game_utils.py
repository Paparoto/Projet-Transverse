import pygame

def display_screamer(screen):
    screamer_image = pygame.image.load("Tileset/hq720.jpg")  # Assure-toi d'avoir cette image
    screamer_sound = pygame.mixer.Sound("Tileset/Jumpscare-Sound-Trimmed-Final.wav")  # Assure-toi d'avoir ce son
    screamer_sound.play()  # Jouer le son du screamer

    screen.fill((0, 0, 0))  # Remplir l'écran de noir
    screamer_image = pygame.transform.scale(screamer_image, (screen.get_width(), screen.get_height()))
    screen.blit(screamer_image, (0, 0))
    pygame.display.flip()

    pygame.time.delay(2000)  # Laisser l'image afficher pendant 2 secondes (ajuste cette durée si nécessaire)

    return False
