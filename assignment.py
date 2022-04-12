# ----------------------------------------------------------------------------- #
# Name:        mini-game-p4-slynj — Save Your Friends! (assignment.py)
# Purpose:     Save Your Friends! is a mini control game made using Pygame. The purpose of this
#              project is to demonstrate the understanding of collision detection in pygame along
#              with the knowledge of lists, functions and library usage. In this game, various types
#              of items falls down from the sky, and the player controls the character with arrow keys.
#              The goal is to get as many coins while maintaining the life.
# Author:      Lyn Jeong
# Created:     01-April-2022
# Updated:     10-April-2022
# --------------------------------------------------------------------------------------- #
# I think this project deserves a level 4+ because it demonstrates all of the level 4 criteria with
# many extra features improving the game.
#
# Features Added:
#   - image usage
#       -> image used for items/characters
#   - background music
#       -> toggle button to turn on/off
#       -> different music on for each screen (main/game/end)
#   - sound effect
#       -> different sound effects for each items
#   - time module used
#       -> calculates how long user played the game (minutes/seconds)
#       -> increases the items' falling speed every 5 second
#   - random module used
#       -> random items falling (coin/cash/bomb/tax)
#       -> random x coordinates
#       -> random y coordinates
#   - different items falling with collision detection
#       -> distinguishes the object touched, adding/subtracting certain values depending on the item
#   - program state used
#       -> program state used to distinguish start/game/end screen
#       -> replayable
#       -> can exit the game during game play (exit button)
#   - item collision indication
#       -> bomb/tax shows a different version of the graphic when touched to indicate that user have
#          collided to those items
#   - different ending screen depending on the score
#   - increasingly gets faster
#       -> item falling speed and character moving speed increases, making it harder to play
# --------------------------------------------------------------------------------------- #
# Image & Code Credits
# coin https://stock.adobe.com/search?k=8+bit+coin&asset_id=392227316
# character https://openclipart.org/detail/248259/retro-character-sprite-sheet
# character controlling logic — Mr. Brooks https://github.com/HDSB-GWS/ICS3-Python-Notes/bl
#                                           ob/master/notes/41%20-%20PyGame/07.%20events%20-%20speed.py
# --------------------------------------------------------------------------------------- #

# Import library / modules
import pygame
import random
import time
import math

# Variables initial setup (written outside of function to use it as a global variable)
mouseUp = False         # indicates if the mouse is clicked
characterSpeed = [0, 0] # speed of the character
keySpeed = 5            # the amount of speed increased by when arrow keys pressed

musicOn = True          # indicates if the music should be on or off
restart = False         # indicates if the variables should be resetted or not
lifePlayer = 5          # the number of player's life left
img = []                # stores the types of item (coin, cash, bomb, tax)

# Variables coins (items)
coinRanInit = True      # indicates if the coin's random XY should be initialized or not
coinRanXList = []       # stores the X coordinate of the coin
coinRanYList = []       # stores the Y coordinate of the coin
coinNum = 10            # number of coins presented on the screen
coinSpeed = 5           # speed of the coin that should be falling at
coinTouch = False       # indicates if the coin touched the character
coinPlayer = 0          # the number of coins earned by the character

# Variables for time
startTime = 0           # the time when the player starts playing
endTime = 0             # the time when the player dies
timeDiff = 0            # the differences of the two time check points
checkP1 = 0             # first time check point
checkP2 = 0             # second time check point


