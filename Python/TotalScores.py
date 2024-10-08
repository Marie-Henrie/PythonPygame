
import pygame
import random
import sys
import alkuGame
from questions import ask_question  # Import the ask_question function from another file

# Initialize the game
alkuGame.tervehdys()
pygame.init()

# Define window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mystic Forest")

# Define colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEECH_BUBBLE_COLOR = (255, 255, 200)  # Light yellow speech bubble
TASSUNJALKI_BG_COLOR = (200, 255, 200)  # Light green for paw prints score background
TASO_BG_COLOR = (200, 200, 255)  # Light blue for level background

# Fonts
font = pygame.font.Font(None, 48)
bubble_font = pygame.font.Font(None, 32)

# Load player cat image
player_cat_img = pygame.image.load("images/cat.png")
cat_width = player_cat_img.get_width()
cat_height = player_cat_img.get_height()

# Load other cats' images and texts
level_cats = {
    1: [
        {"img": pygame.image.load("images/bear.png"), "text": "Soon it starts snowing!", "visible": False},
        {"img": pygame.image.load("images/birdsinging.png"), "text": "What a beautiful day?", "visible": False},
        {"img": pygame.image.load("images/butterfly.png"), "text": "I love flowers I need them!", "visible": False},
        {"img": pygame.image.load("images/fox.png"), "text": "Where is my food?", "visible": False},
        {"img": pygame.image.load("images/reindeer.png"), "text": "Have you seen any moose?", "visible": False},
        {"img": pygame.image.load("images/mouse.png"), "text": "You can see me?", "visible": False},
        {"img": pygame.image.load("images/tassu.png"), "text": "You can see me?", "visible": False},

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
        {"img": pygame.image.load("images/janis.png"), "text": "A big jump!", "visible": False},
        {"img": pygame.image.load("images/ketturepolainen.png"), "text": "Kettu Repolainen is wise!", "visible": False},
        {"img": pygame.image.load("images/koirat.png"), "text": "The dogs are outside!", "visible": False}
    ],
    5: [
        {"img": pygame.image.load("images/bearfront.png"), "text": "Fish in the water", "visible": False},
        {"img": pygame.image.load("images/catwalking.png"), "text": "I love trees!", "visible": False},
        {"img": pygame.image.load("images/rabbit.png"), "text": "I just saw a fox!", "visible": False},
        {"img": pygame.image.load("images/wolf.png"), "text": "I need your help!", "visible": False}
    ]
}

