import pygame
import sys
import tkinter.messagebox as tkMessageBox
from googletrans import Translator
import loginConfig
from questionLogin import startQuestionLogin
from customSettings import startCustomSettings


def startBaseLogin(language):
    # Initialize pygame
    pygame.init()

    # Load your image
    if language == "es":
        image = pygame.image.load('visuals/imágenesEspañol/3.png')

    if language == "en":
        image = pygame.image.load('visuals/imágenesInglés/13.png')


    # Constants
    width, height = 800, 600
    white = (255, 255, 255)
    font = pygame.font.Font(None, 36)
    target_language = language

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

    questionCounter = 0

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
    nextButtonRect = pygame.Rect(center_x - input_box_width // 0.405, center_y + 343, 300, 50)
    nextButtonText = ""

    # Position the input boxes at the center
    inputBoxUsername = pygame.Rect(center_x - input_box_width // 0.405, center_y + 120, input_box_width, input_box_height)
    inputBoxPassword = pygame.Rect(center_x - input_box_width // 0.405, center_y + 270, input_box_width, input_box_height)

    colorUsername = colorPassword = pygame.Color('#FFD6D5')
    font = pygame.font.Font(None, 32)
    textUsername = ''
    textPassword = ''
    textConfirmPassword = ''
    activeUsername = False
    activePassword = False


    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Check if username or password input boxes were clicked
                if inputBoxUsername.collidepoint(event.pos):
                    activeUsername = not activeUsername
                else:
                    activeUsername = False
                if inputBoxPassword.collidepoint(event.pos):
                    activePassword = not activePassword
                else:
                    activePassword = False

                # Check if the Next button was clicked
                if nextButtonRect.collidepoint(event.pos):
                    try:
                        if questionCounter > 2:
                            startQuestionLogin(activeUsername, language)

                        elif loginConfig.baseLogin(textUsername, textPassword) == False:
                            # Passwords do not match, display a pop-up error message
                            questionCounter += 1
                            error_message = translate_text("Contraseña Incorrecta", target_language)
                            tkMessageBox.showerror("Error", error_message)
                        else:
                            startCustomSettings(activeUsername, language)
                    except(FileNotFoundError):
                        tkMessageBox.showerror(":D", "usuario no encontrado")
                    except():
                        tkMessageBox.showerror(":D", "error no reconocido, vuelva a intentarlo")

            if event.type == pygame.KEYDOWN:
                if activeUsername:
                    if event.key == pygame.K_RETURN:
                        username = textUsername
                        textUsername = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textUsername = textUsername[:-1]
                    else:
                        textUsername += event.unicode
                if activePassword:
                    if event.key == pygame.K_RETURN:
                        password = textPassword
                        textPassword = ''
                    elif event.key == pygame.K_BACKSPACE:
                        textPassword = textPassword[:-1]
                    else:
                        textPassword += event.unicode


        # Clear the screen
        window.fill((0, 0, 0))

        # Blit the scaled image onto the screen
        window.blit(scaled_image, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))


        # Draw the Next button
        # pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)
        # drawText(nextButtonText, nextButtonRect.x + 10, nextButtonRect.y + 5)

        # Draw the border around the input boxes
        pygame.draw.rect(window, '#FFD6D5', inputBoxUsername, 2)
        pygame.draw.rect(window, '#FFD6D5', inputBoxPassword, 2)
        pygame.display.flip()
        clock.tick(30)

        # Render the text input fields
        txtSurfaceUsername = font.render(textUsername, True, colorUsername)
        txtSurfacePassword = font.render("*" * len(textPassword), True, colorPassword)
        txtSurfaceConfirmPassword = font.render("*" * len(textConfirmPassword), True, colorPassword)

        window.blit(txtSurfaceUsername, (inputBoxUsername.x + 5, inputBoxUsername.y + 5))
        window.blit(txtSurfacePassword, (inputBoxPassword.x + 5, inputBoxPassword.y + 5))

        pygame.display.flip()
        clock.tick(30)

    # Quit pygame
    pygame.quit()
    sys.exit()

#startBaseLogin("en")