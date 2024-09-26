import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Define window dimensions
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mystic Forest")

# Define colors (RGB)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SPEECH_BUBBLE_COLOR = (255, 255, 200)  # Light yellow for speech bubble

# Load fonts
font = pygame.font.Font(None, 48)
bubble_font = pygame.font.Font(None, 32)
story_font = pygame.font.Font(None, 40)
button_font = pygame.font.Font(None, 60)

# Load player cat image with error handling
def load_image(image_path):
    try:
        return pygame.image.load(image_path)
    except pygame.error as e:
        print(f"Error loading image '{image_path}': {e}")
        return None

# Load images for player cat and other animals
player_cat_img = load_image("images/cat.png")
cat_width = player_cat_img.get_width() if player_cat_img else 0
cat_height = player_cat_img.get_height() if player_cat_img else 0

# Load other cats and their associated text
level_cats = {
    1: [
        {"img": load_image("images/bear.png"), "text": "Soon it starts snowing!", "visible": False},
        {"img": load_image("images/birdsinging.png"), "text": "What a beautiful day?", "visible": False},
        {"img": load_image("images/butterfly.png"), "text": "I love flowers I need them!", "visible": False},
        {"img": load_image("images/fox.png"), "text": "Where is my food?", "visible": False},
        {"img": load_image("images/reindeer.png"), "text": "Have you seen any moose?", "visible": False},
        {"img": load_image("images/mouse.png"), "text": "You can see me?", "visible": False}
    ]
}

# Scale animal images to appropriate size
for level in level_cats:
    for cat in level_cats[level]:
        if cat["img"]:
            cat["img"] = pygame.transform.scale(cat["img"], (100, 100))

# Load background images with error handling
background_images = [load_image("images/metsa.jpg")]

