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

mouseUp = False
characterSpeed = [0, 0]
# Variables for random XY coordinates of the coin
coinRanInit = True
coinRanXList = []
coinRanYList = []
coinNum = 10
coinSpeed = 5
coinTouch = False
coinPlayer = 0
# Variables for life
lifePlayer = 5
img = []
restart = False
level = 1
keySpeed = 5
time = 0


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


def variableReset():
    global mouseUp, coinRanInit, coinRanXList, coinRanYList, coinNum, coinSpeed, coinTouch, coinPlayer, lifePlayer, img, restart, level, keySpeed, time, characterSpeed

    mouseUp = False

    # Character movement variables
    characterSpeed = [0, 0]  # X and Y Speeds

    # Variables for random XY coordinates of the coin
    coinRanInit = True
    coinRanXList = []
    coinRanYList = []
    coinNum = 10
    coinSpeed = 5
    coinTouch = False
    coinPlayer = 0

    # Variables for life
    lifePlayer = 5

    img = []
    restart = False
    level = 1
    keySpeed = 5
    time = 0


def itemInit(file, division):
    itemInits = pygame.image.load(f'resources/{file}').convert_alpha()
    itemInits = pygame.transform.smoothscale(itemInits, (itemInits.get_width() / division, itemInits.get_height() / division))
    return itemInits