def createText(t, f="Arial", s=200, c=(255, 255, 0), b=False, i=False):
    '''
    Receives a string and other characters of a text and returns a rendered text

    Parameters
    ----------
    t: str
        the string of the text to be rendered
    f: str = "Arial"
        the string indicating the font style of the text
    s: int = 200,
        size of the text
    c: tuple[int, int, int] = (255, 255, 0)
        colour of the text
    b: bool = False
        indication if the text would be bold
    i: bool = False
        indication if the text would be italicized

    Returns
    -------
    pygame.Surface
        rendered text
    '''

    font = pygame.font.SysFont(f, s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text


def createBttn(mainSurface, text, textX, textY, c=(0, 0, 0)):
    '''
    Receives a text of the button with XY coordinates and draws a rectangle button with that text

    Parameters
    ----------
    mainSurface: pygame.Surface
        the surface to draw the elements
    text: pygame.Surface
        the rendered text of the button
    textX: float
        the X coordinate of the button
    textY: float
        the Y coordinate of the button
    c: tuple[int, int, int] = (0, 0, 0)
        colour of the button

    Returns
    -------
    None
    '''
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    pygame.draw.rect(mainSurface, c, dimension, border_radius=10)
    mainSurface.blit(text, (textX, textY))


def bttnDimension(mouse, text, textX, textY):
    '''
    Collision detection for the button, returns TRUE or FALSE

    Parameters
    ----------
    mouse: tuple
        XY coordinates of the mouse pointer
    text: pygame.Surface
        the rendered text of the button
    textX: float
        the X coordinate of the button
    textY: float
        the Y coordinate of the button

    Returns
    -------
    bool
        if the mouse is touching the button or not
    '''
    paddingW = text.get_width() * 0.3
    paddingH = text.get_height() * 0.1
    dimension = [textX - paddingW / 2, textY - paddingH / 2, text.get_width() + paddingW, text.get_height() + paddingH]
    bttn = pygame.Rect(dimension)
    if bttn.collidepoint(mouse[0], mouse[1]):
        return True
    else:
        return False


def displayImg(mainSurface, imgFile, x, y):
    '''
    Draws the image on the given coordinates

    Parameters
    ----------
    mainSurface: pygame.Surface
        the surface to draw the elements
    imgFile: pygame.Surface
        the loaded image to be drawn
    x: float
        x coordinate of the image to be drawn
    y: float
        y coordinate of the image to be drawn

    Returns
    -------
    None
    '''
    mainSurface.blit(imgFile, (x, y))


def horizontalC(item, mainSurface):
    '''
    Calculates what coordinate of the item's horizontal centre is

    Parameters
    ----------
    mainSurface: pygame.Surface
        the surface to draw the elements
    item: pygame.Surface
        element to be horizontally centered

    Returns
    -------
    int
        the x coordinate where the element would be centered
    '''
    return int((mainSurface.get_width() - item.get_width()) // 2)


def variableReset():
    '''
    Resets all the global variables before restarting the game

    Parameters
    ----------
    None

    Returns
    -------
    None
    '''
    global mouseUp, coinRanInit, coinRanXList, coinRanYList, coinNum, coinSpeed, coinTouch, coinPlayer, lifePlayer, \
        img, restart, keySpeed, characterSpeed, startTime, endTime, timeDiff, checkP1, checkP2, musicOn

    mouseUp = False
    characterSpeed = [0, 0]
    keySpeed = 5

    restart = False
    lifePlayer = 5
    img = []

    # Variables coins (items)
    coinRanInit = True
    coinRanXList = []
    coinRanYList = []
    coinNum = 10
    coinSpeed = 5
    coinTouch = False
    coinPlayer = 0

    # Variables for time
    startTime = 0
    endTime = 0
    timeDiff = 0
    checkP1 = 0
    checkP2 = 0


# Image files size initialization
def itemInit(file, division):
    '''
    Resets all the global variables before restarting the game

    Parameters
    ----------
    file: str
        the name of the file to load
    division: float
        the multiplier to reduce the image size by

    Returns
    -------
    pygame.Surface
        the resized version of the image
    '''
    itemInits = pygame.image.load(f'resources/{file}').convert_alpha()
    itemInits = pygame.transform.smoothscale(itemInits, (itemInits.get_width() / division, itemInits.get_height() / division))
    return itemInits


# Main Program
def main():
    # -----------------------------Setup------------------------------------------------- #
    global mouseUp, coinRanInit, coinRanXList, coinRanYList, coinNum, coinSpeed, coinTouch, coinPlayer, lifePlayer, \
        img, restart, keySpeed, characterSpeed, startTime, endTime, timeDiff, checkP1, checkP2, musicOn

    pygame.init()  # Prepare the pygame module for use
    pygame.font.init()
    surfaceSize = 800  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    pygame.display.set_caption("Save Your Friends!")

    # -----------------------------Program Variable Initialization----------------------- #
    # Set up some data to describe a small circle and its color
    # Game Setup
    programState = "main"

    # Theme Colour
    BLUE = (65, 104, 158)
    WHITE = (255, 255, 255)

    # Title
    titleImg = pygame.image.load('resources/title.png')

    # Start Button
    startBttn = createText("START", s=30, c=WHITE)
    startBttnC = BLUE

    # Background
    bkgImg = pygame.image.load('resources/background.png').convert_alpha()
    bkgImg = pygame.transform.smoothscale(bkgImg, (surfaceSize, surfaceSize))

    # Home Button
    homeBttn = createText("HOME", s=30, c=WHITE)
    homeBttnC = BLUE

    # Help Button
    helpBttn = createText(" ? ", s=30, c=WHITE)
    helpBttnC = BLUE

    # Replay Button
    replayBttn = createText("REPLAY", s=30, c=WHITE)
    replayBttnC = BLUE

    # Exit Button
    exitBttn = createText("EXIT", s=25, c=WHITE, i=True)
    exitBttnC = (112, 79, 55)

    # Music Button
    musicBttn = createText("SOUND", s=25, c=WHITE, i=True)
    musicBttnC = (112, 79, 55)

    # Character movement variables
    characterPos = [surfaceSize / 2, 600]  # X and Y Positions

    # Item Graphics size initializing
    coinImg = itemInit("coin.png", 3.85)
    characterImg = itemInit("character.png", 2)
    lifeImg = itemInit("heart.png", 50)
    bombImg = itemInit("bomb.png", 7)
    cashImg = itemInit("cash.png", 7)
    taxImg = itemInit("tax.png", 12)
    exclaImg = itemInit("exclamation.png", 12)
    islandImg = itemInit("island.png", 2)
    rulesImg = itemInit("rules.png", 1)
    noFriendsImg = itemInit("noFriends.png", 1)
    oneFriendImg = itemInit("oneFriend.png", 1)
    twoFriendsImg = itemInit("twoFriends.png", 1)
    tenFriendsImg = itemInit("tenFriends.png", 1)
    twentyFriendsImg = itemInit("twentyFriends.png", 1)

    bombEImg = pygame.image.load('resources/bombExplosion.png').convert_alpha()
    bombEImg = pygame.transform.smoothscale(bombEImg, (bombImg.get_width(), bombImg.get_height()))

    coinImgS = pygame.transform.smoothscale(coinImg, (coinImg.get_width() / 1.3, coinImg.get_height() / 1.3))

    # The first 10 items are always all coins
    variableReset()
    for i in range(coinNum):
        img.append(coinImg)

    # Creates a user even that indicates if the song is ended or not
    SONG_END = pygame.USEREVENT
    pygame.mixer.music.set_endevent(SONG_END)

    # Different Sound Effects
    coinSoundEffect = pygame.mixer.Sound('resources/coinSoundEffect.mp3')
    cashSoundEffect = pygame.mixer.Sound('resources/cashSoundEffect.mp3')
    bombSoundEffect = pygame.mixer.Sound('resources/bombSoundEffect.mp3')
    taxSoundEffect = pygame.mixer.Sound('resources/taxSoundEffect.mp3')

    stateChange = True

    # -----------------------------Main Game Loop---------------------------------------- #
    while True:
        # -----------------------------Event Handling------------------------------------ #
        ev = pygame.event.poll()
        # Window close button
        if ev.type == pygame.QUIT:
            break  # ... leave game loop

        # Mouse Click Bool
        if ev.type == pygame.MOUSEBUTTONUP:
            mouseUp = True
        else:
            mouseUp = False

        # Keyboard pressed
        if ev.type == pygame.KEYDOWN:
            if programState == "game":
                # From Mr. Brooks (credit at the top)
                if ev.key == pygame.K_LEFT:
                    characterSpeed[0] -= keySpeed
                elif ev.key == pygame.K_RIGHT:
                    characterSpeed[0] += keySpeed

        # Keyboard released
        if ev.type == pygame.KEYUP:
            if programState == "game":
                characterSpeed[0] = 0

        # Song is ended
        if (ev.type == SONG_END or stateChange) and musicOn:
            if stateChange:
                stateChange = False
                pygame.mixer.music.stop()
            # Different kind of music depending on the state
            if programState == "main":
                pygame.mixer.music.load('resources/mainMusic.mp3')
                pygame.mixer.music.play()
            elif programState == "game":
                pygame.mixer.music.load('resources/gameMusic.mp3')
                pygame.mixer.music.play()
            elif programState == "end":
                pygame.mixer.music.load('resources/endMusic.mp3')
                pygame.mixer.music.play()

        mouse = pygame.mouse.get_pos()

        # Constant colours for buttons
        BUTTNBLUE = (184, 199, 219)
        BUTTNHOVER = (101, 128, 166)
        WHITE = (255, 255, 255)

        # ----------------------------- Game Logic / Drawing --------------------------------#
        mainSurface.fill((118, 150, 194))

        # MAIN SCREEN
        if programState == "main":
            displayImg(mainSurface, titleImg, horizontalC(titleImg, mainSurface), surfaceSize / 2.5)
            displayImg(mainSurface, islandImg, horizontalC(islandImg, mainSurface)-10, surfaceSize/5)
            displayImg(mainSurface, characterImg, horizontalC(characterImg, mainSurface)+50, surfaceSize/3.8)

            createBttn(mainSurface, startBttn, horizontalC(startBttn, mainSurface), surfaceSize - surfaceSize / 3,
                       startBttnC)
            startBttnHov = bttnDimension(mouse, startBttn, horizontalC(startBttn, mainSurface),
                                         surfaceSize - surfaceSize / 3)
            helpBttnHov = bttnDimension(mouse, helpBttn, surfaceSize*0.02, surfaceSize-surfaceSize*0.06)

            if startBttnHov:
                startBttnC = BUTTNBLUE
                if mouseUp:
                    programState = "game"
                    stateChange = True
            elif helpBttnHov:
                displayImg(mainSurface, rulesImg, 0,0)
                helpBttnC = BUTTNBLUE
            else:
                startBttnC = BUTTNHOVER
                helpBttnC = BUTTNHOVER

            createBttn(mainSurface, helpBttn, surfaceSize*0.02, surfaceSize-surfaceSize*0.06, helpBttnC)

            # Music button
            createBttn(mainSurface, musicBttn, surfaceSize * 0.857, surfaceSize * 0.02, musicBttnC)
            musicBttnHov = bttnDimension(mouse, musicBttn, surfaceSize * 0.857, surfaceSize * 0.02)

            if musicBttnHov:
                musicBttnC = BUTTNBLUE
                if mouseUp:
                    if musicOn:
                        musicOn = False
                        pygame.mixer.music.pause()
                    else:
                        musicOn = True
                        pygame.mixer.music.unpause()
            else:
                musicBttnC = BUTTNHOVER

        # GAME SCREEN
        elif programState == "game":
            # if it is a new game, reset everything
            if restart:
                variableReset()

                for i in range(coinNum):
                    img.append(coinImg)

                characterPos = [surfaceSize / 2, 600]  # X and Y Positions

            # Background image
            displayImg(mainSurface, bkgImg, 0, 0)

            # Coin (and other items) initialization (XY, Speed, time)
            if coinRanInit:
                # Mark time
                checkP1 = time.time()
                startTime = time.time()

                # Gets random X values that are not close to each other
                while len(coinRanXList) < coinNum:
                    newX = random.randint(0, surfaceSize - coinImg.get_width())

                    closeX = False
                    for i in range(len(coinRanXList)):
                        # if the random number is with in this range, get a new number
                        if coinRanXList[i] - 50 < newX < coinRanXList[i] + 50:
                            closeX = True

                    if not closeX:
                        coinRanXList.append(newX)

                # Get random Y value
                while len(coinRanYList) < coinNum:
                    newY = random.randint(-800, 0 - coinImg.get_height())
                    coinRanYList.append(newY)

                coinRanInit = False

            # calculate the time, if 5 seconds have passed, increased the speed
            checkP2 = time.time()
            if (checkP2 - checkP1) >= 5:
                checkP1 = checkP2
                coinSpeed += 1
                keySpeed += 1

            for i in range(coinNum):
                # Get XY coordinates of character and items
                characterRect = characterImg.get_rect(topleft=(characterPos[0], characterPos[1]))
                coinRect = coinImg.get_rect(topleft=(coinRanXList[i], coinRanYList[i]))

                # If collision is detected, check what item it is and add/subtract the coin or life
                if characterRect.colliderect(coinRect):
                    coinTouch = True
                    if img[i] == coinImg:
                        if musicOn:
                            coinSoundEffect.play()
                        coinPlayer += 1

                    elif img[i] == cashImg:
                        if musicOn:
                            cashSoundEffect.play()
                        coinPlayer += 5

                    elif img[i] == bombImg:
                        if musicOn:
                            bombSoundEffect.play()
                        displayImg(mainSurface, bombEImg, coinRanXList[i], coinRanYList[i])
                        lifePlayer -= 1

                    elif img[i] == taxImg:
                        if musicOn:
                            taxSoundEffect.play()
                        displayImg(mainSurface, exclaImg, coinRanXList[i], coinRanYList[i])
                        coinPlayer = int(coinPlayer*0.9)
                        lifePlayer -= 1

                        if coinPlayer < 0:
                            coinPlayer = 0

                # If the items touch the character or the ground get a random XY value and a random item
                if coinRanYList[i] >= 610 or coinTouch:

                    coinTouch = False

                    coinRanYList[i] = random.randint(-500, 0 - coinImg.get_height())
                    coinRanXList.pop(i)

                    item = random.randint(0, 100)

                    # different possibilites of the item
                    if item % 5 == 0:
                        img[i] = bombImg
                    elif item % 13 == 0:
                        img[i] = cashImg
                    elif item % 19 == 0:
                        img[i] = taxImg
                    else:
                        img[i] = coinImg

                    # Same logic used at the initializing state at the top (rand XY)
                    while len(coinRanXList) != coinNum:
                        newX = random.randint(0, surfaceSize - coinImg.get_width())

                        closeX = False
                        for j in range(len(coinRanXList)):

                            if coinRanXList[j] - 1.2*coinImg.get_width() < newX < coinRanXList[j] + 1.2*coinImg.get_width():
                                closeX = True

                        if not closeX:
                            coinRanXList.insert(i, newX)
                            break

                else:
                    coinRanYList[i] += coinSpeed

                # Displays the falling coins
                displayImg(mainSurface, img[i], coinRanXList[i], coinRanYList[i])

            # Draw the number of lives left (hart)
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
            coinText = createText(f'x {coinPlayer}', s=25, c=WHITE, b=True)
            mainSurface.blit(coinText, (15 + coinImgS.get_width(), 10))

            # Exit button
            createBttn(mainSurface, exitBttn, surfaceSize*0.9, surfaceSize*0.9, exitBttnC)
            exitBttnHov = bttnDimension(mouse, exitBttn, surfaceSize*0.9, surfaceSize*0.9)

            # Music button
            createBttn(mainSurface, musicBttn, surfaceSize * 0.857, surfaceSize * 0.95, musicBttnC)
            musicBttnHov = bttnDimension(mouse, musicBttn, surfaceSize * 0.857, surfaceSize * 0.95)

            # If exit button is clicked, change the state to main
            if exitBttnHov:
                exitBttnC = (140, 116, 98)
                if mouseUp:
                    restart = True
                    programState = 'main'
                    stateChange = True
            # If music button is clicked, toggle the music (ON/OFF)
            elif musicBttnHov:
                musicBttnC = (140, 116, 98)
                if mouseUp:
                    if musicOn:
                        musicOn = False
                        pygame.mixer.music.pause()
                    else:
                        musicOn = True
                        pygame.mixer.music.unpause()
            else:
                exitBttnC = (112, 79, 55)
                musicBttnC = (112, 79, 55)

            # If life is 0, record the endTime, be ready to reset the variables, and change the state to end
            if lifePlayer == 0:
                endTime = time.time()
                restart = True
                programState = 'end'
                stateChange = True

        # END SCREEN
        if programState == "end":
            # Units for the time are blank and time calculation
            unit = ''
            unit2 = ''
            timeDiff = endTime - startTime

            # Different end screen depending on the number of coins
            if coinPlayer < 10:
                displayImg(mainSurface, noFriendsImg, 0, 0)
            if coinPlayer >= 10:
                displayImg(mainSurface, oneFriendImg, 0, 0)
            if coinPlayer >= 25:
                displayImg(mainSurface, twoFriendsImg, 0, 0)
            if coinPlayer >= 40:
                displayImg(mainSurface, tenFriendsImg, 0, 0)
            if coinPlayer >= 60:
                displayImg(mainSurface, twentyFriendsImg, 0, 0)

            # Display the number of coins earned
            resultText = createText(f'{coinPlayer}', s=50, c=WHITE, b=True)
            mainSurface.blit(resultText, (surfaceSize*0.57, surfaceSize*0.3))

            # If the time is more than 60 seconds, display it as ___ minutes ___ seconds
            if timeDiff < 60:
                timeDiff = int(timeDiff)
                unit = 'seconds'
            elif timeDiff >= 60:
                unit2 = f'{math.ceil(timeDiff % 60)} seconds'
                timeDiff = int(timeDiff/60)
                unit = 'minutes'

                if timeDiff == 1:
                    unit = 'minute'

            # Music button (different colour)
            createBttn(mainSurface, musicBttn, surfaceSize * 0.857, surfaceSize * 0.02, musicBttnC)
            musicBttnHov = bttnDimension(mouse, musicBttn, surfaceSize * 0.857, surfaceSize * 0.02)

            # Same logic as the one in the main/game state
            if musicBttnHov:
                musicBttnC = BUTTNBLUE
                if mouseUp:
                    if musicOn:
                        musicOn = False
                        pygame.mixer.music.pause()
                    else:
                        musicOn = True
                        pygame.mixer.music.unpause()
            else:
                musicBttnC = BUTTNHOVER

            # Display the time as ___seconds or ___minutes ___seconds
            resultText = createText(f'{timeDiff} {unit} {unit2}', s=35, c=WHITE, i=True)
            mainSurface.blit(resultText, (horizontalC(resultText, mainSurface), surfaceSize*0.43))

            # Draw the buttons
            createBttn(mainSurface, homeBttn, surfaceSize/2 - 130, surfaceSize*0.9, homeBttnC)
            homeBttnHov = bttnDimension(mouse, homeBttn, surfaceSize/2 - 130, surfaceSize*0.9)
            createBttn(mainSurface, replayBttn, surfaceSize/2 + 30, surfaceSize*0.9, replayBttnC)
            replayBttnHov = bttnDimension(mouse, replayBttn, surfaceSize/2 + 30, surfaceSize*0.9)

            # If home button is clicked, go back to the main screen
            if homeBttnHov:
                homeBttnC = BUTTNBLUE
                if mouseUp:
                    programState = "main"
                    stateChange = True
                    mouseUp = False
            # If replay button is clicked, go back to the game screen
            elif replayBttnHov:
                replayBttnC = BUTTNBLUE
                if mouseUp:
                    programState = "game"
                    stateChange = True
                    mouseUp = False
            else:
                homeBttnC = BUTTNHOVER
                replayBttnC = BUTTNHOVER

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
