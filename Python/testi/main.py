import pygame
import asyncio


# Initialize Pygame
pygame.init()



# Screen dimensions
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Asyncio Pygame Example")

# Set up clock for framerate control
clock = pygame.time.Clock()

# Load background image and scale it to fit the screen
background_image = pygame.image.load('images/cow.jpg')
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Define a square object
square = pygame.Rect(50, 50, 50, 50)
square_speed = 5

# Function to handle game logic
async def move_square():
    global square
    while True:
        # Move the square
        square.x += square_speed
        if square.x > SCREEN_WIDTH:
            square.x = 0

        # Await the next frame
        await asyncio.sleep(0.016)  # ~60 frames per second

# Function to handle events like quitting
async def handle_events():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return  # Stop the asyncio loop and exit the game

        # Await the next frame
        await asyncio.sleep(0.01)

# Main loop
async def main():
    # Start asynchronous tasks for moving the square and handling events
    asyncio.create_task(move_square())
    asyncio.create_task(handle_events())

    while True:
        # Blit the background image onto the screen
        screen.blit(background_image, (0, 0))

        # Draw the moving square
        pygame.draw.rect(screen, RED, square)

        # Update the display
        pygame.display.flip()

        # Cap the framerate
        clock.tick(60)

        # Await the next frame
        await asyncio.sleep(0.01)

# Run the asyncio event loop
asyncio.run(main())