def main():
    # -----------------------------Setup------------------------------------------------- #
    global mouseUp, coinRanInit, coinRanXList, coinRanYList, coinNum, coinSpeed, coinTouch, coinPlayer, lifePlayer, img, restart, level, keySpeed, time, characterSpeed

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
    titleImg = pygame.image.load('resources/title.png')

    # Start Button
    startBttn = createText("START", s=30, c=(255, 255, 255))
    startBttnC = (65, 104, 158)

    # Background
    bkgImg = pygame.image.load('resources/background.png').convert_alpha()
    bkgImg = pygame.transform.smoothscale(bkgImg, (surfaceSize, surfaceSize))

    # Home Button
    homeBttn = createText("HOME", s=30, c=(255, 255, 255))
    homeBttnC = (65, 104, 158)

    # Character movement variables
    characterPos = [surfaceSize / 2, 600]  # X and Y Positions

    # Item Graphics
    coinImg = itemInit("coin.png", 3.85)
    characterImg = itemInit("character.png", 2)
    lifeImg = itemInit("heart.png", 50)
    bombImg = itemInit("bomb.png", 7)
    cashImg = itemInit("cash.png", 7)
    taxImg = itemInit("tax.png", 12)
    exclaImg = itemInit("exclamation.png", 12)

    bombEImg = pygame.image.load('resources/bombExplosion.png').convert_alpha()
    bombEImg = pygame.transform.smoothscale(bombEImg, (bombImg.get_width(), bombImg.get_height()))

    coinImgS = pygame.transform.smoothscale(coinImg, (coinImg.get_width() / 1.3, coinImg.get_height() / 1.3))

    variableReset()
    for i in range(coinNum):
        img.append(coinImg)

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
                    characterSpeed[0] -= keySpeed
                elif ev.key == pygame.K_RIGHT:
                    characterSpeed[0] += keySpeed

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

            if restart:
                variableReset()

                for i in range(coinNum):
                    img.append(coinImg)

                characterPos = [surfaceSize / 2, 600]  # X and Y Positions

            displayImg(mainSurface, bkgImg, 0, 0)

            if coinRanInit:
                while len(coinRanXList) < coinNum:
                    newX = random.randint(0, surfaceSize - coinImg.get_width())

                    closeX = False
                    for i in range(len(coinRanXList)):

                        if coinRanXList[i] - 50 < newX < coinRanXList[i] + 50:
                            closeX = True

                    if not closeX:
                        coinRanXList.append(newX)

                while len(coinRanYList) < coinNum:
                    newY = random.randint(-800, 0 - coinImg.get_height())
                    coinRanYList.append(newY)

                coinRanInit = False

            # level up by time
            time += 1
            if time > 1000:
                time = 0
                coinSpeed += 2
                keySpeed += 2

            '''
            time += pygame.time.get_ticks()
            print(time)

            if time > 10000:
                time = 0
                print("workd")
                coinSpeed += 30
                keySpeed += 2
                #characterSpeed[0] += 100
            else:
                time = 0
            '''

            for i in range(coinNum):
                characterRect = characterImg.get_rect(topleft=(characterPos[0], characterPos[1]))
                coinRect = coinImg.get_rect(topleft=(coinRanXList[i], coinRanYList[i]))

                if characterRect.colliderect(coinRect):
                    coinTouch = True
                    if img[i] == coinImg:
                        coinPlayer += 1

                    elif img[i] == cashImg:
                        coinPlayer += 5

                    elif img[i] == bombImg:
                        displayImg(mainSurface, bombEImg, coinRanXList[i], coinRanYList[i])
                        lifePlayer -= 1

                    elif img[i] == taxImg:
                        displayImg(mainSurface, exclaImg, coinRanXList[i], coinRanYList[i])
                        coinPlayer = int(coinPlayer*0.9)
                        lifePlayer -= 1

                        if coinPlayer < 0:
                            programState = "end"

                if coinRanYList[i] >= 610 or coinTouch:

                    coinTouch = False

                    coinRanYList[i] = random.randint(-500, 0 - coinImg.get_height())
                    coinRanXList.pop(i)

                    item = random.randint(0, 100)

                    if item % 5 == 0:
                        img[i] = bombImg
                    elif item % 13 == 0:
                        img[i] = cashImg
                    elif item % 19 == 0:
                        img[i] = taxImg
                    else:
                        img[i] = coinImg

                    while len(coinRanXList) != coinNum:
                        newX = random.randint(0, surfaceSize - coinImg.get_width())

                        closeX = False
                        for j in range(len(coinRanXList)):

                            if coinRanXList[j] - 1.5*coinImg.get_width() < newX < \
                                    coinRanXList[j] + 1.5*coinImg.get_width():
                                closeX = True

                        if not closeX:
                            coinRanXList.insert(i, newX)
                            break

                else:
                    coinRanYList[i] += coinSpeed

                # Displays the falling coins
                displayImg(mainSurface, img[i], coinRanXList[i], coinRanYList[i])

            for i in range(lifePlayer):
                lifeImgX = surfaceSize - (i+1)*(lifeImg.get_width())
                displayImg(mainSurface, lifeImg, lifeImgX, 10)

            # If character moves out of the surface, bounce it back
            if characterPos[0] <= 0:
                characterPos[0] = 1
            elif characterPos[0] >= surfaceSize - characterImg.get_width():
                characterPos[0] = surfaceSize - characterImg.get_width() - 1

            # Displays the character image
            characterPos[0] += characterSpeed[0]
            displayImg(mainSurface, characterImg, characterPos[0], characterPos[1])

            # Displays the number of coins with the coin image (top left corner)
            displayImg(mainSurface, coinImgS, 10, 10)
            coinText = createText(f'x {coinPlayer}', s=25, c=(255, 255, 255), b=True)
            mainSurface.blit(coinText, (15 + coinImgS.get_width(), 10))

            if lifePlayer == 0:
                restart = True
                programState = 'end'

        if programState == "end":
            createBttn(mainSurface, homeBttn, horizontalC(homeBttn, mainSurface), surfaceSize - surfaceSize / 3,
                       homeBttnC)
            homeBttnHov = bttnDimension(mouse, homeBttn, horizontalC(homeBttn, mainSurface),
                                         surfaceSize - surfaceSize / 3)
            if homeBttnHov:
                homeBttnC = (184, 199, 219)
                if mouseUp:
                    programState = "main"
                    mouseUp = False
            else:
                homeBttnC = (101, 128, 166)


        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
