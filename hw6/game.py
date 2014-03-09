# -*- coding: utf-8 -*-
"""
Created on Mon Mar  3 15:07:40 2014

@author: josh
"""

# Import a library of functions called 'pygame'
import pygame
# Initialize the game engine
pygame.init()
#Loop until the user clicks the close button.
done = False
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
# -------- Main Program Loop -----------
while not done:
# ALL EVENT PROCESSING SHOULD GO BELOW THIS COMMENT
    for event in pygame.event.get(): # User did something
        if event.type == pygame.QUIT: # If user clicked close
            done = True # Flag that we are done so we exit this loop
        elif event.type == pygame.QUIT:
            print("User asked to quit.")
        elif event.type == pygame.KEYDOWN:
            print("User pressed a key.")
        elif event.type == pygame.KEYUP:
            print("User let go of a key.")
# ALL EVENT PROCESSING SHOULD GO ABOVE THIS COMMENT
# ALL GAME LOGIC SHOULD GO BELOW THIS COMMENT
# ALL GAME LOGIC SHOULD GO ABOVE THIS COMMENT
# ALL CODE TO DRAW SHOULD GO BELOW THIS COMMENT
# ALL CODE TO DRAW SHOULD GO ABOVE THIS COMMENT
# Limit to 20 frames per second
clock.tick(20)