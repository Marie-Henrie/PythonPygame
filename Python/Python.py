import pygame
import random
import sys
import alkuGame
from questions import ask_question  # Tuo ask_question-funktio toisesta tiedostosta


alkuGame.tervehdys()

# Alusta Pygame
pygame.init()

# M��rit� pelin ikkunan mitat
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mystic Forest")

# M��rit� v�rit (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEECH_BUBBLE_COLOR = (255, 255, 200)  # Vaaleankeltainen puhekupla

# Fontti
font = pygame.font.Font(None, 48)
bubble_font = pygame.font.Font(None, 32)



# Lataa pelaajan kissan kuva
player_cat_img = pygame.image.load("images/cat.png")
cat_width = player_cat_img.get_width()
cat_height = player_cat_img.get_height()

# Lataa muiden kissojen kuvat ja niihin liittyv�t tekstit
level_cats = {
    1: [
        {"img": pygame.image.load("images/bear.png"), "text": "Soon it starts snowing!", "visible": False},
        {"img": pygame.image.load("images/birdsinging.png"), "text": "What a beautiful day?", "visible": False},
        {"img": pygame.image.load("images/butterfly.png"), "text": "I love flowers I need them!", "visible": False},
        {"img": pygame.image.load("images/fox.png"), "text": "Where is my food?", "visible": False},
        {"img": pygame.image.load("images/reindeer.png"), "text": "Have you seen any moose?", "visible": False},
        {"img": pygame.image.load("images/mouse.png"), "text": "You can see me?", "visible": False},
        {"img": pygame.image.load("images/karhu.jpg"), "text": "I have live here forever.", "visible": False}
    ],
    2: [
        {"img": pygame.image.load("images/kissa.png"), "text": "Miau!", "visible": False},
        {"img": pygame.image.load("images/kettu.png"), "text": "What the fox say?", "visible": False},
        {"img": pygame.image.load("images/koira.png"), "text": "Hau hau!", "visible": False},
        {"img": pygame.image.load("images/lintu.png"), "text": "I sing what I want.", "visible": False},
        {"img": pygame.image.load("images/peura.png"), "text": "I am Bambi.", "visible": False},
        {"img": pygame.image.load("images/karhu.png"), "text": "Karhu karjuu!", "visible": False}
    ],
    3: [
        {"img": pygame.image.load("images/orava.png"), "text": "Orava hyppii puissa!", "visible": False},
        {"img": pygame.image.load("images/kissakumara.png"), "text": "Mysterious cat!", "visible": False},
        {"img": pygame.image.load("images/orava1.png"), "text": "I live here", "visible": False},
        {"img": pygame.image.load("images/karhuSininen.png"), "text": "Sininen karhu on harvinainen!", "visible": False}
    ],
    4: [
        {"img": pygame.image.load("images/kala.png"), "text": "Fish in the water", "visible": False},
        {"img": pygame.image.load("images/janis.png"), "text": "A big jamp!", "visible": False},
        {"img": pygame.image.load("images/ketturepolainen.png"), "text": "Kettu Repolainen on viisas!", "visible": False},
        {"img": pygame.image.load("images/koirat.png"), "text": "The dogs are outside!", "visible": False}
    ]
}

# Define questions for each level
questions = {
    1: {
        "question": "Is 2 + 2 = 4?",
        "options": ["1. Yes", "2. No"],
        "correct": 1
    },
    2: {
        "question": "Is the sky blue?",
        "options": ["1. Yes", "2. No"],
        "correct": 1
    },
    3: {
        "question": "Do cats bark?",
        "options": ["1. Yes", "2. No"],
        "correct": 2
    },
    # Add more questions for additional levels
}


# Skaalaa kissan kuvat sopivaan kokoon
for level in level_cats:
    for cat in level_cats[level]:
        cat["img"] = pygame.transform.scale(cat["img"], (100, 100))

