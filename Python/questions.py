import pygame

def ask_question(window, font, level, questions):
    # Get the question and options for the current level
    current_question = questions.get(level, {"question": "Default question?", "options": ["1. Yes", "2. No"], "correct": 1})
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
