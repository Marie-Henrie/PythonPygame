# paws.py
import pygame
import random

# Define a class to manage paw prints
class PawPrints:
    def __init__(self, level):
        self.level = level
        self.paw_images = self.load_paw_images()
        self.paw_positions = []
        self.paw_visible = []  # Track visibility of paw prints
        self.create_paw_prints()

    def load_paw_images(self):
        # Load paw images for different levels
        paw_images = {
            1: pygame.image.load("images/tassu.png"),
            2: pygame.image.load("images/tassut.png"),
            3: pygame.image.load("images/tassu.png"),
            4: pygame.image.load("images/tassut.png"),
        }
        return paw_images

    def create_paw_prints(self):
        # Create random positions for paw prints based on the current level
        for _ in range(self.level * 2):  # Example: 2 * level paw prints
            x = random.randint(0, 800 - 50)  # Assuming paw image width is 50
            y = random.randint(0, 600 - 50)  # Assuming paw image height is 50
            self.paw_positions.append(pygame.Rect(x, y, 50, 50))  # Store positions
            self.paw_visible.append(False)  # Initially set paw prints to invisible

    def draw_paws(self, window):
        # Draw paw prints on the window if they are visible
        for i, paw_rect in enumerate(self.paw_positions):
            if self.paw_visible[i]:  # Only draw if visible
                window.blit(self.paw_images[self.level], paw_rect)

    def collect_paw(self, player_rect):
        # Check if the player collects any paw print
        collected = 0  # Count of collected paw prints
        for i, paw_rect in enumerate(self.paw_positions):
            if not self.paw_visible[i] and player_rect.colliderect(paw_rect):
                self.paw_visible[i] = True  # Make the paw print visible
                collected += 1  # Increment the collected count
        return collected  # Return the count of newly collected paw prints
