import random
import pygame
import sys
import tkinter.messagebox as tkMessageBox
from googletrans import Translator
import loginConfig
questions = ["¿En cuál país le gustaria vivir?", "¿Cuál es su libro favorito?", "¿Cuál es su animal favorito?", "¿Cuál es su juego de mesa favorito?", "¿Cuál es su pelicula favorita?"]
def get_random_questions(questions, num_questions=2):
    if num_questions > len(questions):
        num_questions = len(questions)
    random_questions = random.sample(questions, num_questions)
    return random_questions

def startQuestionLogin(user, language):
    # Initialize pygame
    pygame.init()

    # Load your image
    if language == "es":
        image = pygame.image.load('visuals/imágenesEspañol/4.png')

    if language == "en":
        image = pygame.image.load('visuals/imágenesInglés/14.png')


    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    target_language = language
    random_questions = get_random_questions(questions, num_questions=2)

    # Set screen resolution
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h
    window = pygame.display.set_mode((screen_width, screen_height))

    # Calculate the center of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Set the width and height for the input boxes
    input_box_width = 300
    input_box_height = 32



    # Get the image's original dimensions
    original_width, original_height = image.get_size()

    # Calculate the scaling factors to fit the image to the screen
    scale_factor_width = screen_width / original_width
    scale_factor_height = screen_height / original_height

    # Choose the minimum scaling factor to maintain aspect ratio
    min_scale_factor = min(scale_factor_width, scale_factor_height)

    # Scale the image while maintaining aspect ratio
    new_width = int(original_width * min_scale_factor)
    new_height = int(original_height * min_scale_factor)
    scaled_image = pygame.transform.scale(image, (new_width, new_height))
    pygame.display.set_caption("Eagle Defender - Registration")


    """
    input: text (str), x coord (int), y coord (int)
    summary: Renders and displays text on the screen
    outputs: None
    """
    def drawText(text, x, y):
        renderedText = font.render(text, True, (0, 0, 0))
        window.blit(renderedText, (x, y))


    """
    input: text, Language code
    summary: uses Google Translate to translate a given text
    outputs: translated language
    """
    def translate_text(text, target_language):
        translator = Translator()
        try:
            translated = translator.translate(text, dest=target_language)
            return translated.text
        except AttributeError as e:
            print("Translation error:", e)
            return text  # Return the original text in case of an error


    # Define a Next button rectangle
    nextButtonRect = pygame.Rect(center_x - input_box_width // 0.405, center_y + 420, 300, 50)
    nextButtonText = ""

    # Position the input boxes at the center
    inputQuestion1 = pygame.Rect(center_x - input_box_width // 0.405, center_y + 200, input_box_width, input_box_height)
    inputQuestion2 = pygame.Rect(center_x - input_box_width // 0.405, center_y + 350, input_box_width, input_box_height)

    colorUsername = colorPassword = pygame.Color('#FFD6D5')
    font = pygame.font.Font(None, 32)
    textQuestion1 = ''
    textQuestion2 = ''

    activeQuestion1 = False
    activeQuestion2 = False


    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if Q1 or Q2 input boxes were clicked
                if inputQuestion1.collidepoint(event.pos):
                    activeQuestion1 = not activeQuestion1
                else:
                    activeQuestion1 = False
                if inputQuestion2.collidepoint(event.pos):
                    activeQuestion2 = not activeQuestion2
                else:
                    activeQuestion2 = False

                # Check if the Next button was clicked
                if nextButtonRect.collidepoint(event.pos):
                    try:
                        if loginConfig.questionsLogin(textQuestion1, textQuestion2, user) == False:
                            # Passwords do not match, display a pop-up error message
                            error_message = translate_text("Respuestas Incorrectas", target_language)
                            tkMessageBox.showerror("Error", error_message)
                        else:
                            tkMessageBox.showerror(":D", "Acá va lo de Felipe")
                    except():
                        tkMessageBox.showerror(":D", "error no reconocido, vuelva a intentarlo")

            if event.type == pygame.KEYDOWN:
                if activeQuestion1:
                    if event.key == pygame.K_RETURN:
                        username = textQuestion1
                        textQuestion1 = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textQuestion1 = textQuestion1[:-1]
                    else:
                        textQuestion1 += event.unicode
                if activeQuestion2:
                    if event.key == pygame.K_RETURN:
                        password = textQuestion2
                        textQuestion2 = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textQuestion2 = textQuestion2[:-1]
                    else:
                        textQuestion2 += event.unicode


        # Clear the screen
        window.fill((0, 0, 0))

        # Blit the scaled image onto the screen
        window.blit(scaled_image, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))


        # Draw the Next button
        # pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)
        # drawText(nextButtonText, nextButtonRect.x + 10, nextButtonRect.y + 5)

        # Draw the border around the input boxes
        pygame.draw.rect(window, '#FFD6D5', inputQuestion1, 2)
        pygame.draw.rect(window, '#FFD6D5', inputQuestion2, 2)
        pygame.display.flip()
        clock.tick(30)

        # pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)
        # drawText(nextButtonText, nextButtonRect.x + 10, nextButtonRect.y + 5)

        for i, question in enumerate(random_questions):
            label = font.render(question, True, (255, 255, 255))
            label_rect = label.get_rect(center=(screen_width // 5.2, (i + 5.6) * 125))
            window.blit(label, label_rect)


        # Render the text input fields
        txtSurfaceQuestion1 = font.render(textQuestion1, True, colorUsername)
        txtSurfaceQuestion2 = font.render(textQuestion2, True, colorUsername)

        window.blit(txtSurfaceQuestion1, (inputQuestion1.x + 5, inputQuestion1.y + 5))
        window.blit(txtSurfaceQuestion2, (inputQuestion2.x + 5, inputQuestion2.y + 5))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()
# startQuestionLogin("carlos", "en")