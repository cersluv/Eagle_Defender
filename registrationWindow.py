import pygame
import tkinter as tk
from tkinter import filedialog
import tkinter.messagebox as tkMessageBox
import os
from googletrans import Translator
import re
import subprocess

# Initialize pygame
pygame.init()
pygame.display.set_caption("Eagle Defender - Registration")

# Constants
width, height = 800, 600
white = (255, 255, 255)
font = pygame.font.Font(None, 36)
target_language = 'es'

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

# Load your image
image = pygame.image.load('visuals/imágenesEspañol/6.png')

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

# Image upload
uploadedImage = ""
imagePreviewRect = pygame.Rect(center_x + 1175 // 2, center_y, 1000, 500)
uploadButtonRect = pygame.Rect(center_x - 500 // 2, center_y + 280, input_box_width + 200, input_box_height)
uploadButtonText = ""
maxImageSizeBytes = 300 * 1024 * 1024  # 300MB limit

# Define a Next button rectangle
nextButtonRect = pygame.Rect(center_x - 150, center_y + 440, 300, 50)
nextButtonText = "Next"

# Position the input boxes at the center
inputBoxUsername = pygame.Rect(center_x - input_box_width // 2, center_y - 115, input_box_width, input_box_height)
inputBoxPassword = pygame.Rect(center_x - input_box_width // 2, center_y + 50, input_box_width, input_box_height)
inputConfirmPassword = pygame.Rect(center_x - input_box_width // 2, center_y + 200, input_box_width, input_box_height)

colorActive = pygame.Color('#BD2927')
colorUsername = colorPassword = colorInactive = pygame.Color('#FFD6D5')
boxUsernameColor = pygame.Color('#FFD6D5')
boxPasswordColor = pygame.Color('#FFD6D5')
boxConfirmPasswordColor = pygame.Color('#FFD6D5')
textUsername = ''
textPassword = ''
textConfirmPassword = ''
fileExtension = ''
activeUsername = False
activePassword = False
activeConfirmPassword = False

"""
input: text (str), x coord (int), y coord (int)
summary: Renders and displays text on the screen
outputs: None
"""


def drawText(text, x, y):
    renderedText = font.render(text, True, (0, 0, 0))
    window.blit(renderedText, (x, y))


"""
input: None
summary: Draws the image upload button on the screen
outputs: None
"""


def drawUploadButton():
    pygame.draw.rect(window, (0, 128, 255), uploadButtonRect, 0)
    drawText(uploadButtonText, uploadButtonRect.x + 10, uploadButtonRect.y + 5)


"""
input: None
summary: Updates and displays the uploaded image preview on the screen
outputs: None
"""


def updateImagePreview():
    if uploadedImage:
        window.blit(uploadedImage, imagePreviewRect)


"""
input: text
summary: Checks if the given text completes all regulations
outputs: Bool
"""


def usernameVerification(text):
    # Check if the text has a length of 5
    if len(text) < 5:
        return "Nombre de usuario tiene que ser de al menos 5 caracteres de largo"

    # Initialize variables to track if there are letters and numbers
    has_letters = False
    has_numbers = False

    # Iterate through each character in the text
    for char in text:
        if char.isalpha():
            has_letters = True
        elif char.isdigit():
            has_numbers = True

        # If both letters and numbers are found, return True
        if has_letters and has_numbers:
            return ""

    # If the loop completes without finding both letters and numbers, return False
    return "Nombre de usuario tiene que contener al menos 1 letra y 1 número"


"""
input: text
summary: Checks if the given text completes all regulations
outputs: Bool
"""


def passwordVerification(password):
    # Check if the length is 8 characters
    if len(password) < 8:
        return "Contraseña tiene que ser de al menos 8 caracteres de largo"

    # Check if it contains at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return "Contraseña tiene contener al menos 1 letra mayúscula"

    # Check if it contains at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return "Contraseña tiene contener al menos 1 letra minúscula"

    # Check if the sentence contains at least one special character (non-alphanumeric)
    if not re.search(r'[^a-zA-Z0-9]', password):
        return "Contraseña tiene contener al menos 1 número y 1 letra especial: [!¡@#$%^&*?¿]"

    # Check if "textUsername" is not in the password
    if textUsername in password:
        return "Contraseña NO puede contener el nombre de usuario"

    if textPassword != textConfirmPassword:
        return "Passwords do not match. Please re-enter."

    # If all conditions are met, the password is valid
    return ""


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


"""
input: None
summary: saves Information for future logins
outputs: None
"""


def saveInformation():
    mainDir = f"Data/{textUsername}/"
    os.makedirs(os.path.dirname(f"{mainDir}Images/"), exist_ok=True)
    file_path = "Data/" + textUsername + "/information.txt"
    with open(file_path, "w") as file:
        file.write(textPassword + "\n")
    with open("Data/tempUser.txt", "w") as tempFile:
        tempFile.write(f"{textUsername}")

    pygame.image.save(uploadedImage, f"{mainDir}Images/icon{file_extension}")


clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if username were clicked
            if inputBoxUsername.collidepoint(event.pos):
                activeUsername = not activeUsername
                boxUsernameColor = colorActive
            else:
                activeUsername = False
                boxUsernameColor = colorInactive
            # Check if passwod were clicked
            if inputBoxPassword.collidepoint(event.pos):
                activePassword = not activePassword
                boxPasswordColor = colorActive
            else:
                activePassword = False
                boxPasswordColor = colorInactive
            # Check if confirmPassword were clicked
            if inputConfirmPassword.collidepoint(event.pos):
                activeConfirmPassword = not activeConfirmPassword
                boxConfirmPasswordColor = colorActive
            else:
                activeConfirmPassword = False
                boxConfirmPasswordColor = colorInactive
            # Check if the upload button was clicked
            if uploadButtonRect.collidepoint(event.pos):
                root = tk.Tk()
                root.withdraw()  # Hide the main tkinter window
                fileDialog = filedialog.askopenfilename(
                    filetypes=[
                        ("Image files", "*.png *.jpg *.jpeg *.gif *.bmp"),
                        ("All files", "*.*")
                    ]
                )
                root.destroy()  # Destroy the tkinter window
                if fileDialog:
                    file_extension = os.path.splitext(fileDialog)[1]
                    # Check the size of the selected image
                    if os.path.getsize(fileDialog) <= maxImageSizeBytes:
                        # Load the image and display it in the preview area
                        uploadedImage = pygame.image.load(fileDialog)
                        uploadedImage = pygame.transform.scale(uploadedImage, (300, 300))
                    else:
                        error_message = translate_text("Image size exceeds the limit (300MB). Please select a smaller "
                                                       "image.", target_language)
                        tkMessageBox.showerror("Error", error_message)
            # Check if the Next button was clicked
            if nextButtonRect.collidepoint(event.pos):
                if passwordVerification(textPassword) != "":
                    # Passwords do not match, display a pop-up error message
                    error_message = translate_text(passwordVerification(textPassword), target_language)
                    tkMessageBox.showerror("Error", error_message)
                elif usernameVerification(textUsername) != "":
                    error_message = translate_text(usernameVerification(textUsername), target_language)
                    tkMessageBox.showerror("Error", error_message)
                elif uploadedImage == "":
                    error_message = translate_text("Es necesario cargar una imagen para continuar", target_language)
                    tkMessageBox.showerror("Error", error_message)
                else:
                    saveInformation()
                    running = False

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
            if activeConfirmPassword:
                if event.key == pygame.K_RETURN:
                    password = textConfirmPassword
                    textConfirmPassword = ''
                elif event.key == pygame.K_BACKSPACE:
                    textConfirmPassword = textConfirmPassword[:-1]
                else:
                    textConfirmPassword += event.unicode

    # Clear the screen
    window.fill((0, 0, 0))

    # Blit the scaled image onto the screen
    window.blit(scaled_image, ((screen_width - new_width) // 2, (screen_height - new_height) // 2))

    # Draw image upload button
    drawUploadButton()

    # Draw the Next button
    pygame.draw.rect(window, (0, 128, 255), nextButtonRect, 0)
    drawText(nextButtonText, nextButtonRect.x + 10, nextButtonRect.y + 5)

    # Update and display the image preview
    updateImagePreview()

    # Draw the border around the input boxes
    pygame.draw.rect(window, boxUsernameColor, inputBoxUsername, 2)
    pygame.draw.rect(window, boxPasswordColor, inputBoxPassword, 2)
    pygame.draw.rect(window, boxConfirmPasswordColor, inputConfirmPassword, 2)

    # Render the text input fields
    txtSurfaceUsername = font.render(textUsername, True, colorUsername)
    txtSurfacePassword = font.render("*" * len(textPassword), True, colorPassword)
    txtSurfaceConfirmPassword = font.render("*" * len(textConfirmPassword), True, colorPassword)

    window.blit(txtSurfaceUsername, (inputBoxUsername.x + 5, inputBoxUsername.y + 5))
    window.blit(txtSurfacePassword, (inputBoxPassword.x + 5, inputBoxPassword.y + 5))
    window.blit(txtSurfaceConfirmPassword, (inputConfirmPassword.x + 5, inputConfirmPassword.y + 5))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()

subprocess.run(["python", "MusicHandler.py"])
