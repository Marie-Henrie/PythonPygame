# pawscollector.py
import pygame
import random

class PawPrints:
    PAW_IMAGE_SIZE = (50, 50)  # Define a constant size for paw images

    def __init__(self, level, window_width, window_height):
        self.level = level
        self.window_width = window_width
        self.window_height = window_height
        self.paw_image = self.load_paw_image()  # Load a single image
        self.paw_positions = []
        self.paw_visible = []  # Track visibility of paw prints
        self.create_paw_prints()

    def load_paw_image(self):
        # Load the paw image (used for all levels)
        try:
            paw_image = pygame.image.load("images/tassu.png")
            paw_image = pygame.transform.scale(paw_image, self.PAW_IMAGE_SIZE)
            return paw_image
        except pygame.error as e:
            print(f"Error loading paw image: {e}")
            # Return a fallback placeholder surface (violet square)
            placeholder = pygame.Surface(self.PAW_IMAGE_SIZE)
            placeholder.fill((255, 0, 255))  # Violet color
            return placeholder

    def create_paw_prints(self):
        # Create random positions for paw prints based on the current level
        for _ in range(self.level * 2):  # Example: 2 * level paw prints
            x = random.randint(0, self.window_width - self.PAW_IMAGE_SIZE[0])  # Window width - paw width
            y = random.randint(0, self.window_height - self.PAW_IMAGE_SIZE[1])  # Window height - paw height
            self.paw_positions.append(pygame.Rect(x, y, *self.PAW_IMAGE_SIZE))  # Store positions
            self.paw_visible.append(False)  # Initially set paw prints to invisible

    def draw_paws(self, window):
        # Draw paw prints on the window if they are visible
        for i, paw_rect in enumerate(self.paw_positions):
            if self.paw_visible[i]:  # Only draw if visible
                window.blit(self.paw_image, paw_rect)

    def collect_paw(self, player_rect):
        # Check if the player collects any paw print
        collected = 0  # Count of collected paw prints
        for i, paw_rect in enumerate(self.paw_positions):
            if not self.paw_visible[i] and player_rect.colliderect(paw_rect):
                self.paw_visible[i] = True  # Make the paw print visible
                collected += 1  # Increment the collected count
        return collected  # Return the count of newly collected paw prints

    def all_paws_collected(self):
        # Check if all paw prints have been collected
        return all(self.paw_visible)