# Function to draw speech bubbles
def draw_speech_bubble(text, position):
    bubble_width, bubble_height = 200, 100
    bubble_x, bubble_y = position[0] - bubble_width // 2, position[1] - bubble_height - 40

    # Ensure bubble stays within window
    bubble_x = max(0, min(bubble_x, WINDOW_WIDTH - bubble_width))
    bubble_y = max(0, min(bubble_y, WINDOW_HEIGHT - bubble_height))

    pygame.draw.rect(window, SPEECH_BUBBLE_COLOR, (bubble_x, bubble_y, bubble_width, bubble_height), border_radius=10)
    pygame.draw.rect(window, BLACK, (bubble_x, bubble_y, bubble_width, bubble_height), 2, border_radius=10)

    # Split text into lines that fit in the bubble
    words = text.split(' ')
    lines = []
    current_line = ''

    for word in words:
        if bubble_font.size(current_line + word)[0] <= bubble_width - 20:
            current_line += word + ' '
        else:
            lines.append(current_line)
            current_line = word + ' '

    if current_line:
        lines.append(current_line)

    for i, line in enumerate(lines):
        text_surface = bubble_font.render(line.strip(), True, BLACK)
        text_rect = text_surface.get_rect(center=(bubble_x + bubble_width // 2, bubble_y + 20 + i * bubble_font.get_height()))
        window.blit(text_surface, text_rect)

# Function to create cats at random positions without overlapping the player
def create_cats(num_cats, level, player_rect):
    cats = []
    available_cats = level_cats[level]

    for _ in range(num_cats):
        retry_limit = 10  # Prevents infinite loop in case of small space
        while retry_limit > 0:
            x = random.randint(0, WINDOW_WIDTH - cat_width)
            y = random.randint(0, WINDOW_HEIGHT - cat_height)
            cat_data = random.choice(available_cats)
            new_cat_rect = pygame.Rect(x, y, cat_data["img"].get_width(), cat_data["img"].get_height())

            # Ensure no collision with player
            if player_rect.colliderect(new_cat_rect):
                retry_limit -= 1
                continue

            # Ensure no collision with other cats
            collision = any(new_cat_rect.colliderect(cat["rect"]) for cat in cats)

            if not collision:
                cats.append({"rect": new_cat_rect, "img": cat_data["img"], "text": cat_data["text"], "visible": False})
                break

    return cats

# Function to display the story screen with a start button
def show_story_screen():
    story_text = [
        "Mystic Forest is a game where you need to collect", 
        "mystical animals in an enchanted forest.", 
        "Each animal will tell you a story when you approach them.", 
        "Are you ready for the adventure?"
    ]

    start_button_rect = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 100, 200, 50)
    clock = pygame.time.Clock()

    showing_story = True
    while showing_story:
        window.fill(WHITE)

        # Draw the story text
        for i, line in enumerate(story_text):
            text_surface = story_font.render(line, True, BLACK)
            window.blit(text_surface, (WINDOW_WIDTH // 2 - text_surface.get_width() // 2, 100 + i * 40))

        # Draw "Start Game" button
        pygame.draw.rect(window, BLACK, start_button_rect)
        start_text = button_font.render("Start Game", True, WHITE)
        window.blit(start_text, (start_button_rect.x + (start_button_rect.width - start_text.get_width()) // 2, start_button_rect.y + 5))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    showing_story = False  # Exit the story screen and start the game

        pygame.display.update()
        clock.tick(60)  # Limit the frame rate

# Main game loop function
def game_loop():
    level = 1
    max_level = 4
    clock = pygame.time.Clock()
    speech_bubble_active = False
    speech_bubble_timer = 0
    speech_bubble_text = ""
    last_cat_text = None
    score = 0

    while level <= max_level:
        num_cats = level * 3
        player_rect = pygame.Rect(0, WINDOW_HEIGHT - cat_height, cat_width, cat_height)  # Player cat position

        # Create cats until the player cat doesn't collide with any animal
        other_cats = create_cats(num_cats, level, player_rect)  # Create cats for the current level
        
        # Ensure other_cats have valid rects
        while True:
            collision = any(player_rect.colliderect(cat["rect"]) for cat in other_cats)
            if not collision:
                break  # If no collisions, exit loop
            other_cats = create_cats(num_cats, level, player_rect)  # Retry creating cats

        cat_speed = 5

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

            # Limit player cat's movement within the window
            player_rect.x = max(0, min(player_rect.x, WINDOW_WIDTH - cat_width))
            player_rect.y = max(0, min(player_rect.y, WINDOW_HEIGHT - cat_height))

            # Draw background
            window.fill(WHITE)  # Clear the window
            if level - 1 < len(background_images):  # Check if background exists
                window.blit(background_images[level - 1], (0, 0))
            window.blit(player_cat_img, player_rect.topleft)

            # Check for collisions with other cats
            for cat in other_cats:
                if player_rect.colliderect(cat["rect"]):
                    cat["visible"] = True  # Show the cat when hit
                    speech_bubble_text = cat["text"]
                    speech_bubble_active = True
                    last_cat_text = cat
                    score += 1  # Increase score when the player collects a cat
                    other_cats.remove(cat)  # Remove collected cat from the list

            # Draw speech bubble if active
            if speech_bubble_active:
                draw_speech_bubble(speech_bubble_text, (player_rect.x + cat_width // 2, player_rect.y))

                # Timer for speech bubble visibility
                speech_bubble_timer += 1
                if speech_bubble_timer > 100:  # Show bubble for 100 frames
                    speech_bubble_active = False
                    speech_bubble_timer = 0
                    speech_bubble_text = ""

            # Draw other cats only if they are visible
            for cat in other_cats:
                if cat["visible"]:
                    window.blit(cat["img"], cat["rect"].topleft)

            # Display score
            score_surface = font.render(f"Score: {score}", True, BLACK)
            window.blit(score_surface, (10, 10))  # Display score at top-left corner

            pygame.display.update()
            clock.tick(60)  # Limit the frame rate

        level += 1


# Start the game
show_story_screen()
game_loop()
