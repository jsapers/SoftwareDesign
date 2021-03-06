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
        self.cycle1 = Cycle(800,500,10,(0,0,250),-1.0)
        self.cycle2 = Cycle(200,500,10,(250,0,0),1.0)
        self.trail1=[]
        self.trail2=[]
        self.trail1.append(Trail(self.cycle1.color,self.cycle1.height,0,self.cycle1.x,self.cycle1.y))
        self.trail2.append(Trail(self.cycle2.color,self.cycle2.height,0,self.cycle2.x,self.cycle2.y))
    def update(self):
        """updates the cycles and the current paths for each lightcycle"""
        self.cycle1.update()        
        self.cycle2.update()

        #enlongating the path for cycle 1        
        if self.cycle1.vx>0:
           self.trail1[-1].width+=self.cycle1.vx
        if self.cycle1.vx<0:
            self.trail1[-1].width=self.trail1[-1].width-self.cycle1.vx
            self.trail1[-1].x = self.cycle1.x+self.cycle1.width
        if self.cycle1.vy>0:
            self.trail1[-1].height+=self.cycle1.vy
        if self.cycle1.vy<0:
            self.trail1[-1].height=self.trail1[-1].height-self.cycle1.vy
            self.trail1[-1].y = self.cycle1.y+self.cycle1.height

        #enlongating the path for cycle 2      
        if self.cycle2.vx>0:
           self.trail2[-1].width+=self.cycle2.vx
        if self.cycle2.vx<0:
            self.trail2[-1].width=self.trail2[-1].width-self.cycle2.vx
            self.trail2[-1].x = self.cycle2.x+self.cycle2.width
        if self.cycle2.vy>0:
            self.trail2[-1].height+=self.cycle2.vy
        if self.cycle2.vy<0:
            self.trail2[-1].height=self.trail2[-1].height-self.cycle2.vy
            self.trail2[-1].y = self.cycle2.y+self.cycle2.height
        
        for path1 in self.trail1[:-1]:
            #Checking for collisions with paths
            if pygame.Rect(self.cycle1.x,self.cycle1.y,self.cycle1.width,self.cycle1.height).colliderect(pygame.Rect(path1.x,path1.y,path1.width,path1.height)):
                #ends game if it collides                
                return False
        for path1 in self.trail1[:]:
            if pygame.Rect(self.cycle2.x,self.cycle2.y,self.cycle2.width,self.cycle2.height).colliderect(pygame.Rect(path1.x,path1.y,path1.width,path1.height)):               
                return False
        for path2 in self.trail2[:]:        
            if pygame.Rect(self.cycle1.x,self.cycle1.y,self.cycle1.width,self.cycle1.height).colliderect(pygame.Rect(path2.x,path2.y,path2.width,path2.height)):                                
                return False
        for path2 in self.trail2[:-1]:
            if pygame.Rect(self.cycle2.x,self.cycle2.y,self.cycle2.width,self.cycle2.height).colliderect(pygame.Rect(path2.x,path2.y,path2.width,path2.height)):
                return False
        #ends game if the cycle hit the edge of screen
        if not(self.windowRect.contains(pygame.Rect(self.cycle1.x,self.cycle1.y,self.cycle1.width,self.cycle1.height))):
            return False
        if not(self.windowRect.contains(pygame.Rect(self.cycle2.x,self.cycle2.y,self.cycle2.width,self.cycle2.height))):
            return False
        return True
        
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
        """Changes the location based off of the two velocities"""
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
    """ A view of LightCycles rendered in a Pygame window """
    def __init__(self,model,screen,size):
        self.model = model
        self.model.windowRect=pygame.Rect(0,0,size[0],size[1])
        self.screen = screen
    def draw(self):
        """draws the two cycles and all of the paths they made"""
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
        """checks for wasd or arrow key inputs and changes the direction accordingly. Also adds
            a new path when the cycle changes direction"""
        if event.type != KEYDOWN:
            return
        if event.key == pygame.K_LEFT and self.model.cycle1.vx == 0:
            self.model.cycle1.vx = -1.0
            self.model.cycle1.vy = 0.0
            self.model.trail1.append(Trail(self.model.cycle1.color,self.model.cycle1.height,0,self.model.cycle1.x+self.model.cycle1.width,self.model.cycle1.y))
        if event.key == pygame.K_RIGHT and self.model.cycle1.vx == 0:
            self.model.cycle1.vx = 1.0
            self.model.cycle1.vy = 0.0
            self.model.trail1.append(Trail(self.model.cycle1.color,self.model.cycle1.height,0,self.model.cycle1.x,self.model.cycle1.y))
        if event.key == pygame.K_UP and self.model.cycle1.vy == 0:
            self.model.cycle1.vx = 0.0
            self.model.cycle1.vy = -1.0
            self.model.trail1.append(Trail(self.model.cycle1.color,0,self.model.cycle1.width,self.model.cycle1.x,self.model.cycle1.y+self.model.cycle1.height))
        if event.key == pygame.K_DOWN and self.model.cycle1.vy == 0:
            self.model.cycle1.vx = 0.0
            self.model.cycle1.vy = .9999
            self.model.trail1.append(Trail(self.model.cycle1.color,0,self.model.cycle1.width,self.model.cycle1.x,self.model.cycle1.y))
        else:
            self.model.cycle1.vx = self.model.cycle1.vx
            self.model.cycle1.vy = self.model.cycle1.vy
        
        if event.key == pygame.K_a and self.model.cycle2.vx == 0:
            self.model.cycle2.vx = -1.0
            self.model.cycle2.vy = 0.0
            self.model.trail2.append(Trail(self.model.cycle2.color,self.model.cycle2.height,0,self.model.cycle2.x+self.model.cycle2.width,self.model.cycle2.y))
        if event.key == pygame.K_d and self.model.cycle2.vx == 0:
            self.model.cycle2.vx = 1.0
            self.model.cycle2.vy = 0.0
            self.model.trail2.append(Trail(self.model.cycle2.color,self.model.cycle2.height,0,self.model.cycle2.x,self.model.cycle2.y))
        if event.key == pygame.K_w and self.model.cycle2.vy == 0:
            self.model.cycle2.vx = 0.0
            self.model.cycle2.vy = -1.0
            self.model.trail2.append(Trail(self.model.cycle2.color,0,self.model.cycle2.width,self.model.cycle2.x,self.model.cycle2.y+self.model.cycle2.height))
        if event.key == pygame.K_s and self.model.cycle2.vy == 0:
            self.model.cycle2.vx = 0.0
            self.model.cycle2.vy = .9999
            self.model.trail2.append(Trail(self.model.cycle2.color,0,self.model.cycle2.width,self.model.cycle2.x,self.model.cycle2.y))
if __name__ == '__main__':
    pygame.init()

    size = (1000,1000)
    screen = pygame.display.set_mode(size)

    model = LightCycleModel()
    view = PyGameWindowView(model,screen,size)
    controller = Controller(model)


    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == KEYDOWN:
                controller.handle_keyboard_event(event)
        running=model.update()
        view.draw()
        time.sleep(.001)

    pygame.quit()
