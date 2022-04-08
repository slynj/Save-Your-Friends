# -----------------------------------------------------------------------------
# Name:        Assignment Template (assignment.py)
# Purpose:     A description of your program goes here.
#
# Author:      Lyn Jeong
# Created:     13-Sept-2020
# Updated:     13-Sept-2020
# ---------------------------------------------------------------------------------------#
# I think this project deserves a level XXXXXX because ...
#
# Features Added:
#   ...
#   ...
#   ...
# ---------------------------------------------------------------------------------------#
# coin https://stock.adobe.com/search?k=8+bit+coin&asset_id=392227316
# character https://openclipart.org/detail/248259/retro-character-sprite-sheet
import pygame
import random


# Receives a string and other characters of a text and returns a rendered text
def createText(t, f="Arial", s=200, c=(255, 255, 0), b=False, i=False):
    font = pygame.font.SysFont(f, s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text


# Receives a text of the button with XY coordinates and draws a rectangle button with that text
def createBttn(mainSurface, text, textX, textY, c=(0, 0, 0)):
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    pygame.draw.rect(mainSurface, c, dimension, border_radius=10)
    mainSurface.blit(text, (textX, textY))


# Collision detection for the button, returns TRUE or FALSE
def bttnDimension(mouse, text, textX, textY):
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    bttn = pygame.Rect(dimension)
    if bttn.collidepoint(mouse[0], mouse[1]):
        return True
    else:
        return False


# Draws the image on the given coordinates
def displayImg(mainSurface, img, x, y):
    mainSurface.blit(img, (x, y))


# Calculates what coordinate of the item's horizontal centre is
def horizontalC(item, mainSurface):
    return int((mainSurface.get_width() - item.get_width()) // 2)


def main():
    # -----------------------------Setup------------------------------------------------- #
    global mouseUp # MouseUp boolean to use in and out of the while loop

    pygame.init()  # Prepare the pygame module for use
    pygame.font.init()
    surfaceSize = 800  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    pygame.display.set_caption("Save Your Friends")

    # -----------------------------Program Variable Initialization----------------------- #
    # Set up some data to describe a small circle and its color
    # Game Setup
    programState = "game"

    # Title
    titleImg = pygame.image.load('title.png')

    # Start Button
    startBttn = createText("START", s=30, c=(255, 255, 255))
    startBttnC = (65, 104, 158)

    # Background
    bkgImg = pygame.image.load('background.png').convert_alpha()
    bkgImg = pygame.transform.smoothscale(bkgImg, (surfaceSize, surfaceSize))

    # Characters Graphics
    coinImg = pygame.image.load('coin.png').convert_alpha()
    coinImg = pygame.transform.smoothscale(coinImg, (40, 40))

    characterImg = pygame.image.load('character.png').convert_alpha()
    characterPos = [surfaceSize / 2, 600]  # X and Y Positions
    characterSpeed = [0, 0]  # X and Y Speeds
    characterImg = pygame.transform.smoothscale(characterImg,
                                                (characterImg.get_width() / 2, characterImg.get_height() / 2))

    # Mouse click detection
    mouseUp = False

    # Variables for random XY coordinates of the coin
    coinRanInit = True
    coinRanXList = []
    coinRanYList = []
    coinNum = 10
    coinSpeed = 5
    coinTouch = False

    # -----------------------------Main Game Loop----------------------------------------#
    while True:

        # -----------------------------Event Handling------------------------------------#
        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        elif ev.type == pygame.MOUSEBUTTONUP:
            mouseUp = True

        elif ev.type == pygame.KEYDOWN:
            if programState == "game":
                if ev.key == pygame.K_LEFT:
                    characterSpeed[0] -= 5
                elif ev.key == pygame.K_RIGHT:
                    characterSpeed[0] += 5

        elif ev.type == pygame.KEYUP:
            if programState == "game":
                characterSpeed[0] = 0

        mouse = pygame.mouse.get_pos()

        # -----------------------------Game Logic----------------------------------------#
        # Update your game objects and data structures here...

        # -----------------------------Drawing Everything--------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((118, 150, 194))

        if programState == "main":
            # mainSurface.blit(mainTitle, (horizontalC(mainTitle, mainSurface), surfaceSize / 2))
            displayImg(mainSurface, titleImg, horizontalC(titleImg, mainSurface), surfaceSize / 2.5)
            # mainSurface, text, textX, textY, c = (0, 0, 0)
            createBttn(mainSurface, startBttn, horizontalC(startBttn, mainSurface), surfaceSize - surfaceSize / 3,
                       startBttnC)
            # bttnDimension(mouse, text, textX, textY)
            startBttnHov = bttnDimension(mouse, startBttn, horizontalC(startBttn, mainSurface),
                                         surfaceSize - surfaceSize / 3)
            if startBttnHov:
                startBttnC = (184, 199, 219)
                if mouseUp:
                    programState = "game"
            else:
                startBttnC = (101, 128, 166)

        elif programState == "game":
            displayImg(mainSurface, bkgImg, 0, 0)

            if coinRanInit:
                while len(coinRanXList) < coinNum:
                    newX = random.randint(0, surfaceSize - coinImg.get_width())

                    closeX = False
                    for i in range(len(coinRanXList)):

                        if coinRanXList[i] - 60 < newX and newX < coinRanXList[i] + 60:
                            closeX = True

                    if not closeX:
                        coinRanXList.append(newX)

                while len(coinRanYList) < coinNum:
                    newY = random.randint(-800, 0 - coinImg.get_height())
                    coinRanYList.append(newY)

                coinRanInit = False

            for i in range(coinNum):
                characterRect = characterImg.get_rect(topleft=(characterPos[0], characterPos[1]))
                coinRect = coinImg.get_rect(topleft=(coinRanXList[i], coinRanYList[i]))

                if characterRect.colliderect(coinRect):
                    coinTouch = True

                if coinRanYList[i] >= 610 or coinTouch:
                    coinTouch = False

                    coinRanYList[i] = random.randint(-500, 0 - coinImg.get_height())
                    coinRanXList.pop(i)

                    # '''
                    while True:
                        newX = random.randint(0, surfaceSize - coinImg.get_width())

                        closeX = False
                        for j in range(len(coinRanXList)):

                            if coinRanXList[j] - 60 < newX and newX < coinRanXList[j] + 60:
                                closeX = True

                        if not closeX:
                            coinRanXList[i] = newX
                            print(coinRanXList)
                            break

                    # '''

                else:
                    coinRanYList[i] += coinSpeed

            for i in range(coinNum):
                displayImg(mainSurface, coinImg, coinRanXList[i], coinRanYList[i])

            characterPos[0] += characterSpeed[0]
            displayImg(mainSurface, characterImg, characterPos[0], characterPos[1])

            if characterPos[0] <= 0:
                characterPos[0] = 1
            elif characterPos[0] >= surfaceSize - characterImg.get_width():
                characterPos[0] = surfaceSize - characterImg.get_width() - 1

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
