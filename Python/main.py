

import pygame
import random
import sys
import asyncio
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
        {"img": pygame.image.load("images/karhu.png"), "text": "The bear roars!", "visible": False},
        {"img": pygame.image.load("images/kirahvi.png"), "text": "I sing what I want.", "visible": False},
        {"img": pygame.image.load("images/nukkuvaKissa.png"), "text": "I am sleeping.", "visible": False},
        {"img": pygame.image.load("images/otter.png"), "text": "I belong in the water!", "visible": False}
    ],
    3: [
        {"img": pygame.image.load("images/orava.png"), "text": "The squirrel is jumping in the trees!", "visible": False},
        {"img": pygame.image.load("images/kissakumara.png"), "text": "Mysterious cat!", "visible": False},
        {"img": pygame.image.load("images/orava1.png"), "text": "I live here.", "visible": False},
        {"img": pygame.image.load("images/karhuSininen.png"), "text": "The blue bear is rare!", "visible": False},
        {"img": pygame.image.load("images/fox.png"), "text": "Where is my food?!", "visible": False},
        {"img": pygame.image.load("images/catfront.png"), "text": "Mysterious cat!", "visible": False},
        {"img": pygame.image.load("images/catPlay.png"), "text": "I live here.", "visible": False},
        {"img": pygame.image.load("images/ampiainen.png"), "text": "Where is my flower?", "visible": False}
    ],
    4: [
        {"img": pygame.image.load("images/kala.png"), "text": "Fish in the water.", "visible": False},
        {"img": pygame.image.load("images/janis.png"), "text": "A big jump!", "visible": False},
        {"img": pygame.image.load("images/ketturepolainen.png"), "text": "Fox Repolainen is wise!", "visible": False},
        {"img": pygame.image.load("images/koirat.png"), "text": "The dogs are outside!", "visible": False},
        {"img": pygame.image.load("images/forestReindeer.png"), "text": "Have you seen any moose?", "visible": False},
        {"img": pygame.image.load("images/butterflyOrange.png"), "text": "Mysterious cat!", "visible": False},
        {"img": pygame.image.load("images/snake.png"), "text": "I live here.", "visible": False},
        {"img": pygame.image.load("images/wolf.png"), "text": "Leave me alone.", "visible": False}
    ],
    5: [
        {"img": pygame.image.load("images/bearfront.png"), "text": "Fish in the water", "visible": False},
        {"img": pygame.image.load("images/catwalking.png"), "text": "I love trees!", "visible": False},
        {"img": pygame.image.load("images/rabbit.png"), "text": "I just saw a fox!", "visible": False},
        {"img": pygame.image.load("images/wolf.png"), "text": "I need your help!", "visible": False},
        {"img": pygame.image.load("images/orava.png"), "text": "I live here!", "visible": False},
        {"img": pygame.image.load("images/kissakumara.png"), "text": "Mysterious cat!", "visible": False},
        {"img": pygame.image.load("images/pesukarhu.png"), "text": "I live here", "visible": False},
        {"img": pygame.image.load("images/otter.png"), "text": "I love water.", "visible": False}
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

# Define the speech bubble dimensions and position
BUBBLE_WIDTH, BUBBLE_HEIGHT = 220, 160
BUBBLE_X = WINDOW_WIDTH - BUBBLE_WIDTH - 10
BUBBLE_Y = 10

# Function to check if a position overlaps with the speech bubble area
def is_position_valid(position, bubble_rect):
    animal_rect = pygame.Rect(position[0], position[1], cat_width, cat_height)  # Animal rectangle
    return not animal_rect.colliderect(bubble_rect)  # Check for collision with the bubble

# Create a rectangle for the speech bubble area
BUBBLE_RECT = pygame.Rect(BUBBLE_X, BUBBLE_Y, BUBBLE_WIDTH, BUBBLE_HEIGHT)

# Function to create cats at random positions without overlapping the player, other cats, or score display area
def create_cats(num_cats, level, player_rect):
    cats = []
    available_cats = level_cats[level]

    # List to track used animal indices
    used_indices = set()

    # Create a list to hold valid positions
    valid_positions = []

    # Populate valid positions within the window
    for x in range(0, WINDOW_WIDTH - cat_width, cat_width):  # Incrementing by cat_width to avoid overlaps
        for y in range(0, WINDOW_HEIGHT - cat_height, cat_height):  # Same for height
            new_cat_rect = pygame.Rect(x, y, cat_width, cat_height)
            # Ensure no collision with the player's cat or safe zone
            if player_rect.colliderect(new_cat_rect) or (x < SAFE_ZONE_WIDTH and y < SAFE_ZONE_HEIGHT):
                continue  # Skip this position

            # Ensure no collision with the speech bubble area
            if new_cat_rect.colliderect(BUBBLE_RECT):
                continue  # Skip this position

            valid_positions.append((x, y))  # Add valid positions to the list

    # Shuffle valid positions to randomize placement
    random.shuffle(valid_positions)

    # Select cats without repeating within the same level
    for i in range(min(num_cats, len(valid_positions), len(available_cats))):  # Limit to available valid positions and available cats
        # Randomly select an unused index from available_cats
        cat_index = random.choice([index for index in range(len(available_cats)) if index not in used_indices])
        used_indices.add(cat_index)  # Mark this index as used
        
        # Get the cat data using the selected index
        cat_data = available_cats[cat_index]
        
        # Get the corresponding position from valid_positions
        x, y = valid_positions[i]
        new_cat_rect = pygame.Rect(x, y, cat_data["img"].get_width(), cat_data["img"].get_height())
        
        cats.append({"rect": new_cat_rect, "img": cat_data["img"], "text": cat_data["text"], "visible": False})

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

            # Varmista, ettei tassu ole pelaajan hahmon paalla
            if player_rect.colliderect(new_tassu_rect):
                continue

            tassunjaljet.append({"rect": new_tassu_rect, "img": tassu_img, "collected": False})
            break

    return tassunjaljet

# Function to draw speech bubbles in the top-right corner
def draw_speech_bubble_top_right(text):
    bubble_width, bubble_height = 220, 160  # Define the size of the bubble
    bubble_x, bubble_y = WINDOW_WIDTH - bubble_width - 10, 10  # Position in the top-right corner with some padding

    # Draw the speech bubble background
    pygame.draw.rect(window, SPEECH_BUBBLE_COLOR, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(window, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)

    # Render text, wrapping if necessary
    words = text.split(' ')
    lines = []
    current_line = ''

    # Split text into multiple lines to fit within the bubble
    for word in words:
        if bubble_font.size(current_line + word)[0] <= bubble_width - 20:  # Leave space for bubble padding
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '

    if current_line:
        lines.append(current_line)

    # Draw each line of text within the bubble
    for i, line in enumerate(lines):
        text_surface = bubble_font.render(line.strip(), True, BLACK)  # Render each line of text
        text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + 20 + i * bubble_font.get_height()))
        window.blit(text_surface, text_rect)
# Initialize total score and total paw score
total_score = 0
total_paw_score = 0

# Function to handle the game loop
async def main():
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
                            speech_bubble_timer = 0  # Reset timer on new speech

                # Draw other cats
                for cat in other_cats:
                    if cat["visible"]:
                        window.blit(cat["img"], cat["rect"])

                # Handle speech bubble display in the top-right corner
                if speech_bubble_active:
                    draw_speech_bubble_top_right(speech_bubble_text)
                    speech_bubble_timer += 1
                    if speech_bubble_timer > 120:  # Show for 2 seconds
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
                draw_speech_bubble_top_right(last_cat_text)
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
            await asyncio.sleep(0)

    # Call game_over after completing all levels
    game_over()



# Function to handle game over screen
def game_over():
    global total_score, total_paw_score  # Access global variables
    
    window.fill(WHITE)
    
    # Display game over message
    game_over_text = font.render("Game over! You have completed all the levels!", True, BLACK)
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
#main()
asyncio.run(main())