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
        {"img": pygame.image.load("images/karhu.jpg"), "text": "I have lived here forever.", "visible": False}
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

# Scale cat images to appropriate size
for level in level_cats:
    for cat in level_cats[level]:
        cat["img"] = pygame.transform.scale(cat["img"], (100, 100))

# Load background images for each level
background_images = [
    pygame.transform.scale(pygame.image.load("images/metsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/ikivihreys.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/auringonpaiste.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/usvametsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT))
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

# Function to create cats at random positions without overlapping the player or other cats
def create_cats(num_cats, level, player_rect):
    cats = []
    available_cats = level_cats[level]

    for _ in range(num_cats):
        while True:
            x = random.randint(0, WINDOW_WIDTH - cat_width)
            y = random.randint(0, WINDOW_HEIGHT - cat_height)
            cat_data = random.choice(available_cats)
            new_cat_rect = pygame.Rect(x, y, cat_data["img"].get_width(), cat_data["img"].get_height())

            # Ensure no collision with the player's cat
            if player_rect.colliderect(new_cat_rect):
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

# Function to handle the game loop
def game_loop():
    level = 1
    max_level = 4
    clock = pygame.time.Clock()
    state = 'playing'  # Possible states: 'playing', 'show_last_bubble', 'ask_question'
    speech_bubble_text = ""
    last_cat_text = ""
    score = 0

    while level <= max_level:
        num_cats = level * 3
        player_rect = pygame.Rect(0, WINDOW_HEIGHT - cat_height, cat_width, cat_height)  # Player position

        # Create cats
        other_cats = create_cats(num_cats, level, player_rect)

        cat_speed = 5
        score = 0  # Reset score at the start of the level
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
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT]:
                    player_rect.x -= cat_speed
                if keys[pygame.K_RIGHT]:
                    player_rect.x += cat_speed
                if keys[pygame.K_UP]:
                    player_rect.y -= cat_speed
                if keys[pygame.K_DOWN]:
                    player_rect.y += cat_speed

                # Ensure player cat stays within the window bounds
                player_rect.x = max(0, min(WINDOW_WIDTH - cat_width, player_rect.x))
                player_rect.y = max(0, min(WINDOW_HEIGHT - cat_height, player_rect.y))

                # Draw background and player
                window.blit(background_images[level - 1], (0, 0))
                window.blit(player_cat_img, player_rect)

                # Check collisions and activate speech bubble if necessary
                for cat in other_cats:
                    if not cat["visible"] and player_rect.colliderect(cat["rect"]):
                        cat["visible"] = True
                        score += 1
                        if score == num_cats:
                            last_cat_text = cat["text"]
                            state = 'show_last_bubble'
                            break  # Exit collision checking after setting state
                        else:
                            speech_bubble_text = cat["text"]
                            speech_bubble_active = True
                            speech_bubble_timer = 0

                # Draw other cats
                for cat in other_cats:
                    if cat["visible"]:
                        window.blit(cat["img"], cat["rect"])

                # Handle speech bubble display for collected cats
                if speech_bubble_active:
                    draw_speech_bubble(speech_bubble_text, (player_rect.x + cat_width // 2, player_rect.y))
                    speech_bubble_timer += 1
                    if speech_bubble_timer > 120:  # Show for 2 seconds (60 FPS * 2 seconds)
                        speech_bubble_active = False
                        speech_bubble_timer = 0

                # Display score and level
                score_text = font.render(f"Pisteet: {score}/{num_cats}", True, WHITE)
                window.blit(score_text, (10, 10))  # Position at top-left
                level_text = font.render(f"Taso: {level}", True, WHITE)
                window.blit(level_text, (10, 50))  # Below the score

            elif state == 'show_last_bubble':
                # Redraw background and player
                window.blit(background_images[level - 1], (0, 0))
                window.blit(player_cat_img, player_rect)

                # Draw all visible cats
                for cat in other_cats:
                    if cat["visible"]:
                        window.blit(cat["img"], cat["rect"])

                # Draw the last speech bubble
                draw_speech_bubble(last_cat_text, (player_rect.x + cat_width // 2, player_rect.y))
                pygame.display.update()
                pygame.time.wait(2000)  # Wait for 2 seconds to display the speech bubble
                state = 'ask_question'  # Transition to asking question

            elif state == 'ask_question':
                # Ask the level-up question
                level = ask_question(window, font, level, questions)
                pygame.time.wait(1000)  # Optional wait after answering the question
                state = 'playing'  # Reset state for the next level
                running = False  # Exit the current level's game loop

            # Update the display and tick the clock
            if state != 'show_last_bubble':  # Avoid double updating during 'show_last_bubble'
                pygame.display.update()

            clock.tick(60)  # Maintain 60 FPS

    # End game after completing all levels
    game_over()

# Function to handle game over screen
def game_over():
    window.fill(WHITE)
    game_over_text = font.render("Peli ohi! Olet suorittanut kaikki tasot!", True, BLACK)
    window.blit(game_over_text, (WINDOW_WIDTH // 2 - game_over_text.get_width() // 2, WINDOW_HEIGHT // 2 - 50))
    pygame.display.update()
    pygame.time.wait(3000)  # Wait for 3 seconds before quitting
    pygame.quit()
    sys.exit()

# Start the game
game_loop()
