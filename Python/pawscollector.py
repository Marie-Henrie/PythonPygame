import pygame
import random

PAW_IMAGE_SIZE = (50, 50)  # Constant size for paw images
PAW_COLLECTED_COUNT = 0  # Keep track of how many paws have been collected

def load_paw_image():
    """Load and return the paw image, or a placeholder if loading fails."""
    try:
        paw_image = pygame.image.load("images/tassu.png")
        paw_image = pygame.transform.scale(paw_image, PAW_IMAGE_SIZE)
        return paw_image
    except pygame.error as e:
        print(f"Error loading paw image: {e}")
        # Return a fallback placeholder surface (violet square)
        placeholder = pygame.Surface(PAW_IMAGE_SIZE)
        placeholder.fill((255, 0, 255))  # Violet color
        return placeholder

def create_paw(window_width, window_height):
    """Create a single paw dictionary at a random position."""
    x = random.randint(0, window_width - PAW_IMAGE_SIZE[0])
    y = random.randint(0, window_height - PAW_IMAGE_SIZE[1])
    return {
        'image': load_paw_image(),  # Load paw image
        'position': pygame.Rect(x, y, *PAW_IMAGE_SIZE),  # Set paw position
        'visible': True  # Initially visible
    }

def initialize_paws(number_of_paws, window_width, window_height):
    """Initialize a list of paw dictionaries."""
    return [create_paw(window_width, window_height) for _ in range(number_of_paws)]

def draw_paws(window, paws):
    """Draw all visible paws on the screen."""
    for paw in paws:
        if paw['visible']:
            window.blit(paw['image'], paw['position'])

def collect_paw(paws, player_rect):
    """Check if the player collects any paw and update its state."""
    global PAW_COLLECTED_COUNT
    for paw in paws:
        if paw['visible'] and player_rect.colliderect(paw['position']):
            paw['visible'] = False  # Mark the paw as collected (hide it)
            PAW_COLLECTED_COUNT += 1  # Increment collected count
            return True  # Return True to indicate a paw was collected
    return False

def get_collected_count():
    """Return how many paws have been collected."""
    return PAW_COLLECTED_COUNT
