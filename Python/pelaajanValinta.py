
import pygame
import sys

# Alustetaan Pygame
pygame.init()

# Asetetaan pelin ikkunan koko
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Kissapeli - Valitse hahmosi")

# M‰‰ritell‰‰n v‰rit (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Fontti
font = pygame.font.Font(None, 48)

# Ladataan vaihtoehtoiset hahmot (kissakuvat)
cat_images = [
    pygame.image.load("images/cat.png"),
    pygame.image.load("images/lauchingCat.png"),
    pygame.image.load("images/readingCat.png")
]

# Skaalataan kuvat sopiviksi
cat_images = [pygame.transform.scale(img, (100, 100)) for img in cat_images]

# Funktio aloitusruudulle
def show_start_screen():
    selected_index = 0  # Aluksi ensimm‰inen hahmo on valittu
    while True:
        window.fill(WHITE)  # Tausta valkoiseksi

        # N‰ytet‰‰n otsikko
        title_text = font.render("Valitse hahmo", True, BLACK)
        window.blit(title_text, (WINDOW_WIDTH // 2 - title_text.get_width() // 2, 50))

        # Piirret‰‰n hahmot
        for i, img in enumerate(cat_images):
            x_pos = WINDOW_WIDTH // 2 - len(cat_images) * 120 // 2 + i * 120
            y_pos = WINDOW_HEIGHT // 2 - img.get_height() // 2

            # Korostetaan valittua hahmoa
            if i == selected_index:
                pygame.draw.rect(window, (255, 0, 0), (x_pos - 10, y_pos - 10, img.get_width() + 20, img.get_height() + 20), 3)

            window.blit(img, (x_pos, y_pos))

        # P‰ivitet‰‰n n‰yttˆ
        pygame.display.update()

        # K‰sitell‰‰n tapahtumat
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    selected_index = (selected_index - 1) % len(cat_images)  # Siirry vasemmalle
                elif event.key == pygame.K_RIGHT:
                    selected_index = (selected_index + 1) % len(cat_images)  # Siirry oikealle
                elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    # Palautetaan valittu hahmo, kun Enter tai Space painetaan
                    return selected_index

# Pelin p‰‰silmukka
def game_loop(player_cat_img):
    cat_width = player_cat_img.get_width()
    cat_height = player_cat_img.get_height()

    # Pelaajan hahmon aloituspaikka
    cat_x = WINDOW_WIDTH // 2 - cat_width // 2
    cat_y = WINDOW_HEIGHT // 2 - cat_height // 2
    cat_speed = 5

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Otetaan painetut n‰pp‰imet
        keys = pygame.key.get_pressed()

        # Liikutetaan pelaajan kissaa nuolin‰pp‰imill‰
        if keys[pygame.K_LEFT]:
            cat_x -= cat_speed
        if keys[pygame.K_RIGHT]:
            cat_x += cat_speed
        if keys[pygame.K_UP]:
            cat_y -= cat_speed
        if keys[pygame.K_DOWN]:
            cat_y += cat_speed

        # Varmistetaan, ett‰ pelaajan kissa pysyy ikkunan sis‰ll‰
        if cat_x < 0:
            cat_x = 0
        if cat_x > WINDOW_WIDTH - cat_width:
            cat_x = WINDOW_WIDTH - cat_width
        if cat_y < 0:
            cat_y = 0
        if cat_y > WINDOW_HEIGHT - cat_height:
            cat_y = WINDOW_HEIGHT - cat_height

        # T‰ytet‰‰n ikkuna valkoisella
        window.fill(WHITE)

        # Piirret‰‰n pelaajan kissa
        window.blit(player_cat_img, (cat_x, cat_y))

        # P‰ivitet‰‰n n‰ytˆn sis‰ltˆ
        pygame.display.update()

        # Asetetaan pelin p‰ivitysnopeus
        pygame.time.Clock().tick(60)

    # Lopetetaan Pygame
    pygame.quit()
    sys.exit()

# Aloitusruutu ja hahmon valinta
selected_cat_index = show_start_screen()
selected_cat_img = cat_images[selected_cat_index]

# Siirryt‰‰n pelisilmukkaan valitulla hahmolla
game_loop(selected_cat_img)
