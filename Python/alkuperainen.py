
import pygame
import random
import sys

# Alustetaan Pygame
pygame.init()

# Asetetaan pelin ikkunan koko
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Kissapeli - Keraa kissat")

# M‰‰ritell‰‰n v‰rit (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Lataa taustakuva
background_image = pygame.image.load("images/cow.jpg")
# Skaalaa taustakuva ikkunan kokoiseksi
background_image = pygame.transform.scale(background_image, (WINDOW_WIDTH, WINDOW_HEIGHT))

# Ladataan pelaajan kissan kuva
player_cat_img = pygame.image.load("images/cat.png")
cat_width = player_cat_img.get_width()
cat_height = player_cat_img.get_height()

# Ladataan muiden kissojen kuvat
other_cat_imgs = [
    pygame.image.load("images/lauchingCat.png"),
    pygame.image.load("images/no.jpg"),
    pygame.image.load("images/readingCat.png")
]

# Pelaajan kissan aloituspaikka
cat_x = WINDOW_WIDTH // 2 - cat_width // 2
cat_y = WINDOW_HEIGHT // 2 - cat_height // 2

# Pelaajan kissan liikkumisnopeus
cat_speed = 5

# Luodaan lista muista kissoista, joita ker‰t‰‰n
num_cats = 5  # Kuinka monta kissaa kent‰ll‰ on
other_cats = []
for _ in range(num_cats):
    x = random.randint(0, WINDOW_WIDTH - cat_width)
    y = random.randint(0, WINDOW_HEIGHT - cat_height)
    img = random.choice(other_cat_imgs)  # Valitaan satunnainen kissan kuva
    other_cats.append({"rect": pygame.Rect(x, y, img.get_width(), img.get_height()), "img": img})

# Pisteet
score = 0

# Fontti pisteiden n‰ytt‰mist‰ varten
font = pygame.font.Font(None, 36)

# Pelisilmukka
running = True
while running:
    # Tarkistetaan tapahtumat (esim. ikkuna suljetaan)
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

    # Piirret‰‰n taustakuva joka kierroksella
    window.blit(background_image, (0, 0))

    # Piirret‰‰n pelaajan kissa
    window.blit(player_cat_img, (cat_x, cat_y))

    # Luodaan pelaajan kissan rect-objekti tˆrm‰ystarkistusta varten
    player_rect = pygame.Rect(cat_x, cat_y, cat_width, cat_height)

    # Piirret‰‰n ja k‰sitell‰‰n toiset kissat
    remaining_cats = []
    for cat in other_cats:
        cat_rect = cat["rect"]
        if player_rect.colliderect(cat_rect):
            # Jos pelaaja osuu kissaan, kasvatetaan pistem‰‰r‰‰ ja ker‰t‰‰n kissa
            score += 1
        else:
            # Jos ei tˆrm‰t‰, piirret‰‰n kissa ja lis‰t‰‰n se j‰ljelle j‰‰vien listalle
            window.blit(cat["img"], cat_rect.topleft)
            remaining_cats.append(cat)

    other_cats = remaining_cats

    # N‰ytet‰‰n pistem‰‰r‰
    score_text = font.render(f"Pisteet: {score}", True, BLACK)
    window.blit(score_text, (10, 10))

    # Jos kaikki kissat on ker‰tty, peli p‰‰ttyy
    if len(other_cats) == 0:
        game_over_text = font.render("Voitit! Kaikki kissat on keratty!", True, BLACK)
        window.blit(game_over_text, (WINDOW_WIDTH // 2 - 200, WINDOW_HEIGHT // 2))
        pygame.display.update()
        pygame.time.wait(3000)  # Odotetaan 3 sekuntia ennen pelin sulkemista
        running = False

    # P‰ivitet‰‰n n‰ytˆn sis‰ltˆ
    pygame.display.update()

    # Asetetaan pelin p‰ivitysnopeus
    pygame.time.Clock().tick(60)

# Lopetetaan Pygame
pygame.quit()
sys.exit()
