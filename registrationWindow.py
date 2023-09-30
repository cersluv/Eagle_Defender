import pygame
import sys
import tkinter as tk
from tkinter import filedialog
import os

# Initialize pygame
pygame.init()

# Constants
width, height = 800, 600
white = (255, 255, 255)
font = pygame.font.Font(None, 36)

# Create the window
window = pygame.display.set_mode((width, height))
pygame.display.set_caption("Simple Pygame App")

# Input fields
username = ""
password = ""
songs = ["", "", ""]
songLabels = ["Song 1:", "Song 2:", "Song 3:"]
maxSongs = 3  # Maximum number of songs

# Image upload
uploadedImage = None
imagePreviewRect = pygame.Rect(400, 200, 300, 300)
uploadButtonRect = pygame.Rect(400, 150, 100, 30)
uploadButtonText = "Upload Image"
maxImageSizeBytes = 300 * 1024 * 1024  # 300MB limit

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


# Initialize input boxes and their states
inputBoxUsername = pygame.Rect(200, 50, 140, 32)
inputBoxPassword = pygame.Rect(200, 100, 140, 32)
colorInactive = pygame.Color('lightskyblue3')
colorActive = pygame.Color('dodgerblue2')
colorUsername = colorInactive
colorPassword = colorInactive
font = pygame.font.Font(None, 32)
textUsername = ''
textPassword = ''
activeUsername = False
activePassword = False

songInputBoxes = []
songTexts = []
activeSongs = [False] * maxSongs

for i in range(maxSongs):
    inputBoxSong = pygame.Rect(200, 150 + i * 50, 140, 32)
    songInputBoxes.append(inputBoxSong)
    songTexts.append('')
    activeSongs[i] = False

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if a song input box was clicked
            for i, box in enumerate(songInputBoxes):
                if box.collidepoint(event.pos):
                    activeSongs[i] = not activeSongs[i]
                else:
                    activeSongs[i] = False
            # Check if username or password input boxes were clicked
            if inputBoxUsername.collidepoint(event.pos):
                activeUsername = not activeUsername
            else:
                activeUsername = False
            if inputBoxPassword.collidepoint(event.pos):
                activePassword = not activePassword
            else:
                activePassword = False
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
                    # Check the size of the selected image
                    if os.path.getsize(fileDialog) <= maxImageSizeBytes:
                        # Load the image and display it in the preview area
                        uploadedImage = pygame.image.load(fileDialog)
                        uploadedImage = pygame.transform.scale(uploadedImage, (300, 300))
                    else:
                        print("Image size exceeds the limit (300MB). Please select a smaller image.")

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
            # Handle song input
            for i in range(maxSongs):
                if activeSongs[i]:
                    if event.key == pygame.K_RETURN:
                        songs[i] = songTexts[i]
                        songTexts[i] = ''
                        activeSongs[i] = False
                    elif event.key == pygame.K_BACKSPACE:
                        songTexts[i] = songTexts[i][:-1]
                    else:
                        songTexts[i] += event.unicode

    # Clear the screen
    window.fill(white)

    # Draw input fields
    drawText("Username:", 50, 50)
    drawText("Password:", 50, 100)
    drawText(username, 200, 50)
    drawText("*" * len(password), 200, 100)

    # Draw song input fields and labels
    for i in range(maxSongs):
        drawText(songLabels[i], 50, 150 + i * 50)
        drawText(songs[i], 200, 150 + i * 50)

    # Draw image upload button
    drawUploadButton()

    # Update and display the image preview
    updateImagePreview()

    # Render the text input fields
    txtSurfaceUsername = font.render(textUsername, True, colorUsername)
    txtSurfacePassword = font.render("*" * len(textPassword), True, colorPassword)
    window.blit(txtSurfaceUsername, (inputBoxUsername.x + 5, inputBoxUsername.y + 5))
    window.blit(txtSurfacePassword, (inputBoxPassword.x + 5, inputBoxPassword.y + 5))

    for i in range(maxSongs):
        txtSurfaceSong = font.render(songTexts[i], True, colorActive if activeSongs[i] else colorInactive)
        widthSong = max(200, txtSurfaceSong.get_width() + 10)
        songInputBoxes[i].w = widthSong
        window.blit(txtSurfaceSong, (songInputBoxes[i].x + 5, songInputBoxes[i].y + 5))
        pygame.draw.rect(window, colorActive if activeSongs[i] else colorInactive, songInputBoxes[i], 2)

    pygame.display.flip()
    clock.tick(30)

# Quit pygame
pygame.quit()
sys.exit()