# Lataa taustakuvat jokaiselle tasolle
background_images = [
    pygame.transform.scale(pygame.image.load("images/metsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/ikivihreys.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/auringonpaiste.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/usvametsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
]

# Funktio puhekuplien piirt�miseen
def draw_speech_bubble(text, position):
    bubble_width, bubble_height = 200, 100
    bubble_x, bubble_y = position[0] - bubble_width // 2, position[1] - bubble_height - 40  # Nosta yl�s

    # Varmistetaan, ettei puhekupla mene ikkunan ulkopuolelle
    if bubble_x < 0:
        bubble_x = 0
    elif bubble_x + bubble_width > WINDOW_WIDTH:
        bubble_x = WINDOW_WIDTH - bubble_width
    if bubble_y < 0:
        bubble_y = 0
    elif bubble_y + bubble_height > WINDOW_HEIGHT:
        bubble_y = WINDOW_HEIGHT - bubble_height

    pygame.draw.rect(window, SPEECH_BUBBLE_COLOR, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(window, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)

    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        if bubble_font.size(current_line + word)[0] <= bubble_width - 20:  # J�t� tilaa reunalle
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = bubble_font.render(line.strip(), True, BLACK)  # Poista ylim��r�inen v�lily�nti
        text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + 20 + i * bubble_font.get_height()))
        window.blit(text_surface, text_rect)


# Funktio kissojen luomiseen satunnaisiin paikkoihin ilman, ett� ne p��llekk�in pelaajan kissan kanssa
def create_cats(num_cats, level, player_rect):
    cats = []
    available_cats = level_cats[level]

    for _ in range(num_cats):
        while True:
            x = random.randint(0, WINDOW_WIDTH - cat_width)
            y = random.randint(0, WINDOW_HEIGHT - cat_height)
            cat_data = random.choice(available_cats)
            new_cat_rect = pygame.Rect(x, y, cat_data["img"].get_width(), cat_data["img"].get_height())

            # Varmistetaan, ettei ole t�rm�yst� pelaajan kissan kanssa
            if player_rect.colliderect(new_cat_rect):
                continue  # Siirry seuraavaan iteraatioon, jos on t�rm�ys

            # Tarkistetaan my�s ettei kissa t�rm�� heti muihin luotuihin kissoihin
            collision = False
            for cat in cats:
                if new_cat_rect.colliderect(cat["rect"]):
                    collision = True
                    break

            if not collision:
                cats.append({"rect": new_cat_rect, "img": cat_data["img"], "text": cat_data["text"], "visible": False})
                break

    return cats


def game_loop():
    level = 1
    max_level = 4
    clock = pygame.time.Clock()
    speech_bubble_active = False  # Alustetaan puhekupla pois p��lt�
    speech_bubble_timer = 0
    speech_bubble_text = ""
    last_cat_text = None
    score = 0

    while level <= max_level:
        num_cats = level * 3
        player_rect = pygame.Rect(0, WINDOW_HEIGHT - cat_height, cat_width, cat_height)  # Pelaajan kissan sijainti

        # Luodaan kissoja, kunnes pelaajan kissa ei osu yhdenk��n el�imen kanssa
        while True:
            other_cats = create_cats(num_cats, level, player_rect)  # Luo kissoja nykyiselle tasolle
            
            # Tarkistetaan onko pelaajan kissa p��llekk�inen mink��n el�imen kanssa
            collision = any(player_rect.colliderect(cat["rect"]) for cat in other_cats)
            if not collision:
                break  # Jos ei ole t�rm�yksi�, lopetetaan silmukka

        cat_speed = 5
        score = 0  # Nollaa pisteet tason alussa
        speech_bubble_active = False  # Nollaa puhekupla-tila tason alussa
        speech_bubble_timer = 0  # Nollaa puhekuplan ajastin tason alussa


        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= cat_speed
            if keys[pygame.K_RIGHT]:
                player_rect.x += cat_speed
            if keys[pygame.K_UP]:
                player_rect.y -= cat_speed
            if keys[pygame.K_DOWN]:
                player_rect.y += cat_speed

            # Rajoita pelaajan kissan liikett� ikkunan sis�ll�
            if player_rect.x < 0:
                player_rect.x = 0
            elif player_rect.x > WINDOW_WIDTH - cat_width:
                player_rect.x = WINDOW_WIDTH - cat_width
            if player_rect.y < 0:
                player_rect.y = 0
            elif player_rect.y > WINDOW_HEIGHT - cat_height:
                player_rect.y = WINDOW_HEIGHT - cat_height

            # Piirr� tausta
            window.blit(background_images[level - 1], (0, 0))

            # Piirr� pelaajan kissa
            window.blit(player_cat_img, player_rect)

            # Tarkista t�rm�ykset muiden kissojen kanssa
            for cat in other_cats:
                if not cat["visible"] and player_rect.colliderect(cat["rect"]):
                    cat["visible"] = True  # Tee kissa n�kyv�ksi
                    score += 1  # Lis�� pisteit�
                    speech_bubble_active = True  # Aktivoi puhekupla t�rm�yksen j�lkeen
                    speech_bubble_text = cat["text"]  # Aseta puhekuplan teksti
                    speech_bubble_timer = 0  # Nollaa ajastin jokaisen uuden t�rm�yksen yhteydess�

            # Piirr� muut kissat
            for cat in other_cats:
                if cat["visible"]:
                    window.blit(cat["img"], cat["rect"])

            # Piirr� puhekupla, jos aktiivinen
            if speech_bubble_active:
                draw_speech_bubble(speech_bubble_text, (player_rect.x + cat_width // 2, player_rect.y))
                speech_bubble_timer += 1  # Lis�� ajastinta
                if speech_bubble_timer > 120:  # N�yt� 2 sekuntia 60 FPS:ll�
                    speech_bubble_active = False
                    speech_bubble_timer = 0  # Nollaa ajastin
                    last_cat_text = speech_bubble_text  # Tallenna viimeinen kissan teksti seuraavaa tasoa varten

            # N�yt� pisteet ja taso
            score_text = font.render(f"Pisteet: {score}/{num_cats}", True, WHITE)
            window.blit(score_text, (10, 10))  # Aseta pisteiden teksti vasempaan yl�kulmaan

            level_text = font.render(f"Taso: {level}", True, WHITE)
            window.blit(level_text, (10, 50))  # Aseta tasoteksti pisteiden alle

            
            # Jos kaikki kissat on ker�tty, n�yt� viimeisen ker�tyn el�imen teksti ennen siirtymist� seuraavalle tasolle
            if score == num_cats:

                if last_cat_text:
                    # N�yt� viimeisen el�imen puhekupla 2 sekunnin ajan
                    draw_speech_bubble(last_cat_text, (player_rect.x + cat_width // 2, player_rect.y))
                    pygame.display.update()
                    pygame.time.wait(2000)  # N�yt� puhekupla 2 sekuntia ennen tason vaihtoa
                
                    
                # Ask the question after showing the last cat's speech bubble
                level = ask_question(window, font, level, questions)  # Pass the questions to the ask_question function

                # Move to the next level    
                #level += 1
                pygame.time.wait(1000)  # Odota 1 sekunti ennen seuraavaa tasoa
                break  # Poistu pelisilm�st� ja siirry seuraavalle tasolle

            # P�ivit� n�ytt�
            pygame.display.update()

            # Aseta pelin p�ivitysnopeus
            clock.tick(60)  # Varmista 60 FPS



    # Lopeta peli, kun kaikki tasot on suoritettu
    game_over()

# Peli loppuu -toiminto
def game_over():
    window.fill(WHITE)
    game_over_text = font.render("Peli ohi! Olet suorittanut kaikki tasot!", True, BLACK)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))

    pygame.display.update()
    pygame.time.wait(3000)  # Odota 3 sekuntia ennen lopettamista
    pygame.quit()
    sys.exit()

# Aloita peli
game_loop()
