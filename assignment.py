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


def createText(t, f, s=200, c=(255, 255, 0), b=False, i=False):
    font = pygame.font.SysFont(f, s, bold=b, italic=i)
    text = font.render(t, True, c)
    return text


def horizontalC(item, mainSurface):
    return int((mainSurface.get_width() - item.get_width()) // 2), item.get_height()


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
    font = pygame.font.SysFont(None, 24)
    img = font.render('hello', True, (0, 0, 0))
    test = createText("test", "Calibri", c=(0, 100, 0))

    # -----------------------------Main Game Loop----------------------------------------#
    while True:

        # -----------------------------Event Handling------------------------------------#
        ev = pygame.event.poll()  # Look for any event
        if ev.type == pygame.QUIT:  # Window close button clicked?
            break  # ... leave game loop

        # -----------------------------Game Logic----------------------------------------#
        # Update your game objects and data structures here...
        if programState == "main":
            mainScreen(ev, mainSurface)

        # -----------------------------Drawing Everything--------------------------------#
        # We draw everything from scratch on each frame.
        # So first fill everything with the background color
        mainSurface.fill((255, 255, 255))

        mainSurface.blit(test, horizontalC(test, mainSurface))

        # Now the surface is ready, tell pygame to display it!
        pygame.display.flip()

        clock.tick(60)  # Force frame rate to be slower

    pygame.quit()  # Once we leave the loop, close the window.


main()
