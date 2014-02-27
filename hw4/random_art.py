# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 11:34:57 2014

@author: pruvolo
"""

# you do not have to use these particular modules, but they may help
from random import randint
from math import *
import Image
current_depth = 1
def build_random_function(min_depth, max_depth):
    # your doc string goes here
    """Prints an array including function strings prod, sin_pi, cos_pi, x, y  with their
    repsective inputs in nested arrays.
    inputs:
        min_depth: the minimum depth that you want your function to reach
        max_depth: the maximum depth that you want your function to reach
    """
    # your code goes here
    global current_depth        # woah...global vairables? I don't recommend using global variables. It also seems like you're only using it as a variable within this function.
    if current_depth < min_depth:
        current_depth += 1
        choices = ["prod","sin_pi","cos_pi"]
        i = randint(0,len(choices)-1)
        s = choices[i]
        if s == "prod":
            return [s,build_random_function(min_depth, max_depth),build_random_function(min_depth, max_depth)]
        else:
            return [s,build_random_function(min_depth, max_depth)]
        
    elif current_depth >= min_depth:    # why not just use else? If it's not less than, it has to be greater than or equal to.
        
        if current_depth == max_depth:
            current_depth += 1
            choices = ["x","y"]
            i = randint(0,len(choices)-1)
            s = choices[i]
        else:
            current_depth += 1
            choices = ["prod","sin_pi","cos_pi","x","y"]
            i = randint(0,len(choices)-1)
            s = choices[i]

        if s == "prod":
            return [s,build_random_function(min_depth, max_depth),build_random_function(min_depth, max_depth)]
        elif s=="sin_pi" or s=="cos_pi":
            return [s,build_random_function(min_depth, max_depth)]
        else:
            return [s]
        
'''
Ah, I see what you're doing with current_depth. However, you should just use min/max depth and changes in those numbers to drive the recursion forward.
'''

def evaluate_random_function(f, x, y):
    # your doc string goes here

    # your code goes here
    if f[0] == 'prod':
        return evaluate_random_function(f[1], x, y)*evaluate_random_function(f[2], x, y)
    elif f[0] == 'sin_pi':
        return sin(pi*evaluate_random_function(f[1], x, y))
    elif f[0] == 'cos_pi':
        return cos(pi*evaluate_random_function(f[1], x, y))  
    elif f[0] == 'y':
        return y
    elif f[0] == 'x':
        return x

'''
I know it doesn't make much different for this case, but you should always check for base cases first. In this case, your base cases
are x and y. 
'''

def remap_interval(val, input_interval_start, input_interval_end, output_interval_start, output_interval_end):
    """ Maps the input value that is in the interval [input_interval_start, input_interval_end]
        to the output interval [output_interval_start, output_interval_end].  The mapping
        is an affine one (i.e. output = input*c + b).
    
        TODO: please fill out the rest of this docstring
    """
    # your code goes here
    ratio = (output_interval_end-output_interval_start)/(input_interval_end-input_interval_start)
    offset = output_interval_start-input_interval_start*ratio
    return val*ratio + offset
    

global current_depth   
fR = build_random_function(2, 25)
current_depth = 1
fB = build_random_function(2, 25)
current_depth = 1
fG = build_random_function(2, 25)
print fR
print fG
print fB
im = Image.new("RGB",(350,350))
pixels = im.load()
for i in range(0,350):
    for j in range(0,350):
        x = remap_interval(i, 0, 350, -1,1.)
        y = remap_interval(j, 0, 350, -1,1.)
        R = remap_interval(evaluate_random_function(fR, x, y),-1,1,0,256)
        B =remap_interval(evaluate_random_function(fB, x, y),-1,1,0,256)
        G = remap_interval(evaluate_random_function(fG, x, y),-1,1,0,256)
        RBG = (R,G,B)
        
        pixels[i,j] = (int(R),int(G),int(B))
        
im.save("pic" + ".thumbnail", "JPEG")
        
        
