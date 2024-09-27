import pygame
import sys




def tervehdys():
    print("Hei!")

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
        draw_text("The idea of the game is to move and collect points.", small_font, BLACK, screen, WIDTH // 2, HEIGHT // 4 + 50)
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

