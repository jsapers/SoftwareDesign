# -*- coding: utf-8 -*-
"""
Created on Sat Mar 8 23:11:28 2014

@author: dmichael
"""

import pygame
from pygame.locals import *
import random
import math
import time

class LightCycleModel:
    def __init__(self):
        self.cycle1 = Cycle(50,240,10,(250,0,0),.50)
        self.cycle2 = Cycle(590,240,10,(0,0,250),-1.0)
        self.trail1=[]
        self.trail2=[]
    
    def update(self):
        self.cycle1.update()
        self.cycle2.update()
        
class Cycle:
    def __init__(self,x,y,thick,color,vx):
        self.x = x
        self.y = y
        self.width = thick
        self.height = thick
        self.color = color
        self.vx = vx
        self.vy = 0.0
        
    def update(self):
        self.x += self.vx
class Trail:
     def __init__(self,color,hieght,width,x,y):
        self.color=color
        self.hieght=hieght
        self.width=width
        self.x=x
        self.y=y        
class PyGameWindowView:
    """ A view of brick breaker rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        
    def draw(self):
        self.screen.fill(pygame.Color(0,0,0))
        pygame.draw.rect(self.screen, pygame.Color(self.model.cycle1.color[0],self.model.cycle1.color[1],self.model.cycle1.color[2]),pygame.Rect(self.model.cycle1.x,self.model.cycle1.y,self.model.cycle1.width,self.model.cycle1.height))
        #pygame.draw.rect(self.screen, pygame.Color(self.model.cycle2.color[0],self.model.cycle2.color[1],self.model.cycle2.color[2]),pygame.Rect(self.model.cycle2.x,self.model.cycle2.y,self.model.cycle2.width,self.model.cycle2.height))
        pygame.display.update()

class Controller:
    def __init__(self,model):
        self.model = model
    
    def handle_keyboard_event(self,event):
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT and self.model.cycle1.vx == 0:
            self.model.cycle1.vx += -.50
            self.model.cycle1.vy = 0.0
        if event.key == pygame.K_RIGHT and self.model.cycle1.vx == 0:
            self.model.cycle1.vx += .50
            self.model.cycle1.vy = 0.0
        if event.key == pygame.K_UP and self.model.cycle1.vy == 0:
            self.model.cycle1.vx = 0.0
            self.model.cycle1.vy += .50
        if event.key == pygame.K_DOWN and self.model.cycle1.vy == 0:
            self.model.cycle1.vx = 0.0
            self.model.cycle1.vy += -.50
        else:
            self.model.cycle1.vx = self.model.cycle1.vx
            self.model.cycle1.vy = self.model.cycle1.vy
# if event.key == pygame.K_A and self.model.cycle2.vx == 0:
# self.model.cycle2.vx = -1.0
# self.model.cycle2.vy = 0.0
# if event.key == pygame.K_D and self.model.cycle2.vx == 0:
# self.model.cycle2.vx = 1.0
# self.model.cycle2.vy = 0.0
# if event.key == pygame.K_W and self.model.cycle2.vy == 0:
# self.model.cycle2.vx = 0.0
# self.model.cycle2.vy = 1.0
# if event.key == pygame.K_S and self.model.cycle2.vy == 0:
# self.model.cycle2.vx = 0.0
# self.model.cycle2.vy = -1.0
            
if __name__ == '__main__':
    pygame.init()

    size = (640,480)
    screen = pygame.display.set_mode(size)

    model = LightCycleModel()
    view = PyGameWindowView(model,screen)
    controller = Controller(model)


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                controller.handle_keyboard_event(event)
        model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
