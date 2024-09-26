import pygame
import random
import sys

# Alustetaan Pygame
pygame.init()

# Asetetaan pelin ikkunan koko
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mystic Forest")

# M��ritell��n v�rit (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEECH_BUBBLE_COLOR = (255, 255, 200)  # Vaaleankeltainen v�ri puhekuplalle

# Fontti
font = pygame.font.Font(None, 48)
bubble_font = pygame.font.Font(None, 32)

# Ladataan pelaajan kissan kuva
player_cat_img = pygame.image.load("images/cat.png")
cat_width = player_cat_img.get_width()
cat_height = player_cat_img.get_height()

# Muiden kissojen kuvat tasoittain ja niihin liittyv�t tekstit
level_cats = {
    1: [
        {"img": pygame.image.load("images/bear.png"), "text": "Soon it start snowing!"},
        {"img": pygame.image.load("images/birdsinging.png"), "text": "What a beautiful day?"},
        {"img": pygame.image.load("images/butterfly.png"), "text": "I love flowers I need them!"},
        {"img": pygame.image.load("images/fox.png"), "text":"Where is my food?"},
        {"img": pygame.image.load("images/reindeer.png"), "text": "Have you seen any moose?"},
        {"img": pygame.image.load("images/mouse.png"), "text": "You an see me?"}
    ],
    2: [
        {"img": pygame.image.load("images/kissa.png"), "text": "Miau!"},
        {"img": pygame.image.load("images/kettu.png"), "text": "What the fox say?"},
        {"img": pygame.image.load("images/koira.png"), "text": "Hau hau!"},
        {"img": pygame.image.load("images/lintu.png"), "text": "I sing what I want."},
        {"img": pygame.image.load("images/peura.png"), "text": "I am Bambi."},
        {"img": pygame.image.load("images/karhu.png"), "text": "Karhu karjuu!"}
    ],
    3: [
        {"img": pygame.image.load("images/orava.png"), "text": "Orava  hyyppii puissa!"},
        {"img": pygame.image.load("images/kissakumara.png"), "text": "Mysterious cat!"},
        {"img": pygame.image.load("images/orava1.png"), "text": "I live here"},
        {"img": pygame.image.load("images/karhuSininen.png"), "text": "Sininen karhu on harvinainen!"}
    ],
    4: [
        {"img": pygame.image.load("images/kala.png"), "text": "Fish in the water"},
        {"img": pygame.image.load("images/janis.png"), "text": "A big jamp!"},
        {"img": pygame.image.load("images/ketturepolainen.png"), "text": "Kettu Repolainen on viisas!"},
        {"img": pygame.image.load("images/koirat.png"), "text": "The dogs are outside!"}
    ]
}
# Skaalataan kissakuvat sopiviksi
for level in level_cats:
    for cat in level_cats[level]:
        cat["img"] = pygame.transform.scale(cat["img"], (100, 100))

