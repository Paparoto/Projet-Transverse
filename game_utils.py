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

def options_menu(screen):
    font = pygame.font.Font(None, 60)
    clock = pygame.time.Clock()

    back_text = font.render("BACK", True, (255, 255, 255))
    save_text = font.render("SAVE", True, (255, 255, 255))
    resolution_text = font.render("RESOLUTION", True, (255, 255, 255))  # Nouveau texte pour Résolution
    back_rect = pygame.Rect(860, 800, 200, 80)
    save_rect = pygame.Rect(860, 650, 200, 80)
    resolution_rect = pygame.Rect(860, 500, 200, 80)  # Rectangle pour le bouton Résolution

    volume = load_settings()  # Charger le volume depuis le fichier
    pygame.mixer.music.set_volume(volume)

    running = True
    while running:
        screen.fill((30, 30, 30))  # Fond sombre

        mouse_pos = pygame.mouse.get_pos()

        # Afficher "Options"
        options_title = font.render("OPTIONS", True, (255, 255, 255))
        screen.blit(options_title, (850, 100))

        # Affichage des boutons
        color = (100, 100, 100) if back_rect.collidepoint(mouse_pos) else (50, 50, 50)
        pygame.draw.rect(screen, color, back_rect, border_radius=10)
        back_text_rect = back_text.get_rect(center=back_rect.center)
        screen.blit(back_text, back_text_rect)

        # Autres affichages pour "SAVE", "RESOLUTION" et le volume

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_rect.collidepoint(event.pos):
                    running = False  # Fermer le menu et revenir au jeu
                elif save_rect.collidepoint(event.pos):
                    save_settings(volume)  # Sauvegarder les réglages
                elif resolution_rect.collidepoint(event.pos):
                    running = display_screamer(screen)  # Afficher le screamer

        pygame.display.flip()
        clock.tick(60)
