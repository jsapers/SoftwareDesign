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
        self.cycle2 = Cycle(590,240,10,(0,0,250),-.50)
        self.trail1=[]
        self.trail2=[]
    
    def update(self):
        self.cycle1.update()
        self.cycle2.update()
        if self.cycle1.vx>0:
           self.trail1.append(Trail(self.cycle1.color,self.cycle1.height,self.cycle1.vx,self.cycle1.x,self.cycle1.y))
        if self.cycle1.vx<0:
            self.trail1.append(Trail(self.cycle1.color,self.cycle1.height,self.cycle1.vx,self.cycle1.x+self.cycle1.width,self.cycle1.y))
        if self.cycle1.vy>0:
            self.trail1.append(Trail(self.cycle1.color,self.cycle1.vy,self.cycle1.width,self.cycle1.x,self.cycle1.y))
        if self.cycle1.vy<0:
            self.trail1.append(Trail(self.cycle1.color,self.cycle1.vy,self.cycle1.width,self.cycle1.x,self.cycle1.y+self.cycle1.height))
       
        if self.cycle2.vx>0:
           self.trail2.append(Trail(self.cycle2.color,self.cycle2.height,self.cycle2.vx,self.cycle2.x,self.cycle2.y))
        if self.cycle2.vx<0:
            self.trail2.append(Trail(self.cycle2.color,self.cycle2.height,self.cycle2.vx,self.cycle2.x+self.cycle2.width,self.cycle2.y))
        if self.cycle2.vy>0:
            self.trail2.append(Trail(self.cycle2.color,self.cycle2.vy,self.cycle2.width,self.cycle2.x,self.cycle2.y))
        if self.cycle2.vy<0:
            self.trail2.append(Trail(self.cycle2.color,self.cycle2.vy,self.cycle2.width,self.cycle2.x,self.cycle2.y+self.cycle2.height))
        
        
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
        self.y += self.vy
class Trail:
     def __init__(self,color,height,width,x,y):
        self.color=color
        self.height=height
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
        pygame.draw.rect(self.screen, pygame.Color(self.model.cycle2.color[0],self.model.cycle2.color[1],self.model.cycle2.color[2]),pygame.Rect(self.model.cycle2.x,self.model.cycle2.y,self.model.cycle2.width,self.model.cycle2.height))
        for path1 in self.model.trail1:
            pygame.draw.rect(self.screen, pygame.Color(path1.color[0],path1.color[1],path1.color[2]),pygame.Rect(path1.x,path1.y,path1.width,path1.height))
        for path2 in self.model.trail2:
            pygame.draw.rect(self.screen, pygame.Color(path2.color[0],path2.color[1],path2.color[2]),pygame.Rect(path2.x,path2.y,path2.width,path2.height))
            
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
            self.model.cycle1.vy = -.50
        if event.key == pygame.K_DOWN and self.model.cycle1.vy == 0:
            self.model.cycle1.vx = 0.0
            self.model.cycle1.vy = .50
        else:
            self.model.cycle1.vx = self.model.cycle1.vx
            self.model.cycle1.vy = self.model.cycle1.vy
        if event.key == pygame.K_a and self.model.cycle2.vx == 0:
            self.model.cycle2.vx = -.50
            self.model.cycle2.vy = 0.0
        if event.key == pygame.K_d and self.model.cycle2.vx == 0:
            self.model.cycle2.vx = .50
            self.model.cycle2.vy = 0.0
        if event.key == pygame.K_w and self.model.cycle2.vy == 0:
            self.model.cycle2.vx = 0.0
            self.model.cycle2.vy = -.50
        if event.key == pygame.K_s and self.model.cycle2.vy == 0:
            self.model.cycle2.vx = 0.0
            self.model.cycle2.vy = .50
            
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