# Ladataan taustakuvat jokaiselle tasolle
background_images = [
    pygame.transform.scale(pygame.image.load("images/metsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/level1tausta.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/level2tausta.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/level3tausta.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
]


# Puhekupla-funktio, joka rivitt�� tekstin ja varmistaa, ett� puhekupla pysyy pelialueen sis�ll�
def draw_speech_bubble(text, position):
    # Asetetaan puhekuplan koko
    bubble_width, bubble_height = 200, 100

    # Lasketaan alustava puhekuplan sijainti
    bubble_x, bubble_y = position[0] - bubble_width // 2, position[1] - bubble_height - 20

    # Varmistetaan, ett� puhekupla pysyy pelialueen sis�ll� (x-akselilla)
    if bubble_x < 0:
        bubble_x = 0
    elif bubble_x + bubble_width > WINDOW_WIDTH:
        bubble_x = WINDOW_WIDTH - bubble_width

    # Varmistetaan, ett� puhekupla pysyy pelialueen sis�ll� (y-akselilla)
    if bubble_y < 0:
        bubble_y = 0
    elif bubble_y + bubble_height > WINDOW_HEIGHT:
        bubble_y = WINDOW_HEIGHT - bubble_height

    # Piirret��n puhekupla suorakulmiona
    pygame.draw.rect(window, SPEECH_BUBBLE_COLOR, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(window, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)

    # Rivitet��n teksti niin, ett� se mahtuu puhekuplaan
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        # Tarkistetaan nykyisen rivin leveys, jos lis�t��n uusi sana
        if bubble_font.size(current_line + word)[0] <= bubble_width - 10:  # V�hennet��n marginaali
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '

    # Lis�� viimeinen rivi
    if current_line:
        lines.append(current_line)

    # Piirret��n rivitetty teksti puhekuplan sis��n
    for i, line in enumerate(lines):
        text_surface = bubble_font.render(line, True, BLACK)
        text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + 20 + i * bubble_font.get_height()))  # Tekstin pystysuuntainen tasapainotus
        window.blit(text_surface, text_rect)

# Funktio luomaan kissoja satunnaisiin paikkoihin ilman t�rm�yksi� toistensa kanssa
def create_cats(num_cats, level):
    cats = []
    # Valitaan tasolle sopivat kissat
    available_cats = level_cats[level]
    
    for _ in range(num_cats):
        while True:  # Yritet��n l�yt�� vapaa paikka el�imelle
            x = random.randint(0, WINDOW_WIDTH - cat_width)
            y = random.randint(0, WINDOW_HEIGHT - cat_height)
            cat_data = random.choice(available_cats)
            new_cat_rect = pygame.Rect(x, y, cat_data["img"].get_width(), cat_data["img"].get_height())
            
            # Tarkistetaan, osuuko uusi kissa toisten kissojen kanssa
            collision = False
            for cat in cats:
                if new_cat_rect.colliderect(cat["rect"]):
                    collision = True
                    break
            
            if not collision:
                cats.append({"rect": new_cat_rect, "img": cat_data["img"], "text": cat_data["text"]})
                break  # Kissa sijoitettu onnistuneesti, lopetetaan while-looppi t�lle el�imelle
    
    return cats


# Pelin p��silmukka
def game_loop():
    level = 1  # Alkaa tasolta 1
    max_level = 4  # Kuinka monta tasoa peliss� on
    clock = pygame.time.Clock()  # Kellon asettaminen pelin p�ivitystaajuudelle
    speech_bubble_active = False  # Onko puhekupla n�kyviss�
    speech_bubble_timer = 0  # Ajastin puhekuplalle
    speech_bubble_text = ""  # Puhekuplassa n�kyv� teksti
    last_cat_text = None  # Viimeisen ker�tyn el�imen teksti

    while level <= max_level:
        num_cats = level * 3  # Lis�� kissoja jokaisella tasolla
        other_cats = create_cats(num_cats, level)  # Luodaan kissat tasolle
        score = 0

        # Pelaajan hahmon aloituspaikka vasemmassa alakulmassa
        cat_x = 0  # Aina vasemmassa laidassa
        cat_y = WINDOW_HEIGHT - cat_height  # Alimmainen mahdollinen kohta (vasen alalaita)

        cat_speed = 5

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            # Otetaan painetut n�pp�imet
            keys = pygame.key.get_pressed()

            # Liikutetaan pelaajan kissaa nuolin�pp�imill�
            if keys[pygame.K_LEFT]:
                cat_x -= cat_speed
            if keys[pygame.K_RIGHT]:
                cat_x += cat_speed
            if keys[pygame.K_UP]:
                cat_y -= cat_speed
            if keys[pygame.K_DOWN]:
                cat_y += cat_speed

            # Varmistetaan, ett� pelaajan kissa pysyy ikkunan sis�ll�
            cat_x = max(0, min(cat_x, WINDOW_WIDTH - cat_width))
            cat_y = max(0, min(cat_y, WINDOW_HEIGHT - cat_height))

            # N�ytet��n oikea taustakuva riippuen tasosta
            window.blit(background_images[level - 1], (0, 0))

            # Piirret��n pelaajan kissa
            window.blit(player_cat_img, (cat_x, cat_y))

            # Luodaan pelaajan kissan rect-objekti t�rm�ystarkistusta varten
            player_rect = pygame.Rect(cat_x, cat_y, cat_width, cat_height)

            # Piirret��n ja k�sitell��n toiset kissat
            remaining_cats = []
            for cat in other_cats:
                cat_rect = cat["rect"]
                if player_rect.colliderect(cat_rect):
                    # Jos pelaaja t�rm�� kissaan, n�ytet��n puhekupla ja tallenetaan viimeisen el�imen teksti
                    if not speech_bubble_active or speech_bubble_text != cat["text"]:
                        speech_bubble_active = True
                        speech_bubble_timer = pygame.time.get_ticks()  # Tallennetaan puhekuplan n�ytt�misen aloitusaika
                        speech_bubble_text = cat["text"]  # P�ivitet��n uusi teksti puhekuplaan
                        last_cat_text = cat["text"]  # Tallenna viimeisen ker�tyn el�imen teksti
                    score += 1
                else:
                    # Jos ei t�rm�t�, piirret��n kissa ja lis�t��n se j�ljelle j��vien listalle
                    window.blit(cat["img"], cat_rect.topleft)
                    remaining_cats.append(cat)

            other_cats = remaining_cats

            # N�ytet��n puhekupla, jos se on aktiivinen
            if speech_bubble_active:
                draw_speech_bubble(speech_bubble_text, (cat_x + cat_width // 2, cat_y))

                # Poistetaan puhekupla 2 sekunnin kuluttua
                if pygame.time.get_ticks() - speech_bubble_timer > 2000:
                    speech_bubble_active = False

            # N�ytet��n pistem��r� ja taso
            score_text = font.render(f"Pisteet: {score}/{num_cats}", True, BLACK)
            window.blit(score_text, (10, 10))

            level_text = font.render(f"Taso: {level}", True, BLACK)
            window.blit(level_text, (10, 50))

            # Jos kaikki kissat on ker�tty, n�ytet��n viimeisen ker�tyn el�imen teksti ennen seuraavalle tasolle siirtymist�
            if score == num_cats:
                if last_cat_text:
                    draw_speech_bubble(last_cat_text, (cat_x + cat_width // 2, cat_y))
                    pygame.display.update()
                    pygame.time.wait(2000)  # N�ytet��n puhekupla 2 sekunnin ajan ennen tasojen vaihtoa
                level += 1
                pygame.time.wait(1000)  # Odotetaan 1 sekunti ennen seuraavaa tasoa
                break  # P��st��n ulos pelisilmukasta ja siirryt��n seuraavalle tasolle

            # P�ivitet��n n�yt�n sis�lt�
            pygame.display.update()

            # Asetetaan pelin p�ivitysnopeus
            clock.tick(60)  # Varmistetaan 60 FPS

    # Peli p��ttyy, kun kaikki tasot on suoritettu
    game_over()


# Game over -funktio
def game_over():
    window.fill(WHITE)
    game_over_text = font.render("Peli ohi! Olet suorittanut kaikki tasot!", True, BLACK)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

    pygame.display.update()
    pygame.time.wait(3000)  # Odotetaan 3 sekuntia ennen pelin sulkemista
    pygame.quit()
    sys.exit()

# Aloitetaan peli
game_loop()