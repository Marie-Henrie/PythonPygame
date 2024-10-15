

import pygame
import random
import sys
import asyncio

# Initialize pygame
pygame.init()

# Define some constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
BUTTON_COLOR = (100, 200, 100)
BUTTON_HOVER_COLOR = (150, 255, 150)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mystic Forest")

# Define fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

def draw_text(text, font, color, surface, x, y):
    """ Draw text on the screen """
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def game_intro():
    """ Function to display game idea and instructions """
    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill(WHITE)

        # Display game idea
        draw_text("Welcome to the Game!", font, BLACK, screen, WIDTH // 2, HEIGHT // 4)
        draw_text("The idea of the game is to move and find and collect animals.", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 4 + 50)
        draw_text("Use arrow keys to move.", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 4 + 80)

        # Draw Start Game button
        mouse = pygame.mouse.get_pos()
        button_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)

        if button_rect.collidepoint(mouse):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button_rect)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button_rect)

        draw_text("Start Game", font, BLACK, screen, WIDTH // 2, HEIGHT // 2 + 25)

        # Check for mouse click on the button
        if event.type == pygame.MOUSEBUTTONDOWN and button_rect.collidepoint(mouse):
            intro = False

        pygame.display.update()


# Start the game with the intro screen
game_intro()



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
        {"img": pygame.image.load("images/fox.png"), "text": "Soon it starts snowing!", "visible": False},
        {"img": pygame.image.load("images/bear.png"), "text": "What a beautiful day?", "visible": False},
        {"img": pygame.image.load("images/birdsinging.png"), "text": "I love flowers I need them!", "visible": False},
        {"img": pygame.image.load("images/butterfly.png"), "text": "Where is my food?", "visible": False},
    ],
    2: [
        {"img": pygame.image.load("images/fox.png"), "text": "Soon it starts snowing!", "visible": False},
        {"img": pygame.image.load("images/fox.png"), "text": "What a beautiful day?", "visible": False},
        {"img": pygame.image.load("images/fox.png"), "text": "I love flowers I need them!", "visible": False},
        {"img": pygame.image.load("images/fox.png"), "text": "Where is my food?", "visible": False},
      
    ],

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
    
    # Add more questions for additional levels
}

# Scale cat images to appropriate size
for level in level_cats:
    for cat in level_cats[level]:
        cat["img"] = pygame.transform.scale(cat["img"], (100, 100))

# Load background images for each level
background_images = [
    pygame.transform.scale(pygame.image.load("images/metsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
    pygame.transform.scale(pygame.image.load("images/metsa.jpg"), (WINDOW_WIDTH, WINDOW_HEIGHT)),
   
]


def ask_question(window, font, level, questions):
    # Get the question and options for the current level
    current_question = questions.get(level, {"question": "Do you wanna quick?", "options": ["1. Yes", "2. No"], "correct": 1})
    question_text = current_question["question"]
    option_1 = current_question["options"][0]
    option_2 = current_question["options"][1]
    correct_answer = current_question["correct"]

    # Function to display the question and options
    def display_question():
        window.fill((0, 0, 0))  # Clear the window with black
        question_surface = font.render(question_text, True, (255, 255, 255))
        option_1_surface = font.render(option_1, True, (255, 255, 255))
        option_2_surface = font.render(option_2, True, (255, 255, 255))

        # Display the texts in the window
        window.blit(question_surface, (50, 200))
        window.blit(option_1_surface, (50, 250))
        window.blit(option_2_surface, (50, 300))
        pygame.display.update()

    # Function to display feedback on whether the answer is correct or not
    def display_feedback(is_correct):
        window.fill((0, 0, 0))  # Clear the window with black
        if is_correct:
            feedback_surface = font.render("Correct! Moving to the next level.", True, (0, 255, 0))
        else:
            feedback_surface = font.render("Wrong! Replay the level.", True, (255, 0, 0))

        window.blit(feedback_surface, (50, 250))
        pygame.display.update()
        pygame.time.wait(2000)  # Show the feedback for 2 seconds

    # Show the question and wait for user input
    display_question()
    waiting_for_input = True
    while waiting_for_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return level  # Return the current level if the game is quit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # If player selects option 1
                    is_correct = correct_answer == 1  # Check if answer is correct
                    display_feedback(is_correct)  # Show feedback
                    waiting_for_input = False
                elif event.key == pygame.K_2:  # If player selects option 2
                    is_correct = correct_answer == 2  # Check if answer is correct
                    display_feedback(is_correct)  # Show feedback
                    waiting_for_input = False

    # Return the next level if correct, otherwise replay the same level
    if is_correct:
        return level + 1  # Advance to the next level
    else:
        return level  # Replay the same level if the answer was wrong



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
    max_level = 1  # Define the maximum number of levels
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
#main()
asyncio.run(main())