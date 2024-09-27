# question.py

import pygame

def ask_question(window, font, level):
    question_text = "Question: Is 2 + 2 = 4?"
    option_1 = "1. Yes"
    option_2 = "2. No"
    correct_answer = 1  # The correct answer is "Yes" (which is 1)

    # Display the question and options
    def display_question():
        window.fill((0, 0, 0))  # Clear the window to black
        question_surface = font.render(question_text, True, (255, 255, 255))
        option_1_surface = font.render(option_1, True, (255, 255, 255))
        option_2_surface = font.render(option_2, True, (255, 255, 255))

        # Place the text on the window
        window.blit(question_surface, (50, 200))
        window.blit(option_1_surface, (50, 250))
        window.blit(option_2_surface, (50, 300))
        pygame.display.update()

    # Display feedback for correct or incorrect answer
    def display_feedback(is_correct):
        window.fill((0, 0, 0))  # Clear the window to black
        if is_correct:
            feedback_surface = font.render("Correct! Moving to the next level.", True, (0, 255, 0))
        else:
            feedback_surface = font.render("Incorrect! Moving to the next level anyway.", True, (255, 0, 0))

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
                return level  # Return the current level if the user quits
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:  # If the player selects "Yes"
                    display_feedback(correct_answer == 1)  # Show feedback
                    waiting_for_input = False
                elif event.key == pygame.K_2:  # If the player selects "No"
                    display_feedback(correct_answer == 2)  # Show feedback
                    waiting_for_input = False

    # Return the next level, both answers move to the next level
    return level + 1
