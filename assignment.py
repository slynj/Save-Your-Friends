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

import pygame


def mainScreen(ev, mainSurface):
    pass


def createText(t, f="Arial", s=200, c=(255, 255, 0), b=False, i=False):
    font = pygame.font.SysFont(f, s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text


def createBttn(mainSurface, text, textX, textY, c=(0, 0, 0)):
    dimension = [textX, textY, text.get_width(), text.get_height()]
    #rect = ()
    #text = ()
    #pygame.draw.rect(mainSurface, c, dimension)
    mainSurface.blit(text, textX, textY)


def horizontalC(item, mainSurface):
    return int((mainSurface.get_width() - item.get_width()) // 2)


def main():
    # -----------------------------Setup------------------------------------------------- #
    """ Set up the game and run the main game loop """
    pygame.init()  # Prepare the pygame module for use
    pygame.font.init()
    surfaceSize = 800  # Desired physical surface size, in pixels.

    clock = pygame.time.Clock()  # Force frame rate to be slower

    # Create surface of (width, height), and its window.
    mainSurface = pygame.display.set_mode((surfaceSize, surfaceSize))

    # -----------------------------Program Variable Initialization----------------------- #
    # Set up some data to describe a small circle and its color
    programState = "main"

    mainTitle = createText("TITLE", s=150, c=(0, 100, 0))
    startBttn = createText("start", s=50, c=(0, 100, 120))

    # -----------------------------Main Game Loop----------------------------------------#
    while True:

        # -----------------------------Event Handling------------------------------------#
        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        mouse = pygame.mouse.get_pos()

        # -----------------------------Game Logic----------------------------------------#
        # Update your game objects and data structures here...

        # -----------------------------Drawing Everything--------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((255, 255, 255))

        if programState == "main":
            # mainScreen(ev, mainSurface)
            mainSurface.blit(mainTitle, (horizontalC(mainTitle, mainSurface), surfaceSize / 2))

            """
            dimension = [startBttn.get_rect().bottom, startBttn.get_rect().top, startBttn.get_width(),
                         startBttn.get_height()]
            #print(startBttn.get_rect())
            pygame.draw.rect(mainSurface, (0, 0, 0), dimension)
            # mainSurface.blit(mainSurface, startBttn.get_rect(center=(100, 100)))
            """
            #mainSurface, text, textX, textY, c = (0, 0, 0)
            createBttn(mainSurface, startBttn, 100, 300)
            #mainSurface.blit(createBttn())

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