# Define questions for each level
questions = {
    1: {
        "question": "Where do I live?",
        "options": ["1. In the forest", "2. On the street"],
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
    4: {
        "question": "Do you love forest?",
        "options": ["1. Yes", "2. No"],
        "correct": 1
    },
    # Add more questions for additional levels
}

# Scale cat images to appropriate size
for level in level_cats:
    for cat in level_cats[level]:
        cat["img"] = pygame.transform.scale(cat["img"], (100, 100))

# Load background images for each level
background_images = [
    pygame.transform.scale(pygame.image.load("images/metsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/ikivihreys.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/auringonpaiste.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/usvametsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/havumetsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))

]

# Function to draw speech bubbles
def draw_speech_bubble(text, position):
    bubble_width, bubble_height = 200, 100
    bubble_x, bubble_y = position[0] - bubble_width // 2, position[1] - bubble_height - 40  # Adjust position upwards

    # Ensure the speech bubble stays within window boundaries
    if bubble_x < 0:
        bubble_x = 0
    elif bubble_x + bubble_width > WINDOW_WIDTH:
        bubble_x = WINDOW_WIDTH - bubble_width
    if bubble_y < 0:
        bubble_y = 0
    elif bubble_y + bubble_height > WINDOW_HEIGHT:
        bubble_y = WINDOW_HEIGHT - bubble_height

    # Draw the bubble
    pygame.draw.rect(window, SPEECH_BUBBLE_COLOR, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(window, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)

    # Render text
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        if bubble_font.size(current_line + word)[0] <= bubble_width - 20:  # Leave space for bubble edges
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = bubble_font.render(line.strip(), True, BLACK)  # Remove extra spaces
        text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + 20 + i * bubble_font.get_height()))
        window.blit(text_surface, text_rect)

# Define safe zone dimensions for the score display area (top-left corner)
SAFE_ZONE_WIDTH = 220  # A bit wider than the score background area (200px width)
SAFE_ZONE_HEIGHT = 160  # Height covering the score displays for animals, paws, and levels

# Function to create cats at random positions without overlapping the player, other cats, or score display area
def create_cats(num_cats, level, player_rect):
    cats = []
    available_cats = level_cats[level]

    for _ in range(num_cats):
        while True:
            x = random.randint(0, WINDOW_WIDTH - cat_width)
            y = random.randint(0, WINDOW_HEIGHT - cat_height)
            cat_data = random.choice(available_cats)
            new_cat_rect = pygame.Rect(x, y, cat_data["img"].get_width(), cat_data["img"].get_height())

            # Ensure no collision with the player's cat or safe zone
            if player_rect.colliderect(new_cat_rect) or (x < SAFE_ZONE_WIDTH and y < SAFE_ZONE_HEIGHT):
                continue  # Try another position

            # Ensure no collision with existing cats
            collision = False
            for cat in cats:
                if new_cat_rect.colliderect(cat["rect"]):
                    collision = True
                    break

            if not collision:
                cats.append({"rect": new_cat_rect, "img": cat_data["img"], "text": cat_data["text"], "visible": False})
                break

    return cats


# Function to create paw prints at random positions
def create_tassunjaljet(num_tassut, player_rect):
    tassunjaljet = []
    tassu_img = pygame.image.load("images/tassu.png")
    tassu_img = pygame.transform.scale(tassu_img, (50, 50))  # Aseta koko sopivaksi

    for _ in range(num_tassut):
        while True:
            x = random.randint(0, WINDOW_WIDTH - tassu_img.get_width())
            y = random.randint(0, WINDOW_HEIGHT - tassu_img.get_height())
            new_tassu_rect = pygame.Rect(x, y, tassu_img.get_width(), tassu_img.get_height())

            # Varmista, ettei tassu ole pelaajan hahmon päällä
            if player_rect.colliderect(new_tassu_rect):
                continue

            tassunjaljet.append({"rect": new_tassu_rect, "img": tassu_img, "collected": False})
            break

    return tassunjaljet

def draw_speech_bubble(text, position):
    # Define bubble padding, size, and position
    bubble_padding = 10
    max_bubble_width = 200
    bubble_offset_y = 50  # Offset to position the bubble above the animal

    # Prepare the font for the bubble text
    font = pygame.font.SysFont(None, 24)

    # Split the text into words to handle wrapping within the bubble
    words = text.split()
    lines = []
    current_line = ""

    # Create lines that fit within the max bubble width
    for word in words:
        if font.size(current_line + word)[0] <= max_bubble_width:
            current_line += word + " "
        else:
            lines.append(current_line)
            current_line = word + " "
    if current_line:
        lines.append(current_line)

    # Calculate the width and height of the bubble
    bubble_width = max(font.size(line)[0] for line in lines) + 2 * bubble_padding
    bubble_height = (font.size(lines[0])[1] * len(lines)) + 2 * bubble_padding

    # Position the bubble above the animal, with an offset to avoid overlapping
    bubble_x = position[0] - bubble_width // 2
    bubble_y = position[1] - bubble_height - bubble_offset_y

    # Ensure the bubble doesn't go off-screen (adjust boundaries)
    if bubble_x < 0:
        bubble_x = 0
    if bubble_x + bubble_width > WINDOW_WIDTH:
        bubble_x = WINDOW_WIDTH - bubble_width
    if bubble_y < 0:
        bubble_y = 0

    # Draw the speech bubble rectangle with rounded corners
    bubble_rect = pygame.Rect(bubble_x, bubble_y, bubble_width, bubble_height)
    pygame.draw.rect(window, WHITE, bubble_rect, border_radius=10)

    # Draw the text inside the speech bubble
    for i, line in enumerate(lines):
        text_surface = font.render(line, True, BLACK)
        window.blit(text_surface, (bubble_x + bubble_padding, bubble_y + bubble_padding + i * font.size(line)[1]))

    # Draw a small triangle below the bubble, pointing to the animal
    triangle_center_x = position[0]
    triangle_points = [(triangle_center_x - 10, bubble_y + bubble_height), 
                       (triangle_center_x + 10, bubble_y + bubble_height), 
                       (triangle_center_x, bubble_y + bubble_height + 15)]
    pygame.draw.polygon(window, WHITE, triangle_points)

# Initialize total score and total paw score
total_score = 0
total_paw_score = 0

# Function to handle the game loop
def game_loop():
    global total_score, total_paw_score  # Access the global variables
    level = 1
    max_level = 5  # Define the maximum number of levels
    clock = pygame.time.Clock()
    state = 'playing'  # Possible states: 'playing', 'show_last_bubble', 'ask_question'
    speech_bubble_text = ""
    last_cat_text = ""

    while level <= max_level:  # Continue the loop while level is <= max_level
        num_cats = level + 2
        num_tassut = 2  # Number of paw prints per level

        player_rect = pygame.Rect(0, WINDOW_HEIGHT - cat_height, cat_width, cat_height)  # Player position

        # Create cats and paw prints
        other_cats = create_cats(num_cats, level, player_rect)
        tassunjaljet = create_tassunjaljet(num_tassut, player_rect)

        cat_speed = 5
        score = 0  # Reset score at the start of the level
        paw_score = 0  # Reset paw score at the start of the level
        speech_bubble_active = False
        speech_bubble_timer = 0
        last_cat_text = ""
        state = 'playing'  # Reset state for each level

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            if state == 'playing':
                # Player movement logic
                keys = pygame.key.get_pressed()
                
                # Stop the player's movement while the speech bubble is active
                if not speech_bubble_active:
                    if keys[pygame.K_LEFT]:
                        player_rect.x -= cat_speed
                    if keys[pygame.K_RIGHT]:
                        player_rect.x += cat_speed
                    if keys[pygame.K_UP]:
                        player_rect.y -= cat_speed
                    if keys[pygame.K_DOWN]:
                        player_rect.y += cat_speed

                # Ensure player stays within the window
                player_rect.x = max(0, min(WINDOW_WIDTH - cat_width, player_rect.x))
                player_rect.y = max(0, min(WINDOW_HEIGHT - cat_height, player_rect.y))

                # Draw background and player
                window.blit(background_images[level - 1], (0, 0))
                window.blit(player_cat_img, player_rect)

                # Check collisions with paw prints
                for tassu in tassunjaljet:
                    if not tassu["collected"] and player_rect.colliderect(tassu["rect"]):
                        tassu["collected"] = True
                        paw_score += 1

                # Draw paw prints
                for tassu in tassunjaljet:
                    if not tassu["collected"]:
                        window.blit(tassu["img"], tassu["rect"])

                # Check collisions with cats
                for cat in other_cats:
                    if not cat["visible"] and player_rect.colliderect(cat["rect"]):
                        cat["visible"] = True
                        score += 1  # Update score when collecting a cat
                        if score == num_cats:  # All cats collected
                            last_cat_text = cat["text"]
                            state = 'show_last_bubble'
                            break
                        else:
                            speech_bubble_text = cat["text"]
                            speech_bubble_active = True
                            speech_bubble_timer = 0

                # Draw other cats
                for cat in other_cats:
                    if cat["visible"]:
                        window.blit(cat["img"], cat["rect"])

                # Handle speech bubble display
                if speech_bubble_active:
                    draw_speech_bubble(speech_bubble_text, (player_rect.x + cat_width // 2, player_rect.y))
                # Example in your game loop to draw the bubble above the animal
                # Example in your game loop to draw the bubble next to the animal           
                    speech_bubble_timer += 1
                    if speech_bubble_timer > 120:  # 2 seconds
                        speech_bubble_active = False
                        speech_bubble_timer = 0

                # Display scores
                pygame.draw.rect(window, TASO_BG_COLOR, (10, 10, 200, 40))
                animal_score_text = font.render(f"Animals: {score}/{num_cats}", True, BLACK)
                window.blit(animal_score_text, (10, 10))

                pygame.draw.rect(window, TASSUNJALKI_BG_COLOR, (10, 60, 200, 40))
                paw_score_text = font.render(f"Paws: {paw_score}/{num_tassut}", True, BLACK)
                window.blit(paw_score_text, (10, 60))

                pygame.draw.rect(window, TASO_BG_COLOR, (10, 110, 200, 40))
                level_text = font.render(f"Level: {level}", True, BLACK)
                window.blit(level_text, (10, 110))

            elif state == 'show_last_bubble':
                window.blit(background_images[level - 1], (0, 0))
                window.blit(player_cat_img, player_rect)

                # Draw all visible cats
                for cat in other_cats:
                    if cat["visible"]:
                        window.blit(cat["img"], cat["rect"])

                # Draw the last speech bubble
                draw_speech_bubble(last_cat_text, (player_rect.x + cat_width // 2, player_rect.y))
                pygame.display.update()
                pygame.time.wait(2000)
                state = 'ask_question'  # Transition to asking question

            elif state == 'ask_question':
                # Ask the level-up question
                level = ask_question(window, font, level, questions)
                
                # Accumulate total scores after each level
                total_score += score
                total_paw_score += paw_score
                
                pygame.time.wait(1000)  # Optional wait after answering the question
                state = 'playing'  # Reset state for the next level
                running = False  # Exit the current level's game loop

            # Update the display and tick the clock
            if state != 'show_last_bubble':  # Avoid double updating during 'show_last_bubble'
                pygame.display.update()

            clock.tick(60)  # Maintain 60 FPS

    # Call game_over after completing all levels
    game_over()


# Function to handle game over screen
def game_over():
    global total_score, total_paw_score  # Access global variables
    
    window.fill(WHITE)
    
    # Display game over message
    game_over_text = font.render("Peli ohi! Olet suorittanut kaikki tasot!", True, BLACK)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 150))
    
    # Display total score and total paw score
    final_score_text = font.render(f"Total collect of animals: {total_score}", True, BLACK)
    window.blit(final_score_text, (WINDOW_WIDTH // 2 - final_score_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    
    final_paw_score_text = font.render(f"Total collect of paws: {total_paw_score}", True, BLACK)
    window.blit(final_paw_score_text, (WINDOW_WIDTH // 2 - final_paw_score_text.get_width() // 2, WINDOW_HEIGHT // 2 + 50))
    
    pygame.display.update()
    pygame.time.wait(5000)  # Wait for 5 seconds before quitting
    pygame.quit()
    sys.exit()

# Start the game
game_loop()