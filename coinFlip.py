import os
import random
import pygame
import localMultiplayer

# input       : The 2 users that are going to play and the lenguage
# output      : The coin flip Window
# descritpion : A window used to see who´s going to attack first

def startCoinFlip(user1, user2, lenguage):
    print(f'Primer Jugador : {user1}')
    print(f'Segundo Jugador : {user2}')
    print(f'Lenguaje : {lenguage}')
    winnerText = []
    if lenguage == "en":
        winnerText = [user1 +" Attacks", user2+" Attacks", "Continue"]

    if lenguage == "es":
        winnerText = [user1 +" Ataca", user2 +" Ataca", "Continuar"]


    # Inicializar Pygame
    pygame.init()

    # Definir colores
    WHITE = (255, 255, 255)

    # Inicializar la pantalla
    screenInfo = pygame.display.Info()
    screenWidth = screenInfo.current_w
    screenHeigth = screenInfo.current_h
    screen = pygame.display.set_mode((screenWidth, screenHeigth))
    pygame.display.set_caption("Pantalla con Botones")

    # Calculate the center of the screen
    centerX = screenWidth // 2
    centerY = screenHeigth // 2


    # Definir botones y su estado
    button1_visible = True
    button2_visible = True
    button3_visible = False
    button4_visible = False

    font = pygame.font.Font(None, 36)

    # Directory containing the animation images
    framesPath = os.getcwd() + "\\visuals\\frames"
    print(framesPath)
    faceFolder  = framesPath+'\gif_face'
    clawFolder = framesPath + '\gif_claw'
    gacha = [faceFolder, clawFolder]
    randomNumber = random.randint(0, 1) #0 is face  ---- #1 is claw
    n = -1
    print(randomNumber)

    # Load images from the directory into a list

    faceIMG = pygame.image.load(faceFolder+'\\frame_82_delay-0.18s.gif')
    clawIMG = pygame.image.load(clawFolder+'\\frame_85_delay-0.09s.gif')


    images = [pygame.image.load(os.path.join(gacha[randomNumber], img)) for img in os.listdir(gacha[randomNumber])]

    # Set the animation speed
    animation_speed = 15  # in milliseconds
    index = 0
    animation_triggered = False
    clock = pygame.time.Clock()


    # Bucle principal del juego
    running = True
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button1_visible and button2_visible:
                    if button1_rect.collidepoint(mouse_pos):
                        n = 0
                        button1_visible = False
                        button2_visible = False
                        animation_triggered = True

                    if button2_rect.collidepoint(mouse_pos):
                        n = 1
                        button1_visible = False
                        button2_visible = False
                        animation_triggered = True


                elif button3_visible:
                    if button3_rect.collidepoint(mouse_pos) or button4_rect.collidepoint(mouse_pos):
                        if n == randomNumber:
                            print("Jugador 1 ataca") #se llama a la función con jugador 1 atacando
                            localMultiplayer.setVariables(user1, user2, lenguage)
                            running = False
                        else:
                            print("Jugador 2 ataca") #se llama a la función con jugador 2 atacando
                            localMultiplayer.setVariables(user2, user1, lenguage)
                            running = False

        screen.fill((0, 0, 0))
        if animation_triggered:

            originalWidth, originalHeigth = images[index].get_size()
            # Calculate the scaling factors to fit the image to the screen
            scaleFactorWidth = screenWidth / originalWidth
            scaleFactorHeigth = screenHeigth / originalHeigth
            minScaleFactor = min(scaleFactorWidth, scaleFactorHeigth)
            newWidth = int(originalWidth * minScaleFactor)
            newHeigth = int(originalHeigth * minScaleFactor)
            scaledImage = pygame.transform.scale(images[index], (newWidth, newHeigth))

            images[index] = pygame.transform.scale(images[index], (250, 500))
            screen.blit(images[index], (centerX - centerX/7.2, centerY/2))
            index += 1

        if index >= len(images):
            button3_visible = True
            button4_visible = True
            index = index-1

        pygame.time.delay(animation_speed)
        clock.tick(60)

        button_width = 100
        button_height = 50
        button_padding = 200
        start_x = (screenWidth - 2 * button_width - button_padding) // 2
        button_y = 250



        if button1_visible:
            button1_rect = pygame.draw.rect(screen, (0, 0, 0), (start_x, button_y, button_width, button_height))
            faceIMG = pygame.transform.scale(faceIMG, (250, 500))
            screen.blit(faceIMG, (start_x - start_x/9.5, button_y-button_y/1.3))


        if button2_visible:
            button2_rect = pygame.draw.rect(screen, (0, 0, 0), (start_x + button_width + button_padding, button_y, button_width, button_height))
            clawIMG = pygame.transform.scale(clawIMG, (270, 540))
            screen.blit(clawIMG, (start_x + start_x/3.5, button_y-button_y/1.18))


        if button3_visible:
            if n == randomNumber:
                button3_rect = pygame.draw.rect(screen, (0, 0, 0),
                                                        (start_x, button_y, 2 * button_width + button_padding, button_height))
                text = font.render(winnerText[0], True, WHITE)
                text_rect = text.get_rect(center=button3_rect.center)
                screen.blit(text, text_rect)
            else:
                button3_rect = pygame.draw.rect(screen, (0, 0, 0),
                                                         (start_x, button_y, 2 * button_width + button_padding, button_height))
                text = font.render(winnerText[1], True, WHITE)
                text_rect = text.get_rect(center=button3_rect.center)
                screen.blit(text, text_rect)
        if button4_visible:
            button4_rect = pygame.draw.rect(screen, (169, 7, 7),
                                                    (start_x, button_y * 3.3, 2 * button_width + button_padding, button_height))

            text = font.render(winnerText[2], True, WHITE)
            text_rect = text.get_rect(center=button4_rect.center)
            screen.blit(text, text_rect)

        pygame.display.flip()
    pygame.quit()

# startCoinFlip("Dylan", "Carlos", "en") # Usage example.